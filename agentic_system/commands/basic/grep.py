from agentic_system.commands.basic.base import BaseCommand
import re
from pathlib import Path

class GrepCommand(BaseCommand):
    def __init__(self, pattern: str, path: str):
        self.pattern = pattern
        self.path = Path(path)
    def execute(self) -> str:
        if not self.path.exists() or not self.path.is_file():
            return f"File not found: {self.path}"
        try:
            with self.path.open('r', encoding='utf-8') as f:
                lines = f.readlines()
            matches = [line for line in lines if re.search(self.pattern, line)]
            return ''.join(matches) if matches else f"No matches for pattern: {self.pattern}"
        except Exception as e:
            return f"Error grepping file: {e}" 