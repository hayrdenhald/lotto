from bs4 import BeautifulSoup, Tag

from game_result import GameResult

FILE_PATH = "index.html"


class HtmlWriter():

    @staticmethod
    def write_game_result_to_html(game_result: GameResult) -> tuple[bool, str]:
        timestamp = game_result.date
        draw_standard = ', '.join(str(x) for x in game_result.draw_numbers.standard)
        draw_extra = str(game_result.draw_numbers.extra)

        try:
            with open(FILE_PATH, 'r') as html:
                soup = BeautifulSoup(html, 'lxml')
                
                HtmlWriter.create_tag_and_replace(soup,
                    "h3",
                    {"id":"timestamp"},
                    timestamp
                )

                HtmlWriter.create_tag_and_replace(
                    soup, 
                    "h3",
                    {"id": "draw-standard"},
                    draw_standard
                )

                HtmlWriter.create_tag_and_replace(
                    soup, 
                    "h3", 
                    {"id": "draw-extra"}, 
                    f"extra: {draw_extra}"
                )

                
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
    def create_tag_and_replace(soup: BeautifulSoup, tag: str, attrs: dict[str, str] = {}, to_insert: str = "") -> None:
        old_tag = soup.find(tag, attrs)
        assert isinstance(old_tag, Tag)
        new_tag = soup.new_tag("h3", attrs=attrs)
        if to_insert:
            new_tag.insert(0, to_insert)
        old_tag.replace_with(new_tag)

    @staticmethod
    def create_tag_and_append(soup: BeautifulSoup, tag: str, append_to: Tag, attrs: dict[str, str] = {}, to_insert: str = "") -> None:    
        new_tag = soup.new_tag(tag, attrs=attrs)
        if to_insert:
            new_tag.insert(0, to_insert)
        append_to.append(new_tag)

    @staticmethod
    def write_scores_to_html(index_to_table: dict) -> tuple[bool, str]:
        try:
            with open(FILE_PATH, 'r') as html:
                soup = BeautifulSoup(html, 'lxml')
                score_table = soup.find("table", {"id": "scores"})
                assert isinstance(score_table, Tag)

                new_score_table = soup.new_tag("table", attrs={"id": "scores"})

                for idx, score in index_to_table.items():
                    new_score_tr = soup.new_tag("tr")
                    HtmlWriter.create_tag_and_append(soup, "td", new_score_tr, {"style": "text-align: right;"}, str(idx))
                    HtmlWriter.create_tag_and_append(soup, "td", new_score_tr, {"id": f"score-{idx}", "style": "text-align: left;"}, score)
                    new_score_table.append(new_score_tr)
                
                score_table.replace_with(new_score_table)

            with open(FILE_PATH, "wb") as file:
                file.write(soup.prettify("utf-8"))

            success = True
            error = ""
            return (success, error)
        except Exception as ex:
            success = False
            error = str(ex)
            return (success, error)