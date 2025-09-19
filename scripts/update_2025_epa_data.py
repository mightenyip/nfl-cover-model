#!/usr/bin/env python3
"""
Script to update 2025 EPA data after Week 2 games.
This will pull the latest 2025 play-by-play data and calculate updated EPA metrics.
"""

import pandas as pd
import numpy as np
import os
from typing import Dict, List

def load_2025_pbp_data():
    """Load 2025 play-by-play data from nflverse"""
    try:
        # Try to load 2025 data from nflverse
        url = "https://github.com/nflverse/nflverse-data/releases/download/pbp/play_by_play_2025.parquet"
        print(f"Loading 2025 PBP data from {url}...")
        df = pd.read_parquet(url, engine="pyarrow")
        print(f"Loaded {len(df)} plays from 2025")
        return df
    except Exception as e:
        print(f"Could not load 2025 data from nflverse: {e}")
        print("Checking for local 2025 data...")
        
        # Check for local 2025 data
        local_files = [
            "images/play_by_play_2025.parquet",
            "play_by_play_2025.parquet"
        ]
        
        for file_path in local_files:
            if os.path.exists(file_path):
                print(f"Loading local 2025 data from {file_path}...")
                df = pd.read_parquet(file_path, engine="pyarrow")
                print(f"Loaded {len(df)} plays from local 2025 data")
                return df
        
        print("No 2025 data found. You may need to wait for nflverse to release 2025 data.")
        return None

def calculate_team_epa_metrics(pbp_df: pd.DataFrame) -> pd.DataFrame:
    """Calculate EPA metrics for each team through Week 2"""
    
    # Filter to regular season games only
    pbp_df = pbp_df[pbp_df["season_type"] == "REG"].copy()
    
    # Filter to Week 1 and Week 2 only
    pbp_df = pbp_df[pbp_df["week"].isin([1, 2])].copy()
    
    print(f"Analyzing {len(pbp_df)} plays from Weeks 1-2, 2025")
    
    # Calculate offensive EPA per team
    offensive_epa = pbp_df.groupby(['posteam', 'week']).agg({
        'epa': ['sum', 'count', 'mean'],
        'success': 'mean'
    }).round(4)
    
    # Flatten column names
    offensive_epa.columns = ['epa_sum', 'plays', 'epa_per_play', 'success_rate']
    offensive_epa = offensive_epa.reset_index()
    
    # Calculate defensive EPA allowed per team
    defensive_epa = pbp_df.groupby(['defteam', 'week']).agg({
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
    
    # Calculate cumulative stats through Week 2
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

def save_updated_epa_data(team_stats: pd.DataFrame):
    """Save the updated EPA data"""
    
    # Save to CSV
    output_file = "week2/updated_team_epa_after_week2.csv"
    team_stats.to_csv(output_file, index=False)
    print(f"Saved updated EPA data to {output_file}")
    
    # Print summary
    print("\n=== Updated Team EPA After Week 2 ===")
    print("Top 10 Teams by Net EPA:")
    top_teams = team_stats.nlargest(10, 'net_epa_per_play')[['team_name', 'epa_off_per_play', 'epa_def_allowed_per_play', 'net_epa_per_play']]
    print(top_teams.to_string(index=False))
    
    print("\nBottom 10 Teams by Net EPA:")
    bottom_teams = team_stats.nsmallest(10, 'net_epa_per_play')[['team_name', 'epa_off_per_play', 'epa_def_allowed_per_play', 'net_epa_per_play']]
    print(bottom_teams.to_string(index=False))
    
    return output_file

def main():
    """Main function to update EPA data"""
    print("=== Updating 2025 EPA Data After Week 2 ===")
    
    # Load 2025 play-by-play data
    pbp_df = load_2025_pbp_data()
    
    if pbp_df is None:
        print("Could not load 2025 data. Please check if nflverse has released 2025 data.")
        return
    
    # Calculate updated EPA metrics
    team_stats = calculate_team_epa_metrics(pbp_df)
    
    # Save the updated data
    output_file = save_updated_epa_data(team_stats)
    
    print(f"\n✅ Successfully updated EPA data after Week 2")
    print(f"📁 Data saved to: {output_file}")
    print(f"📊 Analyzed {len(team_stats)} teams")

if __name__ == "__main__":
    main()
