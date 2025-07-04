from pathlib import Path
from agentic_system.commands.basic.base import BaseCommand
import os

class LnCommand(BaseCommand):
    def __init__(self, target_path: str, link_path: str):
        self.target_path = Path(target_path)
        self.link_path = Path(link_path)
    def execute(self) -> str:
        try:
            if self.link_path.exists():
                return f"Link already exists: {self.link_path}"
            os.symlink(self.target_path, self.link_path)
            return f"Symlink created: {self.link_path} -> {self.target_path}"
        except Exception as e:
            return f"Error creating symlink: {e}" 