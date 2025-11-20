#!/usr/bin/env python3
"""
Create Week 12 Consensus Predictions
Combine Model A, B, and E predictions into final consensus format
"""

import pandas as pd
import numpy as np

def load_week12_odds():
    """Load Week 12 odds"""
    try:
        odds_df = pd.read_csv("schedule/week12_2025_odds.csv")
        return odds_df
    except FileNotFoundError:
        print("❌ Error: schedule/week12_2025_odds.csv not found")
        return None

def load_model_predictions():
    """Load predictions from all three models"""
    models = {}
    
    # Model A
    try:
        model_a = pd.read_csv("models/model_a/model_a_week12_predictions.csv")
        models['A'] = model_a
        print(f"✅ Loaded Model A: {len(model_a)} predictions")
    except FileNotFoundError:
        print("❌ Model A predictions not found")
        return None
    
    # Model B
    try:
        model_b = pd.read_csv("models/model_b/model_b_week12_predictions.csv")
        models['B'] = model_b
        print(f"✅ Loaded Model B: {len(model_b)} predictions")
    except FileNotFoundError:
        print("❌ Model B predictions not found")
        return None
    
    # Model E
    try:
        model_e = pd.read_csv("models/model_e/model_e_week12_predictions.csv")
        models['E'] = model_e
        print(f"✅ Loaded Model E: {len(model_e)} predictions")
    except FileNotFoundError:
        print("❌ Model E predictions not found")
        return None
    
    return models

def create_consensus_predictions(odds_df, models):
    """Create consensus predictions in week11 format"""
    
    predictions = []
    
    for idx, row in odds_df.iterrows():
        game = f"{row['away_team']} @ {row['home_team']}"
        away_team = row['away_team']
        home_team = row['home_team']
        favorite = row['favorite_team']
        underdog = row['underdog_team']
        spread = row['spread_line']
        total = row['total_line']
        
        # Get predictions from each model
        model_a_row = models['A'][models['A']['game'] == game]
        model_b_row = models['B'][models['B']['game'] == game]
        model_e_row = models['E'][models['E']['game'] == game]
        
        if model_a_row.empty or model_b_row.empty or model_e_row.empty:
            print(f"⚠️ Missing predictions for {game}")
            continue
        
        # Model A predictions
        model_a_pred = "Cover" if model_a_row['predicted_cover'].iloc[0] else "No Cover"
        model_a_prob = model_a_row['cover_probability'].iloc[0]
        model_a_conf = model_a_row['confidence'].iloc[0]
        
        # Model B predictions
        model_b_pred = "Cover" if model_b_row['predicted_cover'].iloc[0] else "No Cover"
        model_b_prob = model_b_row['cover_probability'].iloc[0]
        model_b_conf = model_b_row['confidence'].iloc[0]
        
        # Model E predictions
        model_e_pred = "Cover" if model_e_row['predicted_cover'].iloc[0] else "No Cover"
        model_e_prob = model_e_row['cover_probability'].iloc[0]
        model_e_conf = model_e_row['confidence'].iloc[0]
        
        # Count votes for underdog cover
        underdog_votes = sum([
            model_a_row['predicted_cover'].iloc[0],
            model_b_row['predicted_cover'].iloc[0],
            model_e_row['predicted_cover'].iloc[0]
        ])
        total_votes = 3
        
        # Consensus prediction (majority vote)
        consensus_cover = underdog_votes >= 2
        
        # Average probability
        consensus_prob = np.mean([model_a_prob, model_b_prob, model_e_prob])
        
        # Determine agreement level
        if underdog_votes == 3:
            agreement = "Unanimous (3/3)"
            consensus_votes = "3/3"
        elif underdog_votes == 2:
            # Determine which models agree (underdog covers)
            agreeing_models = []
            if model_a_row['predicted_cover'].iloc[0]:
                agreeing_models.append('A')
            if model_b_row['predicted_cover'].iloc[0]:
                agreeing_models.append('B')
            if model_e_row['predicted_cover'].iloc[0]:
                agreeing_models.append('E')
            agreement = f"Majority ({', '.join(agreeing_models)})"
            consensus_votes = "2/3"
        elif underdog_votes == 1:
            # Determine which models agree (favorite covers - the majority)
            agreeing_models = []
            if not model_a_row['predicted_cover'].iloc[0]:
                agreeing_models.append('A')
            if not model_b_row['predicted_cover'].iloc[0]:
                agreeing_models.append('B')
            if not model_e_row['predicted_cover'].iloc[0]:
                agreeing_models.append('E')
            agreement = f"Majority ({', '.join(agreeing_models)})"
            consensus_votes = "2/3"
        else:  # underdog_votes == 0
            agreement = "Unanimous (3/3)"
            consensus_votes = "3/3"
        
        consensus_pred = "Cover" if consensus_cover else "No Cover"
        
        predictions.append({
            'game': game,
            'away_team': away_team,
            'home_team': home_team,
            'favorite_team': favorite,
            'underdog_team': underdog,
            'spread_line': spread,
            'total_line': total,
            'consensus_prediction': consensus_pred,
            'consensus_probability': round(consensus_prob, 3),
            'consensus_votes': consensus_votes,
            'agreement': agreement,
            'model_a_prediction': model_a_pred,
            'model_a_probability': round(model_a_prob, 3),
            'model_a_confidence': model_a_conf,
            'model_b_prediction': model_b_pred,
            'model_b_probability': round(model_b_prob, 3),
            'model_b_confidence': model_b_conf,
            'model_e_prediction': model_e_pred,
            'model_e_probability': round(model_e_prob, 3),
            'model_e_confidence': model_e_conf,
            'underdog_votes': underdog_votes,
            'total_votes': total_votes
        })
    
    return pd.DataFrame(predictions)

def main():
    """Main function"""
    print("=== Week 12 Consensus Predictions ===")
    print("Combining Model A, B, and E predictions")
    print("=" * 60)
    
    # Load odds
    odds_df = load_week12_odds()
    if odds_df is None:
        return
    
    # Load model predictions
    models = load_model_predictions()
    if models is None:
        return
    
    # Create consensus
    consensus_df = create_consensus_predictions(odds_df, models)
    
    # Save
    output_file = "predictions/week12_predictions_final.csv"
    consensus_df.to_csv(output_file, index=False)
    
    # Summary
    total_games = len(consensus_df)
    underdog_covers = sum(consensus_df['consensus_prediction'] == 'Cover')
    favorite_covers = total_games - underdog_covers
    
    print(f"\n=== Week 12 Consensus Summary ===")
    print(f"Total games: {total_games}")
    print(f"Underdog covers predicted: {underdog_covers}")
    print(f"Favorite covers predicted: {favorite_covers}")
    print(f"Average consensus probability: {consensus_df['consensus_probability'].mean():.1%}")
    
    # Agreement analysis
    unanimous = sum(consensus_df['consensus_votes'] == '3/3')
    majority = sum(consensus_df['consensus_votes'] == '2/3')
    split = sum(consensus_df['consensus_votes'] == '1/3')
    
    print(f"\nAgreement Analysis:")
    print(f"  Unanimous (3/3): {unanimous} games")
    print(f"  Majority (2/3): {majority} games")
    print(f"  Split (1/3): {split} games")
    
    print(f"\n✅ Week 12 consensus predictions saved to {output_file}")
    
    return consensus_df

if __name__ == "__main__":
    main()

