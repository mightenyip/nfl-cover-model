#!/usr/bin/env python3
"""
Model C Updated: Spread Rules with Latest ATS Trends
Based on updated performance data through Week 7
"""

import pandas as pd
import numpy as np
import os

def run_model_c_updated_ats():
    """Run updated Model C using latest ATS trends through Week 7"""
    
    print("=== Model C Updated: Spread Rules + Latest ATS Trends ===")
    print("Incorporating updated ATS performance data through Week 7:")
    print("  Away Teams: 48.6% (52-55-1)")
    print("  Home Teams: 51.4% (55-52-1)")
    print("  Favorites: 54.2% (58-49-1)")
    print("  Dogs: 45.8% (49-58-1)")
    print("  Away Favorites: 53.2% (25-22-0)")
    print("  Away Dogs: 45.0% (27-33-1)")
    print("  Home Favorites: 55.0% (33-27-1)")
    print("  Home Dogs: 46.8% (22-25-0)")

    # Load Week 8 schedule and odds
    week8_odds_path = "../../schedule/week8_2025_odds.csv"
    
    # Check if file exists
    if not os.path.exists(week8_odds_path):
        print(f"Error: {week8_odds_path} not found")
        return None
    
    week8_odds = pd.read_csv(week8_odds_path)

    print(f"Loaded {len(week8_odds)} games from Week 8 odds")

    # Initialize predictions
    predictions = []

    for index, row in week8_odds.iterrows():
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

        # Rule 1: Away Favorites (53.2% ATS) - MODERATE FAVORITE PICK
        if favorite_is_away:
            if abs(spread) <= 7.0:  # Reasonable spread range
                predicted_cover = False  # Favorite covers
                confidence = 'HIGH'
                probability = 0.532
                rule_applied = f"Away Favorite Rule (53.2% ATS) - {favorite_team} -{abs(spread)}"
            else:  # Very large spread
                predicted_cover = True  # Underdog covers
                confidence = 'MEDIUM'
                probability = 0.55
                rule_applied = f"Large Away Favorite Spread - {underdog_team} +{abs(spread)}"

        # Rule 2: Home Favorites (55.0% ATS) - STRONG FAVORITE PICK
        elif favorite_is_home:
            if abs(spread) <= 3.5:  # Small spreads
                predicted_cover = False  # Favorite covers
                confidence = 'HIGH'
                probability = 0.55
                rule_applied = f"Home Favorite Small Spread (55.0% ATS) - {favorite_team} -{abs(spread)}"
            elif abs(spread) <= 6.5:  # Medium spreads
                predicted_cover = False  # Favorite covers
                confidence = 'HIGH'
                probability = 0.55
                rule_applied = f"Home Favorite Medium Spread (55.0% ATS) - {favorite_team} -{abs(spread)}"
            else:  # Large spreads
                predicted_cover = True  # Underdog covers
                confidence = 'MEDIUM'
                probability = 0.58
                rule_applied = f"Large Home Favorite Spread - {underdog_team} +{abs(spread)}"

        # Rule 3: Home Dogs (46.8% ATS) - FADE HOME DOGS
        elif not favorite_is_home and underdog_team == home_team:
            predicted_cover = False  # Favorite covers (fade home dogs)
            confidence = 'HIGH'
            probability = 0.532  # 1 - 0.468
            rule_applied = f"Fade Home Dogs (46.8% ATS) - {favorite_team} -{abs(spread)}"

        # Rule 4: Away Dogs (45.0% ATS) - STRONG FADE
        else:  # Away underdogs
            if abs(spread) <= 4.0:  # Small spreads
                predicted_cover = False  # Favorite covers (strong fade)
                confidence = 'HIGH'
                probability = 0.55
                rule_applied = f"Away Dogs Small Spread (45.0% ATS) - Strong fade"
            else:  # Larger spreads
                predicted_cover = False  # Favorite covers (strong fade)
                confidence = 'MEDIUM'
                probability = 0.55
                rule_applied = f"Away Dogs Large Spread (45.0% ATS) - Strong fade"

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
    week8_data = pd.DataFrame(predictions)

    print(f"\n=== Week 8 Model C Updated Predictions ===")
    
    # Group by rule type
    rule_groups = week8_data.groupby('rule_applied').size()
    
    for rule, count in rule_groups.items():
        rule_games = week8_data[week8_data['rule_applied'] == rule]
        print(f"\n{rule} ({count} games):")
        
        for _, row in rule_games.iterrows():
            print(f"  {row['away_team']} at {row['home_team']}: {row['underdog_team']} +{row['spread_line']} - {row['prediction']} ({row['confidence']}, {row['probability']:.1%})")

    # Summary statistics
    print(f"\n=== Prediction Summary ===")
    print(f"Total Games: {len(week8_data)}")
    print(f"Underdog Covers: {sum(week8_data['predicted_cover'])} ({sum(week8_data['predicted_cover'])/len(week8_data):.1%})")
    print(f"Favorite Covers: {sum(~week8_data['predicted_cover'])} ({sum(~week8_data['predicted_cover'])/len(week8_data):.1%})")
    
    high_conf = week8_data[week8_data['confidence'] == 'HIGH']
    print(f"High Confidence Picks: {len(high_conf)}")
    
    # Show high confidence picks
    if len(high_conf) > 0:
        print(f"\n=== High Confidence Picks ({len(high_conf)} games) ===")
        for _, row in high_conf.iterrows():
            print(f"{row['away_team']} at {row['home_team']}: {row['underdog_team']} +{row['spread_line']} - {row['prediction']} ({row['rule_applied']})")

    # Save predictions
    week8_data.to_csv("model_c_week8_updated_predictions.csv", index=False)
    print(f"\n✅ Updated Model C Week 8 predictions saved to: model_c_week8_updated_predictions.csv")

    return week8_data

