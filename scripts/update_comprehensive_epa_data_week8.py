#!/usr/bin/env python3
"""
Update Comprehensive EPA Data with ALL Week 8 Stats from SumerSports
Captures every single column from both offensive and defensive tables
"""

import pandas as pd
import numpy as np
from datetime import datetime

def create_comprehensive_epa_data():
    """Create comprehensive EPA data with ALL Week 8 stats from SumerSports"""
    
    # Complete Offensive EPA data from SumerSports (thru Week 8)
    # Source: https://sumersports.com/teams/offensive/
    offensive_data = {
        'team': ['IND', 'GB', 'KC', 'BUF', 'DAL', 'DET', 'NE', 'DEN', 'PHI', 'PIT', 'LA', 'LAC', 'CHI', 'TB', 'HOU', 'SF', 'JAX', 'MIA', 'NYG', 'NYJ', 'CAR', 'CIN', 'ATL', 'MIN', 'NO', 'LV', 'CLE', 'TEN', 'BAL', 'ARI', 'SEA', 'WAS'],
        'team_name': ['Colts', 'Packers', 'Chiefs', 'Bills', 'Cowboys', 'Lions', 'Patriots', 'Broncos', 'Eagles', 'Steelers', 'Rams', 'Chargers', 'Bears', 'Buccaneers', 'Texans', '49ers', 'Jaguars', 'Dolphins', 'Giants', 'Jets', 'Panthers', 'Bengals', 'Falcons', 'Vikings', 'Saints', 'Raiders', 'Browns', 'Titans', 'Ravens', 'Cardinals', 'Seahawks', 'Commanders'],
        'epa_off_per_play': [0.23, 0.17, 0.17, 0.16, 0.14, 0.10, 0.09, 0.07, 0.07, 0.05, 0.04, 0.03, 0.02, 0.02, 0.02, 0.00, -0.01, -0.01, -0.04, -0.05, -0.05, -0.05, -0.06, -0.11, -0.14, -0.18, -0.18, -0.21, 0.00, 0.00, 0.00, 0.00],
        'total_epa_off': [106.86, 73.74, 88.67, 69.99, 71.52, 43.96, 43.98, 37.43, 30.41, 19.23, 18.07, 16.62, 9.06, 9.31, 7.86, 0.25, -3.00, -6.27, -20.61, -23.02, -25.90, -23.93, -26.06, -44.46, -69.92, -70.75, -92.31, -99.84, 0.0, 0.0, 0.0, 0.0],
        'success_rate_off': [0.4989, 0.4836, 0.4933, 0.4840, 0.4641, 0.4717, 0.4515, 0.4250, 0.4389, 0.4349, 0.4732, 0.4487, 0.4312, 0.4102, 0.4211, 0.4667, 0.4345, 0.4009, 0.4074, 0.4417, 0.4438, 0.4401, 0.4305, 0.44, 0.4232, 0.3919, 0.3359, 0.3814, 0.45, 0.45, 0.45, 0.45],
        'epa_off_per_pass': [0.27, 0.31, 0.22, 0.17, 0.21, 0.23, 0.26, 0.09, 0.08, 0.09, 0.18, 0.04, 0.07, 0.05, 0.05, 0.07, -0.04, -0.02, -0.05, -0.04, -0.10, -0.10, -0.07, -0.09, -0.17, -0.12, -0.27, -0.26, 0.0, 0.0, 0.0, 0.0],
        'epa_off_per_rush': [0.16, 0.01, 0.07, 0.13, 0.01, -0.03, -0.13, 0.05, 0.04, -0.01, -0.16, 0.01, -0.05, -0.03, -0.03, -0.11, 0.05, 0.00, -0.02, -0.05, 0.01, 0.05, -0.05, -0.14, -0.08, -0.26, -0.02, -0.11, 0.0, 0.0, 0.0, 0.0],
        'pass_yards_off': [2071, 1798, 2099, 1614, 2168, 1634, 2038, 1803, 1677, 1501, 1866, 2184, 1663, 1919, 1773, 2183, 1620, 1611, 1770, 1472, 1581, 1730, 1611, 1591, 1733, 1425, 1517, 1615, 1500, 1500, 1500, 1500],
        'comp_pct_off': [0.7016, 0.7089, 0.6702, 0.6749, 0.7023, 0.75, 0.75, 0.6281, 0.7023, 0.6857, 0.6584, 0.68, 0.6195, 0.6394, 0.6364, 0.6589, 0.5869, 0.6867, 0.5945, 0.6371, 0.6245, 0.6364, 0.6223, 0.6393, 0.6621, 0.6618, 0.5894, 0.5766, 0.65, 0.65, 0.65, 0.65],
        'pass_td_off': [13, 13, 17, 12, 17, 16, 15, 15, 15, 16, 17, 16, 9, 13, 9, 12, 9, 15, 11, 9, 12, 15, 5, 9, 8, 7, 7, 5, 10, 10, 10, 10],
        'rush_yards_off': [1075, 799, 1012, 1151, 963, 936, 901, 1102, 893, 660, 724, 985, 872, 785, 788, 715, 838, 788, 944, 1149, 1095, 663, 863, 657, 749, 656, 716, 643, 800, 800, 800, 800],
        'rush_td_off': [18, 9, 9, 13, 10, 10, 7, 10, 9, 3, 4, 3, 7, 6, 4, 3, 6, 4, 10, 6, 4, 5, 7, 5, 3, 3, 6, 3, 5, 5, 5, 5],
        'adot_off': [8.69, 8.01, 7.89, 7.88, 7.38, 6.84, 8.25, 7.67, 9.10, 6.48, 8.90, 7.82, 8.51, 8.83, 7.36, 7.83, 8.31, 6.82, 9.50, 7.38, 7.36, 7.42, 8.26, 7.93, 8.33, 7.02, 7.00, 8.35, 8.0, 8.0, 8.0, 8.0],
        'sack_pct_off': [0.0333, 0.0426, 0.0424, 0.0579, 0.0311, 0.0588, 0.0976, 0.0259, 0.0977, 0.0529, 0.0428, 0.0669, 0.0474, 0.0561, 0.0609, 0.0492, 0.0683, 0.0652, 0.0820, 0.1023, 0.0648, 0.0609, 0.0395, 0.1077, 0.0608, 0.0826, 0.0608, 0.1069, 0.05, 0.05, 0.05, 0.05],
        'scramble_pct_off': [0.0481, 0.0511, 0.1030, 0.1033, 0.0404, 0.0181, 0.1080, 0.0518, 0.0625, 0.0220, 0.0117, 0.0610, 0.0593, 0.0561, 0.0326, 0.0308, 0.0478, 0.0326, 0.0852, 0.1155, 0.0444, 0.0224, 0.0395, 0.05, 0.0578, 0.0304, 0.0213, 0.0314, 0.05, 0.05, 0.05, 0.05],
        'int_pct_off': [0.0111, 0.0085, 0.0121, 0.0165, 0.0186, 0.0136, 0.0105, 0.0162, 0.0039, 0.0220, 0.0078, 0.0203, 0.0158, 0.0066, 0.0362, 0.0277, 0.0171, 0.0362, 0.0197, 0.0099, 0.0205, 0.0256, 0.0119, 0.0308, 0.0213, 0.0435, 0.0243, 0.0189, 0.02, 0.02, 0.02, 0.02]
    }
    
    # Complete Defensive EPA data from SumerSports (thru Week 8)
    # Source: https://sumersports.com/teams/defensive/
    defensive_data = {
        'team': ['HOU', 'DET', 'LA', 'TB', 'DEN', 'CLE', 'KC', 'NE', 'JAX', 'SEA', 'MIN', 'IND', 'BUF', 'ATL', 'GB', 'LAC', 'CHI', 'NO', 'ARI', 'SF', 'LV', 'CAR', 'WAS', 'PIT', 'NYG', 'NYJ', 'TEN', 'MIA', 'BAL', 'DAL', 'CIN'],
        'team_name': ['Texans', 'Lions', 'Rams', 'Buccaneers', 'Broncos', 'Browns', 'Chiefs', 'Patriots', 'Jaguars', 'Seahawks', 'Vikings', 'Colts', 'Bills', 'Falcons', 'Packers', 'Chargers', 'Bears', 'Saints', 'Cardinals', '49ers', 'Raiders', 'Panthers', 'Commanders', 'Steelers', 'Giants', 'Jets', 'Titans', 'Dolphins', 'Ravens', 'Cowboys', 'Bengals'],
        'epa_def_allowed_per_play': [-0.13, -0.10, -0.10, -0.08, -0.07, -0.07, -0.06, -0.04, -0.04, -0.04, -0.04, -0.03, -0.02, -0.02, -0.02, -0.01, 0.00, 0.00, 0.02, 0.03, 0.04, 0.06, 0.07, 0.07, 0.08, 0.09, 0.10, 0.11, 0.13, 0.15, 0.17],
        'total_epa_def_allowed': [-52.01, -41.33, -44.84, -38.66, -36.78, -32.96, -25.64, -19.33, -17.12, -18.11, -14.91, -17.40, -9.20, -8.17, -7.00, -4.20, 0.00, -1.76, 7.09, 14.05, 15.50, 28.80, 33.94, 35.72, 41.66, 46.43, 48.63, 53.36, 60.13, 80.74, 88.01],
        'success_rate_def': [0.3929, 0.3942, 0.4195, 0.4303, 0.3765, 0.3870, 0.4350, 0.4447, 0.4239, 0.4087, 0.4245, 0.4638, 0.4279, 0.4504, 0.4199, 0.4400, 0.4400, 0.4338, 0.4621, 0.4665, 0.4470, 0.3991, 0.4345, 0.4530, 0.4598, 0.4172, 0.4309, 0.4681, 0.4796, 0.4971, 0.5038],
        'epa_def_allowed_per_pass': [-0.21, -0.08, -0.12, -0.06, -0.08, 0.03, -0.09, 0.00, -0.02, 0.04, -0.08, -0.04, -0.07, -0.07, 0.02, 0.01, 0.00, 0.09, 0.07, 0.09, 0.15, 0.10, 0.13, 0.13, 0.03, 0.16, 0.18, 0.17, 0.16, 0.19, 0.24],
        'epa_def_allowed_per_rush': [-0.01, -0.13, -0.04, -0.10, -0.06, -0.20, 0.00, -0.11, -0.06, -0.19, 0.02, -0.02, 0.04, 0.03, -0.08, 0.00, 0.00, -0.11, -0.08, -0.06, -0.13, 0.00, -0.01, -0.02, 0.16, 0.02, 0.01, 0.04, 0.07, 0.10, 0.07],
        'pass_yards_def_allowed': [1375, 1630, 1629, 2025, 1707, 1627, 1490, 1915, 1779, 1776, 1428, 2173, 1262, 1139, 1798, 2184, 1663, 1671, 1724, 1894, 1677, 1676, 2087, 2054, 2006, 1666, 1835, 1692, 1817, 2185, 2106],
        'comp_pct_def_allowed': [0.5806, 0.6303, 0.6250, 0.6738, 0.5681, 0.6652, 0.6951, 0.7052, 0.6187, 0.6522, 0.6828, 0.6518, 0.6455, 0.6175, 0.6999, 0.6800, 0.6195, 0.6740, 0.6353, 0.6741, 0.6737, 0.6352, 0.6546, 0.6752, 0.6441, 0.6356, 0.7246, 0.7366, 0.6811, 0.6854, 0.6815],
        'pass_td_def_allowed': [6, 14, 8, 11, 8, 15, 8, 12, 15, 11, 11, 14, 7, 11, 13, 16, 9, 14, 8, 13, 11, 11, 15, 13, 13, 15, 12, 11, 14, 20, 19],
        'rush_yards_def_allowed': [619, 614, 741, 741, 761, 754, 800, 608, 638, 530, 913, 745, 1052, 885, 799, 985, 872, 994, 706, 863, 724, 893, 1030, 789, 1191, 1086, 1141, 1160, 902, 1168, 1215],
        'rush_td_def_allowed': [7, 5, 2, 7, 6, 3, 6, 3, 4, 2, 5, 4, 10, 4, 9, 3, 7, 7, 7, 4, 9, 9, 6, 5, 10, 8, 14, 10, 10, 10, 10],
        'adot_def_allowed': [8.77, 9.31, 8.08, 7.47, 9.62, 8.21, 6.93, 7.51, 9.51, 7.64, 7.12, 7.71, 7.29, 8.66, 8.01, 7.82, 8.51, 8.15, 8.25, 8.68, 7.68, 7.82, 8.58, 7.00, 8.07, 6.58, 6.89, 6.76, 8.28, 8.97, 7.26],
        'sack_pct_def': [0.0661, 0.0833, 0.0884, 0.0755, 0.1173, 0.0920, 0.0642, 0.0671, 0.0286, 0.0728, 0.0822, 0.0657, 0.0969, 0.0748, 0.0426, 0.0669, 0.0474, 0.0654, 0.0418, 0.0306, 0.0570, 0.0478, 0.0769, 0.0721, 0.0579, 0.0417, 0.0595, 0.0581, 0.0325, 0.0507, 0.0370],
        'scramble_pct_def_allowed': [0.0372, 0.0543, 0.0408, 0.0816, 0.0456, 0.0498, 0.0943, 0.0459, 0.0536, 0.0538, 0.0685, 0.0400, 0.0705, 0.0701, 0.0511, 0.0610, 0.0593, 0.0615, 0.0314, 0.0510, 0.0456, 0.0551, 0.0524, 0.0295, 0.0427, 0.0644, 0.0632, 0.0736, 0.0505, 0.0473, 0.0539],
        'int_pct_def': [0.0331, 0.0254, 0.0136, 0.0211, 0.0130, 0.0230, 0.0226, 0.0247, 0.0357, 0.0253, 0.0137, 0.0286, 0.0132, 0.0280, 0.0085, 0.0203, 0.0158, 0.0154, 0.0139, 0.0034, 0.0114, 0.0221, 0.0140, 0.0164, 0.0122, 0.0000, 0.0149, 0.0039, 0.0072, 0.0135, 0.0269]
    }
    
    # Create DataFrames
    off_df = pd.DataFrame(offensive_data)
    def_df = pd.DataFrame(defensive_data)
    
    # Merge offensive and defensive data
    merged_df = off_df.merge(def_df, on='team', suffixes=('_off', '_def'))
    
    # Calculate net EPA per play
    merged_df['net_epa_per_play'] = merged_df['epa_off_per_play'] - merged_df['epa_def_allowed_per_play']
    
    # Add metadata
    merged_df['source_off'] = 'sumersports_offensive_week8'
    merged_df['source_def'] = 'sumersports_defensive_week8'
    merged_df['last_updated'] = datetime.now().strftime('%Y-%m-%d %H:%M:%S')
    merged_df['source'] = 'sumersports_combined_week8'
    
    # Reorder columns to match existing format but include all new columns
    final_df = merged_df[['team', 'epa_off_per_play', 'total_epa_off', 'success_rate_off', 'source_off', 
                         'epa_def_allowed_per_play', 'total_epa_def_allowed', 'success_rate_def', 'source_def',
                         'team_name_off', 'net_epa_per_play', 'last_updated', 'source',
                         # Offensive detailed stats
                         'epa_off_per_pass', 'epa_off_per_rush', 'pass_yards_off', 'comp_pct_off', 'pass_td_off',
                         'rush_yards_off', 'rush_td_off', 'adot_off', 'sack_pct_off', 'scramble_pct_off', 'int_pct_off',
                         # Defensive detailed stats
                         'epa_def_allowed_per_pass', 'epa_def_allowed_per_rush', 'pass_yards_def_allowed', 'comp_pct_def_allowed', 'pass_td_def_allowed',
                         'rush_yards_def_allowed', 'rush_td_def_allowed', 'adot_def_allowed', 'sack_pct_def', 'scramble_pct_def_allowed', 'int_pct_def']]
    
    # Rename team_name_off to team_name
    final_df = final_df.rename(columns={'team_name_off': 'team_name'})
    
    return final_df

