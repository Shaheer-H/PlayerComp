import pandas as pd
from sklearn.neighbors import NearestNeighbors

def retrieve_similar_players(sport, player_name=None, query_vector=None, n_neighbors=5):
    """
    Retrieves similar players for a given sport ('nba' or 'soccer').
    
    If player_name is provided, it attempts a name search.
    If query_vector is provided, it uses that vector directly.
    
    Returns a tuple: (target, similar_players)
    """
    if sport.lower() == 'nba':
        file_path = r"data\normalized_data\nba_normalized_extended.csv"
        df = pd.read_csv(file_path)
        # For NBA, use per-minute metrics if available.
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
        # For soccer, we focus on the comparable features.
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

    if player_name:
        # Try to find the player by name (case-insensitive)
        matching = df[df['Player'].str.contains(player_name, case=False, na=False)]
        if matching.empty:
            target = None
        else:
            target = matching.iloc[0]
    else:
        target = None

    # If a query_vector is provided (or if no target was found by name), use it.
    if query_vector is not None:
        vec = query_vector.reshape(1, -1)
    elif target is not None:
        vec = target[features].values.reshape(1, -1)
    else:
        # If no target is found and no query vector provided, we cannot proceed.
        print(f"No target found for sport {sport.upper()} using name '{player_name}'.")
        return None, None

    # Build kNN model on all players' feature vectors
    knn = NearestNeighbors(n_neighbors=n_neighbors+1, algorithm='auto').fit(df[features])
    distances, indices = knn.kneighbors(vec)
    # Exclude the first result if it is the target (only if a name search was done)
    if player_name and target is not None:
        similar_indices = indices[0][1:]
    else:
        similar_indices = indices[0]
    similar_players = df.iloc[similar_indices]

    return target, similar_players

def map_nba_to_soccer(nba_target):
    """
    Map an NBA player's comparable stats to a soccer query vector.
    We assume:
      NBA "Points Per Minute" → Soccer "Goals Per Minute"
      NBA "Assists Per Minute" → Soccer "Assists Per Minute"
    """
    # Check if the NBA target has these columns:
    if 'Points Per Minute' in nba_target and 'Assists Per Minute' in nba_target:
        query = nba_target[['Points Per Minute', 'Assists Per Minute']].values
    else:
        # If not, try the per-game version
        query = nba_target[['Points Per Game', 'Assists Per Game']].values
    return query

def retrieve_similar_players_all(player_name, n_neighbors=5):
    """
    Given a player's name (e.g., "LeBron"), retrieve similar players from both NBA and Soccer.
    
    For the soccer search, if the player's name isn't found (which is expected for names like LeBron),
    we map the NBA player's comparable stats to soccer features.
    """
    print(f"\nRetrieving similar players for '{player_name}' in both NBA and Soccer:")

    # Retrieve from NBA normally
    print("\n=== NBA Similar Players ===")
    nba_target, nba_similar = retrieve_similar_players('nba', player_name, n_neighbors=n_neighbors)
    if nba_target is not None:
        print("Target NBA player:", nba_target['Player'])
        print(nba_similar[['Player']])
    else:
        print("No matching NBA player found.")
    
    # For soccer, first try a name search
    print("\n=== Soccer Similar Players ===")
    soc_target, soc_similar = retrieve_similar_players('soccer', player_name, n_neighbors=n_neighbors)
    if soc_target is not None:
        # If a soccer player was found by name, use that.
        print("Target Soccer player:", soc_target['Player'])
        print(soc_similar[['Player']])
    else:
        # If not, then map the NBA target's comparable stats to the soccer feature space.
        if nba_target is not None:
            # Map NBA stats to soccer analogous features.
            # Here, we use only "Points Per Minute" and "Assists Per Minute" as analogs.
            nba_vector = map_nba_to_soccer(nba_target)
            # Now load the soccer dataset and use only the comparable features.
            soc_file_path = r"data\normalized_data\soccer_normalized_extended.csv"
            soc_df = pd.read_csv(soc_file_path)
            # For our comparison, we use just 'Goals Per Minute' and 'Assists Per Minute'.
            if 'Goals Per Minute' in soc_df.columns and 'Assists Per Minute' in soc_df.columns:
                soc_features = ['Goals Per Minute', 'Assists Per Minute']
            else:
                soc_features = ['Goals Per Game', 'Assists Per Game']
            # Build the kNN model on the soccer comparable features.
            knn = NearestNeighbors(n_neighbors=n_neighbors, algorithm='auto').fit(soc_df[soc_features])
            distances, indices = knn.kneighbors(nba_vector.reshape(1, -1))
            similar_soccer = soc_df.iloc[indices[0]]
            print("NBA player's mapped vector used for soccer search.")
            print("Similar Soccer players:")
            print(similar_soccer[['Player'] + soc_features])
        else:
            print("Cannot map NBA stats to soccer because NBA player not found.")

if __name__ == "__main__":
    player_name = input("Enter player name: ").strip()
    retrieve_similar_players_all(player_name, n_neighbors=5)
