from agentic_system.commands.base import BaseCommand
from pathlib import Path
from typing import Optional

class WriteCommand(BaseCommand):
    def __init__(self, file: str, text: str, force: bool = False):
        self.file = Path(file)
        self.text = text
        self.force = force
    def execute(self) -> str:
        if self.file.exists() and not self.force:
            return f"File {self.file} already exists. Use --force to overwrite."
        try:
            with open(self.file, 'w', encoding='utf-8') as f:
                f.write(self.text)
            return f"Wrote to {self.file}"
        except Exception as e:
            return f"Error writing to {self.file}: {e}" 