import pandas as pd

from config import SOUP


class RankingsParser:

    def __init__(self):
        # Declare vars
        self.rankings = {}
        for key in SOUP.keys():
            self.rankings[key] = []

    def parse(self):
        # Iterate through each ranking table
        for key in SOUP.keys():
            for div in SOUP[key].find("div", class_="table-responsive"):
                for tr in div.findAll("tr"):
                    for i, td in enumerate(tr.findAll("td")):
                        if i == 1:
                            self.rankings[key].append(td.text)

        print(self.rankings)

    # Generate a text file to copy/paste into yahoo chrome extension
    def generate_yahoo_rankings(self):
        string = "\n".join(self.rankings["GENERAL"])
        file = open("yahoo_rankings.txt", "w")
        file.write(string)
        file.close()
