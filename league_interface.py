
import requests
from bs4 import BeautifulSoup

from config import HEADERS

class League:

    def __init__(self, league_id):
        self.league_id = str(league_id)
        self.free_agents = []

    # Find the top free agents from the league
    def find_free_agents(self):
        for i in range(4):  # 4 because each page has 25 players and 25 * 4 is 100
            url = "https://football.fantasysports.yahoo.com/f1/" + self.league_id \
                  + "/players?status=A&pos=O&cut_type=9&stat1=S_S_2020&myteam=0&sort=R_PO&sdir=1&count=" + str(i * 25)
            response = requests.get(url, headers=HEADERS)
            soup = BeautifulSoup(response.content, features="html.parser")
            for div in soup.findAll("div", class_="ysf-player-name Nowrap Grid-u Relative Lh-xs Ta-start"):
                player = div.find("a").text
                position = div.find("span").text.split("- ")[-1]
                self.free_agents.append([position, player])
