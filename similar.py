import pandas as pd
from sklearn.neighbors import NearestNeighbors

def retrieve_similar_players(sport, player_name, n_neighbors=5):
    """
    Retrieve similar players for a given sport ('nba' or 'soccer') based on the normalized features.
    Returns a tuple (target, similar_players) if found, otherwise (None, None).
    """
    if sport.lower() == 'nba':
        file_path = r"data\normalized_data\nba_normalized_extended.csv"
        df = pd.read_csv(file_path)
        # Use per-minute metrics if available; otherwise, fall back to per-game stats.
        if 'Points Per Minute' in df.columns:
            features = [
                'Points Per Minute', 'Assists Per Minute', 'Rebounds Per Minute',
                'Steals Per Minute', 'Blocks Per Minute', 'Field Goal %',
                'Three Point %', 'Free Throw %'
            ]
        else:
            features = [
                'Points Per Game', 'Assists Per Game', 'Rebounds Per Game',
                'Steals Per Game', 'Blocks Per Game', 'Field Goal %',
                'Three Point %', 'Free Throw %'
            ]
    elif sport.lower() == 'soccer':
        file_path = r"data\normalized_data\soccer_normalized_extended.csv"
        df = pd.read_csv(file_path)
        if 'Goals Per Minute' in df.columns:
            features = [
                'Goals Per Minute', 'Assists Per Minute', 'Shot Conversion Rate',
                'Tackles Per Minute', 'Interceptions Per Minute'
            ]
        else:
            features = [
                'Goals Per Game', 'Assists Per Game', 'Shot Conversion Rate',
                'Tackles Per Game', 'Interceptions Per Game'
            ]
    else:
        print("Invalid sport. Please choose 'nba' or 'soccer'.")
        return None, None

    # Search for the player (case-insensitive)
    matching = df[df['Player'].str.contains(player_name, case=False, na=False)]
    if matching.empty:
        print(f"Player '{player_name}' not found in {sport.upper()} dataset.")
        return None, None

    # Use the first matching record for simplicity
    target = matching.iloc[0]
    target_vector = target[features].values.reshape(1, -1)

    # Build a kNN model on all players' feature vectors
    knn = NearestNeighbors(n_neighbors=n_neighbors+1, algorithm='auto').fit(df[features])
    distances, indices = knn.kneighbors(target_vector)
    # Exclude the target itself (first result)
    similar_indices = indices[0][1:]
    similar_players = df.iloc[similar_indices]

    return target, similar_players

def retrieve_similar_players_all(player_name, n_neighbors=5):
    """
    Given a player's name, retrieve similar players from both NBA and Soccer datasets.
    """
    print(f"\nRetrieving similar players for '{player_name}' in both NBA and Soccer:")

    # NBA retrieval
    print("\n=== NBA Similar Players ===")
    nba_target, nba_similar = retrieve_similar_players('nba', player_name, n_neighbors)
    if nba_target is not None:
        print("Target player:", nba_target['Player'])
        print(nba_similar[['Player']])
    else:
        print("No matching NBA player found.")

    # Soccer retrieval
    print("\n=== Soccer Similar Players ===")
    soc_target, soc_similar = retrieve_similar_players('soccer', player_name, n_neighbors)
    if soc_target is not None:
        print("Target player:", soc_target['Player'])
        print(soc_similar[['Player']])
    else:
        print("No matching Soccer player found.")

if __name__ == "__main__":
    player_name = input("Enter player name: ").strip()
    retrieve_similar_players_all(player_name, n_neighbors=5)
