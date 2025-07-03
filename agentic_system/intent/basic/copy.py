from .base import BaseIntentParser
from typing import Optional, Dict
import os
import requests
import json
import re

class CopyIntentParser(BaseIntentParser):
    def __init__(self, prompt_dir=None):
        if prompt_dir is None:
            prompt_dir = os.path.join(os.path.dirname(__file__), '../intent_parsers')
        self.prompt_path = os.path.join(prompt_dir, 'copy.json')
    def load_prompt(self) -> Optional[str]:
        if not os.path.exists(self.prompt_path):
            return None
        with open(self.prompt_path, 'r', encoding='utf-8') as f:
            return f.read()
    def parse(self, instruction: str) -> Optional[Dict]:
        prompt = self.load_prompt()
        if not prompt:
            return None
        prompt = prompt.replace("{{instruction}}", instruction)
        try:
            response = requests.post(
                "http://localhost:11434/api/generate",
                json={"model": "llama2", "prompt": prompt}
            )
            response.raise_for_status()
            resp_text = response.json()["response"]
            match = re.search(r"\{.*\}", resp_text, re.DOTALL)
            if match:
                return json.loads(match.group(0))
        except Exception:
            pass
        return None 