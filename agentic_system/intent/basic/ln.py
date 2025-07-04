from .base import BaseIntentParser
from typing import Optional, Dict
import re

class LnIntentParser(BaseIntentParser):
    def parse(self, instruction: str) -> Optional[Dict]:
        # Match 'ln <target> <link>', 'create symlink <target> <link>'
        match = re.match(r'(?:ln|create symlink)\s+(\S+)\s+(\S+)', instruction, re.IGNORECASE)
        if match:
            target_path = match.group(1).strip()
            link_path = match.group(2).strip()
            return {'action': 'ln', 'target_path': target_path, 'link_path': link_path}
        return None 