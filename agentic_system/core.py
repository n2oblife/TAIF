import requests
from typing import List, Dict, Any, Optional

class Agent:
    def __init__(self, model: str = "llama2", thinking:str = "chain"):
        self.model = model
        self.ollama_url = "http://localhost:11434/api/generate"
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

    def ask(self, prompt: str) -> str:
        """Send a prompt to the LLM and return the response."""
        payload = {
            "model": self.model,
            "prompt": prompt
        }
        response = requests.post(self.ollama_url, json=payload)
        response.raise_for_status()
        return response.json().get("response", "No response from model.")

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