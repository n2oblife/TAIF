from .base import BaseIntentParser
from typing import Optional, Dict
import re

class EchoIntentParser(BaseIntentParser):
    def parse(self, instruction: str) -> Optional[Dict]:
        # Match 'echo <text>', 'print <text>', 'say <text>'
        match = re.match(r'(?:echo|print|say)\s+(.+)', instruction, re.IGNORECASE)
        if match:
            text = match.group(1).strip()
            return {'action': 'echo', 'text': text}
        return None 