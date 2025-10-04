#!/usr/bin/env python3
"""
Model C Week 5 Updated: Spread Rules with Real-World ATS Trends
Based on Week 1-3 performance data
"""

import pandas as pd
import numpy as np
import os

def run_model_c_week5_updated():
    """Run updated Model C for Week 5 using spread-based rules with real ATS trends"""
    
    print("=== Week 5 Model C Updated: Spread Rules + ATS Trends ===")
    print("Incorporating updated ATS performance data:")
    print("  Away Teams: 48.4% (31-33-1)")
    print("  Home Teams: 51.6% (33-31-1)")
    print("  Favorites: 54.7% (35-29-1)")
    print("  Dogs: 45.3% (29-35-1)")
    print("  Away Favorites: 53.8% (14-12-0)")
    print("  Away Dogs: 44.74% (17-21-1)")
    print("  Home Favorites: 55.3% (21-17-1)")
    print("  Home Dogs: 46.2% (12-14-0)")

    # Load Week 5 schedule and odds
    week5_odds_path = "../../schedule/week5_2025_odds.csv"
    week5_odds = pd.read_csv(week5_odds_path)

    print(f"Loaded {len(week5_odds)} games from Week 5 odds")

    # Initialize predictions
    predictions = []

    for index, row in week5_odds.iterrows():
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

        # Rule 1: Away Favorites (53.8% ATS) - MODERATE FAVORITE PICK
        if favorite_is_away:
            if abs(spread) <= 7.0:  # Reasonable spread range
                predicted_cover = False  # Favorite covers
                confidence = 'MEDIUM'
                probability = 0.538
                rule_applied = f"Away Favorite Rule (53.8% ATS) - {favorite_team} -{abs(spread)}"
            else:  # Very large spread
                predicted_cover = True  # Underdog covers
                confidence = 'MEDIUM'
                probability = 0.55
                rule_applied = f"Large Away Favorite Spread - {underdog_team} +{abs(spread)}"

        # Rule 2: Home Favorites (55.3% ATS) - STRONG FAVORITE PICK
        elif favorite_is_home:
            if abs(spread) <= 3.5:  # Small spreads
                predicted_cover = False  # Favorite covers
                confidence = 'HIGH'
                probability = 0.553
                rule_applied = f"Home Favorite Small Spread (55.3% ATS) - {favorite_team} -{abs(spread)}"
            elif abs(spread) <= 6.5:  # Medium spreads
                predicted_cover = False  # Favorite covers
                confidence = 'MEDIUM'
                probability = 0.553
                rule_applied = f"Home Favorite Medium Spread (55.3% ATS) - {favorite_team} -{abs(spread)}"
            else:  # Large spreads
                predicted_cover = True  # Underdog covers
                confidence = 'MEDIUM'
                probability = 0.55
                rule_applied = f"Large Home Favorite Spread - {underdog_team} +{abs(spread)}"

        # Rule 3: Home Dogs (46.2% ATS) - SLIGHT FADE
        elif not favorite_is_home and underdog_team == home_team:
            predicted_cover = False  # Favorite covers (fade home dogs)
            confidence = 'MEDIUM'
            probability = 0.538  # 1 - 0.462
            rule_applied = f"Fade Home Dogs (46.2% ATS) - {favorite_team} -{abs(spread)}"

        # Rule 4: Away Dogs (44.74% ATS) - SLIGHT UNDERDOG FADE
        else:  # Away underdogs
            if abs(spread) <= 4.0:  # Small spreads
                predicted_cover = False  # Favorite covers (fade away dogs)
                confidence = 'MEDIUM'
                probability = 0.553  # 1 - 0.4474
                rule_applied = f"Fade Away Dogs Small Spread (44.74% ATS) - {favorite_team} -{abs(spread)}"
            else:  # Larger spreads
                predicted_cover = True  # Underdog covers
                confidence = 'MEDIUM'
                probability = 0.4474
                rule_applied = f"Away Dogs Large Spread (44.74% ATS) - {underdog_team} +{abs(spread)}"

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
    week5_data = pd.DataFrame(predictions)

    print(f"\n=== Week 5 Model C Updated Predictions ===")
    
    # Group by rule type
    rule_groups = week5_data.groupby('rule_applied').size()
    
    for rule, count in rule_groups.items():
        rule_games = week5_data[week5_data['rule_applied'] == rule]
        print(f"\n{rule} ({count} games):")
        
        for _, row in rule_games.iterrows():
            print(f"  {row['away_team']} at {row['home_team']}: {row['underdog_team']} +{row['spread_line']} - {row['prediction']} ({row['confidence']}, {row['probability']:.1%})")

    # Summary statistics
    print(f"\n=== Prediction Summary ===")
    print(f"Total Games: {len(week5_data)}")
    print(f"Underdog Covers: {sum(week5_data['predicted_cover'])} ({sum(week5_data['predicted_cover'])/len(week5_data):.1%})")
    print(f"Favorite Covers: {sum(~week5_data['predicted_cover'])} ({sum(~week5_data['predicted_cover'])/len(week5_data):.1%})")
    
    high_conf = week5_data[week5_data['confidence'] == 'HIGH']
    print(f"High Confidence Picks: {len(high_conf)}")
    
    # Show high confidence picks
    if len(high_conf) > 0:
        print(f"\n=== High Confidence Picks ({len(high_conf)} games) ===")
        for _, row in high_conf.iterrows():
            print(f"{row['away_team']} at {row['home_team']}: {row['underdog_team']} +{row['spread_line']} - {row['prediction']} ({row['rule_applied']})")

    # Save predictions
    week5_data.to_csv("model_c_week5_updated_predictions.csv", index=False)
    print(f"\n✅ Updated Model C Week 5 predictions saved to: model_c_week5_updated_predictions.csv")

    return week5_data

if __name__ == "__main__":
    run_model_c_week5_updated()
