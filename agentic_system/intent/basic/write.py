from agentic_system.intent.base import BaseIntentParser
from typing import Optional, Dict
import re

class WriteIntentParser(BaseIntentParser):
    def parse(self, instruction: str) -> Optional[Dict]:
        # Match 'write <text> to <file>'
        match = re.match(r'write\s+(.+)\s+to\s+(.+)', instruction, re.IGNORECASE)
        if match:
            text = match.group(1).strip()
            file = match.group(2).strip()
            return {'action': 'write', 'file': file, 'text': text}
        # Match 'write to <file>: <text>'
        match = re.match(r'write to\s+(.+):\s*(.+)', instruction, re.IGNORECASE)
        if match:
            file = match.group(1).strip()
            text = match.group(2).strip()
            return {'action': 'write', 'file': file, 'text': text}
        return None 