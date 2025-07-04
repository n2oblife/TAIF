from agentic_system.commands.base import BaseCommand
from pathlib import Path
from typing import Optional

class WriteCommand(BaseCommand):
    def __init__(self, file: str, content=None, force: bool = False):
        self.file = Path(file)
        self.content = content
        self.force = force
        super().__init__()
    def execute(self) -> str:
        if self.file.exists() and not self.force:
            return f"File {self.file} already exists. Use --force to overwrite."
        try:
            content_to_write = self.content if self.content is not None else ""
            with open(self.file, 'w', encoding='utf-8') as f:
                f.write(content_to_write)
            return f"Wrote to {self.file}"
        except Exception as e:
            return f"Error writing to {self.file}: {e}" 