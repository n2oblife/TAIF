from pathlib import Path
from .base import BaseCommand
from typing import Optional, List
import fnmatch

class LocateCommand(BaseCommand):
    def __init__(self, pattern: str, directory: Optional[str] = None):
        self.pattern = pattern
        self.directory = Path(directory) if directory else Path.cwd()
    def execute(self) -> str:
        matches: List[str] = []
        try:
            for path in self.directory.rglob('*'):
                if fnmatch.fnmatch(path.name, self.pattern):
                    matches.append(str(path))
            if matches:
                return '\n'.join(matches)
            else:
                return f"No files found matching: {self.pattern}"
        except Exception as e:
            return f"Error locating files: {e}" 