import logging
import logging.handlers
import os
import sys

from game_result_parser import *
from result_checker import (get_lotto_numbers_from_environment,
                            score_all_numbers)
from write_to_html import HtmlWriter

logger = logging.getLogger(__name__)
logger.setLevel(logging.DEBUG)
logger_file_handler = logging.handlers.RotatingFileHandler(
    "status.log",
    maxBytes=1024 * 1024,
    backupCount=1,
    encoding="utf8",
)
formatter = logging.Formatter(
    "%(asctime)s - %(name)s - %(levelname)s - %(message)s"
)
logger_file_handler.setFormatter(formatter)
logger.addHandler(logger_file_handler)

API_URL_ENV_VAR = "API_URL"

def main() -> int:
    # api_url = os.environ.get(API_URL_ENV_VAR)
    api_url = "https://www.norsk-tipping.no/lotteri/lotto/resultater"
    if not api_url:
        logger.debug(f"Failed to get api url {API_URL_ENV_VAR} from the environment")
        return 1

    (success, error, html) = get_html_from_url(api_url)
    if not success:
        return 1

    (success, error, data) = get_data_from_html(html)
    if not success:
        logger.debug(f"Getting data from html failed: {error}")
        return 1
    
    (success, error, game_results) = get_game_results_from_data(data)
    if not success:
        logger.debug(f"Getting game results from data failed: {error}")
        return 1

    last_game_result = game_results[0]
    
    (success, error) = HtmlWriter.write_result_to_html(last_game_result)
    if not success:
        logger.debug(f"Writing result to 'index.html' failed: {error}")
        return 1

    (success, error, my_lotto_numbers) = get_lotto_numbers_from_environment()
    if not success:
        logger.debug(f"Failed to get lotto numbers from the environment: {error}")
        return 1

    score = score_all_numbers(
        lotto_numbers=my_lotto_numbers, draw=last_game_result.draw_numbers
    )

    (success, error) = HtmlWriter.write_scores_to_html(score)
    if not success:
        logger.debug(f"Writing scores to 'index.html' failed': {error}")
        return 1

    # score_json = json.dumps(score)

    # print(last_game_result)
    # print(score_json)

    logger.info("Successfully received, parsed and handled results!")
    return 0


if __name__ == "__main__":
    sys.exit(main())
