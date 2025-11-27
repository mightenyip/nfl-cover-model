#!/usr/bin/env python3
"""
Model C Week 13 Predictions
Generate Model C predictions for Week 13 using spread-based rules
"""

import pandas as pd
import numpy as np
from datetime import datetime

def load_week13_odds():
    """Load Week 13 odds"""
    try:
        odds_df = pd.read_csv("schedule/week13_2025_odds.csv")
        print(f"Loaded {len(odds_df)} games from Week 13 odds")
        return odds_df
    except FileNotFoundError:
        print("❌ Error: schedule/week13_2025_odds.csv not found")
        return None

def calculate_model_c_predictions(odds_df):
    """Calculate Model C predictions for Week 13 - Spread-based rules"""
    
    print("\n=== Model C Week 13 Predictions ===")
    print("Using spread-based rules")
    print("=" * 60)
    
    predictions = []
    
    for idx, row in odds_df.iterrows():
        away_team = row['away_team']
        home_team = row['home_team']
        favorite = row['favorite_team']
        underdog = row['underdog_team']
        spread = abs(row['spread_line'])
        
        # Model C logic: Simple spread-based rules
        if spread >= 10:
            pred = "No Cover"
            conf = "MEDIUM"
            prob = 55.0
            rule = "Spread >= 10: Fade favorite"
        elif spread >= 7:
            pred = "No Cover"
            conf = "MEDIUM"
            prob = 55.0
            rule = "Spread >= 7: Fade favorite"
        elif spread >= 3.5:
            pred = "No Cover"
            conf = "HIGH"
            prob = 60.0
            rule = "Spread >= 3.5: Strong fade favorite"
        else:
            pred = "No Cover"
            conf = "MEDIUM"
            prob = 53.8
            rule = "Small spread: Slight fade favorite"
        
        # Create game description
        game_desc = f"{away_team} @ {home_team}"
        if favorite == away_team:
            spread_desc = f"{favorite} {row['spread_line']}"
        else:
            spread_desc = f"{underdog} +{abs(row['spread_line'])}"
        
        predicted_cover = (pred == "Cover")
        
        print(f"{game_desc}: {spread_desc}")
        print(f"  Prediction: {pred} ({conf})")
        print(f"  Probability: {prob:.1f}%")
        print(f"  Rule: {rule}")
        print()
        
        predictions.append({
            'game': game_desc,
            'away_team': away_team,
            'home_team': home_team,
            'favorite': favorite,
            'underdog': underdog,
            'spread': row['spread_line'],
            'spread_description': spread_desc,
            'predicted_cover': predicted_cover,
            'prediction': pred,
            'confidence': conf,
            'probability': prob,
            'rule_applied': rule
        })
    
    return predictions

def main():
    """Main function"""
    print("=== Model C Week 13 Predictions ===")
    print("Generating predictions using spread-based rules")
    print("=" * 60)
    
    # Load data
    odds_df = load_week13_odds()
    if odds_df is None:
        return
    
    # Generate predictions
    predictions = calculate_model_c_predictions(odds_df)
    
    # Save predictions
    predictions_df = pd.DataFrame(predictions)
    output_file = "models/model_c/model_c_week13_predictions.csv"
    predictions_df.to_csv(output_file, index=False)
    
    # Summary
    total_games = len(predictions)
    underdog_covers = sum(1 for p in predictions if p['predicted_cover'])
    favorite_covers = total_games - underdog_covers
    
    print(f"=== Model C Week 13 Summary ===")
    print(f"Total games: {total_games}")
    print(f"Underdog covers predicted: {underdog_covers}")
    print(f"Favorite covers predicted: {favorite_covers}")
    print(f"Average probability: {np.mean([p['probability'] for p in predictions]):.1f}%")
    
    # Confidence distribution
    confidence_counts = {}
    for p in predictions:
        conf = p['confidence']
        confidence_counts[conf] = confidence_counts.get(conf, 0) + 1
    
    print(f"\nConfidence Distribution:")
    for conf in ['HIGH', 'MEDIUM', 'LOW']:
        count = confidence_counts.get(conf, 0)
        print(f"  {conf}: {count} games")
    
    print(f"\n✅ Model C Week 13 predictions saved to {output_file}")

if __name__ == "__main__":
    main()

