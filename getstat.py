import requests
import os

def get_player_stats(sport, league_id=None, season="2022"):
    base_urls = {
        "football": "https://v3.football.api-sports.io/players",
        "basketball": "https://api-basketball.p.rapidapi.com/players"
    }
    
    # Default league IDs
    if league_id is None:
        league_ids = {
            "football": "39",  # EPL
            "basketball": "12"  # NBA
        }
        league_id = league_ids[sport]
    
    try:
        url = base_urls[sport]
        querystring = {"league": league_id, "season": season}
        
        # Different headers for basketball API
        if sport == "basketball":
            headers = {
                "x-rapidapi-key": "87953874cfmshedcea4c87433e56p1bfbe0jsn17729efbfe73",  # Replace with your API key
                "x-rapidapi-host": "api-basketball.p.rapidapi.com"
            }
        else:
            headers = {
                "x-apisports-key": "a605acb900ca07b2004da3b4721b723d",  # Replace with your API key
                "x-apisports-host": "v3.football.api-sports.io"
            }
            
        response = requests.get(url, headers=headers, params=querystring)
        response.raise_for_status()
        return response.json()
    except requests.exceptions.RequestException as e:
        print(f"Error fetching {sport} data: {e}")
        return None