from pathlib import Path
from .base import BaseCommand
import shutil

class RmdirCommand(BaseCommand):
    def __init__(self, path: str, force: bool = False):
        self.path = Path(path)
        self.force = force
    def execute(self) -> str:
        if not self.path.exists() or not self.path.is_dir():
            return f"Directory not found: {self.path}"
        try:
            if self.force:
                shutil.rmtree(self.path)
                return f"Directory and contents removed: {self.path}"
            else:
                self.path.rmdir()
                return f"Empty directory removed: {self.path}"
        except Exception as e:
            return f"Error removing directory: {e}" 