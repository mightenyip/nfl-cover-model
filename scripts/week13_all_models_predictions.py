#!/usr/bin/env python3
"""
Week 13 All Models Predictions Comparison
Combine predictions from all models for Week 13
"""

import pandas as pd
import numpy as np
import os
import sys

def load_all_predictions():
    """Load predictions from all models"""
    
    predictions = {}
    
    # Model A
    try:
        model_a = pd.read_csv("models/model_a/model_a_week13_predictions.csv")
        predictions['Model_A'] = model_a
        print(f"✅ Loaded Model A: {len(model_a)} predictions")
    except FileNotFoundError:
        print("❌ Model A predictions not found")
        return None
    
    # Model B
    try:
        model_b = pd.read_csv("models/model_b/model_b_week13_predictions.csv")
        predictions['Model_B'] = model_b
        print(f"✅ Loaded Model B: {len(model_b)} predictions")
    except FileNotFoundError:
        print("❌ Model B predictions not found")
        return None
    
    # Model C
    try:
        model_c = pd.read_csv("models/model_c/model_c_week13_predictions.csv")
        predictions['Model_C'] = model_c
        print(f"✅ Loaded Model C: {len(model_c)} predictions")
    except FileNotFoundError:
        print("❌ Model C predictions not found")
        return None
    
    # Model D
    try:
        model_d = pd.read_csv("models/model_d/model_d_week13_predictions.csv")
        predictions['Model_D'] = model_d
        print(f"✅ Loaded Model D: {len(model_d)} predictions")
    except FileNotFoundError:
        print("❌ Model D predictions not found")
        return None
    
    # Model E
    try:
        model_e = pd.read_csv("models/model_e/model_e_week13_predictions.csv")
        predictions['Model_E'] = model_e
        print(f"✅ Loaded Model E: {len(model_e)} predictions")
    except FileNotFoundError:
        print("❌ Model E predictions not found")
        return None
    
    return predictions

def create_comparison(predictions):
    """Create a comparison of all model predictions"""
    
    print("\n=== Creating Week 13 All Models Comparison ===")
    
    # Use Model A as the base for game list
    base_model = predictions['Model_A']
    comparison_data = []
    
    # Load odds for spread and total info
    try:
        odds_df = pd.read_csv("schedule/week13_2025_odds.csv")
    except FileNotFoundError:
        print("⚠️  Could not load odds file, proceeding without spread/total")
        odds_df = None
    
    for idx, row in base_model.iterrows():
        game = row['game']
        favorite = row['favorite']
        underdog = row['underdog']
        spread = row['spread']
        
        # Get spread and total from odds if available
        total = None
        if odds_df is not None:
            game_odds = odds_df[
                (odds_df['favorite_team'] == favorite) & 
                (odds_df['underdog_team'] == underdog)
            ]
            if not game_odds.empty:
                total = game_odds['total_line'].iloc[0]
        
        # Get predictions from each model
        model_a_row = predictions['Model_A'][predictions['Model_A']['game'] == game]
        model_b_row = predictions['Model_B'][predictions['Model_B']['game'] == game]
        model_c_row = predictions['Model_C'][predictions['Model_C']['game'] == game]
        model_d_row = predictions['Model_D'][predictions['Model_D']['game'] == game]
        model_e_row = predictions['Model_E'][predictions['Model_E']['game'] == game]
        
        # Extract predictions and probabilities
        model_a_pred = model_a_row['predicted_cover'].iloc[0] if not model_a_row.empty else None
        model_a_prob = model_a_row['cover_probability'].iloc[0] if not model_a_row.empty and 'cover_probability' in model_a_row.columns else None
        model_a_conf = model_a_row['confidence'].iloc[0] if not model_a_row.empty else None
        
        model_b_pred = model_b_row['predicted_cover'].iloc[0] if not model_b_row.empty else None
        model_b_prob = model_b_row['cover_probability'].iloc[0] if not model_b_row.empty and 'cover_probability' in model_b_row.columns else None
        model_b_conf = model_b_row['confidence'].iloc[0] if not model_b_row.empty else None
        
        model_c_pred = model_c_row['predicted_cover'].iloc[0] if not model_c_row.empty else None
        model_c_prob = model_c_row['probability'].iloc[0] / 100.0 if not model_c_row.empty and 'probability' in model_c_row.columns else None
        model_c_conf = model_c_row['confidence'].iloc[0] if not model_c_row.empty else None
        
        model_d_pred = model_d_row['predicted_cover'].iloc[0] if not model_d_row.empty else None
        model_d_conf = model_d_row['confidence'].iloc[0] if not model_d_row.empty else None
        
        model_e_pred = model_e_row['predicted_cover'].iloc[0] if not model_e_row.empty else None
        model_e_prob = model_e_row['cover_probability'].iloc[0] if not model_e_row.empty and 'cover_probability' in model_e_row.columns else None
        model_e_conf = model_e_row['confidence'].iloc[0] if not model_e_row.empty else None
        
        # Count cover predictions
        cover_votes = sum([
            model_a_pred == True if model_a_pred is not None else False,
            model_b_pred == True if model_b_pred is not None else False,
            model_c_pred == True if model_c_pred is not None else False,
            model_d_pred == True if model_d_pred is not None else False,
            model_e_pred == True if model_e_pred is not None else False
        ])
        
        consensus = "Cover" if cover_votes >= 3 else "No Cover"
        
        comparison_data.append({
            'game': game,
            'away_team': row['away_team'],
            'home_team': row['home_team'],
            'favorite': favorite,
            'underdog': underdog,
            'spread': spread,
            'total': total,
            'model_a_prediction': "Cover" if model_a_pred else "No Cover" if model_a_pred is not None else "N/A",
            'model_a_probability': f"{model_a_prob:.1%}" if model_a_prob is not None else "N/A",
            'model_a_confidence': model_a_conf if model_a_conf else "N/A",
            'model_b_prediction': "Cover" if model_b_pred else "No Cover" if model_b_pred is not None else "N/A",
            'model_b_probability': f"{model_b_prob:.1%}" if model_b_prob is not None else "N/A",
            'model_b_confidence': model_b_conf if model_b_conf else "N/A",
            'model_c_prediction': "Cover" if model_c_pred else "No Cover" if model_c_pred is not None else "N/A",
            'model_c_probability': f"{model_c_prob:.1%}" if model_c_prob is not None else "N/A",
            'model_c_confidence': model_c_conf if model_c_conf else "N/A",
            'model_d_prediction': "Cover" if model_d_pred else "No Cover" if model_d_pred is not None else "N/A",
            'model_d_confidence': model_d_conf if model_d_conf else "N/A",
            'model_e_prediction': "Cover" if model_e_pred else "No Cover" if model_e_pred is not None else "N/A",
            'model_e_probability': f"{model_e_prob:.1%}" if model_e_prob is not None else "N/A",
            'model_e_confidence': model_e_conf if model_e_conf else "N/A",
            'consensus_prediction': consensus,
            'cover_votes': cover_votes,
            'total_votes': 5
        })
    
    return pd.DataFrame(comparison_data)

