#!/usr/bin/env python3
"""
Week 8 Consensus Predictions
Combine all model predictions to create consensus picks
"""

import pandas as pd
import numpy as np

def load_all_model_predictions():
    """Load predictions from all models"""
    
    models = {}
    
    # Model A
    try:
        model_a = pd.read_csv("models/model_a/model_a_week8_predictions.csv")
        models['Model_A'] = model_a
        print(f"✅ Loaded Model A: {len(model_a)} predictions")
    except FileNotFoundError:
        print("❌ Model A predictions not found")
    
    # Model B
    try:
        model_b = pd.read_csv("models/model_b/model_b_week8_predictions.csv")
        models['Model_B'] = model_b
        print(f"✅ Loaded Model B: {len(model_b)} predictions")
    except FileNotFoundError:
        print("❌ Model B predictions not found")
    
    # Model C
    try:
        model_c = pd.read_csv("model_c_updated_predictions.csv")
        models['Model_C'] = model_c
        print(f"✅ Loaded Model C: {len(model_c)} predictions")
    except FileNotFoundError:
        print("❌ Model C predictions not found")
    
    # Model D
    try:
        model_d = pd.read_csv("models/model_d/model_d_week8_predictions.csv")
        models['Model_D'] = model_d
        print(f"✅ Loaded Model D: {len(model_d)} predictions")
    except FileNotFoundError:
        print("❌ Model D predictions not found")
    
    # Model E
    try:
        model_e = pd.read_csv("models/model_e/model_e_week8_predictions.csv")
        models['Model_E'] = model_e
        print(f"✅ Loaded Model E: {len(model_e)} predictions")
    except FileNotFoundError:
        print("❌ Model E predictions not found")
    
    return models

def create_consensus_predictions(models):
    """Create consensus predictions from all models"""
    
    print("\n=== Creating Consensus Predictions ===")
    print("=" * 60)
    
    # Get all games from the first model
    first_model = list(models.values())[0]
    consensus_predictions = []
    
    for idx, row in first_model.iterrows():
        game = row['game']
        favorite = row['favorite']
        underdog = row['underdog']
        spread = row['spread']
        
        # Collect predictions from all models
        model_predictions = {}
        model_probabilities = {}
        
        for model_name, model_df in models.items():
            game_row = model_df[model_df['game'] == game]
            if not game_row.empty:
                model_predictions[model_name] = game_row['predicted_cover'].iloc[0]
                # Handle different column names for probability
                if 'cover_probability' in game_row.columns:
                    model_probabilities[model_name] = game_row['cover_probability'].iloc[0]
                elif 'probability' in game_row.columns:
                    model_probabilities[model_name] = game_row['probability'].iloc[0] / 100.0  # Convert percentage to decimal
                else:
                    model_probabilities[model_name] = 0.5  # Default if no probability column
        
        # Calculate consensus
        if model_predictions:
            # Count votes for underdog cover
            underdog_votes = sum(1 for pred in model_predictions.values() if pred)
            total_votes = len(model_predictions)
            
            # Consensus prediction (majority vote)
            consensus_cover = underdog_votes > total_votes / 2
            
            # Average probability
            avg_probability = np.mean(list(model_probabilities.values()))
            
            # Agreement level
            agreement = max(underdog_votes, total_votes - underdog_votes) / total_votes
            
            # Confidence based on agreement
            if agreement >= 0.8:
                confidence = "HIGH"
            elif agreement >= 0.6:
                confidence = "MEDIUM"
            else:
                confidence = "LOW"
            
            # Model breakdown
            model_breakdown = {}
            for model_name, pred in model_predictions.items():
                model_breakdown[model_name] = "Cover" if pred else "No Cover"
            
            consensus_predictions.append({
                'game': game,
                'favorite': favorite,
                'underdog': underdog,
                'spread': spread,
                'consensus_prediction': "Cover" if consensus_cover else "No Cover",
                'consensus_probability': avg_probability,
                'confidence': confidence,
                'agreement': agreement,
                'underdog_votes': underdog_votes,
                'total_votes': total_votes,
                'model_breakdown': str(model_breakdown)
            })
            
            print(f"{game}:")
            print(f"  Consensus: {'Cover' if consensus_cover else 'No Cover'} ({avg_probability:.1%})")
            print(f"  Agreement: {agreement:.1%} ({confidence})")
            print(f"  Votes: {underdog_votes}/{total_votes} for underdog")
            print(f"  Models: {model_breakdown}")
            print()
    
    return consensus_predictions

def main():
    """Main function"""
    print("=== Week 8 Consensus Predictions ===")
    print("Combining all model predictions")
    print("=" * 60)
    
    # Load all model predictions
    models = load_all_model_predictions()
    
    if not models:
        print("❌ No model predictions found")
        return
    
    # Create consensus
    consensus = create_consensus_predictions(models)
    
    # Save consensus predictions
    consensus_df = pd.DataFrame(consensus)
    output_file = "predictions/week8_consensus_predictions.csv"
    consensus_df.to_csv(output_file, index=False)
    
    # Summary
    total_games = len(consensus)
    underdog_covers = sum(1 for p in consensus if p['consensus_prediction'] == 'Cover')
    favorite_covers = total_games - underdog_covers
    
    print(f"=== Week 8 Consensus Summary ===")
    print(f"Total games: {total_games}")
    print(f"Underdog covers predicted: {underdog_covers}")
    print(f"Favorite covers predicted: {favorite_covers}")
    print(f"Average consensus probability: {np.mean([p['consensus_probability'] for p in consensus]):.1%}")
    
    # Confidence distribution
    confidence_counts = {}
    for p in consensus:
        conf = p['confidence']
        confidence_counts[conf] = confidence_counts.get(conf, 0) + 1
    
    print(f"\nConsensus Confidence Distribution:")
    for conf in ['HIGH', 'MEDIUM', 'LOW']:
        count = confidence_counts.get(conf, 0)
        print(f"  {conf}: {count} games")
    
    # Agreement analysis
    high_agreement = sum(1 for p in consensus if p['agreement'] >= 0.8)
    medium_agreement = sum(1 for p in consensus if 0.6 <= p['agreement'] < 0.8)
    low_agreement = sum(1 for p in consensus if p['agreement'] < 0.6)
    
    print(f"\nAgreement Analysis:")
    print(f"  High Agreement (≥80%): {high_agreement} games")
    print(f"  Medium Agreement (60-79%): {medium_agreement} games")
    print(f"  Low Agreement (<60%): {low_agreement} games")
    
    print(f"\n✅ Week 8 consensus predictions saved to {output_file}")

if __name__ == "__main__":
    main()
