#!/usr/bin/env python3
"""
Model D Week 7: Total Rules Predictions
"""

import pandas as pd
import numpy as np
import os

def run_model_d_week7():
    """Run Model D for Week 7 using total-based rules"""
    
    print("=== Week 7 Model D: Total Rules Predictions ===")
    print("Using predefined total-based rules")

    # Load Week 7 schedule and odds
    week7_odds_path = "../../schedule/week7_2025_odds.csv"
    week7_odds = pd.read_csv(week7_odds_path)

    print(f"Loaded {len(week7_odds)} games from Week 7 odds")

    # Initialize predictions
    predictions = []

    for index, row in week7_odds.iterrows():
        spread = row['spread_line']
        total = row['total_line']
        favorite_team = row['favorite_team']
        underdog_team = row['underdog_team']
        home_team = row['home_team']

        predicted_cover = False
        confidence = 'LOW'
        rule_applied = "Default Underdog"

        # Rule 1: Choose FAVORITE (spread <= 6.5) on games with TOTAL >= 46 points
        if total >= 46 and abs(spread) <= 6.5:
            predicted_cover = False  # Favorite covers
            confidence = 'HIGH'
            rule_applied = "High Total + Small Spread = Favorite"

        # Rule 2: Choose UNDERDOG in games with TOTAL <= 45.5 points
        elif total <= 45.5:
            predicted_cover = True  # Underdog covers
            confidence = 'HIGH'
            rule_applied = "Low Total = Underdog"

        # Rule 3: Default to UNDERDOG for other games
        else:
            predicted_cover = True  # Underdog covers
            confidence = 'LOW'
            rule_applied = "Default Underdog"

        predictions.append({
            'away_team': row['away_team'],
            'home_team': row['home_team'],
            'favorite_team': favorite_team,
            'underdog_team': underdog_team,
            'home_team': home_team,
            'spread_line': spread,
            'total_line': total,
            'predicted_cover': predicted_cover,
            'confidence': confidence,
            'rule_applied': rule_applied,
            'prediction': 'Cover' if predicted_cover else 'No Cover'
        })

    # Create DataFrame
    week7_data = pd.DataFrame(predictions)

    print(f"\n=== Week 7 Model D Predictions ===")
    
    # Show predictions grouped by rule
    for rule in week7_data['rule_applied'].unique():
        rule_games = week7_data[week7_data['rule_applied'] == rule]
        print(f"\n{rule} ({len(rule_games)} games):")
        
        for _, row in rule_games.iterrows():
            print(f"  {row['away_team']} at {row['home_team']}: {row['underdog_team']} +{row['spread_line']} (Total: {row['total_line']}) - {row['prediction']} ({row['confidence']})")

    # Save predictions
    week7_data.to_csv("model_d_week7_predictions.csv", index=False)
    print(f"\n✅ Model D Week 7 predictions saved to: model_d_week7_predictions.csv")

    return week7_data

if __name__ == "__main__":
    run_model_d_week7()
