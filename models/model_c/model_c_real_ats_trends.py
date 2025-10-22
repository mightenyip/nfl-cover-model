#!/usr/bin/env python3
"""
Model C with Real ATS Trends (Week 1-7)
Based on actual performance data from our comprehensive analyses
"""

import pandas as pd
import numpy as np
import os

def run_model_c_real_ats():
    """Run Model C using real ATS trends from Week 1-7"""
    
    print("=== Model C with Real ATS Trends (Week 1-7) ===")
    print("Based on actual performance data:")
    print("  Overall Favorites: 64.8% (70-38-0)")
    print("  Overall Underdogs: 35.2% (38-70-0)")
    print("  Favorite-Heavy Weeks: 24.7% underdog rate (5 weeks)")
    print("  Underdog-Heavy Weeks: 73.3% underdog rate (1 week)")
    print("  Balanced Weeks: 50.0% underdog rate (1 week)")

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

        # Rule 1: STRONG FAVORITE BIAS (64.8% overall success)
        # Based on Week 1-7 data showing 64.8% favorite success rate
        
        if favorite_is_away:
            # Away Favorites - Strong pick based on data
            if abs(spread) <= 7.0:  # Reasonable spread range
                predicted_cover = False  # Favorite covers
                confidence = 'VERY_HIGH'
                probability = 0.648  # Based on actual data
                rule_applied = f"Away Favorite Rule (64.8% ATS) - {favorite_team} -{abs(spread)}"
            else:  # Very large spread
                predicted_cover = True  # Underdog covers (fade large spreads)
                confidence = 'MEDIUM'
                probability = 0.60
                rule_applied = f"Large Away Favorite Spread - {underdog_team} +{abs(spread)}"

        elif favorite_is_home:
            # Home Favorites - Strong pick based on data
            if abs(spread) <= 3.5:  # Small spreads
                predicted_cover = False  # Favorite covers
                confidence = 'VERY_HIGH'
                probability = 0.648  # Based on actual data
                rule_applied = f"Home Favorite Small Spread (64.8% ATS) - {favorite_team} -{abs(spread)}"
            elif abs(spread) <= 6.5:  # Medium spreads
                predicted_cover = False  # Favorite covers
                confidence = 'VERY_HIGH'
                probability = 0.648  # Based on actual data
                rule_applied = f"Home Favorite Medium Spread (64.8% ATS) - {favorite_team} -{abs(spread)}"
            else:  # Large spreads
                predicted_cover = True  # Underdog covers (fade large spreads)
                confidence = 'MEDIUM'
                probability = 0.60
                rule_applied = f"Large Home Favorite Spread - {underdog_team} +{abs(spread)}"

        # Rule 2: STRONG FADE UNDERDOGS (35.2% overall success)
        # Based on Week 1-7 data showing 35.2% underdog success rate
        
        elif not favorite_is_home and underdog_team == home_team:
            # Home Underdogs - Strong fade
            predicted_cover = False  # Favorite covers (fade home dogs)
            confidence = 'VERY_HIGH'
            probability = 0.648  # 1 - 0.352
            rule_applied = f"Fade Home Dogs (35.2% ATS) - {favorite_team} -{abs(spread)}"

        else:  # Away underdogs
            # Away Underdogs - Strong fade
            if abs(spread) <= 4.0:  # Small spreads
                predicted_cover = False  # Favorite covers (strong fade)
                confidence = 'VERY_HIGH'
                probability = 0.648  # Based on actual data
                rule_applied = f"Away Dogs Small Spread (35.2% ATS) - Strong fade"
            else:  # Larger spreads
                predicted_cover = False  # Favorite covers (strong fade)
                confidence = 'HIGH'
                probability = 0.648  # Based on actual data
                rule_applied = f"Away Dogs Large Spread (35.2% ATS) - Strong fade"

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

    print(f"\n=== Week 8 Model C Real ATS Predictions ===")
    
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
    
    very_high_conf = week8_data[week8_data['confidence'] == 'VERY_HIGH']
    high_conf = week8_data[week8_data['confidence'] == 'HIGH']
    
    print(f"Very High Confidence Picks: {len(very_high_conf)}")
    print(f"High Confidence Picks: {len(high_conf)}")
    
    # Show very high confidence picks
    if len(very_high_conf) > 0:
        print(f"\n=== Very High Confidence Picks ({len(very_high_conf)} games) ===")
        for _, row in very_high_conf.iterrows():
            print(f"{row['away_team']} at {row['home_team']}: {row['underdog_team']} +{row['spread_line']} - {row['prediction']} ({row['rule_applied']})")

    # Show high confidence picks
    if len(high_conf) > 0:
        print(f"\n=== High Confidence Picks ({len(high_conf)} games) ===")
        for _, row in high_conf.iterrows():
            print(f"{row['away_team']} at {row['home_team']}: {row['underdog_team']} +{row['spread_line']} - {row['prediction']} ({row['rule_applied']})")

    # Save predictions
    week8_data.to_csv("model_c_week8_real_ats_predictions.csv", index=False)
    print(f"\n✅ Real ATS Model C Week 8 predictions saved to: model_c_week8_real_ats_predictions.csv")

    return week8_data

def create_real_ats_summary():
    """Create a summary of the real ATS trends for Model C"""
    
    print("\n=== Real ATS Trends Summary (Week 1-7) ===")
    
    trends = {
        'Overall Favorites': {'record': '70-38-0', 'percent': 64.8, 'strategy': 'STRONG PICK'},
        'Overall Underdogs': {'record': '38-70-0', 'percent': 35.2, 'strategy': 'STRONG FADE'},
        'Favorite-Heavy Weeks': {'record': '58-19-0', 'percent': 75.3, 'strategy': 'EXCEL'},
        'Underdog-Heavy Weeks': {'record': '4-11-0', 'percent': 26.7, 'strategy': 'ADAPT'},
        'Balanced Weeks': {'record': '8-8-0', 'percent': 50.0, 'strategy': 'BALANCED'}
    }
    
    print(f"{'Category':<20} {'Record':<12} {'Percent':<8} {'Strategy'}")
    print("-" * 60)
    
    for category, data in trends.items():
        record = data['record']
        percent = data['percent']
        strategy = data['strategy']
        
        print(f"{category:<20} {record:<12} {percent:<8.1f}% {strategy}")
    
    print(f"\n=== Key Insights ===")
    print(f"✅ STRONGEST EDGES:")
    print(f"  - Overall Favorites: 64.8% (70-38-0)")
    print(f"  - Favorite-Heavy Weeks: 75.3% (58-19-0)")
    print(f"  - Home Favorites: Strong performance")
    print(f"  - Away Favorites: Strong performance")
    
    print(f"\n❌ STRONGEST FADES:")
    print(f"  - Overall Underdogs: 35.2% (38-70-0)")
    print(f"  - Home Dogs: Poor performance")
    print(f"  - Away Dogs: Poor performance")
    
    print(f"\n📊 MODEL C STRATEGY:")
    print(f"  - Favor Favorites heavily (64.8% success rate)")
    print(f"  - Fade Underdogs strongly (35.2% success rate)")
    print(f"  - Use VERY_HIGH confidence for favorite picks")
    print(f"  - Fade large spreads (>6.5 points)")

if __name__ == "__main__":
    # Create real ATS trends summary
    create_real_ats_summary()
    
    # Run Model C with real ATS trends
    run_model_c_real_ats()
