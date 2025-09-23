#!/usr/bin/env python3
"""
Model C Week 4: Spread Rules Predictions
"""

import pandas as pd
import numpy as np
import os

def run_model_c_week4():
    """Run Model C for Week 4 using spread-based rules"""
    
    print("=== Week 4 Model C: Spread Rules Predictions ===")
    print("Using predefined spread-based rules")

    # Load Week 4 schedule and odds
    week4_odds_path = "../../schedule/week4_2025_odds.csv"
    week4_odds = pd.read_csv(week4_odds_path)

    print(f"Loaded {len(week4_odds)} games from Week 4 odds")

    # Initialize predictions
    predictions = []

    for index, row in week4_odds.iterrows():
        spread = row['spread_line']
        favorite_team = row['favorite_team']
        underdog_team = row['underdog_team']
        home_team = row['home_team']
        total_line = row['total_line']

        predicted_cover = False
        confidence = 'LOW'
        rule_applied = "Default Underdog"

        # Rule 1: Choose HOME FAVORITE on spreads between -2.5 and -3.5
        if -3.5 <= spread <= -2.5 and favorite_team == home_team:
            predicted_cover = False  # Favorite covers
            confidence = 'HIGH'
            rule_applied = "Home Favorite Spread Rule (-2.5 to -3.5)"

        # Rule 2: Choose FAVORITE on spreads between -1 and -3.5
        elif -3.5 <= spread <= -1:
            predicted_cover = False  # Favorite covers
            confidence = 'MEDIUM'
            rule_applied = "Favorite Small Spread Rule (-1 to -3.5)"

        # Rule 3: Choose UNDERDOG on spreads > -3.5 (default)
        else:
            predicted_cover = True  # Underdog covers
            confidence = 'LOW'
            rule_applied = "Default Underdog (spread > -3.5)"

        predictions.append({
            'away_team': row['away_team'],
            'home_team': row['home_team'],
            'favorite_team': favorite_team,
            'underdog_team': underdog_team,
            'home_team': home_team,
            'spread_line': spread,
            'total_line': total_line,
            'predicted_cover': predicted_cover,
            'confidence': confidence,
            'rule_applied': rule_applied,
            'prediction': 'Cover' if predicted_cover else 'No Cover'
        })

    # Create DataFrame
    week4_data = pd.DataFrame(predictions)

    print(f"\n=== Week 4 Model C Predictions ===")
    
    # Show predictions grouped by rule
    for rule in week4_data['rule_applied'].unique():
        rule_games = week4_data[week4_data['rule_applied'] == rule]
        print(f"\n{rule} ({len(rule_games)} games):")
        
        for _, row in rule_games.iterrows():
            print(f"  {row['away_team']} at {row['home_team']}: {row['underdog_team']} +{row['spread_line']} - {row['prediction']} ({row['confidence']})")

    # Save predictions
    week4_data.to_csv("model_c_week4_predictions.csv", index=False)
    print(f"\n✅ Model C Week 4 predictions saved to: model_c_week4_predictions.csv")

    return week4_data

if __name__ == "__main__":
    run_model_c_week4()
