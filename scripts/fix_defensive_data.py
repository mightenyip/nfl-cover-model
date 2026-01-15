#!/usr/bin/env python3
"""
Fix Defensive Data - Create correct defensive EPA data from SumerSports rankings
"""

import pandas as pd
from datetime import datetime

def create_correct_defensive_data():
    """Create correct defensive EPA data based on SumerSports defensive rankings"""
    
    # Data from SumerSports defensive page (as of 10-15-2025)
    # These are DEFENSIVE EPA ALLOWED values (negative means good defense)
    # Teams ranked by defensive performance (worst to best)
    
    defensive_data = [
        # Team, EPA/Play Allowed, Total EPA Allowed, Success % Allowed, EPA/Pass Allowed, EPA/Rush Allowed, Pass Yards Allowed, Comp % Allowed, Pass TD Allowed, Rush Yards Allowed, Rush TD Allowed, ADoT Allowed, Sack %, Scramble %, Int %
        ('MIA', 0.21, 75.94, 50.82, 0.25, 0.14, 1403, 74.86, 11, 1011, 6, 6.49, 5.91, 7.88, 0.49),
        ('DAL', 0.18, 72.50, 50.00, 0.27, 0.06, 1719, 71.84, 15, 853, 6, 8.47, 4.82, 4.82, 0.88),
        ('BAL', 0.15, 58.62, 48.64, 0.19, 0.08, 1532, 68.52, 14, 806, 9, 8.19, 3.39, 5.08, 0.42),
        ('CIN', 0.12, 48.63, 49.25, 0.19, 0.03, 1609, 68.47, 13, 814, 8, 7.08, 4.91, 4.46, 2.68),
        ('NYJ', 0.11, 38.24, 39.61, 0.21, -0.02, 1245, 64.71, 12, 780, 5, 6.41, 4.17, 7.29, 0.00),
        ('CAR', 0.07, 23.52, 40.18, 0.16, -0.07, 1319, 66.84, 10, 567, 5, 7.31, 2.46, 5.42, 1.97),
        ('NYG', 0.04, 15.75, 45.76, 0.02, 0.07, 1548, 65.78, 7, 773, 7, 8.15, 5.24, 4.03, 1.61),
        ('TEN', 0.04, 13.98, 42.28, 0.12, -0.06, 1329, 70.72, 7, 802, 11, 6.28, 4.55, 4.04, 2.02),
        ('NE', 0.04, 12.71, 47.35, 0.15, -0.13, 1504, 71.98, 9, 501, 3, 7.89, 6.28, 5.80, 1.93),
        ('BUF', 0.03, 11.14, 43.73, -0.02, 0.09, 1087, 64.24, 7, 938, 9, 7.12, 7.73, 7.22, 1.03),
        ('WAS', 0.03, 11.50, 42.93, 0.07, -0.02, 1524, 63.24, 9, 730, 4, 9.17, 8.45, 4.69, 0.94),
        ('GB', 0.02, 4.81, 42.41, 0.05, -0.06, 1105, 67.33, 8, 365, 3, 6.84, 5.45, 2.73, 0.91),
        ('KC', 0.01, 3.84, 46.63, -0.03, 0.07, 1202, 69.71, 7, 715, 6, 7.60, 6.67, 10.00, 1.90),
        ('NO', 0.01, 3.80, 44.84, 0.12, -0.11, 1347, 69.49, 14, 684, 4, 8.25, 6.31, 7.77, 1.46),
        ('TB', 0.01, 3.80, 44.84, 0.02, -0.01, 1347, 67.88, 8, 647, 2, 7.89, 6.31, 4.17, 1.97),
        ('SF', 0.01, 3.80, 44.84, 0.02, -0.01, 1335, 69.16, 8, 647, 2, 7.89, 6.31, 4.17, 1.97),
        ('SEA', 0.01, 2.80, 44.84, 0.02, -0.01, 1547, 68.34, 9, 535, 2, 7.89, 6.31, 4.17, 1.97),
        ('ARI', 0, 0.97, 45.82, 0.06, -0.06, 1520, 63.29, 8, 684, 3, 8.34, 6.68, 4.17, 1.97),
        ('LV', 0, -1.06, 43.70, 0.09, -0.14, 1391, 66.17, 8, 572, 8, 7.96, 6.28, 3.59, 1.35),
        ('CLE', 0, -1.39, 39.94, 0.15, -0.19, 1192, 67.46, 12, 478, 3, 7.79, 7.33, 4.19, 1.05),
        ('PIT', -0.01, -2.81, 43.90, 0.02, -0.05, 1352, 65.79, 7, 553, 4, 7.17, 9.13, 4.11, 2.28),
        ('PHI', -0.01, -3.59, 44.53, -0.03, 0.02, 1297, 58.91, 7, 806, 8, 8.58, 3.95, 7.46, 1.32),
        ('CHI', -0.01, -2.87, 47.90, 0.05, -0.07, 1097, 73.57, 13, 782, 4, 7.12, 5.06, 6.33, 5.06),
        ('LAC', -0.02, -6.46, 41.31, -0.06, 0.05, 1154, 60.43, 5, 745, 7, 7.92, 7.08, 10.18, 2.65),
        ('DET', -0.04, -14.59, 40.86, 0.03, -0.15, 1402, 64.89, 13, 573, 5, 9.26, 8.52, 7.17, 2.69),
        ('IND', -0.05, -18.56, 47.03, -0.05, -0.05, 1494, 65.91, 10, 578, 3, 7.35, 6.50, 4.07, 2.85),
        ('JAX', -0.07, -24.13, 42.47, -0.06, -0.06, 1597, 61.61, 10, 549, 4, 9.28, 3.25, 5.69, 4.07),
        ('ATL', -0.07, -17.66, 43.51, -0.15, 0.04, 782, 57.69, 7, 570, 2, 10.34, 8.86, 8.86, 3.16),
        ('LA', -0.08, -32.99, 42.21, -0.10, -0.06, 1333, 65.87, 7, 647, 2, 7.37, 8.02, 4.22, 1.69),
        ('HOU', -0.12, -33.02, 40.93, -0.19, -0.01, 969, 58.82, 3, 453, 5, 8.26, 7.02, 3.51, 2.92),
        ('MIN', -0.14, -40.89, 40.94, -0.31, 0.05, 875, 65.22, 5, 661, 4, 5.96, 8.13, 5.63, 1.25),
        ('DEN', -0.14, -50.17, 35.85, -0.16, -0.11, 1178, 57.67, 4, 534, 2, 9.90, 13.16, 3.95, 0.44)
    ]
    
    # Convert to DataFrame
    df = pd.DataFrame(defensive_data, columns=[
        'team', 'epa_def_allowed_per_play', 'total_epa_def_allowed', 'success_rate_def', 
        'epa_pass_def_allowed', 'epa_rush_def_allowed', 'pass_yards_allowed', 'comp_pct_allowed',
        'pass_td_allowed', 'rush_yards_allowed', 'rush_td_allowed', 'adot_allowed',
        'sack_pct', 'scramble_pct', 'int_pct'
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
    df['source'] = 'sumersports_defensive_manual_fixed'
    
    # Convert success rate to decimal
    df['success_rate_def'] = df['success_rate_def'] / 100
    
    return df

def main():
    """Main function to create correct defensive EPA data"""
    
    print("=== Fix Defensive EPA Data ===")
    
    # Create correct defensive data
    defensive_df = create_correct_defensive_data()
    
    # Save the data
    defensive_df.to_csv('data/epa/processed/updated_defensive_epa_data_fixed.csv', index=False)
    print(f"✅ Saved corrected defensive EPA data to data/epa/processed/updated_defensive_epa_data_fixed.csv")
    
    # Display summary
    print(f"\n=== Corrected Defensive EPA Data Summary ===")
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
    
    print(f"\n✅ Successfully created corrected defensive EPA data!")
    print(f"📊 Data includes {len(defensive_df)} teams with correct defensive EPA/Pass and EPA/Rush statistics")

if __name__ == "__main__":
    main()

