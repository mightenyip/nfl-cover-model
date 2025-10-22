#!/usr/bin/env python3
"""
Model D Week 8 Predictions
Generate Model D predictions for Week 8 using simple spread-based rules
"""

import pandas as pd
import numpy as np

def load_week8_odds():
    """Load Week 8 odds"""
    try:
        odds_df = pd.read_csv("schedule/week8_2025_odds.csv")
        print(f"Loaded {len(odds_df)} games from Week 8 odds")
        return odds_df
    except FileNotFoundError:
        print("❌ Error: schedule/week8_2025_odds.csv not found")
        return None

def calculate_model_d_predictions(odds_df):
    """Calculate Model D predictions for Week 8"""
    
    print("\n=== Model D Week 8 Predictions ===")
    print("Using simple spread-based rules")
    print("=" * 60)
    
    predictions = []
    
    for idx, row in odds_df.iterrows():
        away_team = row['away_team']
        home_team = row['home_team']
        favorite = row['favorite_team']
        underdog = row['underdog_team']
        spread = row['spread_line']
        
        # Model D: Simple spread-based rules
        # Rule 1: Fade large spreads (>7 points)
        # Rule 2: Take underdogs on medium spreads (3-7 points)
        # Rule 3: Take favorites on small spreads (<3 points)
        
        if abs(spread) > 7:
            # Large spread - fade the favorite
            predicted_cover = True  # Underdog covers
            confidence = "HIGH"
            probability = 0.65
            rule_applied = "Fade large spread"
        elif abs(spread) >= 3:
            # Medium spread - slight edge to underdog
            predicted_cover = True  # Underdog covers
            confidence = "MEDIUM"
            probability = 0.55
            rule_applied = "Medium spread underdog"
        else:
            # Small spread - slight edge to favorite
            predicted_cover = False  # Favorite covers
            confidence = "MEDIUM"
            probability = 0.55
            rule_applied = "Small spread favorite"
        
        # Create game description
        game_desc = f"{away_team} @ {home_team}"
        if favorite == away_team:
            spread_desc = f"{favorite} {spread}"
        else:
            spread_desc = f"{underdog} +{abs(spread)}"
        
        prediction_text = "Cover" if predicted_cover else "No Cover"
        
        print(f"{game_desc}: {spread_desc}")
        print(f"  Rule: {rule_applied}")
        print(f"  Probability: {probability:.1%} ({confidence})")
        print(f"  Prediction: {prediction_text}")
        print()
        
        predictions.append({
            'game': game_desc,
            'favorite': favorite,
            'underdog': underdog,
            'spread': spread,
            'spread_description': spread_desc,
            'cover_probability': probability,
            'confidence': confidence,
            'rule_applied': rule_applied,
            'predicted_cover': predicted_cover,
            'prediction': prediction_text
        })
    
    return predictions

def main():
    """Main function"""
    print("=== Model D Week 8 Predictions ===")
    print("Generating predictions using simple spread-based rules")
    print("=" * 60)
    
    # Load data
    odds_df = load_week8_odds()
    if odds_df is None:
        return
    
    # Generate predictions
    predictions = calculate_model_d_predictions(odds_df)
    
    # Save predictions
    predictions_df = pd.DataFrame(predictions)
    output_file = "models/model_d/model_d_week8_predictions.csv"
    predictions_df.to_csv(output_file, index=False)
    
    # Summary
    total_games = len(predictions)
    underdog_covers = sum(1 for p in predictions if p['predicted_cover'])
    favorite_covers = total_games - underdog_covers
    
    print(f"=== Model D Week 8 Summary ===")
    print(f"Total games: {total_games}")
    print(f"Underdog covers predicted: {underdog_covers}")
    print(f"Favorite covers predicted: {favorite_covers}")
    print(f"Average cover probability: {np.mean([p['cover_probability'] for p in predictions]):.1%}")
    
    # Confidence distribution
    confidence_counts = {}
    for p in predictions:
        conf = p['confidence']
        confidence_counts[conf] = confidence_counts.get(conf, 0) + 1
    
    print(f"\nConfidence Distribution:")
    for conf in ['HIGH', 'MEDIUM', 'LOW']:
        count = confidence_counts.get(conf, 0)
        print(f"  {conf}: {count} games")
    
    print(f"\n✅ Model D Week 8 predictions saved to {output_file}")

if __name__ == "__main__":
    main()
