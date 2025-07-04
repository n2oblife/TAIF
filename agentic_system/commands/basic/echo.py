from agentic_system.commands.basic.base import BaseCommand

class EchoCommand(BaseCommand):
    def __init__(self, text: str):
        self.text = text
    def execute(self) -> str:
        return self.text 