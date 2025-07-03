from .base import BaseIntentParser
from typing import Optional, Dict
import re

class TreeIntentParser(BaseIntentParser):
    def parse(self, instruction: str) -> Optional[Dict]:
        # Match 'tree <path>' or 'show tree of <path>'
        match = re.match(r'(?:tree|show tree of)\s+(.+)', instruction, re.IGNORECASE)
        if match:
            path = match.group(1).strip()
            return {'action': 'tree', 'path': path}
        # If just 'tree', default to current directory
        if instruction.strip().lower() == 'tree':
            return {'action': 'tree', 'path': '.'}
        return None 