from .base import BaseIntentParser
from typing import Optional, Dict
import re

class PsIntentParser(BaseIntentParser):
    def parse(self, instruction: str) -> Optional[Dict]:
        # Match 'ps', 'list processes', 'show processes'
        if re.match(r'^(ps|list processes|show processes)$', instruction.strip(), re.IGNORECASE):
            return {'action': 'ps'}
        return None 