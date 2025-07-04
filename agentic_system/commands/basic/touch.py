from pathlib import Path
from .base import BaseCommand
import os
import time

class TouchCommand(BaseCommand):
    def __init__(self, path: str):
        self.path = Path(path)
    def execute(self) -> str:
        try:
            if self.path.exists():
                os.utime(self.path, None)
                return f"Timestamp updated: {self.path}"
            else:
                self.path.touch()
                return f"File created: {self.path}"
        except Exception as e:
            return f"Error touching file: {e}" 