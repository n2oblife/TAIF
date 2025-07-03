from pathlib import Path
from .base import BaseCommand
from typing import Optional

class DeleteCommand(BaseCommand):
    def __init__(self, src: str, exclude: Optional[str] = None):
        self.src = Path(src)
        self.exclude = exclude
    def execute(self) -> str:
        if not self.src.exists() or not self.src.is_dir():
            return f"Source directory not found: {self.src}"
        deleted = []
        for file in self.src.iterdir():
            if file.is_file():
                if self.exclude and self.exclude in file.name:
                    continue
                file.unlink()
                deleted.append(file.name)
        return f"Deleted files: {', '.join(deleted)}" if deleted else "No files deleted." 