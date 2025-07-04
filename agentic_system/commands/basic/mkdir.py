from pathlib import Path
from agentic_system.commands.basic.base import BaseCommand

class MkdirCommand(BaseCommand):
    def __init__(self, path: str):
        self.path = Path(path)
    def execute(self) -> str:
        try:
            self.path.mkdir(parents=True, exist_ok=False)
            return f"Directory created: {self.path}"
        except FileExistsError:
            return f"Directory already exists: {self.path}"
        except Exception as e:
            return f"Error creating directory: {e}" 