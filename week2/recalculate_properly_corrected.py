#!/usr/bin/env python3
"""
Recalculate model probabilities with PROPERLY corrected net EPA values
"""

import pandas as pd
import numpy as np

def recalculate_cover_probability(underdog_net_epa, favorite_net_epa, spread, is_home, opponent_def_epa):
    """
    Recalculate cover probability based on corrected net EPA values
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
    print("=== PROPERLY CORRECTED Cover Probabilities ===")
    
    # Load the properly corrected EPA data
    df = pd.read_csv("week2_epa_properly_corrected.csv")
    
    print("\nOriginal vs PROPERLY Corrected Probabilities:")
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
    
    # Focus on Titans vs Rams
    print(f"\n{'='*60}")
    print("RAMS vs TITANS DETAILED ANALYSIS")
    print(f"{'='*60}")
    
    titans_row = df[df['game'] == 'Rams at Titans'].iloc[0]
    
    print(f"Original Model:")
    print(f"  Titans Net EPA: -0.109 (incorrect)")
    print(f"  Rams Net EPA: 0.000 (incorrect)")
    print(f"  Net EPA Diff: 0.109")
    print(f"  Cover Probability: 24.3%")
    
    print(f"\nPROPERLY Corrected Model:")
    print(f"  Titans Net EPA: {titans_row['underdog_net_epa_corrected']:.3f}")
    print(f"  Rams Net EPA: {titans_row['favorite_net_epa_corrected']:.3f}")
    print(f"  Net EPA Diff: {titans_row['net_epa_differential']:.3f}")
    
    corrected_prob = recalculate_cover_probability(
        titans_row['underdog_net_epa_corrected'],
        titans_row['favorite_net_epa_corrected'],
        titans_row['spread'],
        titans_row['is_home'],
        titans_row['opponent_def_epa']
    )
    
    print(f"  Cover Probability: {corrected_prob:.1%}")
    
    change = corrected_prob - 0.243  # Original probability
    change_pct = (change / 0.243) * 100
    
    print(f"\nImpact of Proper Correction:")
    print(f"  Change: {change:+.3f} ({change_pct:+.1f}%)")
    
    if change_pct > 10:
        print(f"  🚨 SIGNIFICANT IMPACT")
    elif change_pct > 5:
        print(f"  ⚠️  MODERATE IMPACT")
    else:
        print(f"  ✅ MINIMAL IMPACT")
    
    print(f"\n💡 Key Insight:")
    print(f"  Titans have TERRIBLE net EPA (-0.547)")
    print(f"  Rams have decent net EPA (+0.046)")
    print(f"  This makes Titans a POOR underdog pick!")

if __name__ == "__main__":
    main()
