import rankings_parser

if __name__ == "__main__":
    parser = rankings_parser.RankingsParser()

    parser.parse()
    parser.generate_ranking_summary()
    parser.generate_yahoo_rankings()