def main():
    """Main function"""
    
    print("="*80)
    print("WEEK 13 2025: ALL MODELS PREDICTIONS COMPARISON")
    print("="*80)
    
    # Load all predictions
    predictions = load_all_predictions()
    if predictions is None:
        print("❌ Failed to load predictions")
        return
    
    # Create comparison
    comparison_df = create_comparison(predictions)
    
    # Save comparison
    output_file = "week13_all_models_predictions.csv"
    comparison_df.to_csv(output_file, index=False)
    print(f"\n✅ Saved comparison to {output_file}")
    
    # Summary statistics
    print("\n" + "="*80)
    print("WEEK 13 PREDICTIONS SUMMARY")
    print("="*80)
    
    print(f"\nTotal games: {len(comparison_df)}")
    
    # Model predictions counts
    print(f"\n=== Model Predictions ===")
    for model in ['A', 'B', 'C', 'D', 'E']:
        col = f'model_{model.lower()}_prediction'
        if col in comparison_df.columns:
            cover_count = (comparison_df[col] == "Cover").sum()
            no_cover_count = (comparison_df[col] == "No Cover").sum()
            print(f"Model {model}: {cover_count} Cover, {no_cover_count} No Cover")
    
    # Consensus predictions
    consensus_covers = (comparison_df['consensus_prediction'] == "Cover").sum()
    consensus_no_covers = (comparison_df['consensus_prediction'] == "No Cover").sum()
    print(f"\nConsensus: {consensus_covers} Cover, {consensus_no_covers} No Cover")
    
    # Agreement analysis
    print(f"\n=== Agreement Analysis ===")
    for i in range(6):
        count = (comparison_df['cover_votes'] == i).sum()
        if count > 0:
            print(f"{i}/5 models predict Cover: {count} games")
    
    # Games with full agreement
    full_agreement_cover = (comparison_df['cover_votes'] == 5).sum()
    full_agreement_no_cover = (comparison_df['cover_votes'] == 0).sum()
    print(f"\nFull agreement (5/5): {full_agreement_cover} Cover, {full_agreement_no_cover} No Cover")
    
    print(f"\n✅ Week 13 all models comparison saved to {output_file}")

if __name__ == "__main__":
    main()

