#!/usr/bin/env python3
"""
Recalculate model probabilities with corrected net EPA values
"""

import pandas as pd
import numpy as np

def recalculate_cover_probability(underdog_net_epa, favorite_net_epa, spread, is_home, opponent_def_epa):
    """
    Recalculate cover probability based on corrected net EPA values
    This is a simplified version of the model logic
    """
    
    # Net EPA differential (underdog - favorite)
    net_epa_diff = underdog_net_epa - favorite_net_epa
    
    # Home field advantage (typically 2-3 points)
    home_advantage = 0.05 if is_home else 0.0
    
    # Opponent defensive EPA impact (negative is good for underdog)
    def_impact = -opponent_def_epa * 0.3  # Scale factor
    
    # Spread impact (larger spreads favor underdogs slightly)
    spread_impact = spread * 0.01
    
    # Base probability from net EPA differential
    base_prob = 0.5 + (net_epa_diff * 2.0)  # Scale factor
    
    # Add other factors
    adjusted_prob = base_prob + home_advantage + def_impact + spread_impact
    
    # Ensure probability is between 0 and 1
    adjusted_prob = max(0.01, min(0.99, adjusted_prob))
    
    return adjusted_prob

def main():
    print("=== Recalculating Cover Probabilities with Corrected Net EPA ===")
    
    # Load the corrected EPA data
    df = pd.read_csv("week2_epa_corrected.csv")
    
    print("\nOriginal vs Corrected Probabilities:")
    print("-" * 80)
    print(f"{'Game':<25} {'Original':<10} {'Corrected':<10} {'Change':<8} {'Impact'}")
    print("-" * 80)
    
    for _, row in df.iterrows():
        # Extract data
        game = row['game']
        underdog_net_epa = row['underdog_net_epa_corrected']
        favorite_net_epa = row['favorite_net_epa_corrected']
        spread = row['spread']
        is_home = row['is_home']
        opponent_def_epa = row['opponent_def_epa']
        original_prob = row['cover_probability']
        
        # Recalculate probability
        corrected_prob = recalculate_cover_probability(
            underdog_net_epa, favorite_net_epa, spread, is_home, opponent_def_epa
        )
        
        # Calculate change
        change = corrected_prob - original_prob
        change_pct = (change / original_prob) * 100
        
        # Determine impact
        if abs(change_pct) < 5:
            impact = "Minimal"
        elif abs(change_pct) < 15:
            impact = "Moderate"
        else:
            impact = "Significant"
        
        print(f"{game:<25} {original_prob:<10.3f} {corrected_prob:<10.3f} {change:+.3f} ({change_pct:+.1f}%) {impact}")
    
    # Focus on Chargers vs Raiders
    print(f"\n{'='*60}")
    print("CHARGERS vs RAIDERS DETAILED ANALYSIS")
    print(f"{'='*60}")
    
    chargers_row = df[df['game'] == 'Chargers at Raiders'].iloc[0]
    
    print(f"Original Model:")
    print(f"  Raiders Net EPA: {chargers_row['underdog_net_epa_corrected']:.3f}")
    print(f"  Chargers Net EPA: 0.000 (incorrect)")
    print(f"  Net EPA Diff: -0.131")
    print(f"  Cover Probability: {chargers_row['cover_probability']:.1%}")
    
    print(f"\nCorrected Model:")
    print(f"  Raiders Net EPA: {chargers_row['underdog_net_epa_corrected']:.3f}")
    print(f"  Chargers Net EPA: {chargers_row['favorite_net_epa_corrected']:.3f}")
    print(f"  Net EPA Diff: {chargers_row['net_epa_differential']:.3f}")
    
    corrected_prob = recalculate_cover_probability(
        chargers_row['underdog_net_epa_corrected'],
        chargers_row['favorite_net_epa_corrected'],
        chargers_row['spread'],
        chargers_row['is_home'],
        chargers_row['opponent_def_epa']
    )
    
    print(f"  Cover Probability: {corrected_prob:.1%}")
    
    change = corrected_prob - chargers_row['cover_probability']
    change_pct = (change / chargers_row['cover_probability']) * 100
    
    print(f"\nImpact of Correction:")
    print(f"  Change: {change:+.3f} ({change_pct:+.1f}%)")
    
    if change_pct > 10:
        print(f"  🚨 SIGNIFICANT IMPACT - Model was overconfident in Raiders")
    elif change_pct > 5:
        print(f"  ⚠️  MODERATE IMPACT - Model slightly overconfident")
    else:
        print(f"  ✅ MINIMAL IMPACT - Model was reasonably accurate")

if __name__ == "__main__":
    main()
