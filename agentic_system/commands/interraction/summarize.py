from pathlib import Path
from agentic_system.commands.base import BaseCommand
from agentic_system.core import Agent
from typing import Optional

class SummarizeCommand(BaseCommand):
    def __init__(self, file: str, model: str = "mistral", max_length: Optional[int] = None):
        self.file = Path(file)
        self.model = model
        self.max_length = max_length
        self.agent = Agent(model=model)
    
    def execute(self) -> str:
        """Execute the summarization process."""
        if not self.file.exists():
            return f"File not found: {self.file}"
        
        if not self.file.is_file():
            return f"Path is not a file: {self.file}"
        
        try:
            # Step 1: Read the file content
            content = self.file.read_text(encoding='utf-8')
            
            # Step 2: Create a summarization prompt
            summary_prompt = self._create_summary_prompt(content)
            
            # Step 3: Use the LLM to summarize
            summary = self.agent.ask(summary_prompt, require_json=False)
            
            return summary
            
        except Exception as e:
            return f"Error summarizing file: {e}"
    
    def _create_summary_prompt(self, content: str) -> str:
        """Create a prompt for summarizing the content."""
        prompt = f"""Please provide a concise, natural language summary of the following content. Focus on the main points and key information. Write in a clear, readable format.

Content to summarize:
{content}

Please provide a summary in natural language (not JSON format):"""
        
        if self.max_length:
            prompt += f"\n\nPlease keep the summary under {self.max_length} words."
        
        return prompt 