from getstat import get_football_player_stats, get_basketball_player_stats

def similarity(stat1, stat2):
    return 1 - abs(stat1 - stat2) / max(stat1, stat2, 1)

def choose_player(data, sport):
    """
    For football only: Lists players for selection.
    """
    players = data.get("response", [])
    if not players:
        print(f"No players found for {sport}.")
        return None
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
    
    # --- Player 1 Selection ---
    sport1 = input("Enter player 1 sport (football or basketball): ").strip().lower()
    if sport1 == "football":
        data1 = get_football_player_stats(season=season)
        player1 = choose_player(data1, sport1)
    elif sport1 == "basketball":
        player1_id = input("Enter basketball player 1 ID: ").strip()
        data1 = get_basketball_player_stats(player_id=player1_id, season=season)
        if data1 and data1.get("response"):
            # Take first result from the response list
            player1 = data1["response"][0]
        else:
            player1 = None
    else:
        print("Invalid sport for player 1.")
        return
    
    if not player1:
        print("Player 1 not found.")
        return

    # --- Player 2 Selection ---
    sport2 = input("Enter player 2 sport (football or basketball): ").strip().lower()
    if sport2 == "football":
        data2 = get_football_player_stats(season=season)
        player2 = choose_player(data2, sport2)
    elif sport2 == "basketball":
        player2_id = input("Enter basketball player 2 ID: ").strip()
        data2 = get_basketball_player_stats(player_id=player2_id, season=season)
        if data2 and data2.get("response"):
            player2 = data2["response"][0]
        else:
            player2 = None
    else:
        print("Invalid sport for player 2.")
        return
    
    if not player2:
        print("Player 2 not found.")
        return

    # --- Extract Statistics ---
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

    # --- Compute Per Game Metrics ---
    # For football, use nested keys:
    if sport1 == "football":
        games1 = float(stats1.get("games", {}).get("appearences", 1))
        goals1 = float(stats1.get("goals", {}).get("total", 0))
        assists1 = float(stats1.get("goals", {}).get("assists", 0))
        scoring1 = goals1
        per_game1 = scoring1 / games1
        assist_rate1 = assists1 / games1
    else:  # basketball – assuming similar nested structure; adjust if needed
        games1 = float(stats1.get("games", {}).get("appearences", 1))
        points1 = float(stats1.get("points", {}).get("total", 0))
        assists1 = float(stats1.get("assists", {}).get("assists", 0))
        scoring1 = points1
        per_game1 = scoring1 / games1
        assist_rate1 = assists1 / games1

    if sport2 == "football":
        games2 = float(stats2.get("games", {}).get("appearences", 1))
        goals2 = float(stats2.get("goals", {}).get("total", 0))
        assists2 = float(stats2.get("goals", {}).get("assists", 0))
        scoring2 = goals2
        per_game2 = scoring2 / games2
        assist_rate2 = assists2 / games2
    else:  # basketball
        games2 = float(stats2.get("games", {}).get("appearences", 1))
        points2 = float(stats2.get("points", {}).get("total", 0))
        assists2 = float(stats2.get("assists", {}).get("assists", 0))
        scoring2 = points2
        per_game2 = scoring2 / games2
        assist_rate2 = assists2 / games2

    # --- Compare Stats ---
    score_similarity = similarity(per_game1, per_game2)
    assist_similarity = similarity(assist_rate1, assist_rate2)
    overall_similarity = (score_similarity + assist_similarity) / 2

    name1 = player1.get("player", {}).get("name", "Unknown")
    name2 = player2.get("player", {}).get("name", "Unknown")
    print(f"\n{name1} ({sport1.title()}) - Scoring per Game: {per_game1:.2f}, Assists per Game: {assist_rate1:.2f}")
    print(f"{name2} ({sport2.title()}) - Scoring per Game: {per_game2:.2f}, Assists per Game: {assist_rate2:.2f}")
    print(f"Overall similarity score: {overall_similarity:.2f}")

if __name__ == "__main__":
    main()
