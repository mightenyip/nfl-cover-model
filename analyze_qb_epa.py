#!/usr/bin/env python3
"""
Analyze quarterback-specific EPA data to compare Joe Burrow vs Jake Browning
"""

import pandas as pd
import numpy as np
import os

def analyze_qb_epa():
    print("=== Quarterback EPA Analysis: Joe Burrow vs Jake Browning ===")
    
    # Load play-by-play data for 2023 and 2024
    pbp_2023 = pd.read_parquet("play_by_play_2023.parquet")
    pbp_2024 = pd.read_parquet("play_by_play_2024.parquet")
    
    # Combine the data
    pbp_data = pd.concat([pbp_2023, pbp_2024], ignore_index=True)
    
    print(f"Loaded {len(pbp_data)} total plays from 2023-2024")
    
    # Filter for Bengals games and passing plays
    bengals_passes = pbp_data[
        (pbp_data['posteam'] == 'CIN') & 
        (pbp_data['play_type'] == 'pass') &
        (pbp_data['passer'].notna())
    ].copy()
    
    print(f"Found {len(bengals_passes)} Bengals passing plays")
    
    # Group by passer and calculate EPA metrics
    qb_stats = bengals_passes.groupby('passer').agg({
        'epa': ['count', 'mean', 'sum'],
        'pass_touchdown': 'sum',
        'interception': 'sum',
        'pass_attempt': 'sum',
        'complete_pass': 'sum',
        'air_yards': 'mean',
        'yards_after_catch': 'mean'
    }).round(4)
    
    # Flatten column names
    qb_stats.columns = ['_'.join(col).strip() for col in qb_stats.columns]
    qb_stats = qb_stats.reset_index()
    
    # Calculate additional metrics
    qb_stats['completion_pct'] = (qb_stats['complete_pass_sum'] / qb_stats['pass_attempt_sum'] * 100).round(2)
    qb_stats['td_rate'] = (qb_stats['pass_touchdown_sum'] / qb_stats['pass_attempt_sum'] * 100).round(2)
    qb_stats['int_rate'] = (qb_stats['interception_sum'] / qb_stats['pass_attempt_sum'] * 100).round(2)
    
    # Rename columns for clarity
    qb_stats = qb_stats.rename(columns={
        'epa_count': 'plays',
        'epa_mean': 'epa_per_play',
        'epa_sum': 'total_epa',
        'air_yards_mean': 'avg_air_yards',
        'yards_after_catch_mean': 'avg_yac'
    })
    
    print("\n=== Bengals Quarterback Performance (2023-2024) ===")
    print(qb_stats[['passer', 'plays', 'epa_per_play', 'total_epa', 'completion_pct', 'td_rate', 'int_rate']].sort_values('epa_per_play', ascending=False))
    
    # Focus on Burrow vs Browning
    burrow_browning = qb_stats[qb_stats['passer'].isin(['J.Burrow', 'J.Browning'])].copy()
    
    if len(burrow_browning) >= 2:
        print("\n=== Joe Burrow vs Jake Browning Comparison ===")
        for _, qb in burrow_browning.iterrows():
            print(f"\n{qb['passer']}:")
            print(f"  Plays: {qb['plays']}")
            print(f"  EPA per Play: {qb['epa_per_play']:.4f}")
            print(f"  Total EPA: {qb['total_epa']:.2f}")
            print(f"  Completion %: {qb['completion_pct']:.1f}%")
            print(f"  TD Rate: {qb['td_rate']:.1f}%")
            print(f"  INT Rate: {qb['int_rate']:.1f}%")
            print(f"  Avg Air Yards: {qb['avg_air_yards']:.1f}")
            print(f"  Avg YAC: {qb['avg_yac']:.1f}")
        
        # Calculate the difference
        burrow = burrow_browning[burrow_browning['passer'] == 'J.Burrow'].iloc[0]
        browning = burrow_browning[burrow_browning['passer'] == 'J.Browning'].iloc[0]
        
        epa_diff = burrow['epa_per_play'] - browning['epa_per_play']
        print(f"\n=== EPA Difference (Burrow - Browning) ===")
        print(f"EPA per Play Difference: {epa_diff:.4f}")
        print(f"Percentage Difference: {(epa_diff / abs(browning['epa_per_play']) * 100):.1f}%")
        
        # Impact on team EPA
        print(f"\n=== Impact on Team EPA ===")
        print(f"If Browning maintains {browning['epa_per_play']:.4f} EPA/play vs Burrow's {burrow['epa_per_play']:.4f}:")
        print(f"Expected EPA reduction per game (assuming ~35 pass attempts): {epa_diff * 35:.2f}")
        
        # Load current Bengals EPA from SumerSports
        sumersports_data = pd.read_csv("sumersports_epa_data.csv")
        bengals_current = sumersports_data[sumersports_data['team'] == 'CIN'].iloc[0]
        
        print(f"\n=== Current Bengals EPA (SumerSports) ===")
        print(f"Offensive EPA per Play: {bengals_current['epa_off_per_play']:.4f}")
        print(f"Net EPA per Play: {bengals_current['net_epa_per_play']:.4f}")
        
        # Estimate adjusted EPA if Browning starts
        adjusted_off_epa = bengals_current['epa_off_per_play'] + (epa_diff * 0.6)  # Assume 60% of offense is passing
        adjusted_net_epa = adjusted_off_epa - (bengals_current['net_epa_per_play'] - bengals_current['epa_off_per_play'])
        
        print(f"\n=== Adjusted Bengals EPA (with Browning) ===")
        print(f"Estimated Offensive EPA per Play: {adjusted_off_epa:.4f}")
        print(f"Estimated Net EPA per Play: {adjusted_net_epa:.4f}")
        print(f"EPA Reduction: {bengals_current['net_epa_per_play'] - adjusted_net_epa:.4f}")
        
        return {
            'burrow_epa': burrow['epa_per_play'],
            'browning_epa': browning['epa_per_play'],
            'epa_difference': epa_diff,
            'current_bengals_epa': bengals_current['net_epa_per_play'],
            'adjusted_bengals_epa': adjusted_net_epa,
            'epa_reduction': bengals_current['net_epa_per_play'] - adjusted_net_epa
        }
    else:
        print("❌ Could not find both Burrow and Browning data")
        return None

if __name__ == "__main__":
    analyze_qb_epa()
