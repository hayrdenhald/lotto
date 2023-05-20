from dataclasses import dataclass
from typing import List


@dataclass
class DrawNumber():
    standard: List[int]
    extra: int

    def __str__(self) -> str:
        return f"{', '.join(str(x) for x in self.standard)}, extra: {self.extra}"
