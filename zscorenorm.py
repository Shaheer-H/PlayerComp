import os
import pandas as pd
from sklearn.preprocessing import StandardScaler

# Define paths to your datasets (adjust file paths as necessary)
nba_file = r"data\bbalstats 21-22\bbalstatsreg21-22.csv"
soccer_file = r"data\futstats.csv"

# --- Load Datasets ---
nba_df = pd.read_csv(nba_file, sep=';', encoding='latin-1')
soccer_df = pd.read_csv(soccer_file, encoding='latin-1')

# --- NBA Dataset Mapping ---
nba_df['Points Per Game'] = nba_df['PTS']
nba_df['Assists Per Game'] = nba_df['AST']
nba_df['Rebounds Per Game'] = nba_df['TRB']
nba_df['Steals Per Game'] = nba_df['STL']
nba_df['Blocks Per Game'] = nba_df['BLK']
nba_df['Field Goal %'] = nba_df['FG%']
nba_df['Three Point %'] = nba_df['3P%']
nba_df['Free Throw %'] = nba_df['FT%']
nba_df['Minutes Per Game'] = nba_df['MP']

nba_columns = [
    'Player', 'Points Per Game', 'Assists Per Game',
    'Rebounds Per Game', 'Steals Per Game', 'Blocks Per Game',
    'Field Goal %', 'Three Point %', 'Free Throw %', 'Minutes Per Game'
]
nba_data = nba_df[nba_columns]

# --- FUT (Soccer) Dataset Mapping ---
soccer_df = soccer_df.rename(columns={
    'Name': 'Player',
    'Goals per match': 'Goals Per Game'
})
soccer_df['Assists Per Game'] = soccer_df['Assists']
soccer_df['Shot Conversion Rate'] = soccer_df.apply(
    lambda row: row['Goals Per Game'] / row['Shots'] if row['Shots'] and row['Shots'] > 0 else 0, axis=1
)
soccer_df['Tackles Per Game'] = soccer_df['Tackles'] / soccer_df['Appearances']
soccer_df['Interceptions Per Game'] = soccer_df['Interceptions'] / soccer_df['Appearances']

soccer_columns = [
    'Player', 'Goals Per Game', 'Assists Per Game', 'Shot Conversion Rate',
    'Tackles Per Game', 'Interceptions Per Game'
]
soccer_data = soccer_df[soccer_columns]

# --- Normalization using z-score (StandardScaler) ---
features_nba = [
    'Points Per Game', 'Assists Per Game', 'Rebounds Per Game',
    'Steals Per Game', 'Blocks Per Game', 'Field Goal %', 'Three Point %',
    'Free Throw %', 'Minutes Per Game'
]
features_soccer = [
    'Goals Per Game', 'Assists Per Game', 'Shot Conversion Rate',
    'Tackles Per Game', 'Interceptions Per Game'
]

scaler_nba = StandardScaler()
nba_data_scaled = nba_data.copy()
nba_data_scaled[features_nba] = scaler_nba.fit_transform(nba_data[features_nba])

scaler_soccer = StandardScaler()
soccer_data_scaled = soccer_data.copy()
soccer_data_scaled[features_soccer] = scaler_soccer.fit_transform(soccer_data[features_soccer])

# Inspect a few rows of the normalized data
print("Z-score normalized NBA Data:")
print(nba_data_scaled.head())

print("\nZ-score normalized Soccer Data:")
print(soccer_data_scaled.head())

# Save the normalized data for later use
os.makedirs("data/normalized_data", exist_ok=True)
nba_data_scaled.to_csv("data/normalized_data/nba_normalized_zscore.csv", index=False)
soccer_data_scaled.to_csv("data/normalized_data/soccer_normalized_zscore.csv", index=False)
