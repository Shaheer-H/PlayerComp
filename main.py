import sys
from getstat import get_football_player_stats, get_basketball_player_stats
from playersearch import search_nba_players_by_name

def normalize(value, max_value):
    """Normalize a stat value to a [0,1] scale using a given maximum."""
    return min(value / max_value, 1.0)

def similarity_component(n1, n2):
    """Compute similarity as (1 - absolute difference) for normalized numbers."""
    return 1 - abs(n1 - n2)

def get_football_rates(player_stats):
    """Extract key per-game rates from football stats.
       Assumes stats are taken from the season dictionary.
    """
    games = float(player_stats.get("games", {}).get("appearences", 1))
    goals = float(player_stats.get("goals", {}).get("total", 0))
    assists = float(player_stats.get("goals", {}).get("assists", 0))
    return {
        "scoring_rate": goals / games,     # goals per game
        "assist_rate": assists / games       # assists per game
    }

def get_basketball_rates(aggregated_stats):
    """Extract key per-game averages from aggregated basketball stats.
       Here the aggregated stats are assumed to already be per game averages.
    """
    # In your aggregated stats, points, assists, etc. are averages.
    return {
        "scoring_rate": aggregated_stats.get("points", 0),
        "assist_rate": aggregated_stats.get("assists", 0)
    }

def calculate_similarity(fb_rates, bb_rates, same_sport=True):
    """
    Compare normalized scoring and assist rates.
    Normalize:
      - Football: max goals/assist per game ~1.0
      - Basketball: max points per game ~40, max assists per game ~10.
    """
    # Normalize the stats
    fb_scoring = normalize(fb_rates["scoring_rate"], 1.0)
    fb_assist = normalize(fb_rates["assist_rate"], 1.0)
    bb_scoring = normalize(bb_rates["scoring_rate"], 40.0)
    bb_assist = normalize(bb_rates["assist_rate"], 10.0)

    # Compute individual similarities
    scoring_sim = similarity_component(fb_scoring, bb_scoring)
    assist_sim = similarity_component(fb_assist, bb_assist)

    # Average similarity of the two stats (weighted equally here)
    stat_similarity = (scoring_sim + assist_sim) / 2

    # If the players are from different sports, apply a penalty factor.
    sport_factor = 1.0 if same_sport else 0.9

    overall = stat_similarity * sport_factor * 100  # scale to 0-100
    return overall

def main():
    print("Enter details for player 1:")
    sport1 = input("Sport (football/basketball): ").strip().lower()
    name1 = input("Player name: ").strip()
    season1 = input("Season (e.g., 2022): ").strip()

    if sport1 == "football":
        # For football, you might need to specify league_id (for example, Ligue 1 is "61" for Neymar)
        league_id = input("League ID (e.g., 61 for Ligue 1): ").strip() or "61"
        data = get_football_player_stats(search=name1, league_id=league_id, season=season1)
        if not data or not data.get("response"):
            print(f"No football player found for {name1} in season {season1}")
            sys.exit(1)
        player1 = data["response"][0]  # For simplicity, pick the first match.
        stats1 = None
        for s in player1.get("statistics", []):
            if str(s.get("league", {}).get("season", "")) == season1:
                stats1 = s
                break
        if not stats1:
            print("No stats found for the selected season.")
            sys.exit(1)
        rates1 = get_football_rates(stats1)
    elif sport1 == "basketball":
        # Use NBA player search to find the player and then fetch stats.
        players = search_nba_players_by_name(name1)
        if not players:
            print(f"No basketball player found for {name1}.")
            sys.exit(1)
        print("Matching NBA players:")
        for i, p in enumerate(players):
            full_name = f"{p.get('firstname', '')} {p.get('lastname', '')}".strip()
            print(f"{i}: {full_name}")
        try:
            idx = int(input("Choose player by index: "))
        except ValueError:
            print("Invalid index.")
            sys.exit(1)
        selected = players[idx]
        player_id = selected.get("id")
        data = get_basketball_player_stats(player_id=player_id, season=season1)
        if not data or not data.get("response"):
            print("No basketball stats found.")
            sys.exit(1)
        # For basketball we assume that the aggregation function from your playersearch.py is used.
        # Here we use a simple average over all games.
        games = data["response"]
        # Aggregate numeric stats
        aggregated = {}
        count = 0
        ignore_keys = {'player', 'team', 'game', 'pos', 'min', 'comment'}
        for game in games:
            for key, value in game.items():
                if key in ignore_keys:
                    continue
                try:
                    num = float(value)
                except (ValueError, TypeError):
                    continue
                aggregated.setdefault(key, 0.0)
                aggregated[key] += num
            count += 1
        for key in aggregated:
            aggregated[key] /= count
        rates1 = get_basketball_rates(aggregated)
    else:
        print("Invalid sport.")
        sys.exit(1)

    print("\nEnter details for player 2:")
    sport2 = input("Sport (football/basketball): ").strip().lower()
    name2 = input("Player name: ").strip()
    season2 = input("Season (e.g., 2022): ").strip()

    if sport2 == "football":
        league_id = input("League ID (e.g., 61 for Ligue 1, 39 for EPL): ").strip() or "61"
        data = get_football_player_stats(search=name2, league_id=league_id, season=season2)
        if not data or not data.get("response"):
            print(f"No football player found for {name2} in season {season2}")
            sys.exit(1)
        player2 = data["response"][0]
        stats2 = None
        for s in player2.get("statistics", []):
            if str(s.get("league", {}).get("season", "")) == season2:
                stats2 = s
                break
        if not stats2:
            print("No stats found for the selected season.")
            sys.exit(1)
        rates2 = get_football_rates(stats2)
    elif sport2 == "basketball":
        players = search_nba_players_by_name(name2)
        if not players:
            print(f"No basketball player found for {name2}.")
            sys.exit(1)
        print("Matching NBA players:")
        for i, p in enumerate(players):
            full_name = f"{p.get('firstname', '')} {p.get('lastname', '')}".strip()
            print(f"{i}: {full_name}")
        try:
            idx = int(input("Choose player by index: "))
        except ValueError:
            print("Invalid index.")
            sys.exit(1)
        selected = players[idx]
        player_id = selected.get("id")
        data = get_basketball_player_stats(player_id=player_id, season=season2)
        if not data or not data.get("response"):
            print("No basketball stats found.")
            sys.exit(1)
        games = data["response"]
        aggregated = {}
        count = 0
        ignore_keys = {'player', 'team', 'game', 'pos', 'min', 'comment'}
        for game in games:
            for key, value in game.items():
                if key in ignore_keys:
                    continue
                try:
                    num = float(value)
                except (ValueError, TypeError):
                    continue
                aggregated.setdefault(key, 0.0)
                aggregated[key] += num
            count += 1
        for key in aggregated:
            aggregated[key] /= count
        rates2 = get_basketball_rates(aggregated)
    else:
        print("Invalid sport.")
        sys.exit(1)

    # Determine if the sports are the same (if not, apply a penalty)
    same_sport = (sport1 == sport2)

    sim_score = calculate_similarity(rates1, rates2, same_sport)
    print("\nPlayer 1 rates:", rates1)
    print("Player 2 rates:", rates2)
    print(f"\nOverall similarity score: {sim_score:.2f} / 100")

if __name__ == "__main__":
    main()
