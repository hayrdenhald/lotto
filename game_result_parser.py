import json
import sys
from typing import Dict, List, Tuple

import requests
from bs4 import BeautifulSoup

from game_result import GameResult

WEBSITE_URL = "https://www.norsk-tipping.no/lotteri/lotto/resultater"

def get_html_from_url(url: str) -> Tuple[bool, str]:
    response = requests.get(WEBSITE_URL)
    if response.status_code == 200:
        html = response.text
        success = True
        return (success, html)
    else:
        success = False
        return (success, response.text)
    
def get_data_from_html(html: str) -> Dict[str, str | int]:
    soup = BeautifulSoup(html, 'lxml')
    scripts = soup.findAll('script')
    SCRIPT_IDX = 4
    script = scripts[SCRIPT_IDX].prettify()
    STR_START = 'window.__PRELOADED_USE_API__ = '
    STR_STOP = "\n      window.__NT_ENV__ = "
    start = script.find(STR_START)
    stop = script.find(STR_STOP)

    if start == -1 or stop == -1:
        success = False
        return (success, {})

    pertinent = script[start + len(STR_START):stop]
    json_object = json.loads(json.loads(pertinent))
    BASE_KEY = "base:https://api.norsk-tipping.no/LotteryGameInfo/v2/api/results/lotto?fromDate=2023-01-30&toDate=2023-05-16"
    base = json_object[BASE_KEY]
    data = base['data']
    success = True

    return (success, data)

def get_game_results_from_data(data: Dict[str, str | int]) -> List[GameResult]:
        game_results = data['gameResult']

        games: List[GameResult] = []

        for game_result in game_results:
            games.append(
                GameResult(
                    game_result['drawId'],
                    game_result['drawDate'],
                    game_result['isFinalized'],
                    game_result['winnerNumber'],
                )
            )
    
        return games
