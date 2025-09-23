#!/usr/bin/env python3
"""
Three-Way Model Comparison: Model A vs Model B vs Model B v2
"""

import pandas as pd
import numpy as np
import os
from datetime import datetime

def compare_all_models():
    """Compare Model A, Model B, and Model B v2 predictions"""
    
    print("=== Three-Way Model Comparison ===")
    print(f"Comparison Date: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}")
    
    # Load all three models
    models = {}
    
    # Model A
    model_a_path = "model_a/model_a_week3_predictions.csv"
    if os.path.exists(model_a_path):
        models['A'] = pd.read_csv(model_a_path)
        print(f"✅ Loaded Model A: {len(models['A'])} games")
    
    # Model B
    model_b_path = "model_b/model_b_week3_predictions.csv"
    if os.path.exists(model_b_path):
        models['B'] = pd.read_csv(model_b_path)
        print(f"✅ Loaded Model B: {len(models['B'])} games")
    
    # Model B v2
    model_b_v2_path = "model_b/model_b_v2_week3_predictions.csv"
    if os.path.exists(model_b_v2_path):
        models['B_v2'] = pd.read_csv(model_b_v2_path)
        print(f"✅ Loaded Model B v2: {len(models['B_v2'])} games")
    
    if len(models) < 2:
        print("❌ Need at least 2 models to compare")
        return
    
    # Merge all models for comparison
    comparison = pd.merge(
        models['A'][['away_team', 'home_team', 'underdog_team', 'spread_line', 
                    'cover_probability', 'confidence', 'predicted_cover']],
        models['B'][['away_team', 'home_team', 'cover_probability', 'confidence', 'predicted_cover']],
        on=['away_team', 'home_team'],
        suffixes=('_A', '_B')
    )
    
    if 'B_v2' in models:
        comparison = pd.merge(
            comparison,
            models['B_v2'][['away_team', 'home_team', 'cover_probability', 'confidence', 'predicted_cover']],
            on=['away_team', 'home_team'],
            suffixes=('', '_B_v2')
        )
        comparison.rename(columns={
            'cover_probability': 'cover_probability_B_v2',
            'confidence': 'confidence_B_v2',
            'predicted_cover': 'predicted_cover_B_v2'
        }, inplace=True)
    
    print(f"\n=== Side-by-Side Predictions ===")
    if 'B_v2' in models:
        print(f"{'Game':<25} {'Spread':<8} {'Model A':<12} {'Model B':<12} {'Model B v2':<12} {'Agreement'}")
        print("-" * 90)
    else:
        print(f"{'Game':<25} {'Spread':<8} {'Model A':<12} {'Model B':<12} {'Agreement'}")
        print("-" * 70)
    
    agreements_ab = 0
    agreements_ab_v2 = 0
    agreements_b_bv2 = 0
    all_agree = 0
    
    for _, row in comparison.iterrows():
        game = f"{row['away_team']} @ {row['home_team']}"
        spread = f"{row['underdog_team']} +{row['spread_line']}"
        model_a_pred = f"{row['cover_probability_A']:.1%} ({row['confidence_A']})"
        model_b_pred = f"{row['cover_probability_B']:.1%} ({row['confidence_B']})"
        
        # Check agreements
        ab_agree = row['predicted_cover_A'] == row['predicted_cover_B']
        if ab_agree:
            agreements_ab += 1
            
        if 'B_v2' in models:
            model_b_v2_pred = f"{row['cover_probability_B_v2']:.1%} ({row['confidence_B_v2']})"
            
            ab_v2_agree = row['predicted_cover_A'] == row['predicted_cover_B_v2']
            b_bv2_agree = row['predicted_cover_B'] == row['predicted_cover_B_v2']
            all_three_agree = (row['predicted_cover_A'] == row['predicted_cover_B'] == row['predicted_cover_B_v2'])
            
            if ab_v2_agree:
                agreements_ab_v2 += 1
            if b_bv2_agree:
                agreements_b_bv2 += 1
            if all_three_agree:
                all_agree += 1
            
            agreement_symbol = "✅✅✅" if all_three_agree else "✅✅" if ab_agree and ab_v2_agree else "✅" if ab_agree or ab_v2_agree else "❌"
            
            print(f"{game:<25} {spread:<8} {model_a_pred:<12} {model_b_pred:<12} {model_b_v2_pred:<12} {agreement_symbol}")
        else:
            agreement_symbol = "✅" if ab_agree else "❌"
            print(f"{game:<25} {spread:<8} {model_a_pred:<12} {model_b_pred:<12} {agreement_symbol}")
    
    # Agreement statistics
    print(f"\n=== Agreement Statistics ===")
    print(f"Model A vs Model B: {agreements_ab}/{len(comparison)} ({agreements_ab/len(comparison):.1%})")
    
    if 'B_v2' in models:
        print(f"Model A vs Model B v2: {agreements_ab_v2}/{len(comparison)} ({agreements_ab_v2/len(comparison):.1%})")
        print(f"Model B vs Model B v2: {agreements_b_bv2}/{len(comparison)} ({agreements_b_bv2/len(comparison):.1%})")
        print(f"All Three Models Agree: {all_agree}/{len(comparison)} ({all_agree/len(comparison):.1%})")
    
    # Statistical comparison
    print(f"\n=== Statistical Comparison ===")
    
    model_a_covers = comparison['predicted_cover_A'].sum()
    model_b_covers = comparison['predicted_cover_B'].sum()
    
    print(f"Underdog Covers Predicted:")
    print(f"  Model A: {model_a_covers}")
    print(f"  Model B: {model_b_covers}")
    
    if 'B_v2' in models:
        model_b_v2_covers = comparison['predicted_cover_B_v2'].sum()
        print(f"  Model B v2: {model_b_v2_covers}")
    
    # Average probabilities
    avg_prob_a = comparison['cover_probability_A'].mean()
    avg_prob_b = comparison['cover_probability_B'].mean()
    
    print(f"\nAverage Cover Probability:")
    print(f"  Model A: {avg_prob_a:.1%}")
    print(f"  Model B: {avg_prob_b:.1%}")
    
    if 'B_v2' in models:
        avg_prob_b_v2 = comparison['cover_probability_B_v2'].mean()
        print(f"  Model B v2: {avg_prob_b_v2:.1%}")
    
    # Confidence distribution comparison
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
    
    if 'B_v2' in models:
        print(f"\nModel B v2 Confidence Levels:")
        conf_b_v2 = comparison['confidence_B_v2'].value_counts()
        for conf in ['VERY_HIGH', 'HIGH', 'MEDIUM', 'LOW', 'VERY_LOW']:
            count = conf_b_v2.get(conf, 0)
            print(f"  {conf}: {count} games")
    
    # Games where models strongly disagree
    print(f"\n=== Strong Disagreements ===")
    if 'B_v2' in models:
        strong_disagreements = comparison[
            ((comparison['cover_probability_A'] > 0.6) & (comparison['cover_probability_B_v2'] < 0.4)) |
            ((comparison['cover_probability_A'] < 0.4) & (comparison['cover_probability_B_v2'] > 0.6)) |
            ((comparison['cover_probability_B'] > 0.6) & (comparison['cover_probability_B_v2'] < 0.4)) |
            ((comparison['cover_probability_B'] < 0.4) & (comparison['cover_probability_B_v2'] > 0.6))
        ]
    else:
        strong_disagreements = comparison[
            ((comparison['cover_probability_A'] > 0.6) & (comparison['cover_probability_B'] < 0.4)) |
            ((comparison['cover_probability_A'] < 0.4) & (comparison['cover_probability_B'] > 0.6))
        ]
    
    if not strong_disagreements.empty:
        for _, row in strong_disagreements.iterrows():
            game = f"{row['away_team']} @ {row['home_team']}"
            print(f"{game}: A {row['cover_probability_A']:.1%} vs B {row['cover_probability_B']:.1%}", end="")
            if 'B_v2' in models:
                print(f" vs B v2 {row['cover_probability_B_v2']:.1%}")
            else:
                print()
    else:
        print("No strong disagreements found")
    
    # Save comparison
    comparison.to_csv("three_way_model_comparison_week3.csv", index=False)
    print(f"\n✅ Comparison saved to: three_way_model_comparison_week3.csv")
    
    # Summary
    print(f"\n=== Model Summary ===")
    print(f"Model A: SumerSports EPA (Original methodology)")
    print(f"Model B: Enhanced EPA (Updated data + advanced features)")
    if 'B_v2' in models:
        print(f"Model B v2: Matchup-Specific EPA (Pass/Rush breakdown)")
    
    return comparison

if __name__ == "__main__":
    compare_all_models()
