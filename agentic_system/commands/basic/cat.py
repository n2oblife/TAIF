from pathlib import Path
from .base import BaseCommand
from typing import Optional

class CatCommand(BaseCommand):
    def __init__(self, path: str):
        self.path = Path(path)
    def execute(self) -> str:
        if not self.path.exists() or not self.path.is_file():
            return f"File not found: {self.path}"
        try:
            return self.path.read_text(encoding='utf-8')
        except Exception as e:
            return f"Error reading file: {e}" 