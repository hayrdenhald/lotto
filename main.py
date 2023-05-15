import logging
import logging.handlers
import os
import sys

from game_result_parser import (WEBSITE_URL, get_data_from_html,
                                get_game_results_from_data, get_html_from_url)
from write_to_html import HtmlWriter

logger = logging.getLogger(__name__)
logger.setLevel(logging.DEBUG)
logger_file_handler = logging.handlers.RotatingFileHandler(
    "status.log",
    maxBytes=1024 * 1024,
    backupCount=1,
    encoding="utf8",
)
formatter = logging.Formatter("%(asctime)s - %(name)s - %(levelname)s - %(message)s")
logger_file_handler.setFormatter(formatter)
logger.addHandler(logger_file_handler)

try:
    SOME_SECRET = os.environ["SOME_SECRET"]
except KeyError:
    SOME_SECRET = "Token not available!"
    #logger.info("Token not available!")
    #raise


def main() -> int:
    # logger.info(f"Token value: {SOME_SECRET}")
    #     temperature = data["forecast"]["temp"]
    #     logger.info(f'Weather in Berlin: {temperature}')

    (success, html) = get_html_from_url(WEBSITE_URL)
    if not success:
        return 1
    
    (success, data) = get_data_from_html(html)
    if not success:
        return 1
    
    game_results = get_game_results_from_data(data)

    latest_game_result = game_results[0]
    print(latest_game_result)

    HtmlWriter.write_result_to_html(latest_game_result.date, str(latest_game_result.draw_numbers))

    return 0

if __name__ == "__main__":
    sys.exit(main())
