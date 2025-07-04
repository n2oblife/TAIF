from .base import BaseIntentParser
from typing import Optional, Dict
import re

class UnameIntentParser(BaseIntentParser):
    def parse(self, instruction: str) -> Optional[Dict]:
        # Match 'uname', 'show os info', 'show system info', 'show platform info'
        if re.match(r'^(uname|show os info|show system info|show platform info)$', instruction.strip(), re.IGNORECASE):
            return {'action': 'uname'}
        return None 