import pandas as pd

from config import SOUP


class RankingsParser:

    def __init__(self):
        # Declare vars
        self.players = []

    def parse(self):
        # Iterate through ranking table
        for div in SOUP.find("div", class_="table-responsive"):
            for tr in div.findAll("tr"):
                for i, td in enumerate(tr.findAll("td")):
                    if i == 1:
                        self.players.append(td.text)

        print(self.players)

    # Generate a text file to copy/paste into yahoo chrome extension
    def generate_yahoo_rankings(self):
        str = "\n".join(self.players)
        file = open("yahoo_rankings.txt", "w")
        file.write(str)
        file.close()
