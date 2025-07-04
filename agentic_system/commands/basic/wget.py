from agentic_system.commands.basic.base import BaseCommand
import requests
from pathlib import Path

class WgetCommand(BaseCommand):
    def __init__(self, url: str, output_path: str):
        self.url = url
        self.output_path = Path(output_path)
    def execute(self) -> str:
        try:
            response = requests.get(self.url)
            response.raise_for_status()
            self.output_path.write_bytes(response.content)
            return f"Downloaded {self.url} to {self.output_path}"
        except Exception as e:
            return f"Error downloading file: {e}" 