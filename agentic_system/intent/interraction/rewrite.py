from agentic_system.intent.base import BaseIntentParser
from typing import Optional, Dict
import re

class RewriteIntentParser(BaseIntentParser):
    def parse(self, instruction: str) -> Optional[Dict]:
        # Match 'rewrite <file> with <prompt> to <output>'
        match = re.match(r'rewrite\s+(.+)\s+with\s+(.+)\s+to\s+(.+)', instruction, re.IGNORECASE)
        if match:
            file = match.group(1).strip()
            prompt = match.group(2).strip()
            output = match.group(3).strip()
            return {'action': 'rewrite', 'file': file, 'prompt': prompt, 'output': output}
        # Match 'rewrite <file> to <output> with <prompt>'
        match = re.match(r'rewrite\s+(.+)\s+to\s+(.+)\s+with\s+(.+)', instruction, re.IGNORECASE)
        if match:
            file = match.group(1).strip()
            output = match.group(2).strip()
            prompt = match.group(3).strip()
            return {'action': 'rewrite', 'file': file, 'prompt': prompt, 'output': output}
        return None 