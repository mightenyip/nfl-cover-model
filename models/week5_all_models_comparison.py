#!/usr/bin/env python3
"""
Week 5 All Models Comparison
Combine predictions from all four models for comprehensive analysis
"""

import pandas as pd
import numpy as np
import os

def create_week5_comparison():
    """Create comprehensive Week 5 predictions comparison"""
    
    print("=== Week 5 All Models Comparison ===")
    
    # Load all model predictions
    model_a = pd.read_csv("model_a/model_a_week5_predictions.csv")
    model_b = pd.read_csv("model_b/model_b_v2_week5_predictions.csv")
    model_c = pd.read_csv("model_c/model_c_week5_updated_predictions.csv")
    model_d = pd.read_csv("model_d/model_d_week5_predictions.csv")
    
    print(f"Loaded predictions from all models")
    print(f"Model A: {len(model_a)} games")
    print(f"Model B: {len(model_b)} games")
    print(f"Model C: {len(model_c)} games")
    print(f"Model D: {len(model_d)} games")
    
    # Create comparison DataFrame
    comparison_data = []
    
    for i in range(len(model_a)):
        game_a = model_a.iloc[i]
        game_b = model_b.iloc[i]
        game_c = model_c.iloc[i]
        game_d = model_d.iloc[i]
        
        # Count consensus predictions
        cover_predictions = sum([
            game_a['predicted_cover'],
            game_b['predicted_cover'],
            game_c['predicted_cover'],
            game_d['predicted_cover']
        ])
        
        consensus_cover = cover_predictions >= 3
        consensus_no_cover = cover_predictions <= 1
        
        # Calculate average confidence (convert to numeric)
        conf_map = {'VERY_HIGH': 5, 'HIGH': 4, 'MEDIUM': 3, 'LOW': 2, 'VERY_LOW': 1}
        
        avg_confidence = np.mean([
            conf_map.get(game_a['confidence'], 3),
            conf_map.get(game_b['confidence'], 3),
            conf_map.get(game_c['confidence'], 3),
            conf_map.get(game_d['confidence'], 3)
        ])
        
        # Determine consensus confidence level
        if avg_confidence >= 4.5:
            consensus_conf = 'VERY_HIGH'
        elif avg_confidence >= 3.5:
            consensus_conf = 'HIGH'
        elif avg_confidence >= 2.5:
            consensus_conf = 'MEDIUM'
        else:
            consensus_conf = 'LOW'
        
        # Calculate average probability
        avg_prob = np.mean([
            game_a['cover_probability'],
            game_b['cover_probability'],
            game_c['probability'],
            0.7 if game_d['predicted_cover'] else 0.3  # Model D doesn't have explicit probabilities
        ])
        
        comparison_data.append({
            'Game': f"{game_a['away_team']} at {game_a['home_team']}",
            'Underdog': game_a['underdog_team'],
            'Spread': game_a['spread_line'],
            'Total': game_a['total_line'],
            'Model_A_Pred': 'Cover' if game_a['predicted_cover'] else 'No Cover',
            'Model_A_Conf': game_a['confidence'],
            'Model_A_Prob': f"{game_a['cover_probability']:.1%}",
            'Model_B_Pred': 'Cover' if game_b['predicted_cover'] else 'No Cover',
            'Model_B_Conf': game_b['confidence'],
            'Model_B_Prob': f"{game_b['cover_probability']:.1%}",
            'Model_C_Pred': 'Cover' if game_c['predicted_cover'] else 'No Cover',
            'Model_C_Conf': game_c['confidence'],
            'Model_C_Prob': f"{game_c['probability']:.1%}",
            'Model_D_Pred': 'Cover' if game_d['predicted_cover'] else 'No Cover',
            'Model_D_Conf': game_d['confidence'],
            'Cover_Count': cover_predictions,
            'Consensus': 'Cover' if consensus_cover else ('No Cover' if consensus_no_cover else 'Split'),
            'Consensus_Conf': consensus_conf,
            'Avg_Probability': f"{avg_prob:.1%}"
        })
    
    # Create DataFrame
    comparison_df = pd.DataFrame(comparison_data)
    
    # Sort by consensus confidence and cover count
    comparison_df['sort_score'] = comparison_df.apply(lambda x: 
        (5 if x['Consensus_Conf'] == 'VERY_HIGH' else 
         4 if x['Consensus_Conf'] == 'HIGH' else 
         3 if x['Consensus_Conf'] == 'MEDIUM' else 2) + 
        (0.1 if x['Consensus'] == 'Cover' or x['Consensus'] == 'No Cover' else 0), axis=1)
    
    comparison_df = comparison_df.sort_values('sort_score', ascending=False)
    comparison_df = comparison_df.drop('sort_score', axis=1)
    
    print(f"\n=== Week 5 Model Consensus Analysis ===")
    
    # Summary statistics
    total_games = len(comparison_df)
    consensus_games = len(comparison_df[comparison_df['Consensus'] != 'Split'])
    split_games = len(comparison_df[comparison_df['Consensus'] == 'Split'])
    
    print(f"Total Games: {total_games}")
    print(f"Consensus Games: {consensus_games} ({consensus_games/total_games:.1%})")
    print(f"Split Decisions: {split_games} ({split_games/total_games:.1%})")
    
    # Show consensus picks
    consensus_picks = comparison_df[comparison_df['Consensus'] != 'Split']
    if len(consensus_picks) > 0:
        print(f"\n=== Consensus Picks ({len(consensus_picks)} games) ===")
        for _, row in consensus_picks.iterrows():
            print(f"{row['Game']}: {row['Underdog']} {row['Spread']} - {row['Consensus']} ({row['Consensus_Conf']}, {row['Avg_Probability']})")
    
    # Show split decisions
    if split_games > 0:
        print(f"\n=== Split Decisions ({split_games} games) ===")
        for _, row in comparison_df[comparison_df['Consensus'] == 'Split'].iterrows():
            print(f"{row['Game']}: {row['Underdog']} {row['Spread']} - Split Decision ({row['Cover_Count']}/4 models pick Cover)")
    
    # High confidence consensus picks
    high_conf_consensus = consensus_picks[consensus_picks['Consensus_Conf'].isin(['HIGH', 'VERY_HIGH'])]
    if len(high_conf_consensus) > 0:
        print(f"\n=== High Confidence Consensus Picks ({len(high_conf_consensus)} games) ===")
        for _, row in high_conf_consensus.iterrows():
            print(f"{row['Game']}: {row['Underdog']} {row['Spread']} - {row['Consensus']} ({row['Consensus_Conf']}, {row['Avg_Probability']})")
            print(f"  Models: A({row['Model_A_Pred']}), B({row['Model_B_Pred']}), C({row['Model_C_Pred']}), D({row['Model_D_Pred']})")
    
    # Save comparison
    comparison_df.to_csv("week5_all_models_comparison.csv", index=False)
    print(f"\n✅ Week 5 all models comparison saved to: week5_all_models_comparison.csv")
    
    return comparison_df

if __name__ == "__main__":
    create_week5_comparison()
