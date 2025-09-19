#!/usr/bin/env python3
"""
Script to pull the latest 2025 play-by-play data from nflverse
"""

import pandas as pd
import numpy as np
import os
from typing import Dict, List

def pull_latest_2025_data():
    """Pull the latest 2025 play-by-play data from nflverse"""
    
    print("=== Pulling Latest 2025 Data from nflverse ===")
    
    try:
        # Try to load the latest 2025 data from nflverse
        url = "https://github.com/nflverse/nflverse-data/releases/download/pbp/play_by_play_2025.parquet"
        print(f"Loading latest 2025 PBP data from {url}...")
        
        # Use requests to handle SSL issues
        import requests
        import io
        
        response = requests.get(url, timeout=30)
        response.raise_for_status()
        
        # Read the parquet data
        df = pd.read_parquet(io.BytesIO(response.content), engine="pyarrow")
        print(f"✅ Successfully loaded {len(df)} plays from latest 2025 data")
        
        return df
        
    except Exception as e:
        print(f"❌ Could not load latest data from nflverse: {e}")
        print("Falling back to local data...")
        
        # Fallback to local data
        local_file = "images/play_by_play_2025.parquet"
        if os.path.exists(local_file):
            df = pd.read_parquet(local_file, engine="pyarrow")
            print(f"📁 Loaded {len(df)} plays from local file")
            return df
        else:
            print("❌ No local data available")
            return None

def analyze_latest_data(df: pd.DataFrame):
    """Analyze what's in the latest data"""
    
    print("\n=== Latest Data Analysis ===")
    print(f"Total plays: {len(df)}")
    print(f"Season: {df['season'].unique()}")
    print(f"Weeks available: {sorted(df['week'].unique())}")
    print(f"Season types: {df['season_type'].unique()}")
    
    # Check by week
    week_summary = df.groupby('week').agg({
        'game_id': 'nunique',
        'epa': 'count'
    })
    print(f"\nPlays by week:")
    print(week_summary)
    
    # Check what games are in the data
    games = df.groupby(['week', 'game_id']).agg({
        'posteam': 'first',
        'defteam': 'first'
    }).reset_index()
    
    print(f"\nGames in dataset:")
    for _, row in games.iterrows():
        print(f"Week {row['week']}: {row['posteam']} @ {row['defteam']} (Game ID: {row['game_id']})")
    
    # Check Bills specifically
    print(f"\n=== Bills Analysis ===")
    bills_off = df[df["posteam"] == "BUF"]
    bills_def = df[df["defteam"] == "BUF"]
    
    print(f"Bills offensive plays: {len(bills_off)}")
    print(f"Bills defensive plays: {len(bills_def)}")
    
    if len(bills_off) > 0:
        print(f"Bills offensive EPA per play: {bills_off['epa'].mean():.4f}")
    if len(bills_def) > 0:
        print(f"Bills defensive EPA allowed per play: {bills_def['epa'].mean():.4f}")
    
    return df

