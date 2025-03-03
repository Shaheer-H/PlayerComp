import kagglehub
import os

# Define the data directory
data_dir = "data"

# Ensure the data directory exists
os.makedirs(data_dir, exist_ok=True)

# Download the latest version of the Premier League player statistics
futstats_path = os.path.join(data_dir, "futstats")
futstats_path = kagglehub.dataset_download("rishikeshkanabar/premier-league-player-statistics-updated-daily", path=futstats_path)
print("Path to Premier League dataset files:", futstats_path)

# Download the latest version of the NBA player statistics
bbalstats_path = os.path.join(data_dir, "bbalstats")
bbalstats_path = kagglehub.dataset_download("vivovinco/nba-player-stats", path=bbalstats_path)
print("Path to NBA dataset files:", bbalstats_path)