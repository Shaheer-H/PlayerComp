import requests
import os

def get_player_stats(sport, league_id=None, season="2022"):
    base_urls = {
        "football": "https://v3.football.api-sports.io/players",
        "basketball": "https://v1.basketball.api-sports.io/players"
    }
    
    if sport == "football":
        if league_id is None:
            league_id = "39"  # EPL
        querystring = {"league": league_id, "season": season}
        headers = {
            "x-apisports-key": "a605acb900ca07b2004da3b4721b723d",
            "x-apisports-host": "v3.football.api-sports.io"
        }
    elif sport == "basketball":
        if league_id is None:
            league_id = "12"  # NBA
        querystring = {"league": league_id, "season": season}
        headers = {
            "x-apisports-key": "a605acb900ca07b2004da3b4721b723d",
            "x-apisports-host": "v1.basketball.api-sports.io"
        }
    else:
        return None

    try:
        response = requests.get(base_urls[sport], headers=headers, params=querystring)
        response.raise_for_status()
        return response.json()
    except requests.exceptions.HTTPError as e:
        print(f"HTTP error occurred for {sport}: {e}")
    except requests.exceptions.RequestException as e:
        print(f"Error fetching {sport} data: {e}")
        return None
