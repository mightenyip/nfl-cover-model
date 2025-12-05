#!/usr/bin/env python3
"""
Create predictions_final CSV files for Week 13 and Week 14
Similar format to Week 11 and Week 12 predictions_final files
"""

import pandas as pd
import numpy as np
import os

def create_predictions_final(week_num):
    """Create predictions_final CSV for a given week"""
    
    print(f"\n=== Creating Week {week_num} Predictions Final ===")
    
    # Load odds
    odds_file = f"schedule/week{week_num}_2025_odds.csv"
    if not os.path.exists(odds_file):
        print(f"❌ {odds_file} not found")
        return None
    
    odds_df = pd.read_csv(odds_file)
    
    # Load individual model predictions
    model_a_file = f"models/model_a/model_a_week{week_num}_predictions.csv"
    model_b_file = f"models/model_b/model_b_week{week_num}_predictions.csv"
    model_e_file = f"models/model_e/model_e_week{week_num}_predictions.csv"
    
    try:
        model_a = pd.read_csv(model_a_file)
        model_b = pd.read_csv(model_b_file)
        model_e = pd.read_csv(model_e_file)
    except FileNotFoundError as e:
        print(f"❌ Error loading model predictions: {e}")
        return None
    
    # Create predictions_final data
    predictions_final = []
    
    for idx, row in odds_df.iterrows():
        game = f"{row['away_team']} @ {row['home_team']}"
        
        # Find matching predictions from each model
        model_a_pred = model_a[model_a['game'] == game]
        model_b_pred = model_b[model_b['game'] == game]
        model_e_pred = model_e[model_e['game'] == game]
        
        if model_a_pred.empty or model_b_pred.empty or model_e_pred.empty:
            print(f"⚠️ Missing predictions for {game}")
            continue
        
        # Extract predictions and probabilities
        ma_cover = model_a_pred['predicted_cover'].iloc[0]
        ma_prob = model_a_pred['cover_probability'].iloc[0] if 'cover_probability' in model_a_pred.columns else 0.5
        ma_conf = model_a_pred['confidence'].iloc[0] if 'confidence' in model_a_pred.columns else 'MEDIUM'
        
        mb_cover = model_b_pred['predicted_cover'].iloc[0]
        mb_prob = model_b_pred['cover_probability'].iloc[0] if 'cover_probability' in model_b_pred.columns else 0.5
        mb_conf = model_b_pred['confidence'].iloc[0] if 'confidence' in model_b_pred.columns else 'MEDIUM'
        
        me_cover = model_e_pred['predicted_cover'].iloc[0]
        me_prob = model_e_pred['cover_probability'].iloc[0] if 'cover_probability' in model_e_pred.columns else 0.5
        me_conf = model_e_pred['confidence'].iloc[0] if 'confidence' in model_e_pred.columns else 'MEDIUM'
        
        # Count votes for underdog cover
        underdog_votes = sum([ma_cover, mb_cover, me_cover])
        total_votes = 3
        
        # Determine consensus
        consensus_cover = underdog_votes >= 2
        consensus_prediction = "Cover" if consensus_cover else "No Cover"
        
        # Calculate consensus probability (average of all three)
        consensus_probability = np.mean([ma_prob, mb_prob, me_prob])
        
        # Format consensus votes
        consensus_votes = f"{underdog_votes}/3"
        
        # Determine agreement level based on consensus (matching Week 11/12 format)
        if underdog_votes == 3:
            agreement = "Unanimous (3/3)"
        elif underdog_votes == 0:
            agreement = "Unanimous (0/3)"
        elif underdog_votes == 2:
            # Two models agree on underdog cover - determine which two
            if ma_cover and mb_cover:
                agreement = "Majority (A, B)"
            elif ma_cover and me_cover:
                agreement = "Majority (A, E)"
            else:  # mb_cover and me_cover
                agreement = "Majority (B, E)"
        else:  # underdog_votes == 1
            # Only one model says underdog cover - use "Split (1/3)" format
            agreement = "Split (1/3)"
        
        # Convert predictions to text
        ma_pred_text = "Cover" if ma_cover else "No Cover"
        mb_pred_text = "Cover" if mb_cover else "No Cover"
        me_pred_text = "Cover" if me_cover else "No Cover"
        
        predictions_final.append({
            'game': game,
            'away_team': row['away_team'],
            'home_team': row['home_team'],
            'favorite_team': row['favorite_team'],
            'underdog_team': row['underdog_team'],
            'spread_line': row['spread_line'],
            'total_line': row['total_line'],
            'consensus_prediction': consensus_prediction,
            'consensus_probability': round(consensus_probability, 3),
            'consensus_votes': consensus_votes,
            'agreement': agreement,
            'model_a_prediction': ma_pred_text,
            'model_a_probability': round(ma_prob, 3),
            'model_a_confidence': ma_conf,
            'model_b_prediction': mb_pred_text,
            'model_b_probability': round(mb_prob, 3),
            'model_b_confidence': mb_conf,
            'model_e_prediction': me_pred_text,
            'model_e_probability': round(me_prob, 3),
            'model_e_confidence': me_conf,
            'underdog_votes': underdog_votes,
            'total_votes': total_votes
        })
    
    # Create DataFrame
    final_df = pd.DataFrame(predictions_final)
    
    # Save to predictions folder
    output_file = f"predictions/week{week_num}_predictions_final.csv"
    os.makedirs("predictions", exist_ok=True)
    final_df.to_csv(output_file, index=False)
    
    print(f"✅ Created {output_file}")
    print(f"   Total games: {len(final_df)}")
    
    # Summary
    consensus_covers = (final_df['consensus_prediction'] == 'Cover').sum()
    consensus_no_covers = (final_df['consensus_prediction'] == 'No Cover').sum()
    
    print(f"   Consensus: {consensus_covers} Cover, {consensus_no_covers} No Cover")
    
    return final_df

def main():
    """Main function"""
    print("="*80)
    print("CREATE WEEK 13 & 14 PREDICTIONS FINAL FILES")
    print("="*80)
    
    # Create for Week 13
    week13_final = create_predictions_final(13)
    
    # Create for Week 14
    week14_final = create_predictions_final(14)
    
    print(f"\n✅ Successfully created predictions_final files for Weeks 13 and 14")

if __name__ == "__main__":
    main()

