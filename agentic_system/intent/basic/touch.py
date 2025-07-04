from .base import BaseIntentParser
from typing import Optional, Dict
import re

class TouchIntentParser(BaseIntentParser):
    def parse(self, instruction: str) -> Optional[Dict]:
        # Match 'touch <path>', 'create file <path>', 'update file <path>'
        match = re.match(r'(?:touch|create file|update file)\s+(.+)', instruction, re.IGNORECASE)
        if match:
            path = match.group(1).strip()
            return {'action': 'touch', 'path': path}
        return None 