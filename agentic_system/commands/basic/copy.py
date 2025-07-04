from pathlib import Path
from agentic_system.commands.basic.base import BaseCommand
import shutil
from typing import Optional

class CopyCommand(BaseCommand):
    def __init__(self, src: str, dst: str, files: Optional[str] = None):
        self.src = Path(src)
        self.dst = Path(dst)
        self.files = files
    def execute(self) -> str:
        if not self.src.exists() or not self.src.is_dir():
            return f"Source directory not found: {self.src}"
        if not self.dst.exists():
            self.dst.mkdir(parents=True, exist_ok=True)
        copied = []
        for file in self.src.iterdir():
            if file.is_file():
                if self.files and file.name not in self.files:
                    continue
                shutil.copy2(str(file), str(self.dst / file.name))
                copied.append(file.name)
        return f"Copied files: {', '.join(copied)}" if copied else "No files copied." 