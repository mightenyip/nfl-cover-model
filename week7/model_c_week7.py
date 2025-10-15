#!/usr/bin/env python3
"""
Model C Week 7: Spread Rules with Real-World ATS Trends
Based on Week 1-6 performance data
"""

import pandas as pd
import numpy as np
import os

def run_model_c_week7():
    """Run Model C for Week 7 using spread-based rules with real ATS trends"""
    
    print("=== Week 7 Model C: Spread Rules + ATS Trends ===")
    print("Incorporating updated ATS performance data through Week 6:")
    print("  Away Teams: 51.9% (40-37-1)")
    print("  Home Teams: 48.1% (37-40-1)")
    print("  Favorites: 53.2% (41-36-1)")
    print("  Dogs: 46.8% (36-41-1)")
    print("  Away Favorites: 56.2% (18-14-0)")
    print("  Away Dogs: 48.89% (22-23-1)")
    print("  Home Favorites: 51.1% (23-22-1)")
    print("  Home Dogs: 43.8% (14-18-0)")

    # Load Week 7 schedule and odds
    week7_odds_path = "../../schedule/week7_2025_odds.csv"
    
    # Check if file exists
    if not os.path.exists(week7_odds_path):
        print(f"Error: {week7_odds_path} not found")
        return None
    
    week7_odds = pd.read_csv(week7_odds_path)

    print(f"Loaded {len(week7_odds)} games from Week 7 odds")

    # Initialize predictions
    predictions = []

    for index, row in week7_odds.iterrows():
        spread = row['spread_line']
        favorite_team = row['favorite_team']
        underdog_team = row['underdog_team']
        home_team = row['home_team']
        away_team = row['away_team']
        total_line = row['total_line']

        # Determine if favorite is home or away
        favorite_is_home = favorite_team == home_team
        favorite_is_away = favorite_team == away_team
        
        predicted_cover = False
        confidence = 'LOW'
        rule_applied = "Default Rule"
        probability = 0.50

        # Rule 1: Away Favorites (56.2% ATS) - STRONG FAVORITE PICK
        if favorite_is_away:
            if abs(spread) <= 7.0:  # Reasonable spread range
                predicted_cover = False  # Favorite covers
                confidence = 'HIGH'
                probability = 0.562
                rule_applied = f"Away Favorite Rule (56.2% ATS) - {favorite_team} -{abs(spread)}"
            else:  # Very large spread
                predicted_cover = True  # Underdog covers
                confidence = 'MEDIUM'
                probability = 0.55
                rule_applied = f"Large Away Favorite Spread - {underdog_team} +{abs(spread)}"

        # Rule 2: Home Favorites (51.1% ATS) - SLIGHT FAVORITE EDGE
        elif favorite_is_home:
            if abs(spread) <= 3.5:  # Small spreads
                predicted_cover = False  # Favorite covers
                confidence = 'MEDIUM'
                probability = 0.511
                rule_applied = f"Home Favorite Small Spread (51.1% ATS) - {favorite_team} -{abs(spread)}"
            elif abs(spread) <= 6.5:  # Medium spreads
                predicted_cover = False  # Favorite covers (slightly)
                confidence = 'MEDIUM'
                probability = 0.511
                rule_applied = f"Home Favorite Medium Spread (51.1% ATS) - {favorite_team} -{abs(spread)}"
            else:  # Large spreads
                predicted_cover = True  # Underdog covers
                confidence = 'MEDIUM'
                probability = 0.55
                rule_applied = f"Large Home Favorite Spread - {underdog_team} +{abs(spread)}"

        # Rule 3: Home Dogs (43.8% ATS) - FADE HOME DOGS
        elif not favorite_is_home and underdog_team == home_team:
            predicted_cover = False  # Favorite covers (fade home dogs)
            confidence = 'HIGH'
            probability = 0.562  # 1 - 0.438
            rule_applied = f"Fade Home Dogs (43.8% ATS) - {favorite_team} -{abs(spread)}"

        # Rule 4: Away Dogs (48.89% ATS) - SLIGHT FADE
        else:  # Away underdogs
            if abs(spread) <= 4.0:  # Small spreads
                predicted_cover = False  # Favorite covers (slight fade)
                confidence = 'MEDIUM'
                probability = 0.511
                rule_applied = f"Away Dogs Small Spread (48.89% ATS) - Slight fade"
            else:  # Larger spreads
                predicted_cover = True  # Underdog covers
                confidence = 'MEDIUM'
                probability = 0.4889
                rule_applied = f"Away Dogs Large Spread (48.89% ATS) - {underdog_team} +{abs(spread)}"

        predictions.append({
            'away_team': away_team,
            'home_team': home_team,
            'favorite_team': favorite_team,
            'underdog_team': underdog_team,
            'spread_line': spread,
            'total_line': total_line,
            'predicted_cover': predicted_cover,
            'confidence': confidence,
            'probability': probability,
            'rule_applied': rule_applied,
            'prediction': 'Cover' if predicted_cover else 'No Cover',
            'favorite_is_home': favorite_is_home,
            'favorite_is_away': favorite_is_away
        })

    # Create DataFrame
    week7_data = pd.DataFrame(predictions)

    print(f"\n=== Week 7 Model C Predictions ===")
    
    # Group by rule type
    rule_groups = week7_data.groupby('rule_applied').size()
    
    for rule, count in rule_groups.items():
        rule_games = week7_data[week7_data['rule_applied'] == rule]
        print(f"\n{rule} ({count} games):")
        
        for _, row in rule_games.iterrows():
            print(f"  {row['away_team']} at {row['home_team']}: {row['underdog_team']} +{row['spread_line']} - {row['prediction']} ({row['confidence']}, {row['probability']:.1%})")

    # Summary statistics
    print(f"\n=== Prediction Summary ===")
    print(f"Total Games: {len(week7_data)}")
    print(f"Underdog Covers: {sum(week7_data['predicted_cover'])} ({sum(week7_data['predicted_cover'])/len(week7_data):.1%})")
    print(f"Favorite Covers: {sum(~week7_data['predicted_cover'])} ({sum(~week7_data['predicted_cover'])/len(week7_data):.1%})")
    
    high_conf = week7_data[week7_data['confidence'] == 'HIGH']
    print(f"High Confidence Picks: {len(high_conf)}")
    
    # Show high confidence picks
    if len(high_conf) > 0:
        print(f"\n=== High Confidence Picks ({len(high_conf)} games) ===")
        for _, row in high_conf.iterrows():
            print(f"{row['away_team']} at {row['home_team']}: {row['underdog_team']} +{row['spread_line']} - {row['prediction']} ({row['rule_applied']})")

    # Save predictions
    week7_data.to_csv("model_c_week7_predictions.csv", index=False)
    print(f"\n✅ Model C Week 7 predictions saved to: model_c_week7_predictions.csv")

    return week7_data

if __name__ == "__main__":
    run_model_c_week7()
