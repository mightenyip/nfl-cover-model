#!/usr/bin/env python3
"""
Model C Week 3 Retroactive: What would the updated Model C have predicted for Week 3?
"""

import pandas as pd
import numpy as np
import os

def run_model_c_week3_retroactive():
    """Run updated Model C logic on Week 3 data to see what it would have predicted"""
    
    print("=== Week 3 Model C Updated (Retroactive Analysis) ===")
    print("Applying updated Model C logic to Week 3 data")

    # Load Week 3 schedule and odds
    week3_odds_path = "../../schedule/week3_2025_odds.csv"
    week3_odds = pd.read_csv(week3_odds_path)

    print(f"Loaded {len(week3_odds)} games from Week 3 odds")

    # Initialize predictions
    predictions = []

    for index, row in week3_odds.iterrows():
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

        # Rule 1: Away Favorites (60.0% ATS) - STRONG FAVORITE PICK
        if favorite_is_away:
            if abs(spread) <= 7.0:  # Reasonable spread range
                predicted_cover = False  # Favorite covers
                confidence = 'HIGH'
                probability = 0.60
                rule_applied = f"Away Favorite Rule (60.0% ATS) - {favorite_team} -{abs(spread)}"
            else:  # Very large spread
                predicted_cover = True  # Underdog covers
                confidence = 'MEDIUM'
                probability = 0.55
                rule_applied = f"Large Away Favorite Spread - {underdog_team} +{abs(spread)}"

        # Rule 2: Home Favorites (51.9% ATS) - SLIGHT FAVORITE EDGE
        elif favorite_is_home:
            if abs(spread) <= 3.5:  # Small spreads
                predicted_cover = False  # Favorite covers
                confidence = 'MEDIUM'
                probability = 0.52
                rule_applied = f"Home Favorite Small Spread (51.9% ATS) - {favorite_team} -{abs(spread)}"
            elif abs(spread) <= 6.5:  # Medium spreads
                predicted_cover = True  # Underdog covers
                confidence = 'MEDIUM'
                probability = 0.52
                rule_applied = f"Home Favorite Medium Spread - {underdog_team} +{abs(spread)}"
            else:  # Large spreads
                predicted_cover = True  # Underdog covers
                confidence = 'HIGH'
                probability = 0.58
                rule_applied = f"Large Home Favorite Spread - {underdog_team} +{abs(spread)}"

        # Rule 3: Home Dogs (40.0% ATS) - AVOID or FADE
        elif not favorite_is_home and underdog_team == home_team:
            predicted_cover = False  # Favorite covers (fade home dogs)
            confidence = 'HIGH'
            probability = 0.60
            rule_applied = f"Fade Home Dogs (40.0% ATS) - {favorite_team} -{abs(spread)}"

        # Rule 4: Away Dogs (48.15% ATS) - SLIGHT UNDERDOG EDGE
        else:  # Away underdogs
            if abs(spread) <= 4.0:  # Small spreads
                predicted_cover = True  # Underdog covers
                confidence = 'MEDIUM'
                probability = 0.52
                rule_applied = f"Away Dogs Small Spread (48.15% ATS) - {underdog_team} +{abs(spread)}"
            else:  # Larger spreads
                predicted_cover = True  # Underdog covers
                confidence = 'MEDIUM'
                probability = 0.48
                rule_applied = f"Away Dogs Large Spread - {underdog_team} +{abs(spread)}"

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
    week3_data = pd.DataFrame(predictions)

    print(f"\n=== Week 3 Model C Updated (Retroactive) Predictions ===")
    
    # Group by rule type
    rule_groups = week3_data.groupby('rule_applied').size()
    
    for rule, count in rule_groups.items():
        rule_games = week3_data[week3_data['rule_applied'] == rule]
        print(f"\n{rule} ({count} games):")
        
        for _, row in rule_games.iterrows():
            print(f"  {row['away_team']} at {row['home_team']}: {row['underdog_team']} +{row['spread_line']} - {row['prediction']} ({row['confidence']}, {row['probability']:.1%})")

    # Summary statistics
    print(f"\n=== Week 3 Model C Updated Prediction Summary ===")
    print(f"Total Games: {len(week3_data)}")
    print(f"Underdog Covers: {sum(week3_data['predicted_cover'])} ({sum(week3_data['predicted_cover'])/len(week3_data):.1%})")
    print(f"Favorite Covers: {sum(~week3_data['predicted_cover'])} ({sum(~week3_data['predicted_cover'])/len(week3_data):.1%})")
    
    high_conf = week3_data[week3_data['confidence'] == 'HIGH']
    print(f"High Confidence Picks: {len(high_conf)}")
    
    # Show high confidence picks
    if len(high_conf) > 0:
        print(f"\n=== High Confidence Picks ({len(high_conf)} games) ===")
        for _, row in high_conf.iterrows():
            print(f"{row['away_team']} at {row['home_team']}: {row['underdog_team']} +{row['spread_line']} - {row['prediction']} ({row['rule_applied']})")

    # Save predictions
    week3_data.to_csv("model_c_week3_updated_retroactive_predictions.csv", index=False)
    print(f"\n✅ Retroactive Week 3 Model C Updated predictions saved to: model_c_week3_updated_retroactive_predictions.csv")

    return week3_data

if __name__ == "__main__":
    run_model_c_week3_retroactive()
