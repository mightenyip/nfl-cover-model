#!/usr/bin/env python3
"""
Create Week 5 Detailed EPA Data from SumerSports
Data source: https://sumersports.com/teams/offensive/ (Last Updated 10-03-2025)
"""

import pandas as pd
from datetime import datetime

def create_week5_detailed_epa():
    """Create detailed EPA data for Week 5 using latest SumerSports data"""
    
    print("Creating Week 5 detailed EPA data from SumerSports...")
    print("Source: https://sumersports.com/teams/offensive/")
    print("Last Updated: 10-03-2025 06:20 AM EST")
    
    # Offensive EPA data from SumerSports (as of 10-03-2025)
    detailed_data = [
        {'team': 'BUF', 'team_name': 'Buffalo Bills', 'epa_off_per_play': 0.20, 'epa_pass_off': 0.23, 'epa_rush_off': 0.15, 
         'epa_def_allowed_per_play': 0.06, 'epa_pass_def_allowed': 0.05, 'epa_rush_def_allowed': 0.04},
        
        {'team': 'IND', 'team_name': 'Indianapolis Colts', 'epa_off_per_play': 0.16, 'epa_pass_off': 0.23, 'epa_rush_off': 0.07, 
         'epa_def_allowed_per_play': -0.03, 'epa_pass_def_allowed': -0.05, 'epa_rush_def_allowed': -0.01},
        
        {'team': 'GB', 'team_name': 'Green Bay Packers', 'epa_off_per_play': 0.15, 'epa_pass_off': 0.28, 'epa_rush_off': 0.00, 
         'epa_def_allowed_per_play': 0.02, 'epa_pass_def_allowed': 0.01, 'epa_rush_def_allowed': 0.03},
        
        {'team': 'DET', 'team_name': 'Detroit Lions', 'epa_off_per_play': 0.15, 'epa_pass_off': 0.30, 'epa_rush_off': -0.02, 
         'epa_def_allowed_per_play': -0.05, 'epa_pass_def_allowed': -0.07, 'epa_rush_def_allowed': -0.03},
        
        {'team': 'BAL', 'team_name': 'Baltimore Ravens', 'epa_off_per_play': 0.13, 'epa_pass_off': 0.14, 'epa_rush_off': 0.10, 
         'epa_def_allowed_per_play': 0.05, 'epa_pass_def_allowed': 0.08, 'epa_rush_def_allowed': -0.02},
        
        {'team': 'DAL', 'team_name': 'Dallas Cowboys', 'epa_off_per_play': 0.12, 'epa_pass_off': 0.17, 'epa_rush_off': 0.03, 
         'epa_def_allowed_per_play': 0.17, 'epa_pass_def_allowed': 0.14, 'epa_rush_def_allowed': 0.11},
        
        {'team': 'KC', 'team_name': 'Kansas City Chiefs', 'epa_off_per_play': 0.12, 'epa_pass_off': 0.13, 'epa_rush_off': 0.08, 
         'epa_def_allowed_per_play': 0.12, 'epa_pass_def_allowed': 0.10, 'epa_rush_def_allowed': 0.09},
        
        {'team': 'NE', 'team_name': 'New England Patriots', 'epa_off_per_play': 0.08, 'epa_pass_off': 0.23, 'epa_rush_off': -0.15, 
         'epa_def_allowed_per_play': -0.06, 'epa_pass_def_allowed': -0.08, 'epa_rush_def_allowed': -0.04},
        
        {'team': 'WAS', 'team_name': 'Washington Commanders', 'epa_off_per_play': 0.07, 'epa_pass_off': 0.01, 'epa_rush_off': 0.13, 
         'epa_def_allowed_per_play': -0.10, 'epa_pass_def_allowed': -0.11, 'epa_rush_def_allowed': 0.07},
        
        {'team': 'DEN', 'team_name': 'Denver Broncos', 'epa_off_per_play': 0.05, 'epa_pass_off': 0.08, 'epa_rush_off': 0.01, 
         'epa_def_allowed_per_play': -0.05, 'epa_pass_def_allowed': -0.03, 'epa_rush_def_allowed': -0.08},
        
        {'team': 'LA', 'team_name': 'Los Angeles Rams', 'epa_off_per_play': 0.04, 'epa_pass_off': 0.18, 'epa_rush_off': -0.18, 
         'epa_def_allowed_per_play': -0.13, 'epa_pass_def_allowed': -0.12, 'epa_rush_def_allowed': -0.08},
        
        {'team': 'TB', 'team_name': 'Tampa Bay Buccaneers', 'epa_off_per_play': 0.03, 'epa_pass_off': 0.06, 'epa_rush_off': 0.00, 
         'epa_def_allowed_per_play': -0.04, 'epa_pass_def_allowed': -0.20, 'epa_rush_def_allowed': -0.14},
        
        {'team': 'JAX', 'team_name': 'Jacksonville Jaguars', 'epa_off_per_play': 0.03, 'epa_pass_off': 0.02, 'epa_rush_off': 0.04, 
         'epa_def_allowed_per_play': 0.31, 'epa_pass_def_allowed': 0.28, 'epa_rush_def_allowed': 0.20},
        
        {'team': 'MIA', 'team_name': 'Miami Dolphins', 'epa_off_per_play': 0.03, 'epa_pass_off': 0.02, 'epa_rush_off': 0.03, 
         'epa_def_allowed_per_play': 0.29, 'epa_pass_def_allowed': 0.24, 'epa_rush_def_allowed': 0.18},
        
        {'team': 'SF', 'team_name': 'San Francisco 49ers', 'epa_off_per_play': 0.02, 'epa_pass_off': 0.13, 'epa_rush_off': -0.14, 
         'epa_def_allowed_per_play': -0.02, 'epa_pass_def_allowed': -0.03, 'epa_rush_def_allowed': -0.08},
        
        {'team': 'SEA', 'team_name': 'Seattle Seahawks', 'epa_off_per_play': 0.02, 'epa_pass_off': 0.04, 'epa_rush_off': -0.01, 
         'epa_def_allowed_per_play': -0.04, 'epa_pass_def_allowed': -0.03, 'epa_rush_def_allowed': -0.05},
        
        {'team': 'PHI', 'team_name': 'Philadelphia Eagles', 'epa_off_per_play': 0.02, 'epa_pass_off': 0.08, 'epa_rush_off': -0.06, 
         'epa_def_allowed_per_play': -0.05, 'epa_pass_def_allowed': -0.04, 'epa_rush_def_allowed': -0.02},
        
        {'team': 'ARI', 'team_name': 'Arizona Cardinals', 'epa_off_per_play': 0.01, 'epa_pass_off': 0.17, 'epa_rush_off': -0.13, 
         'epa_def_allowed_per_play': -0.02, 'epa_pass_def_allowed': -0.04, 'epa_rush_def_allowed': -0.09},
        
        {'team': 'PIT', 'team_name': 'Pittsburgh Steelers', 'epa_off_per_play': 0.01, 'epa_pass_off': 0.06, 'epa_rush_off': -0.05, 
         'epa_def_allowed_per_play': -0.08, 'epa_pass_def_allowed': -0.10, 'epa_rush_def_allowed': -0.06},
        
        {'team': 'LAC', 'team_name': 'Los Angeles Chargers', 'epa_off_per_play': -0.01, 'epa_pass_off': 0.02, 'epa_rush_off': -0.06, 
         'epa_def_allowed_per_play': -0.10, 'epa_pass_def_allowed': -0.11, 'epa_rush_def_allowed': -0.07},
        
        {'team': 'NYJ', 'team_name': 'New York Jets', 'epa_off_per_play': -0.01, 'epa_pass_off': 0.03, 'epa_rush_off': -0.06, 
         'epa_def_allowed_per_play': 0.17, 'epa_pass_def_allowed': 0.14, 'epa_rush_def_allowed': 0.09},
        
        {'team': 'CHI', 'team_name': 'Chicago Bears', 'epa_off_per_play': -0.02, 'epa_pass_off': 0.07, 'epa_rush_off': -0.15, 
         'epa_def_allowed_per_play': 0.06, 'epa_pass_def_allowed': 0.04, 'epa_rush_def_allowed': 0.05},
        
        {'team': 'ATL', 'team_name': 'Atlanta Falcons', 'epa_off_per_play': -0.03, 'epa_pass_off': -0.02, 'epa_rush_off': -0.03, 
         'epa_def_allowed_per_play': 0.07, 'epa_pass_def_allowed': 0.06, 'epa_rush_def_allowed': 0.05},
        
        {'team': 'HOU', 'team_name': 'Houston Texans', 'epa_off_per_play': -0.05, 'epa_pass_off': -0.08, 'epa_rush_off': 0.01, 
         'epa_def_allowed_per_play': 0.05, 'epa_pass_def_allowed': 0.03, 'epa_rush_def_allowed': 0.13},
        
        {'team': 'CAR', 'team_name': 'Carolina Panthers', 'epa_off_per_play': -0.07, 'epa_pass_off': -0.08, 'epa_rush_off': -0.03, 
         'epa_def_allowed_per_play': 0.29, 'epa_pass_def_allowed': 0.26, 'epa_rush_def_allowed': 0.19},
        
        {'team': 'NO', 'team_name': 'New Orleans Saints', 'epa_off_per_play': -0.08, 'epa_pass_off': -0.14, 'epa_rush_off': 0.02, 
         'epa_def_allowed_per_play': 0.01, 'epa_pass_def_allowed': 0.04, 'epa_rush_def_allowed': -0.06},
        
        {'team': 'MIN', 'team_name': 'Minnesota Vikings', 'epa_off_per_play': -0.09, 'epa_pass_off': -0.15, 'epa_rush_off': -0.01, 
         'epa_def_allowed_per_play': -0.06, 'epa_pass_def_allowed': -0.09, 'epa_rush_def_allowed': -0.05},
        
        {'team': 'LV', 'team_name': 'Las Vegas Raiders', 'epa_off_per_play': -0.10, 'epa_pass_off': -0.05, 'epa_rush_off': -0.18, 
         'epa_def_allowed_per_play': 0.18, 'epa_pass_def_allowed': 0.16, 'epa_rush_def_allowed': 0.12},
        
        {'team': 'NYG', 'team_name': 'New York Giants', 'epa_off_per_play': -0.11, 'epa_pass_off': -0.10, 'epa_rush_off': -0.10, 
         'epa_def_allowed_per_play': 0.07, 'epa_pass_def_allowed': 0.06, 'epa_rush_def_allowed': 0.04},
        
        {'team': 'CLE', 'team_name': 'Cleveland Browns', 'epa_off_per_play': -0.20, 'epa_pass_off': -0.31, 'epa_rush_off': 0.01, 
         'epa_def_allowed_per_play': -0.06, 'epa_pass_def_allowed': -0.08, 'epa_rush_def_allowed': -0.04},
        
        {'team': 'TEN', 'team_name': 'Tennessee Titans', 'epa_off_per_play': -0.25, 'epa_pass_off': -0.33, 'epa_rush_off': -0.09, 
         'epa_def_allowed_per_play': 0.16, 'epa_pass_def_allowed': 0.14, 'epa_rush_def_allowed': 0.12},
        
        {'team': 'CIN', 'team_name': 'Cincinnati Bengals', 'epa_off_per_play': -0.28, 'epa_pass_off': -0.34, 'epa_rush_off': -0.15, 
         'epa_def_allowed_per_play': -0.03, 'epa_pass_def_allowed': -0.05, 'epa_rush_def_allowed': -0.08}
    ]
    
    # Create DataFrame
    df = pd.DataFrame(detailed_data)
    
    # Calculate net EPA
    df['net_epa_per_play'] = df['epa_off_per_play'] - df['epa_def_allowed_per_play']
    
    # Add metadata
    df['last_updated'] = '2025-10-03 06:20:00'
    df['source'] = 'sumersports_week5_updated'
    
    print(f"Created detailed EPA data for {len(df)} teams")
    
    # Save to detailed_epa_data.csv (overwrite old data)
    df.to_csv("../detailed_epa_data.csv", index=False)
    print("✅ Updated detailed EPA data saved to: ../detailed_epa_data.csv")
    
    # Also save to data directory
    df.to_csv("../data/detailed_epa_data_week5.csv", index=False)
    print("✅ Updated detailed EPA data saved to: ../data/detailed_epa_data_week5.csv")
    
    # Display summary
    print("\n=== Top 5 Teams by Net EPA ===")
    top_5 = df.nlargest(5, 'net_epa_per_play')[['team_name', 'net_epa_per_play', 'epa_off_per_play', 'epa_def_allowed_per_play']]
    for _, row in top_5.iterrows():
        print(f"{row['team_name']}: Net EPA {row['net_epa_per_play']:.3f} (Off: {row['epa_off_per_play']:.3f}, Def: {row['epa_def_allowed_per_play']:.3f})")
    
    print("\n=== Bottom 5 Teams by Net EPA ===")
    bottom_5 = df.nsmallest(5, 'net_epa_per_play')[['team_name', 'net_epa_per_play', 'epa_off_per_play', 'epa_def_allowed_per_play']]
    for _, row in bottom_5.iterrows():
        print(f"{row['team_name']}: Net EPA {row['net_epa_per_play']:.3f} (Off: {row['epa_off_per_play']:.3f}, Def: {row['epa_def_allowed_per_play']:.3f})")
    
    return df

if __name__ == "__main__":
    create_week5_detailed_epa()
