from abc import ABC, abstractmethod
from typing import Optional, Dict

class BaseIntentParser(ABC):
    @abstractmethod
    def parse(self, instruction: str) -> Optional[Dict]:
        pass 