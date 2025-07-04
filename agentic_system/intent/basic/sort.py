from .base import BaseIntentParser
from typing import Optional, Dict
import re

class SortIntentParser(BaseIntentParser):
    def parse(self, instruction: str) -> Optional[Dict]:
        # Match 'sort <file>', 'sort <file> to <output>'
        match = re.match(r'sort\s+(\S+)(?:\s+to\s+(\S+))?', instruction, re.IGNORECASE)
        if match:
            path = match.group(1).strip()
            output_path = match.group(2).strip() if match.group(2) else None
            intent = {'action': 'sort', 'path': path}
            if output_path:
                intent['output_path'] = output_path
            return intent
        return None 