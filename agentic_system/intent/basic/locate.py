from .base import BaseIntentParser
from typing import Optional, Dict
import re

class LocateIntentParser(BaseIntentParser):
    def parse(self, instruction: str) -> Optional[Dict]:
        # Match 'locate <pattern>', 'find <pattern> in <directory>'
        match = re.match(r'(?:locate|find)\s+(\S+)(?:\s+in\s+(\S+))?', instruction, re.IGNORECASE)
        if match:
            pattern = match.group(1).strip()
            directory = match.group(2).strip() if match.group(2) else None
            intent = {'action': 'locate', 'pattern': pattern}
            if directory:
                intent['directory'] = directory
            return intent
        return None 