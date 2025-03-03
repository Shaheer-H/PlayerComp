import os
import pandas as pd
from sklearn.preprocessing import StandardScaler

# Define paths to your datasets (adjust file names as necessary)
nba_file = r"data\bbalstats 21-22\bbalstatsreg21-22.csv"
soccer_file = r"data\futstats.csv"

# Load datasets
nba_df = pd.read_csv(nba_file, encoding='latin-1')
soccer_df = pd.read_csv(soccer_file)

# --- Basketball Dataset ---
# Assume these columns exist; adjust column names based on your CSV:
nba_columns = [
    'Player', 'Points Per Game', 'Assists Per Game', 
    'Rebounds Per Game', 'Steals Per Game', 'Blocks Per Game', 
    'Field Goal %', 'Three Point %', 'Free Throw %', 'Minutes Per Game'
]
nba_data = nba_df[nba_columns]

# --- Soccer Dataset ---
# Assume these columns exist; adjust as needed:
soccer_columns = [
    'Player', 'Goals Per Game', 'Assists Per Game', 
    'Total Shots', 'Tackles Per Game', 'Interceptions Per Game', 
    'Minutes Played'
]
soccer_data = soccer_df[soccer_columns]

# For soccer, compute an additional metric: Shot Conversion Rate
soccer_data['Shot Conversion Rate'] = soccer_data.apply(
    lambda row: row['Goals Per Game'] / row['Total Shots'] if row['Total Shots'] and row['Total Shots'] > 0 else 0, axis=1
)

# Optionally, rename soccer "Minutes Played" to "Minutes Per Game" if you standardize this metric:
soccer_data = soccer_data.rename(columns={'Minutes Played': 'Minutes Per Game'})

# --- Normalization ---
# Define features to normalize for NBA:
features_nba = [
    'Points Per Game', 'Assists Per Game', 'Rebounds Per Game', 
    'Steals Per Game', 'Blocks Per Game', 'Field Goal %', 'Three Point %', 'Free Throw %', 'Minutes Per Game'
]
# Define features to normalize for Soccer:
features_soccer = [
    'Goals Per Game', 'Assists Per Game', 'Shot Conversion Rate', 
    'Tackles Per Game', 'Interceptions Per Game', 'Minutes Per Game'
]

# You might choose different scalers based on your strategy. Here we use StandardScaler.
scaler_nba = StandardScaler()
nba_data_scaled = nba_data.copy()
nba_data_scaled[features_nba] = scaler_nba.fit_transform(nba_data[features_nba])

scaler_soccer = StandardScaler()
soccer_data_scaled = soccer_data.copy()
soccer_data_scaled[features_soccer] = scaler_soccer.fit_transform(soccer_data[features_soccer])

# Inspect a few rows of the normalized data
print("Normalized NBA Data:")
print(nba_data_scaled.head())

print("\nNormalized Soccer Data:")
print(soccer_data_scaled.head())

# Optionally, save the normalized data for later use
os.makedirs("normalized_data", exist_ok=True)
nba_data_scaled.to_csv("normalized_data/nba_normalized_extended.csv", index=False)
soccer_data_scaled.to_csv("normalized_data/soccer_normalized_extended.csv", index=False)
