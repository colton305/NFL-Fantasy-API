from config import LEAGUE_IDS, TEAM_INDEXES
from rankings_parser import RankingsParser
from team_interface import Team

if __name__ == "__main__":
    parser = RankingsParser()

    parser.parse()
    parser.generate_ranking_summary()
    parser.generate_yahoo_rankings()

    teams = []
    for i, league in enumerate(LEAGUE_IDS):
        teams.append(Team(league, TEAM_INDEXES[i]))
        teams[i].generate_roster()
    for team in teams:
        print(team.roster)
