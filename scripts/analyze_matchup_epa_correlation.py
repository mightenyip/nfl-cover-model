#!/usr/bin/env python3
"""
Analyze correlation between matchup EPA differences and actual spread performance
"""

import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
import seaborn as sns
from scipy import stats

def analyze_matchup_epa_correlation():
    """Analyze correlation between matchup EPA differences and spread performance"""
    print("=== Matchup EPA Correlation Analysis ===")
    print("Analyzing relationship between matchup EPA differences and spread performance")
    print("=" * 70)
    
    # Load historical data (we'll need to create this from previous weeks)
    # For now, let's use Week 8 data as an example and show the methodology
    
    # Load Week 8 Model X data
    model_x_df = pd.read_csv('models/model_x/model_x_week8_predictions.csv')
    
    print("Week 8 Matchup EPA Analysis:")
    print("-" * 40)
    
    # Calculate matchup EPA difference for each game
    # matchupEPA_diff = matchupEPA_favorite - matchupEPA_underdog
    matchup_epa_diffs = []
    
    for idx, row in model_x_df.iterrows():
        favorite = row['favorite']
        underdog = row['underdog']
        spread = row['spread']
        
        # Determine which team is home/away
        if favorite == row['game'].split(' @ ')[1]:  # Home team is favorite
            fav_matchup_epa = row['home_matchup_epa']
            dog_matchup_epa = row['away_matchup_epa']
        else:  # Away team is favorite
            fav_matchup_epa = row['away_matchup_epa']
            dog_matchup_epa = row['home_matchup_epa']
        
        matchup_epa_diff = fav_matchup_epa - dog_matchup_epa
        
        matchup_epa_diffs.append({
            'game': row['game'],
            'favorite': favorite,
            'underdog': underdog,
            'spread': spread,
            'fav_matchup_epa': fav_matchup_epa,
            'dog_matchup_epa': dog_matchup_epa,
            'matchup_epa_diff': matchup_epa_diff,
            'net_matchup_advantage': row['net_matchup_advantage']
        })
    
    matchup_df = pd.DataFrame(matchup_epa_diffs)
    
    print("Matchup EPA Differences (Favorite - Underdog):")
    print("-" * 50)
    
    for _, row in matchup_df.iterrows():
        print(f"{row['game']}:")
        print(f"  Favorite ({row['favorite']}) Matchup EPA: {row['fav_matchup_epa']:.3f}")
        print(f"  Underdog ({row['underdog']}) Matchup EPA: {row['dog_matchup_epa']:.3f}")
        print(f"  Matchup EPA Diff: {row['matchup_epa_diff']:.3f}")
        print(f"  Spread: {row['favorite']} {row['spread']}")
        print()
    
    # Sort by matchup EPA difference
    matchup_df_sorted = matchup_df.sort_values('matchup_epa_diff', ascending=False)
    
    print("Games Ranked by Matchup EPA Difference:")
    print("-" * 50)
    for idx, (_, row) in enumerate(matchup_df_sorted.iterrows(), 1):
        print(f"{idx:2d}. {row['game']}: {row['matchup_epa_diff']:.3f} ({row['favorite']} {row['spread']})")
    
    print()
    print("=== Correlation Analysis Methodology ===")
    print("To analyze correlation, we need historical data with actual results.")
    print("The analysis would work as follows:")
    print()
    print("1. Calculate matchupEPA_diff = matchupEPA_favorite - matchupEPA_underdog")
    print("2. Calculate margin_vs_spread = actual_game_margin - spread")
    print("3. Compute correlation: corr = df['matchupEPA_diff'].corr(df['margin_vs_spread'])")
    print()
    print("Interpretation:")
    print("• Negative correlation → stronger favorites (higher EPA_diff) tend to underperform spread")
    print("• Positive correlation → favorites outperform expectations")
    print("• Zero correlation → no relationship between matchup EPA and spread performance")
    print()
    print("=== Week 8 Matchup EPA Differences Summary ===")
    print(f"Average Matchup EPA Difference: {matchup_df['matchup_epa_diff'].mean():.3f}")
    print(f"Standard Deviation: {matchup_df['matchup_epa_diff'].std():.3f}")
    print(f"Range: {matchup_df['matchup_epa_diff'].min():.3f} to {matchup_df['matchup_epa_diff'].max():.3f}")
    print()
    print("Games with Largest Favorable Matchup EPA Differences:")
    top_3 = matchup_df.nlargest(3, 'matchup_epa_diff')
    for _, row in top_3.iterrows():
        print(f"  {row['game']}: {row['matchup_epa_diff']:.3f} ({row['favorite']} {row['spread']})")
    print()
    print("Games with Largest Unfavorable Matchup EPA Differences:")
    bottom_3 = matchup_df.nsmallest(3, 'matchup_epa_diff')
    for _, row in bottom_3.iterrows():
        print(f"  {row['game']}: {row['matchup_epa_diff']:.3f} ({row['favorite']} {row['spread']})")
    
    # Save the analysis
    output_path = 'data/epa/analysis/matchup_epa_analysis_week8.csv'
    matchup_df.to_csv(output_path, index=False)
    print(f"\n✅ Matchup EPA analysis saved to: {output_path}")
    
    return matchup_df

def create_correlation_analysis_template():
    """Create a template for correlation analysis with historical data"""
    print("\n=== Correlation Analysis Template ===")
    print("To perform the full correlation analysis, you would need:")
    print()
    print("1. Historical game results with actual margins")
    print("2. Historical spreads for those games")
    print("3. Historical EPA data for those games")
    print()
    print("Then run:")
    print("```python")
    print("# Calculate matchup EPA differences")
    print("df['matchupEPA_diff'] = df['fav_matchup_epa'] - df['dog_matchup_epa']")
    print()
    print("# Calculate margin vs spread")
    print("df['margin_vs_spread'] = df['actual_margin'] - df['spread']")
    print()
    print("# Compute correlation")
    print("correlation = df['matchupEPA_diff'].corr(df['margin_vs_spread'])")
    print("print(f'Correlation: {correlation:.3f}')")
    print("```")
    print()
    print("This would reveal if Model X's matchup EPA differences")
    print("can predict which teams will outperform or underperform their spreads.")

if __name__ == "__main__":
    matchup_df = analyze_matchup_epa_correlation()
    create_correlation_analysis_template()
