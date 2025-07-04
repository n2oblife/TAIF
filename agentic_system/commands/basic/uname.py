import platform
from agentic_system.commands.basic.base import BaseCommand

class UnameCommand(BaseCommand):
    def __init__(self):
        pass
    def execute(self) -> str:
        return platform.uname().__str__() 