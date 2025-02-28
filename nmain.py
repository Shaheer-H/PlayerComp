from getstat import get_player_stats

def similarity(stat1, stat2):
    return 1 - abs(stat1 - stat2) / max(stat1, stat2, 1)

def choose_player(data, sport):
    players = data.get("response", [])
    if not players:
        print(f"No players found for {sport}.")
        return None
    # List available players
    for i, player in enumerate(players):
        name = player.get("player", {}).get("name", "Unknown")
        print(f"{i}: {name}")
    try:
        index = int(input("Choose player by index: "))
    except ValueError:
        print("Invalid input.")
        return None
    if index < 0 or index >= len(players):
        print("Index out of range.")
        return None
    return players[index]

def main():
    season = input("Enter season (default 2022): ").strip() or "2022"
    
    # Select player 1
    sport1 = input("Enter player 1 sport (football or basketball): ").strip().lower()
    data1 = get_player_stats(sport1, season=season)
    player1 = choose_player(data1, sport1)
    if player1 is None:
        return

    # Select player 2
    sport2 = input("Enter player 2 sport (football or basketball): ").strip().lower()
    data2 = get_player_stats(sport2, season=season)
    player2 = choose_player(data2, sport2)
    if player2 is None:
        return

    # Extract stats for player1 and player2 (using the first statistic set)
    try:
        stats1 = player1["statistics"][0]
    except (KeyError, IndexError):
        print("Player 1 statistics missing.")
        return
    try:
        stats2 = player2["statistics"][0]
    except (KeyError, IndexError):
        print("Player 2 statistics missing.")
        return

    # Compute per game metrics:
    # For football, assume keys: "games", "goals", "assists"
    games1 = float(stats1.get("games", {}).get("appearences", 1))
    goals1 = float(stats1.get("goals", {}).get("total", 0))
    assists1 = float(stats1.get("goals", {}).get("assists", 0))
    gpg = goals1 / games1
    apg_soccer = assists1 / games1

    # For basketball, assume keys: "games", "points", "assists"
    games2 = float(stats2.get("games", {}).get("appearences", 1))
    points2 = float(stats2.get("points", {}).get("total", 0))
    assists2 = float(stats2.get("assists", {}).get("assists", 0))
    ppg = points2 / games2
    apg_basket = assists2 / games2

    # Compare equivalent stats
    goal_similarity = similarity(gpg, ppg)
    assist_similarity = similarity(apg_soccer, apg_basket)
    overall_similarity = (goal_similarity + assist_similarity) / 2

    name1 = player1.get("player", {}).get("name", "Unknown")
    name2 = player2.get("player", {}).get("name", "Unknown")
    print(f"\n{name1} ({sport1.title()}) - Goals/PPG: {gpg:.2f}, Assists/PG: {apg_soccer:.2f}")
    print(f"{name2} ({sport2.title()}) - PPG: {ppg:.2f}, APG: {apg_basket:.2f}")
    print(f"Overall similarity score: {overall_similarity:.2f}")

if __name__ == "__main__":
    main()
