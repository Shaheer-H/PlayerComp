import requests

def get_football_player_stats(search=None, league_id="39", season="2022"):
    """
    Fetches football (EPL) player statistics.
    Optionally filters by a player's name using the 'search' parameter.
    """
    url = "https://v3.football.api-sports.io/players"
    querystring = {"league": league_id, "season": season}
    if search:
        querystring["search"] = search
    headers = {
        "x-apisports-key": "a605acb900ca07b2004da3b4721b723d",
        "x-apisports-host": "v3.football.api-sports.io"
    }
    try:
        response = requests.get(url, headers=headers, params=querystring)
        response.raise_for_status()
        return response.json()
    except requests.exceptions.HTTPError as e:
        print(f"HTTP error occurred for football: {e}")
    except requests.exceptions.RequestException as e:
        print(f"Error fetching football data: {e}")
    return None

def get_basketball_player_stats(player_id, season="2022"):
    url = "https://api-nba-v1.p.rapidapi.com/players/statistics"
    querystring = {"id": player_id, "season": season}
    headers = {
        "x-rapidapi-key": "87953874cfmshedcea4c87433e56p1bfbe0jsn17729efbfe73",
        "x-rapidapi-host": "api-nba-v1.p.rapidapi.com"
    }
    try:
        response = requests.get(url, headers=headers, params=querystring)
        response.raise_for_status()
        return response.json()
    except requests.exceptions.HTTPError as e:
        print(f"HTTP error occurred for basketball: {e}")
    except requests.exceptions.RequestException as e:
        print(f"Error fetching basketball data: {e}")
    return None


