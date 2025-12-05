#!/usr/bin/env python3
"""
Week 14 Consensus Predictions for Models A, B, and E only
"""

import pandas as pd
import numpy as np

def main():
    # Load the full comparison
    df = pd.read_csv("week14_all_models_predictions.csv")
    
    # Create consensus based on A, B, E only
    results = []
    
    for _, row in df.iterrows():
        game = row['game']
        favorite = row['favorite']
        underdog = row['underdog']
        spread = row['spread']
        total = row['total']
        
        # Get predictions from A, B, E
        model_a = row['model_a_prediction'] == 'Cover'
        model_b = row['model_b_prediction'] == 'Cover'
        model_e = row['model_e_prediction'] == 'Cover'
        
        # Count cover votes
        cover_votes = sum([model_a, model_b, model_e])
        
        # Consensus (majority vote: 2 out of 3)
        consensus = "Cover" if cover_votes >= 2 else "No Cover"
        
        # Average probability (convert percentages to decimals first)
        probs = []
        if pd.notna(row['model_a_probability']) and str(row['model_a_probability']) != 'N/A':
            prob_str = str(row['model_a_probability']).replace('%', '')
            probs.append(float(prob_str) / 100)
        if pd.notna(row['model_b_probability']) and str(row['model_b_probability']) != 'N/A':
            prob_str = str(row['model_b_probability']).replace('%', '')
            probs.append(float(prob_str) / 100)
        if pd.notna(row['model_e_probability']) and str(row['model_e_probability']) != 'N/A':
            prob_str = str(row['model_e_probability']).replace('%', '')
            probs.append(float(prob_str) / 100)
        
        avg_prob = np.mean(probs) if probs else None
        
        results.append({
            'game': game,
            'favorite': favorite,
            'underdog': underdog,
            'spread': spread,
            'total': total,
            'model_a': row['model_a_prediction'],
            'model_a_prob': row['model_a_probability'],
            'model_a_conf': row['model_a_confidence'],
            'model_b': row['model_b_prediction'],
            'model_b_prob': row['model_b_probability'],
            'model_b_conf': row['model_b_confidence'],
            'model_e': row['model_e_prediction'],
            'model_e_prob': row['model_e_probability'],
            'model_e_conf': row['model_e_confidence'],
            'consensus_abe': consensus,
            'cover_votes_abe': cover_votes,
            'avg_probability': f"{avg_prob:.1%}" if avg_prob else "N/A"
        })
    
    result_df = pd.DataFrame(results)
    
    # Save to CSV
    output_file = "week14_abe_consensus_predictions.csv"
    result_df.to_csv(output_file, index=False)
    
    # Print summary
    print("="*80)
    print("WEEK 13 CONSENSUS PREDICTIONS: MODELS A, B, E ONLY")
    print("="*80)
    print(f"\nTotal games: {len(result_df)}")
    
    # Count consensus predictions
    consensus_covers = (result_df['consensus_abe'] == 'Cover').sum()
    consensus_no_covers = (result_df['consensus_abe'] == 'No Cover').sum()
    
    print(f"\nConsensus Predictions:")
    print(f"  Cover: {consensus_covers}")
    print(f"  No Cover: {consensus_no_covers}")
    
    # Individual model counts
    print(f"\nIndividual Model Predictions:")
    print(f"  Model A - Cover: {(result_df['model_a'] == 'Cover').sum()}, No Cover: {(result_df['model_a'] == 'No Cover').sum()}")
    print(f"  Model B - Cover: {(result_df['model_b'] == 'Cover').sum()}, No Cover: {(result_df['model_b'] == 'No Cover').sum()}")
    print(f"  Model E - Cover: {(result_df['model_e'] == 'Cover').sum()}, No Cover: {(result_df['model_e'] == 'No Cover').sum()}")
    
    # Agreement analysis
    print(f"\nAgreement Analysis:")
    for votes in range(4):
        count = (result_df['cover_votes_abe'] == votes).sum()
        if count > 0:
            print(f"  {votes}/3 models predict Cover: {count} games")
    
    # Full agreement
    full_agreement_cover = (result_df['cover_votes_abe'] == 3).sum()
    full_agreement_no_cover = (result_df['cover_votes_abe'] == 0).sum()
    print(f"\nFull agreement (3/3):")
    print(f"  Cover: {full_agreement_cover} games")
    print(f"  No Cover: {full_agreement_no_cover} games")
    
    # Print detailed predictions
    print(f"\n" + "="*80)
    print("DETAILED PREDICTIONS")
    print("="*80)
    for _, row in result_df.iterrows():
        print(f"\n{row['game']}")
        print(f"  Spread: {row['spread']} | Total: {row['total']}")
        print(f"  Model A: {row['model_a']} ({row['model_a_prob']}, {row['model_a_conf']})")
        print(f"  Model B: {row['model_b']} ({row['model_b_prob']}, {row['model_b_conf']})")
        print(f"  Model E: {row['model_e']} ({row['model_e_prob']}, {row['model_e_conf']})")
        print(f"  🎯 Consensus (A/B/E): {row['consensus_abe']} ({row['cover_votes_abe']}/3)")
    
    print(f"\n✅ Saved to {output_file}")

if __name__ == "__main__":
    main()

