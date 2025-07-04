from .base import BaseIntentParser
from typing import Optional, Dict
import re

class CatIntentParser(BaseIntentParser):
    def parse(self, instruction: str) -> Optional[Dict]:
        # Match 'cat <path>' or 'show contents of <path>'
        match = re.match(r'(?:cat|show contents of|display contents of)\s+(.+)', instruction, re.IGNORECASE)
        if match:
            path = match.group(1).strip()
            return {'action': 'cat', 'path': path}
        return None 