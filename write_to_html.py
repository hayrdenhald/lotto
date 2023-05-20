from bs4 import BeautifulSoup, Tag

from game_result import GameResult

FILE_PATH = "index.html"


class HtmlWriter():

    @staticmethod
    def write_result_to_html(game_result: GameResult) -> tuple[bool, str]:
        date = game_result.date
        draw_numbers_and_extra = str(game_result.draw_numbers)

        try:
            with open(FILE_PATH, 'r') as html:
                soup = BeautifulSoup(html, 'lxml')
                date_h2 = soup.find("h2", {"id": "date"})
                numbers_h3 = soup.find("h3", {"id": "numbers"})
                assert isinstance(date_h2, Tag)
                date_h2.insert(0, date)
                assert isinstance(numbers_h3, Tag)
                numbers_h3.insert(0, draw_numbers_and_extra)

            with open(FILE_PATH, "wb") as file:
                file.write(soup.prettify("utf-8"))

            success = True
            error = ""
            return (success, error)
        except Exception as ex:
            success = False
            error = str(ex)
            return (success, error)
