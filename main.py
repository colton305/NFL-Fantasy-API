from config import LEAGUE_IDS, TEAM_INDEXES
from rankings_parser import RankingsParser
from team_interface import Team
from league_interface import League

if __name__ == "__main__":
    parser = RankingsParser()

    parser.parse()
    parser.generate_ranking_summary()
    parser.generate_yahoo_rankings()

    leagues = []
    teams = []
    for league_id in LEAGUE_IDS:
        leagues.append(League(league_id))
        leagues[-1].find_free_agents()
        print(leagues[-1].free_agents)

    for i, index in enumerate(TEAM_INDEXES):
        teams.append(Team(leagues[i].league_id, index))
        teams[-1].generate_roster()
        teams[-1].save_roster()
        print(teams[-1].roster)
