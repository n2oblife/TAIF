from .base import BaseIntentParser
from typing import Optional, Dict
import re

class WgetIntentParser(BaseIntentParser):
    def parse(self, instruction: str) -> Optional[Dict]:
        # Match 'wget <url> to <output>', 'download <url> to <output>'
        match = re.match(r'(?:wget|download)\s+(\S+)\s+to\s+(\S+)', instruction, re.IGNORECASE)
        if match:
            url = match.group(1).strip()
            output_path = match.group(2).strip()
            return {'action': 'wget', 'url': url, 'output_path': output_path}
        return None 