from pathlib import Path
from .base import BaseCommand

class WcCommand(BaseCommand):
    def __init__(self, path: str):
        self.path = Path(path)
    def execute(self) -> str:
        if not self.path.exists() or not self.path.is_file():
            return f"File not found: {self.path}"
        try:
            text = self.path.read_text(encoding='utf-8')
            lines = text.splitlines()
            words = text.split()
            chars = len(text)
            return f"Lines: {len(lines)}, Words: {len(words)}, Characters: {chars}"
        except Exception as e:
            return f"Error counting file: {e}" 