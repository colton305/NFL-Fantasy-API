
import csv


# Compare the team roster to league free agents to determine whether to add or drop
def query_free_agents(league):
    # Generate free agents as a list
    free_agents = league.find_free_agents()
    # Generate roster as a list
    with open("rosters/"+league.league_id+".csv", "r") as file:
        reader = csv.reader(file)
        roster = list(reader)
    # Generate rankings as a list
    with open("ranking_summary.csv") as file:
        reader = csv.reader(file)
        rankings = list(reader)
    # Find the lowest ranked player at each position
    worst_players = []
    lowest_rank = {"QB": 0, "RB": 0, "WR": 0, "TE": 0, "DEF": 0, "K": 0}
    for player in roster:
        for ranking in rankings:
            # Parse the general rankings
            if player[1] == ranking[1]:
                for garbage_player in worst_players:
                    if garbage_player[0] == player[0]:
                        worst_players.remove(garbage_player)
                worst_players.append(player)
                lowest_rank[player[0]] = int(ranking[0])
            # Parse the defensive rankings
            elif player[1] == ranking[6]:
                for garbage_player in worst_players:
                    if garbage_player[0] == player[0]:
                        worst_players.remove(garbage_player)
                worst_players.append(player)
                lowest_rank[player[0]] = int(ranking[0])
            # Parse the kicker rankings
            elif player[1] == ranking[7]:
                for garbage_player in worst_players:
                    if garbage_player[0] == player[0]:
                        worst_players.remove(garbage_player)
                worst_players.append(player)
                lowest_rank[player[0]] = int(ranking[0])
    # See if any free agent is ranked higher than a team member
    for free_agent in free_agents:
        if free_agent[0] != "DEF" and free_agent[0] != "K":
            for i in range(lowest_rank[free_agent[0].split(",")[0]]):
                if free_agent[1] == rankings[i][1]:
                    if lowest_rank[free_agent[0].split(",")[0]] > lowest_rank["WR"]:
                        for garbage_player in worst_players:
                            if garbage_player[0] == free_agent[0]:
                                print("Drop", garbage_player, "Add", free_agent)
                    else:
                        for garbage_player in worst_players:
                            if garbage_player[0] == "WR":
                                print("Drop", garbage_player, "Add", free_agent)
        elif free_agent[0] == "DEF":
            for i in range(lowest_rank["DEF"]):
                if free_agent[1] == rankings[i][6]:
                    for garbage_player in worst_players:
                        if garbage_player[0] == free_agent[0]:
                            print("Drop", garbage_player, "Add", free_agent)
        elif free_agent[0] == "K":
            for i in range(lowest_rank["K"]):
                if free_agent[1] == rankings[i][7]:
                    for garbage_player in worst_players:
                        if garbage_player[0] == free_agent[0]:
                            print("Drop", garbage_player, "Add", free_agent)
