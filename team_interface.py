
import requests
from bs4 import BeautifulSoup
import pandas as pd
import csv
import re

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
        # Remove the players on ir
        while len(self.roster) > 15:  # 15 is the default roster size
            self.roster.pop(-3)

    # Save the roster to a csv
    def save_roster(self):
        df = pd.DataFrame(self.roster)
        df.to_csv("rosters/"+self.league_id+".csv", index=False)

    # Start and sit players on game-day
    def start_sit(self):
        with open("ranking_summary.csv") as file:
            reader = csv.reader(file)
            rankings = list(reader)
        game_day_rank = []
        for player in self.roster:
            if player[0] == "RB" or player[0] == "WR":
                for ranking in rankings:
                    if re.sub(r"[^A-Za-z]+", '', player[1]) == re.sub(r"[^A-Za-z]+", '', ranking[1]):
                        if not game_day_rank:
                            game_day_rank.append([player[0], player[1], ranking[0]])
                            break
                        appended = False
                        for i, lis in enumerate(game_day_rank):
                            if int(ranking[0]) < int(lis[2]):
                                game_day_rank.insert(i, [player[0], player[1], ranking[0]])
                                appended = True
                                break
                        if not appended:
                            game_day_rank.append([player[0], player[1], ranking[0]])
                        break
        return game_day_rank

