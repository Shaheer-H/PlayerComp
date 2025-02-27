import numpy as np
from sklearn.preprocessing import MinMaxScaler
from getstat import get_player_stats

# 1. Data Ingestion: load your data (from API calls or local storage)
def load_data(season="2022"):
    try:
        soccer_data = get_player_stats("football", season=season)
        basketball_data = get_player_stats("basketball", season=season)
    except Exception as e:
        print(f"Warning: Using sample data due to API error: {e}")
        # Sample data for testing
        return {
            "soccer": {
                "Kevin De Bruyne": {
                    "goals_per_game": 0.3,
                    "assists_per_game": 0.8,
                    "shot_accuracy": 0.65,
                    "minutes_per_game": 85,
                    "xG": 0.45,
                    "xA": 0.75,
                    "tackles": 1.2,
                    "interceptions": 0.8,
                    "clearances": 0.3,
                    "pass_completion": 0.85
                }
            },
            "basketball": {
                "Chris Paul": {
                    "points_per_game": 15.8,
                    "assists_per_game": 8.9,
                    "fg_percentage": 0.47,
                    "minutes_per_game": 32,
                    "bpm": 4.5,
                    "rebounds": 4.2,
                    "blocks": 0.3,
                    "steals": 1.5,
                    "assist_turnover_ratio": 4.2
                }
            }
        }
    
    data = {
        "soccer": {},
        "basketball": {}
    }
    
    # Parse soccer data
    if soccer_data and 'response' in soccer_data:
        for player in soccer_data['response']:
            name = player['player']['name']
            stats = player['statistics'][0]  # Get the first season's stats
            games = stats.get('games', {}).get('appearences', 1)  # Avoid division by zero
            
            data["soccer"][name] = {
                "goals_per_game": stats.get('goals', {}).get('total', 0) / games,
                "assists_per_game": stats.get('goals', {}).get('assists', 0) / games,
                "shot_accuracy": stats.get('shots', {}).get('on', 0) / stats.get('shots', {}).get('total', 1),
                "minutes_per_game": stats.get('games', {}).get('minutes', 0) / games,
                "xG": stats.get('goals', {}).get('expected', 0),
                "xA": stats.get('goals', {}).get('expected_assists', 0),
                "tackles": stats.get('tackles', {}).get('total', 0) / games,
                "interceptions": stats.get('interceptions', 0) / games,
                "clearances": stats.get('clearances', 0) / games,
                "pass_completion": stats.get('passes', {}).get('accuracy', 0)
            }
    
    # Parse basketball data
    if basketball_data and 'response' in basketball_data:
        for player in basketball_data['response']:
            name = player['player']['name']
            stats = player['statistics'][0]
            games = stats.get('games', {}).get('played', 1)
            
            data["basketball"][name] = {
                "points_per_game": stats.get('points', 0) / games,
                "assists_per_game": stats.get('assists', 0) / games,
                "fg_percentage": stats.get('fgp', 0),
                "minutes_per_game": stats.get('minutes', 0) / games,
                "bpm": stats.get('plusMinus', 0),
                "rebounds": stats.get('rebounds', 0) / games,
                "blocks": stats.get('blocks', 0) / games,
                "steals": stats.get('steals', 0) / games,
                "assist_turnover_ratio": stats.get('assists', 0) / max(stats.get('turnovers', 1), 1)
            }
    
    return data

# 2. Data Normalization / Feature Extraction
def preprocess_data(data):
    processed_data = {"soccer": {}, "basketball": {}}
    
    # Calculate means and standard deviations for normalization
    for sport in data:
        stats = {}
        for metric in next(iter(data[sport].values())).keys():
            values = [player_stats[metric] for player_stats in data[sport].values()]
            stats[metric] = {
                'mean': np.mean(values),
                'std': np.std(values) if np.std(values) != 0 else 1
            }
        
        # Normalize each player's stats
        for player, player_stats in data[sport].items():
            processed_data[sport][player] = {
                metric: (value - stats[metric]['mean']) / stats[metric]['std']
                for metric, value in player_stats.items()
            }
    
    return processed_data

def build_feature_vector(player_stats, sport):
    """
    Convert player statistics into comparable feature vectors
    Features are ordered: [scoring, playmaking, efficiency, minutes, impact, defense, distribution]
    """
    if sport == "soccer":
        return np.array([
            player_stats.get('goals_per_game', 0),
            player_stats.get('assists_per_game', 0),
            player_stats.get('shot_accuracy', 0),
            player_stats.get('minutes_per_game', 0),
            (player_stats.get('xG', 0) + player_stats.get('xA', 0)) / 2,  # offensive impact
            (player_stats.get('tackles', 0) + player_stats.get('interceptions', 0) + 
             player_stats.get('clearances', 0)) / 3,  # defensive composite
            player_stats.get('pass_completion', 0)
        ])
    else:  # basketball
        return np.array([
            player_stats.get('points_per_game', 0),
            player_stats.get('assists_per_game', 0),
            player_stats.get('fg_percentage', 0),
            player_stats.get('minutes_per_game', 0),
            player_stats.get('bpm', 0),  # using BPM for impact
            (player_stats.get('rebounds', 0) + player_stats.get('blocks', 0) + 
             player_stats.get('steals', 0)) / 3,  # defensive composite
            player_stats.get('assist_turnover_ratio', 0)
        ])

def calculate_similarity(player1_stats, player2_stats, sport1, sport2):
    """
    Calculate similarity score between two players
    """
    # Build feature vectors
    vec1 = build_feature_vector(player1_stats, sport1)
    vec2 = build_feature_vector(player2_stats, sport2)
    
    # Normalize vectors to account for different scales across sports
    scaler = MinMaxScaler()
    normalized_vecs = scaler.fit_transform([vec1, vec2])
    
    # Calculate cosine similarity
    similarity = np.dot(normalized_vecs[0], normalized_vecs[1]) / (
        np.linalg.norm(normalized_vecs[0]) * np.linalg.norm(normalized_vecs[1])
    )
    
    return similarity

def compare_players(soccer_player, basketball_player, data):
    """
    Compare a soccer player to a basketball player and return similarity score
    """
    try:
        soccer_stats = data['soccer'][soccer_player]
        basketball_stats = data['basketball'][basketball_player]
        
        similarity = calculate_similarity(soccer_stats, basketball_stats, 'soccer', 'basketball')
        
        print(f"\nComparing {soccer_player} (Soccer) with {basketball_player} (Basketball)")
        print(f"Similarity Score: {similarity:.2f} (0 = completely different, 1 = very similar)")
        
        return similarity
        
    except KeyError:
        print(f"Error: One or both players not found in dataset")
        return None

def main():
    data = load_data()
    
    # Check if we have data
    if not data['soccer'] or not data['basketball']:
        print("Error: Failed to load player data")
        return
        
    processed_data = preprocess_data(data)
    
    # Example comparison
    soccer_player = "Kevin De Bruyne"
    basketball_player = "Chris Paul"
    
    similarity = compare_players(soccer_player, basketball_player, processed_data)
    if similarity is not None:
        print(f"Similarity score: {similarity}")

if __name__ == "__main__":
    main()
