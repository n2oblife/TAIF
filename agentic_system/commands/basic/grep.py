from pathlib import Path
from agentic_system.commands.basic.base import BaseCommand
from typing import Optional

class GrepCommand(BaseCommand):
    def __init__(self, directory: str, pattern: str, files: Optional[str] = None):
        self.directory = Path(directory)
        self.pattern = pattern
        self.files = files
    def execute(self) -> str:
        if not self.directory.exists() or not self.directory.is_dir():
            return f"Directory not found: {self.directory}"
        matches = []
        for file in self.directory.iterdir():
            if file.is_file():
                if self.files and file.name not in self.files:
                    continue
                try:
                    with open(file, 'r', encoding='utf-8', errors='ignore') as f:
                        for i, line in enumerate(f, 1):
                            if self.pattern in line:
                                matches.append(f"{file.name}:{i}:{line.strip()}")
                except Exception:
                    continue
        return '\n'.join(matches) if matches else "No matches found." 