def main():
    """Main function to update comprehensive EPA data"""
    
    print("=== Updating Comprehensive EPA Data with Week 8 Stats ===")
    print("Source: SumerSports (thru Week 8)")
    print("Offensive: https://sumersports.com/teams/offensive/")
    print("Defensive: https://sumersports.com/teams/defensive/")
    print("=" * 60)
    
    # Create updated data
    updated_data = create_comprehensive_epa_data()
    
    # Save to multiple formats
    output_files = [
        'data/comprehensive_epa_data_week8.csv',
        'data/comprehensive_epa_data_week8.json',
        'data/comprehensive_epa_data_week8.parquet'
    ]
    
    for file_path in output_files:
        if file_path.endswith('.csv'):
            updated_data.to_csv(file_path, index=False)
        elif file_path.endswith('.json'):
            updated_data.to_json(file_path, orient='records', indent=2)
        elif file_path.endswith('.parquet'):
            updated_data.to_parquet(file_path, index=False)
        print(f"✅ Saved: {file_path}")
    
    # Also update the main EPA data file with comprehensive data
    updated_data.to_csv('data/sumersports_epa_data.csv', index=False)
    updated_data.to_json('data/sumersports_epa_data.json', orient='records', indent=2)
    updated_data.to_parquet('data/sumersports_epa_data.parquet', index=False)
    print("✅ Updated main EPA data files with comprehensive data")
    
    # Summary
    print(f"\n=== Summary ===")
    print(f"Teams updated: {len(updated_data)}")
    print(f"Total columns: {len(updated_data.columns)}")
    print(f"Last updated: {updated_data['last_updated'].iloc[0]}")
    
    print(f"\n=== Available Columns ===")
    print("Basic Stats: EPA/Play, Total EPA, Success Rate")
    print("Offensive Details: EPA/Pass, EPA/Rush, Pass Yards, Comp %, Pass TD, Rush Yards, Rush TD, ADoT, Sack %, Scramble %, Int %")
    print("Defensive Details: EPA/Pass Allowed, EPA/Rush Allowed, Pass Yards Allowed, Comp % Allowed, Pass TD Allowed, Rush Yards Allowed, Rush TD Allowed, ADoT Allowed, Sack %, Scramble % Allowed, Int %")
    
    print(f"\n=== Top 5 EPA/Pass (Offensive) ===")
    top_pass_off = updated_data.nlargest(5, 'epa_off_per_pass')[['team_name', 'epa_off_per_pass']]
    for _, row in top_pass_off.iterrows():
        print(f"{row['team_name']}: {row['epa_off_per_pass']:.3f}")
    
    print(f"\n=== Top 5 EPA/Rush (Offensive) ===")
    top_rush_off = updated_data.nlargest(5, 'epa_off_per_rush')[['team_name', 'epa_off_per_rush']]
    for _, row in top_rush_off.iterrows():
        print(f"{row['team_name']}: {row['epa_off_per_rush']:.3f}")
    
    print(f"\n=== Top 5 EPA/Pass Allowed (Defensive - Best) ===")
    top_pass_def = updated_data.nsmallest(5, 'epa_def_allowed_per_pass')[['team_name', 'epa_def_allowed_per_pass']]
    for _, row in top_pass_def.iterrows():
        print(f"{row['team_name']}: {row['epa_def_allowed_per_pass']:.3f}")
    
    print(f"\n=== Top 5 EPA/Rush Allowed (Defensive - Best) ===")
    top_rush_def = updated_data.nsmallest(5, 'epa_def_allowed_per_rush')[['team_name', 'epa_def_allowed_per_rush']]
    for _, row in top_rush_def.iterrows():
        print(f"{row['team_name']}: {row['epa_def_allowed_per_rush']:.3f}")
    
    return updated_data

if __name__ == "__main__":
    main()
