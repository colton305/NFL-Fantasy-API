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

    def parse_ros_rankings(self):
        with open("ros_rankings.txt", "r") as file:
            articles = file.read().split(",")
        rb_ratings = []
        wr_ratings = []
        for i, article in enumerate(articles):
            response = requests.get("https://www.thescore.com/news/"+article, headers=HEADERS)
            soup = BeautifulSoup(response.content, features="html.parser")
            for div in soup.find("div", class_="table-responsive"):
                for tr in div.findAll("tr"):
                    for j, td in enumerate(tr.findAll("td")):
                        if j == 0:
                            # Access the soup keys by index, split on \n
                            self.rankings[list(SOUP.keys())[i + 1]].append(td.text.split("\n")[-1])
                        elif i == 1 and j == 2:
                            rb_ratings.append(int(td.text))
                        elif i == 2 and j == 2:
                            wr_ratings.append(int(td.text))
        offset = 0
        for i, rb_rating in enumerate(rb_ratings):
            if rb_rating <= 11:
                print(wr_ratings)
            while True:
                if rb_rating >= wr_ratings[0]:
                    self.rankings["GENERAL"].append(self.rankings["RB"][i])
                    break
                else:
                    try:
                        self.rankings["GENERAL"].append(self.rankings["WR"][offset])
                    except IndexError:
                        print(offset, len(self.rankings["WR"]))
                    wr_ratings.pop(0)
                    offset += 1

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
