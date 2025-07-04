from .base import BaseIntentParser
from typing import Optional, Dict
import re

class WcIntentParser(BaseIntentParser):
    def parse(self, instruction: str) -> Optional[Dict]:
        # Match 'wc <file>', 'count <file>', 'count words in <file>'
        match = re.match(r'(?:wc|count|count words in)\s+(.+)', instruction, re.IGNORECASE)
        if match:
            path = match.group(1).strip()
            return {'action': 'wc', 'path': path}
        return None 