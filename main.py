import roster_functions
from config import LEAGUE_IDS, TEAM_INDEXES
from rankings_parser import RankingsParser
from team_interface import Team
from league_interface import League

COMMANDS = ["parse draft rankings", "parse rankings", "parse ros rankings", "generate rosters", "query free agents",
            "start sit", "quit", "exit"]

if __name__ == "__main__":
    while True:
        command = input("Enter command: ")

        if command == "parse draft rankings":
            parser = RankingsParser()
            parser.parse_draft_rankings()
            parser.generate_ranking_summary()
            parser.generate_yahoo_rankings()
            print(parser.rankings)
        elif command == "parse rankings":
            parser = RankingsParser()
            parser.parse_rankings()
            parser.generate_ranking_summary()
            print(parser.rankings)
        elif command == "parse ros rankings":
            parser = RankingsParser()
            parser.parse_ros_rankings()
            parser.generate_ranking_summary()
            print(parser.rankings)
        elif command == "generate rosters":
            leagues = []
            teams = []
            for league_id in LEAGUE_IDS:
                leagues.append(League(league_id))

            for i, index in enumerate(TEAM_INDEXES):
                teams.append(Team(leagues[i].league_id, index))
                teams[-1].generate_roster()
                teams[-1].save_roster()
                print("League #" + str(leagues[i].league_id) + ":")
                print(teams[-1].roster)
                print()
        elif command == "query free agents":
            leagues = []
            for league_id in LEAGUE_IDS:
                leagues.append(League(league_id))
                print("League #" + str(leagues[-1].league_id) + ":")
                roster_functions.query_free_agents(leagues[-1])
                print()
        elif command == "start sit":
            for i, index in enumerate(TEAM_INDEXES):
                team = Team(LEAGUE_IDS[i], index)
                team.generate_roster()
                ss = team.start_sit()
                print("League #" + str(LEAGUE_IDS[i]) + ":")
                print(team.roster[0][1])
                wrs = 0
                rbs = 0
                while wrs < 2:
                    for ranking in ss:
                        if ranking[0] == "WR":
                            print(ranking[1])
                            ss.remove(ranking)
                            break
                    wrs += 1
                while rbs < 2:
                    for ranking in ss:
                        if ranking[0] == "RB":
                            print(ranking[1])
                            ss.remove(ranking)
                            break
                    rbs += 1
                print(team.roster[5][1])  # Print the tight end
                print(ss[0][1])  # Print the flex
        elif command == "quit" or command == "exit":
            break
        elif command == "help":
            print(COMMANDS)
        else:
            print("Command not recognized: type 'help' for a list commands")
