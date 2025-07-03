from pathlib import Path
from .base import BaseCommand
from typing import Optional

class LsCommand(BaseCommand):
    def __init__(self, path: str = '.'):  # default to current directory
        self.path = Path(path)
    def execute(self) -> str:
        if not self.path.exists() or not self.path.is_dir():
            return f"Directory not found: {self.path}"
        return '\n'.join(str(p) for p in self.path.iterdir()) 