def create_ats_trends_summary():
    """Create a summary of the latest ATS trends for Model C"""
    
    print("\n=== Latest ATS Trends Summary (Through Week 7) ===")
    
    trends = {
        'Away Teams': {'record': '52-55-1', 'percent': 48.6},
        'Home Teams': {'record': '55-52-1', 'percent': 51.4},
        'Favorites': {'record': '58-49-1', 'percent': 54.2},
        'Dogs': {'record': '49-58-1', 'percent': 45.8},
        'Away Favorites': {'record': '25-22-0', 'percent': 53.2},
        'Away Dogs': {'record': '27-33-1', 'percent': 45.0},
        'Home Favorites': {'record': '33-27-1', 'percent': 55.0},
        'Home Dogs': {'record': '22-25-0', 'percent': 46.8}
    }
    
    print(f"{'Category':<15} {'Record':<12} {'Percent':<8} {'Strategy'}")
    print("-" * 60)
    
    for category, data in trends.items():
        record = data['record']
        percent = data['percent']
        
        if percent > 52:
            strategy = "STRONG PICK"
        elif percent > 50:
            strategy = "SLIGHT EDGE"
        elif percent > 48:
            strategy = "SLIGHT FADE"
        else:
            strategy = "STRONG FADE"
        
        print(f"{category:<15} {record:<12} {percent:<8.1f}% {strategy}")
    
    print(f"\n=== Key Insights ===")
    print(f"✅ STRONGEST EDGES:")
    print(f"  - Home Favorites: 55.0% (33-27-1)")
    print(f"  - Away Favorites: 53.2% (25-22-0)")
    print(f"  - Home Teams: 51.4% (55-52-1)")
    print(f"  - Favorites: 54.2% (58-49-1)")
    
    print(f"\n❌ STRONGEST FADES:")
    print(f"  - Away Dogs: 45.0% (27-33-1)")
    print(f"  - Home Dogs: 46.8% (22-25-0)")
    print(f"  - Dogs: 45.8% (49-58-1)")
    print(f"  - Away Teams: 48.6% (52-55-1)")
    
    print(f"\n📊 MODEL C STRATEGY:")
    print(f"  - Favor Favorites (54.2% vs 45.8% Dogs)")
    print(f"  - Favor Home Teams (51.4% vs 48.6% Away)")
    print(f"  - Strong fade of Home Dogs (46.8%)")
    print(f"  - Strong fade of Away Dogs (45.0%)")

if __name__ == "__main__":
    # Create ATS trends summary
    create_ats_trends_summary()
    
    # Run updated Model C
    run_model_c_updated_ats()
