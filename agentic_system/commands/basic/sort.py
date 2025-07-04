from pathlib import Path
from agentic_system.commands.basic.base import BaseCommand
from typing import Optional

class SortCommand(BaseCommand):
    def __init__(self, path: str, output_path: Optional[str] = None):
        self.path = Path(path)
        self.output_path = Path(output_path) if output_path else None
    def execute(self) -> str:
        if not self.path.exists() or not self.path.is_file():
            return f"File not found: {self.path}"
        try:
            lines = self.path.read_text(encoding='utf-8').splitlines()
            lines.sort()
            result = '\n'.join(lines)
            if self.output_path:
                self.output_path.write_text(result, encoding='utf-8')
                return f"Sorted lines written to: {self.output_path}"
            return result
        except Exception as e:
            return f"Error sorting file: {e}" 