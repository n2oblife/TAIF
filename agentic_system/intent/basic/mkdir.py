from .base import BaseIntentParser
from typing import Optional, Dict
import re

class MkdirIntentParser(BaseIntentParser):
    def parse(self, instruction: str) -> Optional[Dict]:
        # Match 'mkdir <path>', 'make directory <path>', 'create folder <path>'
        match = re.match(r'(?:mkdir|make directory|create folder)\s+(.+)', instruction, re.IGNORECASE)
        if match:
            path = match.group(1).strip()
            return {'action': 'mkdir', 'path': path}
        return None 