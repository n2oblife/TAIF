from .base import BaseIntentParser
from typing import Optional, Dict
import re

class PwdIntentParser(BaseIntentParser):
    def parse(self, instruction: str) -> Optional[Dict]:
        # Match 'pwd', 'print working directory', 'show current directory', etc.
        if re.match(r'^(pwd|print working directory|show current directory)$', instruction.strip(), re.IGNORECASE):
            return {'action': 'pwd'}
        return None 