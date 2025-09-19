#!/usr/bin/env python3
"""
Check what's actually in the 2025 data file
"""

import pandas as pd

def check_2025_data():
    """Check what weeks are available in the 2025 data"""
    
    # Load the 2025 play-by-play data
    pbp_df = pd.read_parquet("images/play_by_play_2025.parquet", engine="pyarrow")
    
    print("=== 2025 Data Check ===")
    print(f"Total plays in 2025 file: {len(pbp_df)}")
    
    # Check what weeks are available
    print(f"\nWeeks available: {sorted(pbp_df['week'].unique())}")
    print(f"Season types: {pbp_df['season_type'].unique()}")
    
    # Check by week
    week_summary = pbp_df.groupby('week').agg({
        'game_id': 'nunique',
        'epa': 'count'
    })
    print(f"\nPlays by week:")
    print(week_summary)
    
    # Check what games are in the data
    games = pbp_df.groupby(['week', 'game_id']).agg({
        'posteam': 'first',
        'defteam': 'first'
    }).reset_index()
    
    print(f"\nGames in dataset:")
    for _, row in games.iterrows():
        print(f"Week {row['week']}: {row['posteam']} @ {row['defteam']} (Game ID: {row['game_id']})")
    
    # Check if this is actually 2024 data mislabeled
    print(f"\nSeason: {pbp_df['season'].unique()}")
    print(f"Date range: {pbp_df['game_date'].min()} to {pbp_df['game_date'].max()}")

if __name__ == "__main__":
    check_2025_data()
