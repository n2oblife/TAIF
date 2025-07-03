from agentic_system.commands.base import BaseCommand
from pathlib import Path
import shutil
from typing import Optional, List

class MoveCommand(BaseCommand):
    def __init__(self, src: str, dst: str, files: Optional[List[str]] = None):
        self.src = Path(src)
        self.dst = Path(dst)
        self.files = files
    def execute(self) -> str:
        if not self.src.exists() or not self.src.is_dir():
            return f"Source directory not found: {self.src}"
        if not self.dst.exists():
            self.dst.mkdir(parents=True, exist_ok=True)
        moved = []
        for file in self.src.iterdir():
            if file.is_file():
                if self.files and file.name not in self.files:
                    continue
                shutil.move(str(file), str(self.dst / file.name))
                moved.append(file.name)
        return f"Moved files: {', '.join(moved)}" if moved else "No files moved." 