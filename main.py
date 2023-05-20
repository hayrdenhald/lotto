import logging
import logging.handlers
import os
import sys

from game_result_parser import *
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


def main() -> int:
    (success, error, html) = get_html_from_url(WEBSITE_URL)
    if not success:
        return 1

    (success, error, data) = get_data_from_html(html)
    if not success:
        logger.error(f"Getting data from html failed: {error}")
        return 1

    (success, error, game_results) = get_game_results_from_data(data)
    if not success:
        logger.error(f"Getting game results from data failed: {error}")
        return 1

    (success, error) = HtmlWriter.write_result_to_html(game_results[0])
    if not success:
        logger.error(f"Writing result to 'index.html' failed: {error}")
        return 1

    # try:
    #     SOME_SECRET = os.environ["SOME_SECRET"]
    # except KeyError:
    #     SOME_SECRET = "Token not available!"
    #     logger.info("Token not available!")
    #     # raise

    logger.info(f"Succesfully got results, and wrote to HTML file.")
    return 0


if __name__ == "__main__":
    sys.exit(main())