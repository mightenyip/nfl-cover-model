#!/usr/bin/env python3
"""
Update EPA Data with Week 8 Stats from SumerSports
Complete data from both offensive and defensive pages
"""

import pandas as pd
import numpy as np
from datetime import datetime

def create_updated_epa_data():
    """Create updated EPA data with Week 8 stats from SumerSports"""
    
    # Offensive EPA data from SumerSports (thru Week 8)
    offensive_data = {
        'team': ['IND', 'GB', 'KC', 'BUF', 'DAL', 'DET', 'NE', 'DEN', 'PHI', 'PIT', 'LA', 'LAC', 'CHI', 'TB', 'HOU', 'SF', 'JAX', 'MIA', 'NYG', 'NYJ', 'CAR', 'CIN', 'ATL', 'MIN', 'NO', 'LV', 'CLE', 'TEN'],
        'team_name': ['Colts', 'Packers', 'Chiefs', 'Bills', 'Cowboys', 'Lions', 'Patriots', 'Broncos', 'Eagles', 'Steelers', 'Rams', 'Chargers', 'Bears', 'Buccaneers', 'Texans', '49ers', 'Jaguars', 'Dolphins', 'Giants', 'Jets', 'Panthers', 'Bengals', 'Falcons', 'Vikings', 'Saints', 'Raiders', 'Browns', 'Titans'],
        'epa_off_per_play': [0.23, 0.17, 0.17, 0.16, 0.14, 0.10, 0.09, 0.07, 0.07, 0.05, 0.04, 0.03, 0.02, 0.02, 0.02, 0.00, -0.01, -0.01, -0.04, -0.05, -0.05, -0.05, -0.06, -0.11, -0.14, -0.18, -0.18, -0.21],
        'total_epa_off': [106.86, 73.74, 88.67, 69.99, 71.52, 43.96, 43.98, 37.43, 30.41, 19.23, 18.07, 16.62, 9.06, 9.31, 7.86, 0.25, -3.00, -6.27, -20.61, -23.02, -25.90, -23.93, -26.06, -44.46, -69.92, -70.75, -92.31, -99.84],
        'success_rate_off': [0.4989, 0.4836, 0.4933, 0.4840, 0.4641, 0.4717, 0.4515, 0.4250, 0.4389, 0.4349, 0.4732, 0.4487, 0.4312, 0.4102, 0.4211, 0.4667, 0.4345, 0.4009, 0.4074, 0.4417, 0.4438, 0.4401, 0.4305, 0.44, 0.4232, 0.3919, 0.3359, 0.3814]
    }
    
    # Defensive EPA data from SumerSports (thru Week 8) - Note: These are EPA ALLOWED (negative is good)
    defensive_data = {
        'team': ['HOU', 'DET', 'LA', 'TB', 'DEN', 'CLE', 'KC', 'NE', 'JAX', 'SEA', 'MIN', 'IND', 'BUF', 'ATL', 'GB', 'LAC', 'CHI', 'NO', 'ARI', 'SF', 'LV', 'CAR', 'WAS', 'PIT', 'NYG', 'NYJ', 'TEN', 'MIA', 'BAL', 'DAL', 'CIN'],
        'team_name': ['Texans', 'Lions', 'Rams', 'Buccaneers', 'Broncos', 'Browns', 'Chiefs', 'Patriots', 'Jaguars', 'Seahawks', 'Vikings', 'Colts', 'Bills', 'Falcons', 'Packers', 'Chargers', 'Bears', 'Saints', 'Cardinals', '49ers', 'Raiders', 'Panthers', 'Commanders', 'Steelers', 'Giants', 'Jets', 'Titans', 'Dolphins', 'Ravens', 'Cowboys', 'Bengals'],
        'epa_def_allowed_per_play': [-0.13, -0.10, -0.10, -0.08, -0.07, -0.07, -0.06, -0.04, -0.04, -0.04, -0.04, -0.03, -0.02, -0.02, -0.02, -0.01, 0.00, 0.00, 0.02, 0.03, 0.04, 0.06, 0.07, 0.07, 0.08, 0.09, 0.10, 0.11, 0.13, 0.15, 0.17],
        'total_epa_def_allowed': [-52.01, -41.33, -44.84, -38.66, -36.78, -32.96, -25.64, -19.33, -17.12, -18.11, -14.91, -17.40, -9.20, -8.17, -7.00, -4.20, 0.00, -1.76, 7.09, 14.05, 15.50, 28.80, 33.94, 35.72, 41.66, 46.43, 48.63, 53.36, 60.13, 80.74, 88.01],
        'success_rate_def': [0.3929, 0.3942, 0.4195, 0.4303, 0.3765, 0.3870, 0.4350, 0.4447, 0.4239, 0.4087, 0.4245, 0.4638, 0.4279, 0.4504, 0.4199, 0.4400, 0.4400, 0.4338, 0.4621, 0.4665, 0.4470, 0.3991, 0.4345, 0.4530, 0.4598, 0.4172, 0.4309, 0.4681, 0.4796, 0.4971, 0.5038]
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
    
    # Reorder columns to match existing format
    final_df = merged_df[['team', 'epa_off_per_play', 'total_epa_off', 'success_rate_off', 'source_off', 
                         'epa_def_allowed_per_play', 'total_epa_def_allowed', 'success_rate_def', 'source_def',
                         'team_name_off', 'net_epa_per_play', 'last_updated', 'source']]
    
    # Rename team_name_off to team_name
    final_df = final_df.rename(columns={'team_name_off': 'team_name'})
    
    return final_df

def main():
    """Main function to update EPA data"""
    
    print("=== Updating EPA Data with Week 8 Stats ===")
    print("Source: SumerSports (thru Week 8)")
    print("Offensive: https://sumersports.com/teams/offensive/")
    print("Defensive: https://sumersports.com/teams/defensive/")
    print("=" * 50)
    
    # Create updated data
    updated_data = create_updated_epa_data()
    
    # Save to multiple formats
    output_files = [
        'data/sumersports_epa_data_week8.csv',
        'data/sumersports_epa_data_week8.json',
        'data/sumersports_epa_data_week8.parquet'
    ]
    
    for file_path in output_files:
        if file_path.endswith('.csv'):
            updated_data.to_csv(file_path, index=False)
        elif file_path.endswith('.json'):
            updated_data.to_json(file_path, orient='records', indent=2)
        elif file_path.endswith('.parquet'):
            updated_data.to_parquet(file_path, index=False)
        print(f"✅ Saved: {file_path}")
    
    # Also update the main EPA data file
    updated_data.to_csv('data/sumersports_epa_data.csv', index=False)
    updated_data.to_json('data/sumersports_epa_data.json', orient='records', indent=2)
    updated_data.to_parquet('data/sumersports_epa_data.parquet', index=False)
    print("✅ Updated main EPA data files")
    
    # Summary
    print(f"\n=== Summary ===")
    print(f"Teams updated: {len(updated_data)}")
    print(f"Last updated: {updated_data['last_updated'].iloc[0]}")
    
    print(f"\n=== Top 5 Offensive EPA/Play ===")
    top_off = updated_data.nlargest(5, 'epa_off_per_play')[['team_name', 'epa_off_per_play', 'total_epa_off']]
    for _, row in top_off.iterrows():
        print(f"{row['team_name']}: {row['epa_off_per_play']:.3f} ({row['total_epa_off']:.1f} total)")
    
    print(f"\n=== Top 5 Defensive EPA/Play (Best Defense) ===")
    top_def = updated_data.nsmallest(5, 'epa_def_allowed_per_play')[['team_name', 'epa_def_allowed_per_play', 'total_epa_def_allowed']]
    for _, row in top_def.iterrows():
        print(f"{row['team_name']}: {row['epa_def_allowed_per_play']:.3f} ({row['total_epa_def_allowed']:.1f} total)")
    
    print(f"\n=== Top 5 Net EPA/Play ===")
    top_net = updated_data.nlargest(5, 'net_epa_per_play')[['team_name', 'net_epa_per_play']]
    for _, row in top_net.iterrows():
        print(f"{row['team_name']}: {row['net_epa_per_play']:.3f}")
    
    return updated_data

if __name__ == "__main__":
    main()
