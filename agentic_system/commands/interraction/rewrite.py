from agentic_system.commands.base import BaseCommand
from agentic_system.core import Agent
from pathlib import Path
from typing import Optional

class RewriteCommand(BaseCommand):
    def __init__(self, file: str, prompt: str, output: str, model: str = "llama2"):
        self.file = Path(file)
        self.prompt = prompt
        self.output = Path(output)
        self.model = model
    def execute(self) -> str:
        if not self.file.exists():
            return f"Input file not found: {self.file}"
        try:
            with open(self.file, 'r', encoding='utf-8') as f:
                content = f.read()
            agent = Agent(model=self.model)
            full_prompt = f"{self.prompt}\n\n---\n\n{content}"
            rewritten = agent.ask(full_prompt)
            with open(self.output, 'w', encoding='utf-8') as out:
                out.write(rewritten)
            return f"Rewritten file saved to {self.output}"
        except Exception as e:
            return f"Error rewriting file: {e}" 