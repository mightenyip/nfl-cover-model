#!/usr/bin/env python3
"""
Combine Updated EPA Data - Combine offensive and defensive EPA data
"""

import pandas as pd
from datetime import datetime

def combine_epa_data():
    """Combine offensive and defensive EPA data"""
    
    # Load the data
    offensive_df = pd.read_csv('data/updated_offensive_epa_data.csv')
    defensive_df = pd.read_csv('data/updated_defensive_epa_data_correct.csv')
    
    # Merge on team
    combined_df = pd.merge(offensive_df, defensive_df, on='team', how='outer', suffixes=('_off', '_def'))
    
    # Clean up columns
    combined_df['team_name'] = combined_df['team_name_off'].fillna(combined_df['team_name_def'])
    combined_df = combined_df.drop(['team_name_off', 'team_name_def'], axis=1)
    
    # The columns should already be correctly named from the individual files
    # No need to rename since they're already in the right format
    
    # Calculate net EPA metrics
    combined_df['net_epa_per_play'] = combined_df['epa_off_per_play'] - combined_df['epa_def_allowed_per_play']
    combined_df['net_epa_pass'] = combined_df['epa_pass_off'] - combined_df['epa_pass_def_allowed']
    combined_df['net_epa_rush'] = combined_df['epa_rush_off'] - combined_df['epa_rush_def_allowed']
    
    # Add metadata
    combined_df['last_updated'] = datetime.now()
    combined_df['source'] = 'sumersports_combined_manual'
    
    # Select and reorder columns for consistency with Model B v2
    final_columns = [
        'team', 'team_name', 'epa_off_per_play', 'epa_pass_off', 'epa_rush_off', 
        'total_epa_off', 'success_rate_off', 'source_off',
        'epa_def_allowed_per_play', 'epa_pass_def_allowed', 'epa_rush_def_allowed',
        'total_epa_def_allowed', 'success_rate_def', 'source_def',
        'net_epa_per_play', 'net_epa_pass', 'net_epa_rush',
        'last_updated', 'source'
    ]
    
    # Add missing columns if they don't exist
    for col in final_columns:
        if col not in combined_df.columns:
            if col == 'source_off':
                combined_df[col] = 'sumersports_offensive_manual'
            elif col == 'source_def':
                combined_df[col] = 'sumersports_defensive_manual'
            else:
                combined_df[col] = None
    
    # Select final columns
    final_df = combined_df[final_columns]
    
    return final_df

def main():
    """Main function to combine EPA data"""
    
    print("=== Combine Updated EPA Data ===")
    
    # Combine the data
    combined_df = combine_epa_data()
    
    # Save the data
    combined_df.to_csv('data/detailed_epa_data.csv', index=False)
    combined_df.to_csv('data/detailed_epa_data_week7.csv', index=False)
    print(f"✅ Saved combined EPA data to data/detailed_epa_data.csv")
    print(f"✅ Saved combined EPA data to data/detailed_epa_data_week7.csv")
    
    # Display summary
    print(f"\n=== Combined EPA Data Summary ===")
    print(f"Teams: {len(combined_df)}")
    print(f"Last Updated: {combined_df['last_updated'].iloc[0]}")
    
    # Top 5 teams by Net EPA
    print(f"\nTop 5 Teams by Net EPA:")
    top_teams = combined_df.nlargest(5, 'net_epa_per_play')[['team_name', 'net_epa_per_play', 'net_epa_pass', 'net_epa_rush']]
    print(top_teams.to_string(index=False))
    
    # Top 5 offensive teams
    print(f"\nTop 5 Offensive Teams:")
    top_off = combined_df.nlargest(5, 'epa_off_per_play')[['team_name', 'epa_off_per_play', 'epa_pass_off', 'epa_rush_off']]
    print(top_off.to_string(index=False))
    
    # Top 5 defensive teams (lowest EPA allowed)
    print(f"\nTop 5 Defensive Teams (Lowest EPA Allowed):")
    top_def = combined_df.nsmallest(5, 'epa_def_allowed_per_play')[['team_name', 'epa_def_allowed_per_play', 'epa_pass_def_allowed', 'epa_rush_def_allowed']]
    print(top_def.to_string(index=False))
    
    print(f"\n✅ Successfully combined updated EPA data!")
    print(f"📊 Data includes {len(combined_df)} teams with latest EPA/Pass and EPA/Rush statistics")
    print(f"🔄 Model B v2 can now use this updated data for predictions")

if __name__ == "__main__":
    main()
