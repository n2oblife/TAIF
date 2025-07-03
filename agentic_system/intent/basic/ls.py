from .base import BaseIntentParser
from typing import Optional, Dict
import re

class LsIntentParser(BaseIntentParser):
    def parse(self, instruction: str) -> Optional[Dict]:
        # Match 'ls <path>' or 'list files in <path>'
        match = re.match(r'(?:ls|list files in)\s+(.+)', instruction, re.IGNORECASE)
        if match:
            path = match.group(1).strip()
            return {'action': 'ls', 'path': path}
        # If just 'ls' or 'list files', default to current directory
        if instruction.strip().lower() in ['ls', 'list files']:
            return {'action': 'ls', 'path': '.'}
        return None 