from dataclasses import dataclass
from datetime import datetime
from typing import Dict, List

from draw_number import DrawNumber


@dataclass
class GameResult():
    draw_id: int
    _date: str
    is_finalized: bool
    _draw_numbers: DrawNumber

    def __init__(
            self,
            draw_id: int,
            date_raw: str,
            is_finalized_raw: str,
            draw_number_raw: List[Dict[str, str | int]]
    ):
        self.draw_id = draw_id
        self._date = datetime.fromisoformat(
            date_raw).strftime('%Y/%m/%d %H:%M')
        self.is_finalized = bool(is_finalized_raw)
        self._draw_numbers = self.parse_draw_number(draw_number_raw)

    def parse_draw_number(self, draw_number_raw) -> DrawNumber:
        standard = []
        extra = -1
        for number_raw in draw_number_raw:
            number = number_raw['number']
            type = number_raw['type']
            if type == 2:
                extra = number
            else:
                standard.append(number)
        return DrawNumber(standard, extra)

    @property
    def date(self):
        return self._date

    @property
    def draw_numbers(self):
        return self._draw_numbers
