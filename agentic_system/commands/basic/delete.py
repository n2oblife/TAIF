from agentic_system.commands.basic.base import BaseCommand
from pathlib import Path
import os

class DeleteCommand(BaseCommand):
    def __init__(self, path: str):
        self.path = Path(path)
    def execute(self) -> str:
        try:
            if self.path.is_file():
                self.path.unlink()
                return f"Deleted file: {self.path}"
            elif self.path.is_dir():
                os.rmdir(self.path)
                return f"Deleted directory: {self.path}"
            else:
                return f"Path not found: {self.path}"
        except Exception as e:
            return f"Error deleting: {e}" 