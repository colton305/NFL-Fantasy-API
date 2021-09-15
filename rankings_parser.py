import pandas as pd
import requests
from bs4 import BeautifulSoup

from config import SOUP, HEADERS


class RankingsParser:

    def __init__(self):
        # Declare vars
        self.rankings = {}
        for key in SOUP.keys():
            self.rankings[key] = []

    def parse_draft_rankings(self):
        # Iterate through each ranking table
        for key in SOUP.keys():
            for div in SOUP[key].find("div", class_="table-responsive"):
                for tr in div.findAll("tr"):
                    for i, td in enumerate(tr.findAll("td")):
                        if i == 1:
                            self.rankings[key].append(td.text)
        print(self.rankings)

    def parse_rankings(self):
        with open("weekly_rankings.txt", "r") as file:
            articles = file.read().split(",")
        for i, article in enumerate(articles):
            response = requests.get("https://www.thescore.com/news/"+article, headers=HEADERS)
            soup = BeautifulSoup(response.content, features="html.parser")
            for div in soup.find("div", class_="table-responsive"):
                for tr in div.findAll("tr"):
                    for j, td in enumerate(tr.findAll("td")):
                        if i == 6 and j == 1:
                            self.rankings["GENERAL"].append(td.text)
                        else:
                            if j == 1:
                                self.rankings[list(SOUP.keys())[i + 1]].append(td.text)  # Access the soup keys by index

    # Convert self.rankings to a csv
    def generate_ranking_summary(self):
        df = pd.DataFrame(dict([(k, pd.Series(v)) for k, v in self.rankings.items()]))
        df.to_csv("ranking_summary.csv")

    # Generate a text file to copy/paste into yahoo chrome extension
    def generate_yahoo_rankings(self):
        string = "\n".join(self.rankings["GENERAL"])
        file = open("yahoo_rankings.txt", "w")
        file.write(string)
        file.close()
