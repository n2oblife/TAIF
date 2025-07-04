import requests
import subprocess
import platform
import os
import json
from typing import List, Dict, Any, Optional
from .prompts.default import DEFAULT_SYSTEM_PROMPT

class Agent:
    def __init__(self, model: str = "deepseek-r1", thinking: str = "chain", verbose: bool = False, system_prompt: Optional[str] = None, 
                 thinker_model: Optional[str] = None, formatter_model: Optional[str] = None):
        self.model = model
        self.ollama_url = "http://127.0.0.1:11434/api/chat"
        self.verbose = verbose
        
        # Dual-LLM architecture
        self.thinker_model = thinker_model or "deepseek-r1"  # Large model for reasoning
        self.formatter_model = formatter_model or "mistral"  # Small model for formatting
        self.use_dual_llm = thinker_model is not None or formatter_model is not None
        
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
        self.system_prompt = system_prompt if system_prompt is not None else DEFAULT_SYSTEM_PROMPT

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
        if require_json:
            # Use adaptive switching based on request complexity
            if self._is_complex_request(prompt):
                if self.use_dual_llm:
                    return self._ask_with_dual_llm(prompt)
                else:
                    # Fallback to single LLM with enhanced prompt for complex requests
                    return self._ask_single_llm(prompt, require_json)
            else:
                # Simple request - use single LLM for speed
                return self._ask_single_llm(prompt, require_json)
        else:
            # Non-JSON requests always use single LLM
            return self._ask_single_llm(prompt, require_json)
    
    def _ask_single_llm(self, prompt: str, require_json: bool = False) -> str:
        """Send a prompt to a single LLM and return the response."""
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
    
    def _ask_with_dual_llm(self, prompt: str) -> str:
        """Use dual-LLM architecture: thinker for reasoning, formatter for JSON output."""
        if self.verbose:
            print(f"[Dual-LLM] Processing: {prompt}")
        
        # Step 1: Use thinker model to understand and plan
        thinker_prompt = f"""Analyze this request and determine what action needs to be taken. 
        Think through the steps and provide a clear plan.
        
        Request: {prompt}
        
        Think through this step by step:"""
        
        thinker_response = self._ask_with_model(thinker_prompt, self.thinker_model, require_json=False)
        
        if self.verbose:
            print(f"[Thinker] Analysis: {thinker_response}")
        
        # Check if thinker failed and fallback to simple analysis
        if "Failed to communicate" in thinker_response or "timeout" in thinker_response.lower():
            if self.verbose:
                print("[Dual-LLM] Thinker failed, using fallback analysis")
            thinker_response = f"Simple analysis: User wants to {prompt.lower()}"
        
        # Step 2: Use formatter model to create JSON response
        formatter_prompt = f"""Based on the analysis below, create a JSON response with the appropriate action and parameters.

Analysis: {thinker_response}

Original Request: {prompt}

Return ONLY a valid JSON object in this format:
{{
  "action": "command_name",
  "parameters": {{
    "param1": "value1",
    "param2": "value2"
  }}
}}"""
        
        formatter_response = self._ask_with_model(formatter_prompt, self.formatter_model, require_json=True)
        
        if self.verbose:
            print(f"[Formatter] JSON: {formatter_response}")
        
        return formatter_response
    
    def _ask_with_model(self, prompt: str, model: str, require_json: bool = False) -> str:
        """Send a prompt to a specific model and return the response."""
        messages = [
            {"role": "system", "content": self.system_prompt},
            {"role": "user", "content": prompt}
        ]
        
        payload = {
            "model": model,
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
            return result
        except requests.exceptions.RequestException as e:
            error_msg = f"Failed to communicate with Ollama using model {model}: {e}"
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

    def set_system_prompt(self, prompt: str):
        """Update the system prompt used by the agent."""
        self.system_prompt = prompt

    def get_system_prompt(self) -> str:
        """Get the current system prompt."""
        return self.system_prompt

    def _is_complex_request(self, prompt: str, complexity_threshold: int = 3) -> bool:
        """
        Determine if a request is complex and would benefit from dual-LLM reasoning.
        
        Complexity indicators:
        - Multi-step operations (and, then, also, furthermore)
        - Conditional logic (if, when, unless, based on)
        - Complex file patterns (wildcards, multiple files)
        - Analysis or summarization tasks
        - Operations involving multiple directories or files
        """
        prompt_lower = prompt.lower()
        
        # Multi-step indicators
        multi_step_keywords = [
            'and', 'then', 'also', 'furthermore', 'additionally', 'moreover',
            'first', 'second', 'third', 'next', 'after', 'before',
            'while', 'during', 'meanwhile', 'simultaneously'
        ]
        
        # Conditional logic indicators
        conditional_keywords = [
            'if', 'when', 'unless', 'based on', 'depending on', 'according to',
            'provided that', 'assuming', 'given that', 'in case'
        ]
        
        # Complex file operations
        complex_file_patterns = [
            '*.', 'all', 'every', 'multiple', 'several', 'various',
            'recursive', 'subdirectories', 'nested', 'deep'
        ]
        
        # Analysis and summarization tasks
        analysis_keywords = [
            'analyze', 'summarize', 'review', 'examine', 'investigate',
            'compare', 'contrast', 'evaluate', 'assess', 'study',
            'find', 'identify', 'detect', 'locate', 'search'
        ]
        
        # Multi-location operations
        multi_location_keywords = [
            'from', 'to', 'between', 'across', 'throughout',
            'source', 'destination', 'target', 'backup', 'archive'
        ]
        
        # Count complexity indicators
        complexity_score = 0
        
        # Check for multi-step operations
        for keyword in multi_step_keywords:
            if keyword in prompt_lower:
                complexity_score += 2
                break
        
        # Check for conditional logic
        for keyword in conditional_keywords:
            if keyword in prompt_lower:
                complexity_score += 3
                break
        
        # Check for complex file patterns
        for pattern in complex_file_patterns:
            if pattern in prompt_lower:
                complexity_score += 1
        
        # Check for analysis tasks
        for keyword in analysis_keywords:
            if keyword in prompt_lower:
                complexity_score += 2
                break
        
        # Check for multi-location operations
        for keyword in multi_location_keywords:
            if keyword in prompt_lower:
                complexity_score += 1
        
        # Additional complexity factors
        if len(prompt.split()) > 15:  # Long requests are often complex
            complexity_score += 1
        
        if prompt_lower.count('and') > 1:  # Multiple "and" clauses
            complexity_score += 1
        
        if any(char in prompt_lower for char in ['*', '?', '[', ']']):  # Wildcards
            complexity_score += 2
        
        # Determine if request is complex
        is_complex = complexity_score >= complexity_threshold
        
        if self.verbose:
            print(f"[Complexity Analysis] Score: {complexity_score}, Complex: {is_complex}")
            if is_complex:
                print(f"[Complexity Analysis] Using dual-LLM for: {prompt}")
            else:
                print(f"[Complexity Analysis] Using single LLM for: {prompt}")
        
        return is_complex

    def get_complexity_analysis(self, prompt: str, complexity_threshold: int = 3) -> dict:
        """
        Get detailed complexity analysis for a prompt.
        Useful for debugging and understanding the decision-making process.
        """
        prompt_lower = prompt.lower()
        
        analysis = {
            'prompt': prompt,
            'word_count': len(prompt.split()),
            'complexity_score': 0,
            'is_complex': False,
            'indicators': []
        }
        
        # Multi-step indicators
        multi_step_keywords = [
            'and', 'then', 'also', 'furthermore', 'additionally', 'moreover',
            'first', 'second', 'third', 'next', 'after', 'before',
            'while', 'during', 'meanwhile', 'simultaneously'
        ]
        
        # Conditional logic indicators
        conditional_keywords = [
            'if', 'when', 'unless', 'based on', 'depending on', 'according to',
            'provided that', 'assuming', 'given that', 'in case'
        ]
        
        # Complex file operations
        complex_file_patterns = [
            '*.', 'all', 'every', 'multiple', 'several', 'various',
            'recursive', 'subdirectories', 'nested', 'deep'
        ]
        
        # Analysis and summarization tasks
        analysis_keywords = [
            'analyze', 'summarize', 'review', 'examine', 'investigate',
            'compare', 'contrast', 'evaluate', 'assess', 'study',
            'find', 'identify', 'detect', 'locate', 'search'
        ]
        
        # Multi-location operations
        multi_location_keywords = [
            'from', 'to', 'between', 'across', 'throughout',
            'source', 'destination', 'target', 'backup', 'archive'
        ]
        
        # Check for multi-step operations
        for keyword in multi_step_keywords:
            if keyword in prompt_lower:
                analysis['complexity_score'] += 2
                analysis['indicators'].append(f"Multi-step: '{keyword}'")
                break
        
        # Check for conditional logic
        for keyword in conditional_keywords:
            if keyword in prompt_lower:
                analysis['complexity_score'] += 3
                analysis['indicators'].append(f"Conditional: '{keyword}'")
                break
        
        # Check for complex file patterns
        for pattern in complex_file_patterns:
            if pattern in prompt_lower:
                analysis['complexity_score'] += 1
                analysis['indicators'].append(f"Complex pattern: '{pattern}'")
        
        # Check for analysis tasks
        for keyword in analysis_keywords:
            if keyword in prompt_lower:
                analysis['complexity_score'] += 2
                analysis['indicators'].append(f"Analysis task: '{keyword}'")
                break
        
        # Check for multi-location operations
        for keyword in multi_location_keywords:
            if keyword in prompt_lower:
                analysis['complexity_score'] += 1
                analysis['indicators'].append(f"Multi-location: '{keyword}'")
        
        # Additional complexity factors
        if len(prompt.split()) > 15:
            analysis['complexity_score'] += 1
            analysis['indicators'].append("Long request (>15 words)")
        
        if prompt_lower.count('and') > 1:
            analysis['complexity_score'] += 1
            analysis['indicators'].append("Multiple 'and' clauses")
        
        if any(char in prompt_lower for char in ['*', '?', '[', ']']):
            analysis['complexity_score'] += 2
            analysis['indicators'].append("Wildcards present")
        
        analysis['is_complex'] = analysis['complexity_score'] >= complexity_threshold
        
        return analysis

    def execute_multi_step_task(self, task_description: str) -> str:
        """
        Execute a multi-step task that requires multiple operations.
        
        This method allows the agent to break down complex tasks into steps,
        execute each step, and combine the results.
        """
        if self.verbose:
            print(f"[Multi-Step Task] {task_description}")
        
        # Add to chain of thought
        self.add_chain_thought(f"Starting multi-step task: {task_description}")
        
        # For now, handle specific multi-step tasks
        if "summarize" in task_description.lower():
            return self._execute_summarization_task(task_description)
        else:
            return f"Multi-step task not yet implemented: {task_description}"
    
    def _execute_summarization_task(self, task_description: str) -> str:
        """Execute a summarization task."""
        self.add_chain_thought("Detected summarization task")
        
        # Extract file path from task description
        # This is a simple extraction - in a real system, you'd use more sophisticated NLP
        words = task_description.lower().split()
        file_path = None
        
        # Look for file paths in different patterns
        for i, word in enumerate(words):
            # Pattern 1: "file path" or "document path"
            if word in ["file", "document", "text"] and i + 1 < len(words):
                potential_path = words[i + 1]
                # Check if it looks like a file path (contains slashes, dots, or is a simple filename)
                if any(char in potential_path for char in ['/', '\\', '.']) or len(potential_path) > 3:
                    file_path = potential_path
                    break
            
            # Pattern 2: Direct file path (starts with drive letter or contains path separators)
            elif any(char in word for char in ['/', '\\', '.']) and len(word) > 3:
                file_path = word
                break
        
        # If still no file path found, try to extract from the end of the sentence
        if not file_path:
            # Look for the last word that might be a file path
            for word in reversed(words):
                if any(char in word for char in ['/', '\\', '.']) and len(word) > 3:
                    file_path = word
                    break
        
        if not file_path:
            return "Could not identify file to summarize. Please specify the file path clearly."
        
        self.add_chain_thought(f"Identified file to summarize: {file_path}")
        
        try:
            # Step 1: Read the file
            from pathlib import Path
            file_path_obj = Path(file_path)
            
            if not file_path_obj.exists():
                return f"File not found: {file_path}"
            
            if not file_path_obj.is_file():
                return f"Path is not a file: {file_path}"
            
            content = file_path_obj.read_text(encoding='utf-8')
            self.add_chain_thought(f"Successfully read file: {len(content)} characters")
            
            # Step 2: Create summarization prompt
            summary_prompt = f"""Please provide a concise, natural language summary of the following content. Focus on the main points and key information. Write in a clear, readable format.

Content to summarize:
{content}

Please provide a summary in natural language:"""
            
            # Step 3: Generate summary
            summary = self.ask(summary_prompt, require_json=False)
            self.add_chain_thought("Generated summary using LLM")
            
            return f"Summary of {file_path}:\n\n{summary}"
            
        except Exception as e:
            error_msg = f"Error during summarization: {e}"
            self.add_chain_thought(f"Error: {error_msg}")
            return error_msg 