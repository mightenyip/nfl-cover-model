#!/usr/bin/env python3
"""
Debug script to check Bills EPA calculation
"""

import pandas as pd
import numpy as np

def debug_bills_epa():
    """Debug the Bills EPA calculation"""
    
    # Load the 2025 play-by-play data
    pbp_df = pd.read_parquet("images/play_by_play_2025.parquet", engine="pyarrow")
    
    # Filter to regular season, Weeks 1-2
    pbp_df = pbp_df[(pbp_df["season_type"] == "REG") & (pbp_df["week"].isin([1, 2]))].copy()
    
    print("=== Bills EPA Debug ===")
    print(f"Total plays in dataset: {len(pbp_df)}")
    
    # Check Bills offensive plays
    bills_off = pbp_df[pbp_df["posteam"] == "BUF"].copy()
    print(f"\nBills offensive plays: {len(bills_off)}")
    if len(bills_off) > 0:
        print(f"Bills offensive EPA sum: {bills_off['epa'].sum():.4f}")
        print(f"Bills offensive EPA per play: {bills_off['epa'].mean():.4f}")
        print(f"Bills offensive plays by week:")
        print(bills_off.groupby('week')['epa'].agg(['count', 'sum', 'mean']))
    
    # Check Bills defensive plays
    bills_def = pbp_df[pbp_df["defteam"] == "BUF"].copy()
    print(f"\nBills defensive plays: {len(bills_def)}")
    if len(bills_def) > 0:
        print(f"Bills defensive EPA allowed sum: {bills_def['epa'].sum():.4f}")
        print(f"Bills defensive EPA allowed per play: {bills_def['epa'].mean():.4f}")
        print(f"Bills defensive plays by week:")
        print(bills_def.groupby('week')['epa'].agg(['count', 'sum', 'mean']))
    
    # Check for any data issues
    print(f"\n=== Data Quality Check ===")
    print(f"Bills offensive plays with null EPA: {bills_off['epa'].isna().sum()}")
    print(f"Bills defensive plays with null EPA: {bills_def['epa'].isna().sum()}")
    
    # Check if there are any unusual EPA values
    print(f"\nBills offensive EPA range: {bills_off['epa'].min():.4f} to {bills_off['epa'].max():.4f}")
    print(f"Bills defensive EPA range: {bills_def['epa'].min():.4f} to {bills_def['epa'].max():.4f}")
    
    # Let's also check what the actual games were
    print(f"\n=== Bills Games ===")
    bills_games = pbp_df[(pbp_df["posteam"] == "BUF") | (pbp_df["defteam"] == "BUF")].copy()
    if len(bills_games) > 0:
        game_summary = bills_games.groupby(['week', 'game_id']).agg({
            'posteam': 'first',
            'defteam': 'first',
            'epa': ['count', 'sum']
        })
        print(game_summary)
    
    # Check if there's a data swap issue
    print(f"\n=== Checking for Data Issues ===")
    
    # Let's manually calculate Bills defensive EPA
    bills_def_manual = pbp_df[pbp_df["defteam"] == "BUF"]["epa"].dropna()
    if len(bills_def_manual) > 0:
        bills_def_epa_manual = bills_def_manual.mean()
        print(f"Manual Bills defensive EPA calculation: {bills_def_epa_manual:.4f}")
    
    # Check if the issue is in our aggregation
    print(f"\n=== Aggregation Check ===")
    bills_def_agg = pbp_df[pbp_df["defteam"] == "BUF"].groupby('week').agg({
        'epa': ['sum', 'count', 'mean']
    })
    print("Bills defensive EPA by week:")
    print(bills_def_agg)

if __name__ == "__main__":
    debug_bills_epa()
