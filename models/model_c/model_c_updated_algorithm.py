#!/usr/bin/env python3
"""
Model C Updated Algorithm
Sophisticated ATS prediction model based on spread ranges, totals, and historical trends
"""

import pandas as pd
import numpy as np
import os
import sys

def run_model_c_updated(week_odds_file):
    """
    Updated Model C Algorithm:
    
    1. Bet FAVORITE on spread between -1 and -3.5
    2. Bet HOME FAVORITE on spreads between -2.5 and -3.5  
    3. Bet FAVORITE (spread of 6.5 or less) on games with TOTAL OF 46 POINTS OR HIGHER
    
    If none of the above apply, use ATS trends:
    - Favorites: 57.5% (69-51-1)
    - Home Favorites: 58.6% (41-29-1)
    - Away Favorites: 56.0% (28-22-0)
    """
    
    print("=== Model C Updated Algorithm ===")
    print("Using sophisticated spread/total rules + ATS trends")
    
    try:
        odds_df = pd.read_csv(week_odds_file)
        print(f"Loaded {len(odds_df)} games from {week_odds_file}")
    except FileNotFoundError:
        print(f"❌ Error: {week_odds_file} not found")
        return None
    
    predictions = []
    
    for idx, row in odds_df.iterrows():
        game = f"{row['away_team']} @ {row['home_team']}"
        favorite = row['favorite_team']
        underdog = row['underdog_team']
        spread = abs(row['spread_line'])  # Always positive for comparison
        total = row['total_line']
        home_team = row['home_team']
        
        predicted_cover = None
        confidence = 'LOW'
        probability = 50.0
        rule_applied = "Default ATS Trend"
        
        # Rule 1: Bet FAVORITE on spread between -1 and -3.5
        if 1.0 <= spread <= 3.5:
            predicted_cover = False  # Favorite covers
            confidence = 'HIGH'
            probability = 65.0
            rule_applied = "Favorite Small Spread Rule (1-3.5)"
        
        # Rule 2: Bet HOME FAVORITE on spreads between -2.5 and -3.5
        elif 2.5 <= spread <= 3.5 and favorite == home_team:
            predicted_cover = False  # Home favorite covers
            confidence = 'HIGH'
            probability = 70.0
            rule_applied = "Home Favorite Spread Rule (2.5-3.5)"
        
        # Rule 3: Bet FAVORITE (spread ≤ 6.5) on games with TOTAL ≥ 46
        elif spread <= 6.5 and total >= 46:
            predicted_cover = False  # Favorite covers
            confidence = 'MEDIUM'
            probability = 60.0
            rule_applied = "High Total + Small Spread Rule"
        
        # Default: Use ATS trends
        else:
            if favorite == home_team:
                # Home Favorite: 58.6% success rate
                predicted_cover = False  # Home favorite covers
                confidence = 'MEDIUM'
                probability = 58.6
                rule_applied = "Home Favorite ATS Trend (58.6%)"
            else:
                # Away Favorite: 56.0% success rate
                predicted_cover = False  # Away favorite covers
                confidence = 'MEDIUM'
                probability = 56.0
                rule_applied = "Away Favorite ATS Trend (56.0%)"
        
        predictions.append({
            'game': game,
            'favorite': favorite,
            'underdog': underdog,
            'spread': row['spread_line'],
            'total': total,
            'predicted_cover': predicted_cover,
            'confidence': confidence,
            'probability': probability,
            'rule_applied': rule_applied
        })
    
    # Convert to DataFrame
    predictions_df = pd.DataFrame(predictions)
    
    # Summary
    high_confidence = len(predictions_df[predictions_df['confidence'] == 'HIGH'])
    medium_confidence = len(predictions_df[predictions_df['confidence'] == 'MEDIUM'])
    low_confidence = len(predictions_df[predictions_df['confidence'] == 'LOW'])
    
    favorite_picks = len(predictions_df[predictions_df['predicted_cover'] == False])
    underdog_picks = len(predictions_df[predictions_df['predicted_cover'] == True])
    
    print(f"\n=== Prediction Summary ===")
    print(f"High Confidence: {high_confidence} games")
    print(f"Medium Confidence: {medium_confidence} games")
    print(f"Low Confidence: {low_confidence} games")
    print(f"Favorite Picks: {favorite_picks} games")
    print(f"Underdog Picks: {underdog_picks} games")
    
    # Show rule breakdown
    print(f"\n=== Rule Breakdown ===")
    rule_counts = predictions_df['rule_applied'].value_counts()
    for rule, count in rule_counts.items():
        print(f"{rule}: {count} games")
    
    return predictions_df

def test_week8_performance():
    """Test the updated Model C against Week 8 results"""
    
    print("\n=== Testing Updated Model C on Week 8 ===")
    
    # Week 8 odds
    week8_odds = "schedule/week8_2025_odds.csv"
    predictions = run_model_c_updated(week8_odds)
    
    if predictions is None:
        return
    
    # Week 8 actual results (from our analysis)
    actual_results = {
        'Vikings @ Chargers': False,  # Chargers covered
        'Dolphins @ Falcons': True,   # Dolphins covered
        'Jets @ Bengals': True,       # Jets covered
        'Browns @ Patriots': False,   # Patriots covered
        'Giants @ Eagles': False,     # Eagles covered
        'Bills @ Panthers': False,    # Bills covered
        'Bears @ Ravens': False,      # Ravens covered
        '49ers @ Texans': False,      # Texans covered
        'Buccaneers @ Saints': False, # Buccaneers covered
        'Cowboys @ Broncos': False,   # Broncos covered
        'Titans @ Colts': False,      # Colts covered
        'Packers @ Steelers': False,  # Packers covered
        'Commanders @ Chiefs': False  # Chiefs covered
    }
    
    # Calculate performance
    correct = 0
    total = len(predictions)
    
    print(f"\n=== Week 8 Performance Analysis ===")
    for _, pred in predictions.iterrows():
        game = pred['game']
        predicted = pred['predicted_cover']
        actual = actual_results.get(game, None)
        
        if actual is not None:
            result = "✓ CORRECT" if predicted == actual else "✗ WRONG"
            if predicted == actual:
                correct += 1
            print(f"{game}: Predicted {'Cover' if predicted else 'No Cover'} | Actual {'Cover' if actual else 'No Cover'} | {result}")
    
    accuracy = correct / total * 100
    print(f"\nUpdated Model C Week 8 Performance: {correct}/{total} ({accuracy:.1f}%)")
    
    return predictions

if __name__ == "__main__":
    # Test on Week 8
    test_week8_performance()
