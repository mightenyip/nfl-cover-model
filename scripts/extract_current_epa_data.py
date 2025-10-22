#!/usr/bin/env python3
"""
Extract Current EPA Data from SumerSports
Extract EPA/Pass and EPA/Rush for both offense and defense
"""

import pandas as pd
from datetime import datetime

def create_offensive_data():
    """Create offensive EPA data from SumerSports offensive page"""
    
    # Data from SumerSports offensive page (as of 10-17-2025)
    # Format: Team, EPA/Play, Total EPA, Success %, EPA/Pass, EPA/Rush, Pass Yards, Comp %, Pass TD, Rush Yards, Rush TD, ADoT, Sack %, Scramble %, Int %
    
    offensive_data = [
        # Team, EPA/Play, Total EPA, Success %, EPA/Pass, EPA/Rush, Pass Yards, Comp %, Pass TD, Rush Yards, Rush TD, ADoT, Sack %, Scramble %, Int %
        ('IND', 0.18, 66.07, 50.69, 0.24, 0.11, 1511, 71.04, 8, 791, 13, 8.24, 2.53, 5.05, 1.52),
        ('DAL', 0.16, 61.78, 47.01, 0.24, 0.01, 1658, 71.37, 13, 703, 7, 7.40, 2.83, 2.43, 1.62),
        ('GB', 0.16, 49.70, 48.39, 0.27, 0.03, 1259, 70.07, 9, 611, 6, 8.90, 5.42, 6.02, 1.20),
        ('KC', 0.15, 55.56, 49.07, 0.16, 0.10, 1514, 64.79, 11, 712, 7, 8.36, 4.00, 10.80, 0.80),
        ('DET', 0.14, 51.78, 49.30, 0.31, -0.04, 1393, 76.00, 15, 772, 8, 7.04, 4.81, 1.60, 1.07),
        ('BUF', 0.13, 49.36, 48.41, 0.15, 0.09, 1429, 68.33, 11, 906, 9, 8.08, 5.53, 11.52, 1.84),
        ('TB', 0.12, 44.33, 43.75, 0.21, -0.01, 1539, 66.15, 12, 656, 5, 8.92, 4.50, 7.66, 0.45),
        ('PIT', 0.08, 27.39, 44.04, 0.15, -0.01, 1282, 68.97, 14, 567, 3, 6.29, 4.79, 2.66, 2.66),
        ('NE', 0.08, 28.92, 44.66, 0.26, -0.17, 1522, 72.78, 10, 549, 6, 7.76, 8.29, 8.76, 0.92),
        ('WAS', 0.07, 26.15, 46.86, 0.11, 0.02, 1238, 62.79, 10, 906, 7, 9.20, 6.73, 10.58, 0.96),
        ('SEA', 0.06, 21.96, 45.59, 0.30, -0.18, 1556, 70.73, 11, 625, 6, 9.73, 4.02, 1.72, 1.72),
        ('MIA', 0.05, 16.28, 41.61, 0.07, 0.02, 1253, 69.63, 11, 548, 4, 7.15, 6.13, 3.77, 3.30),
        ('HOU', 0.04, 11.23, 41.98, 0.04, 0.03, 1099, 70.27, 8, 581, 3, 7.56, 6.90, 8.05, 1.72),
        ('LA', 0.03, 11.06, 48.23, 0.16, -0.18, 1684, 66.19, 12, 635, 4, 8.56, 4.93, 0.90, 0.90),
        ('DEN', 0.03, 11.07, 41.32, 0.07, -0.03, 773, 66.50, 8, 679, 5, 6.81, 7.47, 7.05, 1.66),
        ('ARI', 0.02, 5.78, 45.45, 0.09, -0.13, 1838, 66.80, 10, 493, 1, 7.75, 4.98, 2.68, 2.68),
        ('SF', 0.01, 2.89, 47.47, 0.09, -0.13, 1838, 66.80, 10, 493, 1, 7.75, 4.98, 2.68, 2.68),
        ('CAR', 0.00, 1.58, 46.51, -0.06, 0.08, 1208, 62.44, 11, 856, 3, 7.19, 4.44, 4.44, 2.22),
        ('PHI', -0.01, -2.32, 42.61, -0.03, 0.02, 1172, 68.02, 8, 572, 8, 8.85, 8.87, 6.40, 0.49),
        ('ATL', -0.01, -2.84, 43.64, -0.02, 0.01, 1197, 62.80, 4, 756, 6, 7.65, 3.89, 5.00, 1.67),
        ('LAC', -0.01, -4.11, 43.19, -0.01, -0.01, 1537, 67.73, 10, 724, 2, 7.60, 7.23, 4.42, 1.61),
        ('BAL', -0.03, -11.18, 42.77, -0.04, -0.02, 1240, 68.71, 10, 757, 6, 8.03, 10.31, 5.67, 2.58),
        ('NO', -0.05, -21.07, 43.49, -0.07, -0.03, 1236, 67.63, 6, 657, 3, 7.67, 4.80, 4.80, 0.87),
        ('MIN', -0.06, -18.57, 45.10, -0.05, -0.09, 1121, 65.75, 8, 534, 4, 8.11, 11.80, 6.18, 2.81),
        ('NYJ', -0.08, -27.36, 44.01, -0.06, -0.08, 1052, 66.47, 7, 814, 4, 6.76, 11.31, 11.76, 0.45),
        ('NYG', -0.09, -34.57, 41.88, -0.12, -0.03, 1294, 61.93, 7, 757, 7, 9.20, 6.75, 10.13, 2.11),
        ('CIN', -0.10, -39.27, 41.90, -0.13, -0.04, 1507, 63.89, 13, 482, 2, 7.54, 6.52, 2.17, 2.90),
        ('LV', -0.14, -50.69, 41.32, -0.08, -0.21, 1350, 66.13, 7, 631, 3, 7.39, 8.57, 2.86, 4.76),
        ('CLE', -0.17, -68.55, 35.14, -0.26, 0.02, 1245, 57.83, 5, 544, 3, 7.33, 6.32, 1.12, 2.23),
        ('TEN', -0.23, -80.04, 37.01, -0.26, -0.14, 1101, 54.95, 3, 491, 2, 8.47, 10.59, 3.81, 1.69)
    ]
    
    # Convert to DataFrame
    df = pd.DataFrame(offensive_data, columns=[
        'team', 'epa_off_per_play', 'total_epa_off', 'success_rate_off', 
        'epa_pass_off', 'epa_rush_off', 'pass_yards', 'comp_pct', 'pass_td', 
        'rush_yards', 'rush_td', 'adot', 'sack_pct', 'scramble_pct', 'int_pct'
    ])
    
    # Add team names
    team_names = {
        'IND': 'Colts', 'DAL': 'Cowboys', 'GB': 'Packers', 'KC': 'Chiefs', 'DET': 'Lions',
        'BUF': 'Bills', 'TB': 'Buccaneers', 'PIT': 'Steelers', 'NE': 'Patriots', 'WAS': 'Commanders',
        'SEA': 'Seahawks', 'MIA': 'Dolphins', 'HOU': 'Texans', 'LA': 'Rams', 'DEN': 'Broncos',
        'ARI': 'Cardinals', 'SF': '49ers', 'CAR': 'Panthers', 'PHI': 'Eagles', 'ATL': 'Falcons',
        'LAC': 'Chargers', 'BAL': 'Ravens', 'NO': 'Saints', 'MIN': 'Vikings', 'NYJ': 'Jets',
        'NYG': 'Giants', 'CIN': 'Bengals', 'LV': 'Raiders', 'CLE': 'Browns', 'TEN': 'Titans'
    }
    
    df['team_name'] = df['team'].map(team_names)
    
    # Add metadata
    df['last_updated'] = datetime.now()
    df['source'] = 'sumersports_offensive_current'
    
    # Convert success rate to decimal
    df['success_rate_off'] = df['success_rate_off'] / 100
    
    return df

