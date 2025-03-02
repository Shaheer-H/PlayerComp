import json
import requests
from getstat import get_football_player_stats, get_basketball_player_stats

def search_nba_players_by_name(name):
    """
    Uses the NBA API to search for players by name.
    Returns a list of player dictionaries from the API response.
    """
    url = "https://api-nba-v1.p.rapidapi.com/players"
    querystring = {"search": name}
    headers = {
        "x-rapidapi-key": "87953874cfmshedcea4c87433e56p1bfbe0jsn17729efbfe73",
        "x-rapidapi-host": "api-nba-v1.p.rapidapi.com"
    }
    try:
        response = requests.get(url, headers=headers, params=querystring)
        response.raise_for_status()
        data = response.json()
        return data.get("response", [])
    except Exception as e:
        print(f"Error searching NBA players: {e}")
        return []

def aggregate_basketball_stats(games):
    """
    Aggregates a list of game stat dictionaries by computing the average for each numeric stat.
    Keys that are clearly non-numeric (like 'player', 'team', 'game', 'pos', 'min', 'comment')
    are skipped.
    """
    if not games:
        return {}
    aggregate = {}
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
            aggregate.setdefault(key, 0.0)
            aggregate[key] += num
        count += 1
    
    # Compute averages
    avg_stats = { key: (total / count) for key, total in aggregate.items() }
    return avg_stats

def display_stats(stats, sport, player_name, season):
    print(f"\n{sport.title()} stats for {player_name} (Season: {season}):")
    if not stats:
        print("No stats available.")
        return
    for key, value in stats.items():
        print(f"{key}: {value:.2f}")

def football_search(name, season):
    """
    Searches for a football (soccer) player by name using the API.
    If multiple players match, asks the user to choose one.
    Then, it attempts to extract and display the statistics for the given season.
    """
    data = get_football_player_stats(search=name, season=season)
    if not data or "response" not in data or not data["response"]:
        print("No football player found with that name for season", season)
        return

    players = data["response"]
    if len(players) > 1:
        print("Multiple football players found:")
        for i, p in enumerate(players):
            p_name = p.get("player", {}).get("name", "Unknown")
            print(f"{i}: {p_name}")
        try:
            idx = int(input("Choose player by index: "))
        except ValueError:
            print("Invalid input.")
            return
        if idx < 0 or idx >= len(players):
            print("Index out of range.")
            return
        player_data = players[idx]
    else:
        player_data = players[0]

    # Look for season-specific stats
    stats = None
    for season_stats in player_data.get("statistics", []):
        if str(season_stats.get("league", {}).get("season", "")) == season:
            stats = season_stats
            break
    if not stats:
        print("No stats found for season", season)
        return
    print(json.dumps(stats, indent=2))

def basketball_search(name, season):
    """
    Searches for a basketball player by name using the NBA API search endpoint.
    If multiple matches are found, prompts the user to choose one.
    Then fetches season stats using the player's ID, aggregates the data, and displays it.
    """
    players = search_nba_players_by_name(name)
    if not players:
        print("No basketball players found with that name.")
        return

    # Display matching players with name, jersey (if available), and position
    print("Matching NBA players:")
    for i, p in enumerate(players):
        first = p.get("firstname", "")
        last = p.get("lastname", "")
        full_name = f"{first} {last}".strip()
        league_std = p.get("leagues", {}).get("standard", {})
        jersey = league_std.get("jersey")
        pos = league_std.get("pos")
        extra = []
        if jersey:
            extra.append(f"Jersey: {jersey}")
        if pos:
            extra.append(f"Pos: {pos}")
        extra_str = ", ".join(extra) if extra else ""
        print(f"{i}: {full_name} {f'({extra_str})' if extra_str else ''}")

    try:
        idx = int(input("Choose player by index: "))
    except ValueError:
        print("Invalid input.")
        return
    if idx < 0 or idx >= len(players):
        print("Index out of range.")
        return
    selected = players[idx]
    first = selected.get("firstname", "")
    last = selected.get("lastname", "")
    full_name = f"{first} {last}".strip()

    player_id = selected.get("id")
    if not player_id:
        print("Selected player does not have an ID.")
        return

    data = get_basketball_player_stats(player_id=player_id, season=season)
    if not data or "response" not in data or not data["response"]:
        print("No basketball stats found for that player and season.")
        return

    games = data["response"]
    aggregated = aggregate_basketball_stats(games)
    display_stats(aggregated, "basketball", full_name, season)

def main():
    sport = input("Enter sport (football/basketball): ").strip().lower()
    season = input("Enter season (e.g., 2022): ").strip()
    player_name = input("Enter player name: ").strip()
    
    if sport == "football":
        football_search(player_name, season)
    elif sport == "basketball":
        basketball_search(player_name, season)
    else:
        print("Invalid sport entered. Please choose either 'football' or 'basketball'.")

if __name__ == "__main__":
    main()
