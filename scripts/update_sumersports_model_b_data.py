#!/usr/bin/env python3
"""
Update Model B EPA Data from SumerSports
Last Updated: October 7, 2025 from SumerSports.com
"""

import pandas as pd
from datetime import datetime

def create_updated_epa_data():
    """Create updated EPA data from SumerSports (as of 10-07-2025)"""
    
    print("=== Updating Model B EPA Data from SumerSports ===")
    print("Source: https://sumersports.com/teams/offensive/ and /defensive/")
    print("Last Updated: 10-07-2025 11:02 AM EST\n")
    
    # Offensive EPA data from SumerSports (Offensive page)
    # Positive EPA/Play means better offense
    offensive_data = {
        'BAL': {'name': 'Baltimore Ravens', 'epa_off': 0.21, 'epa_pass_off': 0.28, 'epa_rush_off': 0.12},
        'BUF': {'name': 'Buffalo Bills', 'epa_off': 0.18, 'epa_pass_off': 0.23, 'epa_rush_off': 0.15},
        'DET': {'name': 'Detroit Lions', 'epa_off': 0.15, 'epa_pass_off': 0.30, 'epa_rush_off': -0.02},
        'IND': {'name': 'Indianapolis Colts', 'epa_off': 0.16, 'epa_pass_off': 0.23, 'epa_rush_off': 0.07},
        'GB': {'name': 'Green Bay Packers', 'epa_off': 0.15, 'epa_pass_off': 0.28, 'epa_rush_off': 0.0},
        'KC': {'name': 'Kansas City Chiefs', 'epa_off': 0.12, 'epa_pass_off': 0.13, 'epa_rush_off': 0.08},
        'DAL': {'name': 'Dallas Cowboys', 'epa_off': 0.12, 'epa_pass_off': 0.17, 'epa_rush_off': 0.03},
        'WAS': {'name': 'Washington Commanders', 'epa_off': 0.07, 'epa_pass_off': 0.01, 'epa_rush_off': 0.13},
        'NE': {'name': 'New England Patriots', 'epa_off': 0.08, 'epa_pass_off': 0.23, 'epa_rush_off': -0.15},
        'SEA': {'name': 'Seattle Seahawks', 'epa_off': 0.06, 'epa_pass_off': 0.10, 'epa_rush_off': 0.01},
        'MIA': {'name': 'Miami Dolphins', 'epa_off': 0.05, 'epa_pass_off': -0.02, 'epa_rush_off': 0.13},
        'TB': {'name': 'Tampa Bay Buccaneers', 'epa_off': 0.05, 'epa_pass_off': 0.18, 'epa_rush_off': -0.13},
        'PHI': {'name': 'Philadelphia Eagles', 'epa_off': 0.03, 'epa_pass_off': 0.05, 'epa_rush_off': 0.01},
        'SF': {'name': 'San Francisco 49ers', 'epa_off': 0.03, 'epa_pass_off': 0.18, 'epa_rush_off': -0.16},
        'DEN': {'name': 'Denver Broncos', 'epa_off': 0.02, 'epa_pass_off': -0.02, 'epa_rush_off': 0.07},
        'LA': {'name': 'Los Angeles Rams', 'epa_off': 0.02, 'epa_pass_off': 0.0, 'epa_rush_off': 0.03},
        'JAX': {'name': 'Jacksonville Jaguars', 'epa_off': 0.01, 'epa_pass_off': -0.08, 'epa_rush_off': 0.13},
        'PIT': {'name': 'Pittsburgh Steelers', 'epa_off': 0.0, 'epa_pass_off': 0.01, 'epa_rush_off': -0.01},
        'HOU': {'name': 'Houston Texans', 'epa_off': 0.0, 'epa_pass_off': -0.02, 'epa_rush_off': 0.02},
        'NO': {'name': 'New Orleans Saints', 'epa_off': -0.01, 'epa_pass_off': 0.03, 'epa_rush_off': -0.07},
        'CIN': {'name': 'Cincinnati Bengals', 'epa_off': -0.02, 'epa_pass_off': 0.05, 'epa_rush_off': -0.12},
        'CHI': {'name': 'Chicago Bears', 'epa_off': -0.05, 'epa_pass_off': -0.01, 'epa_rush_off': -0.09},
        'ATL': {'name': 'Atlanta Falcons', 'epa_off': -0.07, 'epa_pass_off': -0.15, 'epa_rush_off': 0.03},
        'LAC': {'name': 'Los Angeles Chargers', 'epa_off': -0.08, 'epa_pass_off': -0.14, 'epa_rush_off': 0.0},
        'CAR': {'name': 'Carolina Panthers', 'epa_off': -0.08, 'epa_pass_off': -0.13, 'epa_rush_off': -0.01},
        'ARI': {'name': 'Arizona Cardinals', 'epa_off': -0.09, 'epa_pass_off': -0.17, 'epa_rush_off': 0.02},
        'NYG': {'name': 'New York Giants', 'epa_off': -0.11, 'epa_pass_off': -0.19, 'epa_rush_off': 0.0},
        'TEN': {'name': 'Tennessee Titans', 'epa_off': -0.12, 'epa_pass_off': -0.17, 'epa_rush_off': -0.05},
        'NYJ': {'name': 'New York Jets', 'epa_off': -0.13, 'epa_pass_off': -0.17, 'epa_rush_off': -0.08},
        'LV': {'name': 'Las Vegas Raiders', 'epa_off': -0.14, 'epa_pass_off': -0.17, 'epa_rush_off': -0.10},
        'CLE': {'name': 'Cleveland Browns', 'epa_off': -0.19, 'epa_pass_off': -0.25, 'epa_rush_off': -0.10},
        'MIN': {'name': 'Minnesota Vikings', 'epa_off': -0.03, 'epa_pass_off': -0.08, 'epa_rush_off': 0.03},
    }
    
    # Defensive EPA data from SumerSports (Defensive page)
    # Negative EPA/Play means better defense (they allow less EPA to opponents)
    defensive_data = {
        'MIN': {'epa_def': -0.13, 'epa_pass_def': -0.30, 'epa_rush_def': 0.05},
        'HOU': {'epa_def': -0.12, 'epa_pass_def': -0.19, 'epa_rush_def': -0.01},
        'DET': {'epa_def': -0.10, 'epa_pass_def': -0.05, 'epa_rush_def': -0.18},
        'DEN': {'epa_def': -0.09, 'epa_pass_def': -0.07, 'epa_rush_def': -0.11},
        'IND': {'epa_def': -0.08, 'epa_pass_def': -0.09, 'epa_rush_def': -0.06},
        'JAX': {'epa_def': -0.07, 'epa_pass_def': -0.12, 'epa_rush_def': 0.04},
        'ATL': {'epa_def': -0.05, 'epa_pass_def': -0.13, 'epa_rush_def': 0.05},
        'PHI': {'epa_def': -0.05, 'epa_pass_def': -0.07, 'epa_rush_def': -0.02},
        'LAC': {'epa_def': -0.04, 'epa_pass_def': -0.07, 'epa_rush_def': 0.01},
        'SF': {'epa_def': -0.03, 'epa_pass_def': 0.02, 'epa_rush_def': -0.11},
        'CLE': {'epa_def': -0.03, 'epa_pass_def': 0.12, 'epa_rush_def': -0.22},
        'LA': {'epa_def': -0.03, 'epa_pass_def': -0.02, 'epa_rush_def': -0.03},
        'ARI': {'epa_def': -0.02, 'epa_pass_def': 0.06, 'epa_rush_def': -0.16},
        'NO': {'epa_def': -0.01, 'epa_pass_def': 0.04, 'epa_rush_def': -0.06},
        'KC': {'epa_def': -0.01, 'epa_pass_def': -0.04, 'epa_rush_def': 0.02},
        'GB': {'epa_def': 0.01, 'epa_pass_def': 0.07, 'epa_rush_def': -0.08},
        'CHI': {'epa_def': 0.01, 'epa_pass_def': 0.03, 'epa_rush_def': -0.02},
        'WAS': {'epa_def': 0.01, 'epa_pass_def': 0.09, 'epa_rush_def': -0.10},
        'SEA': {'epa_def': 0.01, 'epa_pass_def': 0.12, 'epa_rush_def': -0.18},
        'BUF': {'epa_def': 0.02, 'epa_pass_def': -0.02, 'epa_rush_def': 0.07},
        'TB': {'epa_def': 0.03, 'epa_pass_def': 0.11, 'epa_rush_def': -0.10},
        'PIT': {'epa_def': 0.04, 'epa_pass_def': 0.11, 'epa_rush_def': -0.05},
        'CAR': {'epa_def': 0.05, 'epa_pass_def': 0.09, 'epa_rush_def': -0.01},
        'NE': {'epa_def': 0.05, 'epa_pass_def': 0.18, 'epa_rush_def': -0.14},
        'LV': {'epa_def': 0.06, 'epa_pass_def': 0.19, 'epa_rush_def': -0.14},
        'NYG': {'epa_def': 0.06, 'epa_pass_def': 0.04, 'epa_rush_def': 0.10},
        'TEN': {'epa_def': 0.08, 'epa_pass_def': 0.13, 'epa_rush_def': 0.02},
        'CIN': {'epa_def': 0.11, 'epa_pass_def': 0.18, 'epa_rush_def': 0.01},
        'NYJ': {'epa_def': 0.15, 'epa_pass_def': 0.26, 'epa_rush_def': 0.02},
        'BAL': {'epa_def': 0.17, 'epa_pass_def': 0.21, 'epa_rush_def': 0.12},
        'DAL': {'epa_def': 0.19, 'epa_pass_def': 0.30, 'epa_rush_def': 0.03},
        'MIA': {'epa_def': 0.23, 'epa_pass_def': 0.26, 'epa_rush_def': 0.17},
    }
    
    # Combine the data
    combined_data = []
    for team_abbr, off_stats in offensive_data.items():
        def_stats = defensive_data.get(team_abbr, {'epa_def': 0, 'epa_pass_def': 0, 'epa_rush_def': 0})
        
        net_epa = off_stats['epa_off'] - def_stats['epa_def']
        
        combined_data.append({
            'team': team_abbr,
            'team_name': off_stats['name'],
            'epa_off_per_play': off_stats['epa_off'],
            'epa_pass_off': off_stats['epa_pass_off'],
            'epa_rush_off': off_stats['epa_rush_off'],
            'epa_def_allowed_per_play': def_stats['epa_def'],
            'epa_pass_def_allowed': def_stats['epa_pass_def'],
            'epa_rush_def_allowed': def_stats['epa_rush_def'],
            'net_epa_per_play': net_epa,
            'last_updated': '2025-10-07 11:02:00',
            'source': 'sumersports_week5_oct7'
        })
    
    # Create DataFrame
    df = pd.DataFrame(combined_data)
    
    # Sort by net EPA (best to worst)
    df = df.sort_values('net_epa_per_play', ascending=False).reset_index(drop=True)
    
    # Save to CSV
    output_file = 'detailed_epa_data.csv'
    df.to_csv(output_file, index=False)
    print(f"✅ Updated EPA data saved to {output_file}")
    
    # Print summary
    print(f"\n📊 Summary:")
    print(f"Total teams: {len(df)}")
    print(f"Last updated: 2025-10-07 11:02:00 EST")
    print(f"Source: SumerSports.com\n")
    
    print("🔴 Top 5 Offenses (EPA/Play):")
    top_offense = df.nlargest(5, 'epa_off_per_play')[['team_name', 'epa_off_per_play']]
    for idx, row in top_offense.iterrows():
        print(f"  {row['team_name']}: {row['epa_off_per_play']:.2f}")
    
    print("\n🛡️  Top 5 Defenses (EPA Allowed/Play):")
    top_defense = df.nsmallest(5, 'epa_def_allowed_per_play')[['team_name', 'epa_def_allowed_per_play']]
    for idx, row in top_defense.iterrows():
        print(f"  {row['team_name']}: {row['epa_def_allowed_per_play']:.2f}")
    
    print("\n📈 Top 5 Overall (Net EPA):")
    top_net = df.nlargest(5, 'net_epa_per_play')[['team_name', 'net_epa_per_play']]
    for idx, row in top_net.iterrows():
        print(f"  {row['team_name']}: {row['net_epa_per_play']:.2f}")
    
    return df

if __name__ == "__main__":
    create_updated_epa_data()

