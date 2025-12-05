#!/usr/bin/env python3
"""
Week 14 Consensus Predictions for Models A, B, and E - Formatted with Favorite/Underdog
"""

import pandas as pd
import numpy as np

def main():
    # Load the consensus data
    df = pd.read_csv("week14_abe_consensus_predictions.csv")
    
    results = []
    
    for _, row in df.iterrows():
        game = row['game']
        favorite = row['favorite']
        underdog = row['underdog']
        spread = abs(row['spread'])
        
        # Determine who is covering
        consensus = row['consensus_abe']
        if consensus == 'Cover':
            prediction = f"{underdog} (Underdog) covers +{spread}"
            prediction_short = "Underdog covers"
        else:
            prediction = f"{favorite} (Favorite) covers -{spread}"
            prediction_short = "Favorite covers"
        
        # Individual model predictions
        model_a_pred = row['model_a']
        model_b_pred = row['model_b']
        model_e_pred = row['model_e']
        
        if model_a_pred == 'Cover':
            model_a_detail = f"{underdog} covers"
        else:
            model_a_detail = f"{favorite} covers"
            
        if model_b_pred == 'Cover':
            model_b_detail = f"{underdog} covers"
        else:
            model_b_detail = f"{favorite} covers"
            
        if model_e_pred == 'Cover':
            model_e_detail = f"{underdog} covers"
        else:
            model_e_detail = f"{favorite} covers"
        
        results.append({
            'game': game,
            'favorite': favorite,
            'underdog': underdog,
            'spread': f"{favorite} -{spread}",
            'consensus_prediction': prediction_short,
            'consensus_detail': prediction,
            'model_a': model_a_detail,
            'model_a_prob': row['model_a_prob'],
            'model_a_conf': row['model_a_conf'],
            'model_b': model_b_detail,
            'model_b_prob': row['model_b_prob'],
            'model_b_conf': row['model_b_conf'],
            'model_e': model_e_detail,
            'model_e_prob': row['model_e_prob'],
            'model_e_conf': row['model_e_conf'],
            'cover_votes': row['cover_votes_abe'],
            'agreement': f"{row['cover_votes_abe']}/3",
            'avg_probability': row['avg_probability']
        })
    
    result_df = pd.DataFrame(results)
    
    # Save to CSV
    output_file = "week14_abe_consensus_formatted.csv"
    result_df.to_csv(output_file, index=False)
    
    # Print formatted summary
    print("="*80)
    print("WEEK 13 CONSENSUS PREDICTIONS: MODELS A, B, E")
    print("Favorite vs Underdog Cover Predictions")
    print("="*80)
    
    # Count favorite vs underdog covers
    favorite_covers = (result_df['consensus_prediction'] == 'Favorite covers').sum()
    underdog_covers = (result_df['consensus_prediction'] == 'Underdog covers').sum()
    
    print(f"\nTotal games: {len(result_df)}")
    print(f"\nConsensus Predictions:")
    print(f"  Favorite covers: {favorite_covers} games")
    print(f"  Underdog covers: {underdog_covers} games")
    
    # Full agreement games
    full_agreement = result_df[result_df['cover_votes'].isin([0, 3])]
    print(f"\nFull Agreement (3/3 models): {len(full_agreement)} games")
    
    # Print detailed predictions
    print(f"\n" + "="*80)
    print("DETAILED PREDICTIONS")
    print("="*80)
    
    for _, row in result_df.iterrows():
        print(f"\n{row['game']}")
        print(f"  Spread: {row['spread']}")
        print(f"  🎯 Consensus: {row['consensus_detail']} ({row['agreement']} models)")
        print(f"  Model A: {row['model_a']} ({row['model_a_prob']}, {row['model_a_conf']})")
        print(f"  Model B: {row['model_b']} ({row['model_b_prob']}, {row['model_b_conf']})")
        print(f"  Model E: {row['model_e']} ({row['model_e_prob']}, {row['model_e_conf']})")
    
    # Summary by agreement level
    print(f"\n" + "="*80)
    print("PREDICTIONS BY AGREEMENT LEVEL")
    print("="*80)
    
    print(f"\n=== Full Agreement (3/3) ===")
    for _, row in result_df[result_df['cover_votes'].isin([0, 3])].iterrows():
        print(f"{row['game']}: {row['consensus_detail']}")
    
    print(f"\n=== Partial Agreement (2/3) ===")
    for _, row in result_df[result_df['cover_votes'] == 2].iterrows():
        print(f"{row['game']}: {row['consensus_detail']}")
    
    print(f"\n=== Split Decisions (1/3) ===")
    for _, row in result_df[result_df['cover_votes'] == 1].iterrows():
        print(f"{row['game']}: {row['consensus_detail']}")
    
    print(f"\n✅ Saved formatted predictions to {output_file}")

if __name__ == "__main__":
    main()

