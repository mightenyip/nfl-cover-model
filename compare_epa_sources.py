#!/usr/bin/env python3
"""
Compare EPA data from different sources
"""

import pandas as pd
import numpy as np
import os

def compare_epa_sources():
    """Compare EPA data from SumerSports vs nflverse"""
    
    print("=== EPA Data Source Comparison ===")
    
    # Load SumerSports data
    sumersports_path = "sumersports_epa_data.csv"
    if os.path.exists(sumersports_path):
        sumersports_df = pd.read_csv(sumersports_path)
        print(f"✅ Loaded SumerSports data: {len(sumersports_df)} teams")
    else:
        print("❌ SumerSports data not found")
        return
    
    # Load nflverse data
    nflverse_path = os.path.join("week2", "latest_team_epa_data.csv")
    if os.path.exists(nflverse_path):
        nflverse_df = pd.read_csv(nflverse_path)
        print(f"✅ Loaded nflverse data: {len(nflverse_df)} teams")
    else:
        print("❌ nflverse data not found")
        return
    
    # Merge the data for comparison
    comparison_df = pd.merge(
        sumersports_df[['team', 'team_name', 'epa_off_per_play', 'epa_def_allowed_per_play', 'net_epa_per_play']],
        nflverse_df[['team', 'team_name', 'epa_off_per_play', 'epa_def_allowed_per_play', 'net_epa_per_play']],
        on='team',
        how='inner',
        suffixes=('_sumersports', '_nflverse')
    )
    
    # Rename team_name columns to avoid conflicts
    comparison_df = comparison_df.rename(columns={
        'team_name_sumersports': 'team_name'
    })
    comparison_df = comparison_df.drop('team_name_nflverse', axis=1)
    
    print(f"\n✅ Combined data for {len(comparison_df)} teams")
    
    # Calculate differences
    comparison_df['epa_off_diff'] = comparison_df['epa_off_per_play_sumersports'] - comparison_df['epa_off_per_play_nflverse']
    comparison_df['epa_def_diff'] = comparison_df['epa_def_allowed_per_play_sumersports'] - comparison_df['epa_def_allowed_per_play_nflverse']
    comparison_df['net_epa_diff'] = comparison_df['net_epa_per_play_sumersports'] - comparison_df['net_epa_per_play_nflverse']
    
    # Display summary statistics
    print(f"\n=== Summary Statistics ===")
    print(f"Offensive EPA Difference (SumerSports - nflverse):")
    print(f"  Mean: {comparison_df['epa_off_diff'].mean():.4f}")
    print(f"  Std:  {comparison_df['epa_off_diff'].std():.4f}")
    print(f"  Min:  {comparison_df['epa_off_diff'].min():.4f}")
    print(f"  Max:  {comparison_df['epa_off_diff'].max():.4f}")
    
    print(f"\nDefensive EPA Difference (SumerSports - nflverse):")
    print(f"  Mean: {comparison_df['epa_def_diff'].mean():.4f}")
    print(f"  Std:  {comparison_df['epa_def_diff'].std():.4f}")
    print(f"  Min:  {comparison_df['epa_def_diff'].min():.4f}")
    print(f"  Max:  {comparison_df['epa_def_diff'].max():.4f}")
    
    print(f"\nNet EPA Difference (SumerSports - nflverse):")
    print(f"  Mean: {comparison_df['net_epa_diff'].mean():.4f}")
    print(f"  Std:  {comparison_df['net_epa_diff'].std():.4f}")
    print(f"  Min:  {comparison_df['net_epa_diff'].min():.4f}")
    print(f"  Max:  {comparison_df['net_epa_diff'].max():.4f}")
    
    # Show teams with largest differences
    print(f"\n=== Teams with Largest Differences ===")
    
    print(f"\nTop 5 Offensive EPA Differences (SumerSports higher):")
    top_off = comparison_df.nlargest(5, 'epa_off_diff')[['team_name', 'epa_off_per_play_sumersports', 'epa_off_per_play_nflverse', 'epa_off_diff']]
    print(top_off.to_string(index=False))
    
    print(f"\nTop 5 Offensive EPA Differences (nflverse higher):")
    bottom_off = comparison_df.nsmallest(5, 'epa_off_diff')[['team_name', 'epa_off_per_play_sumersports', 'epa_off_per_play_nflverse', 'epa_off_diff']]
    print(bottom_off.to_string(index=False))
    
    print(f"\nTop 5 Net EPA Differences (SumerSports higher):")
    top_net = comparison_df.nlargest(5, 'net_epa_diff')[['team_name', 'net_epa_per_play_sumersports', 'net_epa_per_play_nflverse', 'net_epa_diff']]
    print(top_net.to_string(index=False))
    
    print(f"\nTop 5 Net EPA Differences (nflverse higher):")
    bottom_net = comparison_df.nsmallest(5, 'net_epa_diff')[['team_name', 'net_epa_per_play_sumersports', 'net_epa_per_play_nflverse', 'net_epa_diff']]
    print(bottom_net.to_string(index=False))
    
    # Show Bills specifically (since we discussed them)
    bills_data = comparison_df[comparison_df['team'] == 'BUF']
    if not bills_data.empty:
        print(f"\n=== Bills Comparison ===")
        bills_row = bills_data.iloc[0]
        print(f"Offensive EPA - SumerSports: {bills_row['epa_off_per_play_sumersports']:.4f}, nflverse: {bills_row['epa_off_per_play_nflverse']:.4f}")
        print(f"Defensive EPA - SumerSports: {bills_row['epa_def_allowed_per_play_sumersports']:.4f}, nflverse: {bills_row['epa_def_allowed_per_play_nflverse']:.4f}")
        print(f"Net EPA - SumerSports: {bills_row['net_epa_per_play_sumersports']:.4f}, nflverse: {bills_row['net_epa_per_play_nflverse']:.4f}")
    
    # Save comparison
    comparison_df.to_csv("epa_source_comparison.csv", index=False)
    print(f"\n✅ Saved comparison to epa_source_comparison.csv")
    
    # Calculate correlation
    off_corr = comparison_df['epa_off_per_play_sumersports'].corr(comparison_df['epa_off_per_play_nflverse'])
    def_corr = comparison_df['epa_def_allowed_per_play_sumersports'].corr(comparison_df['epa_def_allowed_per_play_nflverse'])
    net_corr = comparison_df['net_epa_per_play_sumersports'].corr(comparison_df['net_epa_per_play_nflverse'])
    
    print(f"\n=== Correlation Analysis ===")
    print(f"Offensive EPA correlation: {off_corr:.4f}")
    print(f"Defensive EPA correlation: {def_corr:.4f}")
    print(f"Net EPA correlation: {net_corr:.4f}")

if __name__ == "__main__":
    compare_epa_sources()
