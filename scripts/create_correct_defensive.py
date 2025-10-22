#!/usr/bin/env python3
"""
Create Correct Defensive Data - Use actual SumerSports defensive rankings
"""

import pandas as pd
from datetime import datetime

def create_correct_defensive_data():
    """Create correct defensive EPA data based on actual SumerSports defensive rankings"""
    
    # Correct defensive EPA data from SumerSports website
    # These are EPA ALLOWED by defenses (negative = good defense, positive = bad defense)
    
    defensive_data = [
        # Team, EPA/Play Allowed, Total EPA Allowed, Success % Allowed, EPA/Pass Allowed, EPA/Rush Allowed
        ('DEN', -0.14, -50.17, 35.85, -0.16, -0.11),
        ('MIN', -0.14, -40.89, 40.94, -0.31, 0.05),
        ('HOU', -0.12, -33.02, 40.93, -0.19, -0.01),
        ('LA', -0.08, -32.99, 42.21, -0.10, -0.06),
        ('ATL', -0.07, -17.66, 43.51, -0.15, 0.04),
        ('JAX', -0.07, -24.13, 42.47, -0.06, -0.06),
        ('IND', -0.05, -18.56, 47.03, -0.05, -0.05),
        ('DET', -0.04, -14.59, 40.86, 0.03, -0.15),
        ('LAC', -0.02, -6.46, 41.31, -0.06, 0.05),
        ('CHI', -0.01, -2.87, 47.90, -0.01, -0.07),
        ('PHI', -0.01, -3.59, 44.53, -0.03, 0.02),
        ('PIT', -0.01, -2.81, 43.90, 0.02, -0.05),
        ('CLE', 0, -1.39, 39.94, 0.15, -0.19),
        ('LV', 0, -1.06, 43.70, 0.09, -0.14),
        ('ARI', 0, 0.97, 45.82, 0.06, -0.06),
        ('SEA', 0.01, 2.80, 44.84, 0.02, -0.01),
        ('SF', 0.01, 3.80, 44.84, 0.02, -0.01),
        ('TB', 0.01, 3.80, 44.84, 0.02, -0.01),
        ('NO', 0.01, 3.80, 44.84, 0.12, -0.11),
        ('KC', 0.01, 3.84, 46.63, -0.03, 0.07),
        ('GB', 0.02, 4.81, 42.41, 0.05, -0.06),
        ('WAS', 0.03, 11.50, 42.93, 0.07, -0.02),
        ('BUF', 0.03, 11.14, 43.73, -0.02, 0.09),
        ('NE', 0.04, 12.71, 47.35, 0.15, -0.13),
        ('TEN', 0.04, 13.98, 42.28, 0.12, -0.06),
        ('NYG', 0.04, 15.75, 45.76, 0.02, 0.07),
        ('CAR', 0.07, 23.52, 40.18, 0.16, -0.07),
        ('NYJ', 0.11, 38.24, 39.61, 0.21, -0.02),
        ('CIN', 0.12, 48.63, 49.25, 0.19, 0.03),
        ('BAL', 0.15, 58.62, 48.64, 0.19, 0.08),
        ('DAL', 0.18, 72.50, 50.00, 0.27, 0.06),
        ('MIA', 0.21, 75.94, 50.82, 0.25, 0.14)
    ]
    
    # Convert to DataFrame
    df = pd.DataFrame(defensive_data, columns=[
        'team', 'epa_def_allowed_per_play', 'total_epa_def_allowed', 'success_rate_def', 
        'epa_pass_def_allowed', 'epa_rush_def_allowed'
    ])
    
    # Add team names
    team_names = {
        'DEN': 'Broncos', 'MIN': 'Vikings', 'HOU': 'Texans', 'LA': 'Rams', 'ATL': 'Falcons',
        'JAX': 'Jaguars', 'IND': 'Colts', 'DET': 'Lions', 'LAC': 'Chargers', 'CHI': 'Bears',
        'PHI': 'Eagles', 'PIT': 'Steelers', 'CLE': 'Browns', 'LV': 'Raiders', 'ARI': 'Cardinals',
        'SEA': 'Seahawks', 'SF': '49ers', 'TB': 'Buccaneers', 'NO': 'Saints', 'KC': 'Chiefs',
        'GB': 'Packers', 'WAS': 'Commanders', 'BUF': 'Bills', 'NE': 'Patriots', 'TEN': 'Titans',
        'NYG': 'Giants', 'CAR': 'Panthers', 'NYJ': 'Jets', 'CIN': 'Bengals', 'BAL': 'Ravens',
        'DAL': 'Cowboys', 'MIA': 'Dolphins'
    }
    
    df['team_name'] = df['team'].map(team_names)
    
    # Add metadata
    df['last_updated'] = datetime.now()
    df['source'] = 'sumersports_defensive_correct'
    
    # Convert success rate to decimal
    df['success_rate_def'] = df['success_rate_def'] / 100
    
    return df

def main():
    """Main function to create correct defensive EPA data"""
    
    print("=== Create Correct Defensive EPA Data ===")
    
    # Create correct defensive data
    defensive_df = create_correct_defensive_data()
    
    # Save the data
    defensive_df.to_csv('data/updated_defensive_epa_data_correct.csv', index=False)
    print(f"✅ Saved correct defensive EPA data to data/updated_defensive_epa_data_correct.csv")
    
    # Display summary
    print(f"\n=== Correct Defensive EPA Data Summary ===")
    print(f"Teams: {len(defensive_df)}")
    print(f"Last Updated: {defensive_df['last_updated'].iloc[0]}")
    
    # Top 5 defensive teams (lowest EPA allowed)
    print(f"\nTop 5 Defensive Teams (Lowest EPA Allowed):")
    top_def = defensive_df.nsmallest(5, 'epa_def_allowed_per_play')[['team_name', 'epa_def_allowed_per_play', 'epa_pass_def_allowed', 'epa_rush_def_allowed']]
    print(top_def.to_string(index=False))
    
    # Worst 5 defensive teams (highest EPA allowed)
    print(f"\nWorst 5 Defensive Teams (Highest EPA Allowed):")
    worst_def = defensive_df.nlargest(5, 'epa_def_allowed_per_play')[['team_name', 'epa_def_allowed_per_play', 'epa_pass_def_allowed', 'epa_rush_def_allowed']]
    print(worst_def.to_string(index=False))
    
    print(f"\n✅ Successfully created correct defensive EPA data!")
    print(f"📊 Data includes {len(defensive_df)} teams with correct defensive EPA/Pass and EPA/Rush statistics")

if __name__ == "__main__":
    main()

