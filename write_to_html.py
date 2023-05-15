import os

from bs4 import BeautifulSoup

FILE_PATH = "index.html"

class HtmlWriter():

    @staticmethod
    def write_result_to_html(date: str, draw_numbers_and_extra: str) -> bool:
        # try:
            with open(FILE_PATH, 'r') as html:
                soup = BeautifulSoup(html, 'lxml')
                date_h2 = soup.find("h2", {"id": "date"})
                numbers_h3 = soup.find("h3", {"id": "numbers"})
                date_h2.string = date
                numbers_h3.string = draw_numbers_and_extra

            with open(FILE_PATH, "wb") as file:
                file.write(soup.prettify("utf-8"))  
            
            success = True
            return success
        # except Exception as ex:
        #     print(f"EXCEPTION: {ex}")
        #     success = False
        #     return success
