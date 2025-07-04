from .base import BaseIntentParser
from typing import Optional, Dict
import re

class RmdirIntentParser(BaseIntentParser):
    def parse(self, instruction: str) -> Optional[Dict]:
        # Match 'rmdir <path>', 'remove directory <path>', 'delete folder <path>'
        # Optionally match 'force' or 'recursively'
        match = re.match(r'(?:rmdir|remove directory|delete folder)\s+(.+?)(?:\s+(force|recursively))?$', instruction, re.IGNORECASE)
        if match:
            path = match.group(1).strip()
            force = bool(match.group(2))
            return {'action': 'rmdir', 'path': path, 'force': force}
        return None 