def calculate_updated_epa_metrics(df: pd.DataFrame):
    """Calculate updated EPA metrics with the latest data"""
    
    # Filter to regular season games only
    df = df[df["season_type"] == "REG"].copy()
    
    print(f"\n=== Calculating Updated EPA Metrics ===")
    print(f"Analyzing {len(df)} plays from {df['week'].nunique()} weeks")
    
    # Calculate offensive EPA per team
    offensive_epa = df.groupby(['posteam', 'week']).agg({
        'epa': ['sum', 'count', 'mean'],
        'success': 'mean'
    }).round(4)
    
    # Flatten column names
    offensive_epa.columns = ['epa_sum', 'plays', 'epa_per_play', 'success_rate']
    offensive_epa = offensive_epa.reset_index()
    
    # Calculate defensive EPA allowed per team
    defensive_epa = df.groupby(['defteam', 'week']).agg({
        'epa': ['sum', 'count', 'mean'],
        'success': 'mean'
    }).round(4)
    
    # Flatten column names
    defensive_epa.columns = ['epa_allowed_sum', 'plays_faced', 'epa_allowed_per_play', 'success_rate_allowed']
    defensive_epa = defensive_epa.reset_index()
    
    # Merge offensive and defensive stats
    team_stats = pd.merge(
        offensive_epa, 
        defensive_epa, 
        left_on=['posteam', 'week'], 
        right_on=['defteam', 'week'], 
        how='outer'
    )
    
    # Clean up team column
    team_stats['team'] = team_stats['posteam'].fillna(team_stats['defteam'])
    team_stats = team_stats.drop(['posteam', 'defteam'], axis=1)
    
    # Calculate net EPA
    team_stats['net_epa'] = team_stats['epa_per_play'] - team_stats['epa_allowed_per_play']
    
    # Calculate cumulative stats through all available weeks
    cumulative_stats = team_stats.groupby('team').agg({
        'epa_sum': 'sum',
        'plays': 'sum',
        'epa_allowed_sum': 'sum',
        'plays_faced': 'sum',
        'success_rate': 'mean',
        'success_rate_allowed': 'mean'
    }).round(4)
    
    # Calculate cumulative EPA per play
    cumulative_stats['epa_off_per_play'] = cumulative_stats['epa_sum'] / cumulative_stats['plays']
    cumulative_stats['epa_def_allowed_per_play'] = cumulative_stats['epa_allowed_sum'] / cumulative_stats['plays_faced']
    cumulative_stats['net_epa_per_play'] = cumulative_stats['epa_off_per_play'] - cumulative_stats['epa_def_allowed_per_play']
    
    # Reset index to get team as column
    cumulative_stats = cumulative_stats.reset_index()
    
    # Add team name mapping
    team_mapping = {
        'ARI': 'Cardinals', 'ATL': 'Falcons', 'BAL': 'Ravens', 'BUF': 'Bills',
        'CAR': 'Panthers', 'CHI': 'Bears', 'CIN': 'Bengals', 'CLE': 'Browns',
        'DAL': 'Cowboys', 'DEN': 'Broncos', 'DET': 'Lions', 'GB': 'Packers',
        'HOU': 'Texans', 'IND': 'Colts', 'JAX': 'Jaguars', 'KC': 'Chiefs',
        'LA': 'Rams', 'LAC': 'Chargers', 'LV': 'Raiders', 'MIA': 'Dolphins',
        'MIN': 'Vikings', 'NE': 'Patriots', 'NO': 'Saints', 'NYG': 'Giants',
        'NYJ': 'Jets', 'PHI': 'Eagles', 'PIT': 'Steelers', 'SF': '49ers',
        'SEA': 'Seahawks', 'TB': 'Buccaneers', 'TEN': 'Titans', 'WAS': 'Commanders'
    }
    
    cumulative_stats['team_name'] = cumulative_stats['team'].map(team_mapping)
    
    return cumulative_stats

def main():
    """Main function to pull and analyze latest data"""
    
    # Pull the latest data
    df = pull_latest_2025_data()
    
    if df is None:
        print("❌ Could not load any data")
        return
    
    # Analyze what's in the data
    df = analyze_latest_data(df)
    
    # Calculate updated EPA metrics
    team_stats = calculate_updated_epa_metrics(df)
    
    # Save the updated data
    output_file = "week2/latest_team_epa_data.csv"
    team_stats.to_csv(output_file, index=False)
    print(f"\n✅ Saved updated EPA data to {output_file}")
    
    # Print Bills specifically
    bills_data = team_stats[team_stats['team'] == 'BUF']
    if len(bills_data) > 0:
        print(f"\n=== Bills Updated EPA ===")
        print(f"Offensive EPA per play: {bills_data['epa_off_per_play'].iloc[0]:.4f}")
        print(f"Defensive EPA allowed per play: {bills_data['epa_def_allowed_per_play'].iloc[0]:.4f}")
        print(f"Net EPA per play: {bills_data['net_epa_per_play'].iloc[0]:.4f}")
    
    # Print top and bottom teams
    print(f"\n=== Top 5 Teams by Net EPA ===")
    top_teams = team_stats.nlargest(5, 'net_epa_per_play')[['team_name', 'epa_off_per_play', 'epa_def_allowed_per_play', 'net_epa_per_play']]
    print(top_teams.to_string(index=False))
    
    print(f"\n=== Bottom 5 Teams by Net EPA ===")
    bottom_teams = team_stats.nsmallest(5, 'net_epa_per_play')[['team_name', 'epa_off_per_play', 'epa_def_allowed_per_play', 'net_epa_per_play']]
    print(bottom_teams.to_string(index=False))

if __name__ == "__main__":
    main()
