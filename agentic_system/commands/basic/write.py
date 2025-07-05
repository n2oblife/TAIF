from agentic_system.commands.basic.base import BaseCommand
from pathlib import Path
from typing import Optional

class WriteCommand(BaseCommand):
    def __init__(self, file: str, text: str):
        self.file = Path(file)
        self.text = text
    def execute(self) -> str:
        try:
            self.file.write_text(self.text, encoding='utf-8')
            return f"Wrote to {self.file}"
        except Exception as e:
            return f"Error writing to file: {e}" 