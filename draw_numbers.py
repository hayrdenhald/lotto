from dataclasses import dataclass


@dataclass
class DrawNumber():
    standard: list[int]
    extra: int

    def __str__(self) -> str:
        return f"{', '.join(str(x) for x in self.standard)}, extra: {self.extra}"