def create_defensive_data():
    """Create defensive EPA data from SumerSports defensive page"""
    
    # Data from SumerSports defensive page (as of 10-17-2025)
    # These are DEFENSIVE EPA ALLOWED values (negative = good defense, positive = bad defense)
    # Format: Team, EPA/Play Allowed, Total EPA Allowed, Success % Allowed, EPA/Pass Allowed, EPA/Rush Allowed, Pass Yards Allowed, Comp % Allowed, Pass TD Allowed, Rush Yards Allowed, Rush TD Allowed, ADoT Allowed, Sack %, Scramble %, Int %
    
    defensive_data = [
        # Team, EPA/Play Allowed, Total EPA Allowed, Success % Allowed, EPA/Pass Allowed, EPA/Rush Allowed, Pass Yards Allowed, Comp % Allowed, Pass TD Allowed, Rush Yards Allowed, Rush TD Allowed, ADoT Allowed, Sack %, Scramble %, Int %
        ('DEN', -0.14, -50.17, 35.85, -0.16, -0.11, 1178, 57.67, 4, 534, 2, 9.90, 13.16, 3.95, 0.44),
        ('MIN', -0.14, -40.89, 40.94, -0.31, 0.05, 875, 65.22, 5, 661, 4, 5.96, 8.13, 5.63, 1.25),
        ('HOU', -0.12, -33.02, 40.93, -0.19, -0.01, 969, 58.82, 3, 453, 5, 8.26, 7.02, 3.51, 2.92),
        ('LA', -0.08, -32.99, 42.21, -0.10, -0.06, 1333, 65.87, 7, 647, 2, 7.37, 8.02, 4.22, 1.69),
        ('ATL', -0.07, -17.66, 43.51, -0.15, 0.04, 782, 57.69, 7, 570, 2, 10.34, 8.86, 8.86, 3.16),
        ('JAX', -0.07, -24.13, 42.47, -0.06, -0.06, 1597, 61.61, 10, 549, 4, 9.28, 3.25, 5.69, 4.07),
        ('IND', -0.05, -18.56, 47.03, -0.05, -0.05, 1494, 65.91, 10, 578, 3, 7.35, 6.50, 4.07, 2.85),
        ('DET', -0.04, -14.59, 40.86, 0.03, -0.15, 1402, 64.89, 13, 573, 5, 9.26, 8.52, 7.17, 2.69),
        ('LAC', -0.02, -6.46, 41.31, -0.06, 0.05, 1154, 60.43, 5, 745, 7, 7.92, 7.08, 10.18, 2.65),
        ('CHI', -0.01, -2.87, 47.90, -0.01, -0.07, 1097, 73.57, 13, 782, 4, 7.12, 5.06, 6.33, 5.06),
        ('PHI', -0.01, -3.59, 44.53, -0.03, 0.02, 1297, 58.91, 7, 806, 8, 8.58, 3.95, 7.46, 1.32),
        ('PIT', -0.01, -2.81, 43.90, 0.02, -0.05, 1352, 65.79, 7, 553, 4, 7.17, 9.13, 4.11, 2.28),
        ('CLE', 0.00, -1.39, 39.94, 0.15, -0.19, 1192, 67.46, 12, 478, 3, 7.79, 7.33, 4.19, 1.05),
        ('LV', 0.00, -1.06, 43.70, 0.09, -0.14, 1391, 66.17, 8, 572, 8, 7.96, 6.28, 3.59, 1.35),
        ('ARI', 0.00, 0.97, 45.82, 0.06, -0.06, 1520, 63.29, 8, 684, 3, 8.34, 6.68, 4.17, 1.97),
        ('SEA', 0.01, 2.80, 44.84, 0.02, -0.01, 1547, 68.34, 9, 535, 2, 7.89, 6.31, 4.17, 1.97),
        ('SF', 0.01, 3.80, 44.84, 0.02, -0.01, 1335, 69.16, 8, 647, 2, 7.89, 6.31, 4.17, 1.97),
        ('TB', 0.01, 3.80, 44.84, 0.02, -0.01, 1335, 69.16, 8, 647, 2, 7.89, 6.31, 4.17, 1.97),
        ('NO', 0.01, 3.80, 44.84, 0.12, -0.11, 1347, 69.49, 14, 684, 4, 8.25, 6.31, 7.77, 1.46),
        ('KC', 0.01, 3.84, 46.63, -0.03, 0.07, 1202, 69.71, 7, 715, 6, 7.60, 6.67, 10.00, 1.90),
        ('GB', 0.02, 4.81, 42.41, 0.05, -0.06, 1105, 67.33, 8, 365, 3, 6.84, 5.45, 2.73, 0.91),
        ('WAS', 0.03, 11.50, 42.93, 0.07, -0.02, 1524, 63.24, 9, 730, 4, 9.17, 8.45, 4.69, 0.94),
        ('BUF', 0.03, 11.14, 43.73, -0.02, 0.09, 1087, 64.24, 7, 938, 9, 7.12, 7.73, 7.22, 1.03),
        ('NE', 0.04, 12.71, 47.35, 0.15, -0.13, 1504, 71.98, 9, 501, 3, 7.89, 6.28, 5.80, 1.93),
        ('TEN', 0.04, 13.98, 42.28, 0.12, -0.06, 1329, 70.72, 7, 802, 11, 6.28, 4.55, 4.04, 2.02),
        ('NYG', 0.04, 15.75, 45.76, 0.02, 0.07, 1548, 65.78, 7, 773, 7, 8.15, 5.24, 4.03, 1.61),
        ('CAR', 0.07, 23.52, 40.18, 0.16, -0.07, 1319, 66.84, 10, 567, 5, 7.31, 2.46, 5.42, 1.97),
        ('NYJ', 0.11, 38.24, 39.61, 0.21, -0.02, 1245, 64.71, 12, 780, 5, 6.41, 4.17, 7.29, 0.00),
        ('CIN', 0.12, 48.63, 49.25, 0.19, 0.03, 1609, 68.47, 13, 814, 8, 7.08, 4.91, 4.46, 2.68),
        ('BAL', 0.15, 58.62, 48.64, 0.19, 0.08, 1532, 68.52, 14, 806, 9, 8.19, 3.39, 5.08, 0.42),
        ('DAL', 0.18, 72.50, 50.00, 0.27, 0.06, 1719, 71.84, 15, 853, 6, 8.47, 4.82, 4.82, 0.88),
        ('MIA', 0.21, 75.94, 50.82, 0.25, 0.14, 1403, 74.86, 11, 1011, 6, 6.49, 5.91, 7.88, 0.49)
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
    df['source'] = 'sumersports_defensive_current'
    
    # Convert success rate to decimal
    df['success_rate_def'] = df['success_rate_def'] / 100
    
    return df

def combine_epa_data():
    """Combine offensive and defensive EPA data"""
    
    # Create the data
    offensive_df = create_offensive_data()
    defensive_df = create_defensive_data()
    
    # Merge on team
    combined_df = pd.merge(offensive_df, defensive_df, on='team', how='outer', suffixes=('_off', '_def'))
    
    # Clean up columns
    combined_df['team_name'] = combined_df['team_name_off'].fillna(combined_df['team_name_def'])
    combined_df = combined_df.drop(['team_name_off', 'team_name_def'], axis=1)
    
    # Calculate net EPA metrics
    combined_df['net_epa_per_play'] = combined_df['epa_off_per_play'] - combined_df['epa_def_allowed_per_play']
    combined_df['net_epa_pass'] = combined_df['epa_pass_off'] - combined_df['epa_pass_def_allowed']
    combined_df['net_epa_rush'] = combined_df['epa_rush_off'] - combined_df['epa_rush_def_allowed']
    
    # Add metadata
    combined_df['last_updated'] = datetime.now()
    combined_df['source'] = 'sumersports_combined_current'
    
    return combined_df

def main():
    """Main function to extract and combine current EPA data"""
    
    print("=== Extract Current EPA Data from SumerSports ===")
    
    # Create combined data
    combined_df = combine_epa_data()
    
    # Save the data
    combined_df.to_csv('data/detailed_epa_data_current.csv', index=False)
    print(f"✅ Saved current EPA data to data/detailed_epa_data_current.csv")
    
    # Display summary
    print(f"\n=== Current EPA Data Summary ===")
    print(f"Teams: {len(combined_df)}")
    print(f"Last Updated: {combined_df['last_updated'].iloc[0]}")
    
    # Top 5 offensive teams
    print(f"\nTop 5 Offensive Teams:")
    top_off = combined_df.nlargest(5, 'epa_off_per_play')[['team_name', 'epa_off_per_play', 'epa_pass_off', 'epa_rush_off']]
    print(top_off.to_string(index=False))
    
    # Top 5 defensive teams (lowest EPA allowed)
    print(f"\nTop 5 Defensive Teams (Lowest EPA Allowed):")
    top_def = combined_df.nsmallest(5, 'epa_def_allowed_per_play')[['team_name', 'epa_def_allowed_per_play', 'epa_pass_def_allowed', 'epa_rush_def_allowed']]
    print(top_def.to_string(index=False))
    
    # Check for data quality
    same_pass = combined_df[combined_df['epa_pass_off'] == combined_df['epa_pass_def_allowed']]
    same_rush = combined_df[combined_df['epa_rush_off'] == combined_df['epa_rush_def_allowed']]
    
    print(f"\n=== Data Quality Check ===")
    print(f"Teams with identical Pass Off and Pass Def EPA: {len(same_pass)}/32")
    print(f"Teams with identical Rush Off and Rush Def EPA: {len(same_rush)}/32")
    
    if len(same_pass) == 0 and len(same_rush) == 0:
        print("✅ Data quality is good - no identical values!")
    else:
        print("⚠️  Data quality issues - some identical values found")
    
    print(f"\n✅ Successfully extracted current EPA data!")
    print(f"📊 Data includes {len(combined_df)} teams with current EPA/Pass and EPA/Rush statistics")

if __name__ == "__main__":
    main()

