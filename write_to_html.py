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
                assert isinstance(date_h2, Tag)
                new_date_h2 = soup.new_tag("h2", attrs={"id":"date"})
                new_date_h2.insert(0, date)
                date_h2.replace_with(new_date_h2)

                numbers_h3 = soup.find("h3", {"id": "numbers"})
                assert isinstance(numbers_h3, Tag)
                new_numbers_h3 = soup.new_tag("h3", attrs={"id":"numbers"})
                new_numbers_h3.insert(0, draw_numbers_and_extra)
                numbers_h3.replace_with(new_numbers_h3)
                
            with open(FILE_PATH, "wb") as file:
                file.write(soup.prettify("utf-8"))

            success = True
            error = ""
            return (success, error)
        except Exception as ex:
            success = False
            error = str(ex)
            return (success, error)
    
    @staticmethod
    def write_scores_to_html(index_to_score: dict) -> tuple[bool, str]:
        # try:
        with open(FILE_PATH, 'r') as html:
            soup = BeautifulSoup(html, 'lxml')
            scores_ul = soup.find("ul", {"id": "scores"})
            assert isinstance(scores_ul, Tag)

            new_scores_ul = soup.new_tag("ul", attrs={"id": "scores"})

            for idx, score in index_to_score.items():
                new_score_li = soup.new_tag("li", attrs={"id": f"score-{idx}"})
                new_score_li.insert(0, f"{idx}: {score}")
                new_scores_ul.append(new_score_li)
            
            scores_ul.replace_with(new_scores_ul)

        with open(FILE_PATH, "wb") as file:
            file.write(soup.prettify("utf-8"))

        success = True
        error = ""
        return (success, error)
        # except Exception as ex:
        #     success = False
        #     error = str(ex)
        #     return (success, error)