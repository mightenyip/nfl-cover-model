#!/usr/bin/env python3
"""
Model Comparison Framework - Compare Model A vs Model B predictions
"""

import pandas as pd
import numpy as np
import os
from datetime import datetime

def compare_models():
    """Compare Model A vs Model B predictions and performance"""
    
    print("=== Model A vs Model B Comparison ===")
    print(f"Comparison Date: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}")
    
    # Load Model A predictions (original SumerSports model)
    model_a_path = "model_a/model_a_week3_predictions.csv"
    if os.path.exists(model_a_path):
        model_a = pd.read_csv(model_a_path)
        print(f"✅ Loaded Model A: {len(model_a)} games")
    else:
        print("❌ Model A predictions not found")
        return
    
    # Load Model B predictions (enhanced EPA model)
    model_b_path = "model_b/model_b_week3_predictions.csv"
    if os.path.exists(model_b_path):
        model_b = pd.read_csv(model_b_path)
        print(f"✅ Loaded Model B: {len(model_b)} games")
    else:
        print("❌ Model B predictions not found")
        return
    
    # Merge the models for comparison
    comparison = pd.merge(
        model_a[['away_team', 'home_team', 'underdog_team', 'spread_line', 
                'cover_probability', 'confidence', 'predicted_cover']],
        model_b[['away_team', 'home_team', 'cover_probability', 'confidence', 'predicted_cover']],
        on=['away_team', 'home_team'],
        suffixes=('_A', '_B')
    )
    
    print(f"\n=== Side-by-Side Predictions ===")
    print(f"{'Game':<25} {'Spread':<8} {'Model A':<12} {'Model B':<12} {'Agreement'}")
    print("-" * 70)
    
    agreements = 0
    for _, row in comparison.iterrows():
        game = f"{row['away_team']} @ {row['home_team']}"
        spread = f"{row['underdog_team']} +{row['spread_line']}"
        model_a_pred = f"{row['cover_probability_A']:.1%} ({row['confidence_A']})"
        model_b_pred = f"{row['cover_probability_B']:.1%} ({row['confidence_B']})"
        
        agreement = "✅" if row['predicted_cover_A'] == row['predicted_cover_B'] else "❌"
        if row['predicted_cover_A'] == row['predicted_cover_B']:
            agreements += 1
            
        print(f"{game:<25} {spread:<8} {model_a_pred:<12} {model_b_pred:<12} {agreement}")
    
    agreement_rate = agreements / len(comparison)
    print(f"\nAgreement Rate: {agreement_rate:.1%} ({agreements}/{len(comparison)} games)")
    
    # Statistical comparison
    print(f"\n=== Statistical Comparison ===")
    
    # Cover predictions
    model_a_covers = comparison['predicted_cover_A'].sum()
    model_b_covers = comparison['predicted_cover_B'].sum()
    
    print(f"Model A: {model_a_covers} underdog covers predicted")
    print(f"Model B: {model_b_covers} underdog covers predicted")
    print(f"Difference: {abs(model_a_covers - model_b_covers)} games")
    
    # Average probabilities
    avg_prob_a = comparison['cover_probability_A'].mean()
    avg_prob_b = comparison['cover_probability_B'].mean()
    
    print(f"\nAverage Cover Probability:")
    print(f"Model A: {avg_prob_a:.1%}")
    print(f"Model B: {avg_prob_b:.1%}")
    print(f"Difference: {abs(avg_prob_a - avg_prob_b):.1%}")
    
    # Confidence distribution
    print(f"\n=== Confidence Distribution ===")
    
    print(f"Model A Confidence Levels:")
    conf_a = comparison['confidence_A'].value_counts()
    for conf in ['HIGH', 'MEDIUM', 'LOW']:
        count = conf_a.get(conf, 0)
        print(f"  {conf}: {count} games")
    
    print(f"\nModel B Confidence Levels:")
    conf_b = comparison['confidence_B'].value_counts()
    for conf in ['VERY_HIGH', 'HIGH', 'MEDIUM', 'LOW', 'VERY_LOW']:
        count = conf_b.get(conf, 0)
        print(f"  {conf}: {count} games")
    
    # Games where models strongly disagree
    print(f"\n=== Strong Disagreements ===")
    strong_disagreements = comparison[
        (comparison['cover_probability_A'] > 0.6) & (comparison['cover_probability_B'] < 0.4) |
        (comparison['cover_probability_A'] < 0.4) & (comparison['cover_probability_B'] > 0.6)
    ]
    
    if not strong_disagreements.empty:
        for _, row in strong_disagreements.iterrows():
            game = f"{row['away_team']} @ {row['home_team']}"
            print(f"{game}: Model A {row['cover_probability_A']:.1%} vs Model B {row['cover_probability_B']:.1%}")
    else:
        print("No strong disagreements found")
    
    # Save comparison
    comparison.to_csv("model_comparison_week3.csv", index=False)
    print(f"\n✅ Comparison saved to: model_comparison_week3.csv")
    
    # Performance summary
    print(f"\n=== Performance Summary ===")
    print(f"Model A: SumerSports EPA (Original methodology)")
    print(f"Model B: Enhanced EPA (Updated data + advanced features)")
    print(f"Agreement: {agreement_rate:.1%}")
    print(f"Model A avg probability: {avg_prob_a:.1%}")
    print(f"Model B avg probability: {avg_prob_b:.1%}")
    
    return comparison

if __name__ == "__main__":
    compare_models()
