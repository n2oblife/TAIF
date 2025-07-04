import requests
import subprocess
import platform
import os
import json
from typing import List, Dict, Any, Optional

class Agent:
    def __init__(self, model: str = "deepseek-r1", thinking: str = "chain", verbose: bool = False):
        self.model = model
        self.ollama_url = "http://127.0.0.1:11434/api/chat"
        self.verbose = verbose
        # Goal management
        self.goal_achieved = False
        self.goal_description = ""
        self.goal_status = ""
        self.goal_progress = 0
        self.goal_steps = []
        self.goal_current_step = 0
        self.goal_current_step_description = ""
        self.thinking = thinking
        # Chain of Thought: linear reasoning steps
        self.chain_of_thought: List[str] = []
        # Tree of Thought: branching reasoning, each node is a dict with 'thought', 'children', etc.
        self.tree_of_thought: Dict[str, Any] = {"thought": "root", "children": []}
        self.current_tree_node: Optional[Dict[str, Any]] = self.tree_of_thought
        
        # System prompt for the agent
        self.system_prompt = """You are TAIF (tAIsk force), an intelligent agent that can control a computer and execute CLI commands. You have access to various file system operations and can perform tasks through command-line interfaces.

Your capabilities include:
- File operations: read (cat), write, copy, move, delete files
- Directory operations: list contents (ls), create, remove directories
- Text processing: search (grep), filter, sort content
- System information: get current directory, system info
- Network operations: download files

Available actions: cat, ls, write, copy, move, delete, grep, tree

When a user gives you a task, you must:
1. Understand the intent
2. Determine the appropriate command to execute
3. Return a JSON response with the command parameters

IMPORTANT: You must ALWAYS respond with valid JSON only. No additional text, explanations, or markdown formatting.

JSON Response Format:
{
  "action": "command_name",
  "parameters": {
    "param1": "value1",
    "param2": "value2"
  }
}

Examples:

User: "Show contents of file.txt"
Response: {"action": "cat", "parameters": {"path": "file.txt"}}

User: "List files in current directory"
Response: {"action": "ls", "parameters": {"path": "."}}

User: "Copy file1.txt to backup/"
Response: {"action": "copy", "parameters": {"src": "file1.txt", "dst": "backup/"}}

User: "Search for 'error' in all .log files"
Response: {"action": "grep", "parameters": {"directory": ".", "pattern": "error", "files": "*.log"}}

User: "Search for 'foo' in /tmp"
Response: {"action": "grep", "parameters": {"directory": "/tmp", "pattern": "foo"}}

User: "Delete file1.txt"
Response: {"action": "delete", "parameters": {"src": ".", "files": "file1.txt"}}

User: "Write 'Hello World' to newfile.txt"
Response: {"action": "write", "parameters": {"file": "newfile.txt", "content": "Hello World"}}

Remember: Only return the JSON object, nothing else."""

    def start_ollama(self) -> bool:
        """Start Ollama server using OS-specific script."""
        try:
            system = platform.system().lower()
            if system == "windows":
                script_path = "start_ollama.bat"
                subprocess.Popen([script_path], shell=True)
            elif system == "linux" or system == "darwin":  # Linux or macOS
                script_path = "start_ollama.sh"
                subprocess.run(["bash", script_path], check=True)
            else:
                print(f"Unsupported OS: {system}")
                return False
            
            print("Ollama server started successfully.")
            return True
        except Exception as e:
            print(f"Failed to start Ollama: {e}")
            return False

    def stop_ollama(self) -> bool:
        """Stop Ollama server using OS-specific script."""
        try:
            system = platform.system().lower()
            if system == "windows":
                script_path = "stop_ollama.bat"
                subprocess.run([script_path], check=True)
            elif system == "linux" or system == "darwin":  # Linux or macOS
                script_path = "stop_ollama.sh"
                subprocess.run(["bash", script_path], check=True)
            else:
                print(f"Unsupported OS: {system}")
                return False
            
            print("Ollama server stopped successfully.")
            return True
        except Exception as e:
            print(f"Failed to stop Ollama: {e}")
            return False

    def check_ollama_status(self) -> bool:
        """Check if Ollama is running and accessible."""
        try:
            response = requests.get("http://127.0.0.1:11434/api/tags", timeout=5)
            response.raise_for_status()
            return True
        except requests.exceptions.RequestException:
            return False

    def ask(self, prompt: str, require_json: bool = False) -> str:
        """Send a prompt to the LLM and return the response."""
        if self.verbose:
            print(f"[Agent -> LLM] Prompt: {prompt}")
        
        # Always use system prompt for consistent behavior
        messages = [
            {"role": "system", "content": self.system_prompt},
            {"role": "user", "content": prompt}
        ]
        
        payload = {
            "model": self.model,
            "messages": messages,
            "stream": False,
            "format": "json" if require_json else None
        }
        
        # Remove None values from payload
        payload = {k: v for k, v in payload.items() if v is not None}
        
        try:
            response = requests.post(self.ollama_url, json=payload, timeout=30)
            response.raise_for_status()
            result = response.json().get("message", {}).get("content", "No response from model.")
            
            if self.verbose:
                print(f"[LLM -> Agent] Response: {result}")
            
            return result
        except requests.exceptions.RequestException as e:
            error_msg = f"Failed to communicate with Ollama: {e}"
            if self.verbose:
                print(f"[ERROR] {error_msg}")
            return error_msg

    def add_chain_thought(self, thought: str):
        """Add a step/thought to the chain of thought."""
        self.chain_of_thought.append(thought)

    def add_tree_thought(self, thought: str, parent: Optional[Dict[str, Any]] = None) -> Dict[str, Any]:
        """Add a thought to the tree of thought under the given parent node."""
        node = {"thought": thought, "children": []}
        if parent is None:
            parent = self.current_tree_node or self.tree_of_thought
        parent["children"].append(node)
        return node

    def set_current_tree_node(self, node: Dict[str, Any]):
        """Set the current node in the tree of thought for further expansion."""
        self.current_tree_node = node

    def reset_reasoning(self):
        """Reset chain and tree of thought for a new reasoning session."""
        self.chain_of_thought = []
        self.tree_of_thought = {"thought": "root", "children": []}
        self.current_tree_node = self.tree_of_thought 