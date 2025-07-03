from pathlib import Path
from .base import BaseCommand
from typing import Optional

class TreeCommand(BaseCommand):
    def __init__(self, path: str = '.', max_depth: Optional[int] = None):
        self.path = Path(path)
        self.max_depth = max_depth
    def execute(self) -> str:
        if not self.path.exists() or not self.path.is_dir():
            return f"Directory not found: {self.path}"
        lines = []
        def walk(p: Path, prefix: str = '', depth: int = 0):
            if self.max_depth is not None and depth > self.max_depth:
                return
            children = sorted(p.iterdir(), key=lambda x: (not x.is_dir(), x.name))
            for i, child in enumerate(children):
                connector = '└── ' if i == len(children) - 1 else '├── '
                lines.append(f"{prefix}{connector}{child.name}")
                if child.is_dir():
                    walk(child, prefix + ('    ' if i == len(children) - 1 else '│   '), depth + 1)
        lines.append(str(self.path.resolve()))
        walk(self.path)
        return '\n'.join(lines) 