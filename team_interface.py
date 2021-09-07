
import requests
from bs4 import BeautifulSoup

from config import HEADERS


class Team:

    def __init__(self, league_id, index):
        self.roster = []
        self.league_id = str(league_id)
        self.index = str(index)

    # Create a list of players from each team
    def generate_roster(self):
        response = requests.get("https://football.fantasysports.yahoo.com/f1/" + self.league_id
                                + "/" + self.index, headers=HEADERS)
        soup = BeautifulSoup(response.content, features="html.parser")
        for div in soup.findAll("div", class_="ysf-player-name Nowrap Grid-u Relative Lh-xs Ta-start"):
            try:
                position = div.find("span").text.split("- ")[-1]
                player = div.find("a").text
                self.roster.append([position, player])
            except AttributeError:
                pass
