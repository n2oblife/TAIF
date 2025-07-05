"""
Dual-LLM Intent Parser

This module implements an intelligent intent parsing system using two LLMs:
1. Thinker model: Analyzes natural language and determines intent
2. Formatter model: Converts intent into structured JSON
"""

from typing import Optional, Dict, Any
from .base import BaseIntentParser
from ..core import Agent


class DualLLMIntentParser(BaseIntentParser):
    """Intent parser using dual-LLM architecture for natural language understanding."""
    
    def __init__(self, thinker_model: str = "deepseek-r1", formatter_model: str = "mistral", verbose: bool = False):
        self.agent = Agent(
            verbose=verbose,
            thinker_model=thinker_model,
            formatter_model=formatter_model
        )
        self.verbose = verbose
    
    def parse(self, instruction: str) -> Optional[Dict[str, Any]]:
        """
        Parse natural language instruction using dual-LLM architecture.
        
        Args:
            instruction: Natural language instruction from user
            
        Returns:
            Parsed intent as dictionary or None if parsing fails
        """
        if self.verbose:
            print(f"[DualLLM Parser] Analyzing: {instruction}")
        
        # Step 1: Use thinker model to understand the intent
        thinker_prompt = f"""Analyze this user instruction and determine what action they want to perform.

User Instruction: "{instruction}"

Think through this step by step:
1. What is the user trying to accomplish?
2. What type of file operation is this? (list, read, write, copy, move, delete, etc.)
3. What are the key parameters? (file paths, directories, content, etc.)
4. Are there any special conditions or filters?

Provide a clear analysis of the user's intent."""

        thinker_response = self.agent._ask_with_model(thinker_prompt, self.agent.thinker_model, require_json=False)
        
        if self.verbose:
            print(f"[Thinker] Analysis: {thinker_response}")
        
        # Check if thinker failed and fallback to simple analysis
        if "Failed to communicate" in thinker_response or "timeout" in thinker_response.lower():
            if self.verbose:
                print("[DualLLM Parser] Thinker failed, using fallback analysis")
            thinker_response = f"Simple analysis: User wants to perform an operation related to '{instruction}'"
        
        # Step 2: Use formatter model to create structured JSON
        formatter_prompt = f"""Based on the analysis below, create a JSON response with the appropriate action and parameters.

Analysis: {thinker_response}

Original User Instruction: "{instruction}"

Available actions: ls, cat, write, copy, move, delete, mkdir, rmdir, grep, locate, echo, touch, wc, sort, uname, pwd, ps, wget, ln, tree, rewrite

Return ONLY a valid JSON object in this format:
{{
  "action": "command_name",
  "parameters": {{
    "param1": "value1",
    "param2": "value2"
  }}
}}

Examples:
- "list files" → {{"action": "ls", "parameters": {{"path": "."}}}}
- "show contents of file.txt" → {{"action": "cat", "parameters": {{"path": "file.txt"}}}}
- "create folder backup" → {{"action": "mkdir", "parameters": {{"path": "backup"}}}}
- "copy file.txt to backup/" → {{"action": "copy", "parameters": {{"src": "file.txt", "dst": "backup/"}}}}
- "find all Python files" → {{"action": "locate", "parameters": {{"pattern": "*.py"}}}}
- "tell me what contains the readme" → {{"action": "cat", "parameters": {{"path": "README.md"}}}}
- "what contains the guideline" → {{"action": "cat", "parameters": {{"path": "GUIDELINES.md"}}}}
- "what contains the requirements" → {{"action": "cat", "parameters": {{"path": "requirements.txt"}}}}

If the instruction is unclear or doesn't match any available action, return null."""

        formatter_response = self.agent._ask_with_model(formatter_prompt, self.agent.formatter_model, require_json=True)
        
        if self.verbose:
            print(f"[Formatter] JSON: {formatter_response}")
        
        # Parse the JSON response
        try:
            import json
            parsed_intent = json.loads(formatter_response)
            
            # Validate the parsed intent
            if parsed_intent is None or parsed_intent.get("action") is None:
                if self.verbose:
                    print("[DualLLM Parser] No valid action found")
                return None
            
            if self.verbose:
                print(f"[DualLLM Parser] Parsed intent: {parsed_intent}")
            
            return parsed_intent
            
        except json.JSONDecodeError as e:
            if self.verbose:
                print(f"[DualLLM Parser] JSON parsing failed: {e}")
            return None
        except Exception as e:
            if self.verbose:
                print(f"[DualLLM Parser] Parsing failed: {e}")
            return None 