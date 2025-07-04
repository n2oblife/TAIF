from pathlib import Path
from agentic_system.commands.basic.base import BaseCommand

class PwdCommand(BaseCommand):
    def __init__(self):
        pass
    def execute(self) -> str:
        return str(Path.cwd()) 