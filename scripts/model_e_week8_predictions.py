#!/usr/bin/env python3
"""
Model E Week 8 Predictions
Generate Model E predictions for Week 8 using random baseline
"""

import pandas as pd
import numpy as np
import random

def load_week8_odds():
    """Load Week 8 odds"""
    try:
        odds_df = pd.read_csv("schedule/week8_2025_odds.csv")
        print(f"Loaded {len(odds_df)} games from Week 8 odds")
        return odds_df
    except FileNotFoundError:
        print("❌ Error: schedule/week8_2025_odds.csv not found")
        return None

def calculate_model_e_predictions(odds_df):
    """Calculate Model E predictions for Week 8"""
    
    print("\n=== Model E Week 8 Predictions ===")
    print("Using random baseline (50/50)")
    print("=" * 60)
    
    # Set random seed for reproducibility
    random.seed(42)
    np.random.seed(42)
    
    predictions = []
    
    for idx, row in odds_df.iterrows():
        away_team = row['away_team']
        home_team = row['home_team']
        favorite = row['favorite_team']
        underdog = row['underdog_team']
        spread = row['spread_line']
        
        # Model E: Random baseline
        # Randomly choose between underdog and favorite
        predicted_cover = random.choice([True, False])
        
        # Random probability between 45-55%
        probability = random.uniform(0.45, 0.55)
        
        # Random confidence
        confidence = random.choice(['LOW', 'MEDIUM'])
        
        # Create game description
        game_desc = f"{away_team} @ {home_team}"
        if favorite == away_team:
            spread_desc = f"{favorite} {spread}"
        else:
            spread_desc = f"{underdog} +{abs(spread)}"
        
        prediction_text = "Cover" if predicted_cover else "No Cover"
        
        print(f"{game_desc}: {spread_desc}")
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
            'predicted_cover': predicted_cover,
            'prediction': prediction_text
        })
    
    return predictions

def main():
    """Main function"""
    print("=== Model E Week 8 Predictions ===")
    print("Generating random baseline predictions")
    print("=" * 60)
    
    # Load data
    odds_df = load_week8_odds()
    if odds_df is None:
        return
    
    # Generate predictions
    predictions = calculate_model_e_predictions(odds_df)
    
    # Save predictions
    predictions_df = pd.DataFrame(predictions)
    output_file = "models/model_e/model_e_week8_predictions.csv"
    predictions_df.to_csv(output_file, index=False)
    
    # Summary
    total_games = len(predictions)
    underdog_covers = sum(1 for p in predictions if p['predicted_cover'])
    favorite_covers = total_games - underdog_covers
    
    print(f"=== Model E Week 8 Summary ===")
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
    
    print(f"\n✅ Model E Week 8 predictions saved to {output_file}")

if __name__ == "__main__":
    main()
