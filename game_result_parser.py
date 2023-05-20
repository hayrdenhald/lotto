import json
from typing import Any

import requests
from bs4 import BeautifulSoup

from game_result import GameResult

WEBSITE_URL = "https://www.norsk-tipping.no/lotteri/lotto/resultater"


def get_html_from_url(url: str) -> tuple[bool, str, str]:
    response = requests.get(WEBSITE_URL)
    if response.status_code == 200:
        html = response.text
        success = True
        return (success, "", html)
    else:
        success = False
        error = f"Getting HTML from url failed, status code: {response.status_code}"
        return (success, error, response.text)


def get_data_from_html(html: str) -> tuple[bool, str, dict]:
    soup = BeautifulSoup(html, 'lxml')
    scripts = soup.findAll('script')
    SCRIPT_IDX = 4
    script = scripts[SCRIPT_IDX].prettify()

    success, pertinent = get_text_section_between(
        script,
        start_excl="window.__PRELOADED_USE_API__ = ",
        stop_excl="\n      window.__NT_ENV__ = "
    )
    if not success:
        error = "Getting a inbetween text section (PRELOADED_USE_API) failed!"
        return (success, error, {})

    json_object = json.loads(json.loads(pertinent))

    success, base_key = get_text_section_between(
        str(json_object),
        start_excl="{'",
        stop_excl="':"
    )
    if not success:
        error = "Getting a inbetween text section (base_key) failed!"
        return (success, error, {})

    base = json_object[base_key]
    data = base['data']

    success = True
    return (success, "", data)


def get_text_section_between(text: str, start_excl: str, stop_excl) -> tuple[bool, str]:
    start = text.find(start_excl)
    stop = text.find(stop_excl)

    if start == -1 or stop == -1:
        success = False
        return (success, "")

    section = text[start + len(start_excl):stop]
    success = True
    return (success, section)


def get_game_results_from_data(data: dict[str, Any]) -> tuple[bool, str,  list[GameResult]]:
    if 'gameResult' not in data:
        success = False
        return (success, "The data does not contain the key 'gameResult'", [])

    game_results_raw = data['gameResult']

    game_results: list[GameResult] = []

    for game_result_raw in game_results_raw:
        game_results.append(
            GameResult(
                game_result_raw['drawId'],
                game_result_raw['drawDate'],
                game_result_raw['isFinalized'],
                game_result_raw['winnerNumber'],
            )
        )

    if not game_results:
        success = False
        return (success, "No game results found during parsing of data!", [])

    success = True
    return (success, "", game_results)
