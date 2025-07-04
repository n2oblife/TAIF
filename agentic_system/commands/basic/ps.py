from agentic_system.commands.basic.base import BaseCommand
import subprocess

class PsCommand(BaseCommand):
    def __init__(self):
        pass
    def execute(self) -> str:
        try:
            try:
                import psutil
                procs = [f"{p.pid} {p.name()}" for p in psutil.process_iter(['pid', 'name'])]
                return '\n'.join(procs)
            except ImportError:
                # Fallback to 'ps' command (Unix only)
                result = subprocess.run(['ps', 'aux'], capture_output=True, text=True)
                return result.stdout
        except Exception as e:
            return f"Error listing processes: {e}" 