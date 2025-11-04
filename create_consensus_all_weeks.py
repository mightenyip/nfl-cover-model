"""
Create consensus predictions for all weeks
Combine all model predictions to create consensus
"""

import pandas as pd
import os
import numpy as np

def get_team_mapping():
    """Get team name to abbreviation mapping"""
    return {
        '49ers': 'SF', 'Bears': 'CHI', 'Bengals': 'CIN', 'Bills': 'BUF', 'Broncos': 'DEN',
        'Browns': 'CLE', 'Buccaneers': 'TB', 'Cardinals': 'ARI', 'Chargers': 'LAC', 'Chiefs': 'KC',
        'Colts': 'IND', 'Commanders': 'WAS', 'Cowboys': 'DAL', 'Dolphins': 'MIA', 'Eagles': 'PHI',
        'Falcons': 'ATL', 'Giants': 'NYG', 'Jaguars': 'JAX', 'Jets': 'NYJ', 'Lions': 'DET',
        'Packers': 'GB', 'Panthers': 'CAR', 'Patriots': 'NE', 'Raiders': 'LV', 'Rams': 'LA',
        'Ravens': 'BAL', 'Saints': 'NO', 'Seahawks': 'SEA', 'Steelers': 'PIT', 'Texans': 'HOU',
        'Titans': 'TEN', 'Vikings': 'MIN'
    }

def load_all_models_for_week(week_num):
    """Load all model predictions for a given week"""
    models = {}
    
    # Model A
    try:
        model_a = pd.read_csv(f"predictions/model_a_week{week_num}_predictions.csv")
        models['Model_A'] = model_a
    except:
        pass
    
    # Model B
    try:
        model_b = pd.read_csv(f"models/model_b/model_b_week{week_num}_predictions.csv")
        models['Model_B'] = model_b
    except:
        pass
    
    # Model C
    try:
        model_c = pd.read_csv(f"models/model_c/model_c_week{week_num}_predictions.csv")
        models['Model_C'] = model_c
    except:
        pass
    
    # Model D
    try:
        model_d = pd.read_csv(f"models/model_d/model_d_week{week_num}_predictions.csv")
        models['Model_D'] = model_d
    except:
        pass
    
    # Model E
    try:
        model_e = pd.read_csv(f"models/model_e/model_e_week{week_num}_predictions.csv")
        models['Model_E'] = model_e
    except:
        pass
    
    return models

def create_consensus_for_week(week_num):
    """Create consensus predictions for a specific week"""
    
    models = load_all_models_for_week(week_num)
    
    if len(models) == 0:
        return None
    
    # Get all games from the first model
    first_model = list(models.values())[0]
    consensus_predictions = []
    
    for idx, row in first_model.iterrows():
        # Get game name - try different column names
        if 'game' in row:
            game = row['game']
        elif 'Game' in row:
            game = row['Game']
        else:
            continue
        
        # Get favorite and underdog
        favorite = row.get('favorite', row.get('favorite_team', ''))
        underdog = row.get('underdog', row.get('underdog_team', ''))
        spread = row.get('spread', row.get('spread_line', 0))
        
        # Collect predictions from all models
        model_predictions_dict = {}
        model_probabilities = {}
        
        for model_name, model_df in models.items():
            # Find matching game
            game_row = None
            if 'game' in model_df.columns:
                game_row = model_df[model_df['game'] == game]
            elif 'Game' in model_df.columns:
                game_row = model_df[model_df['Game'] == game]
            
            if not game_row.empty:
                # Get prediction
                if 'predicted_cover' in game_row.columns:
                    model_predictions_dict[model_name] = game_row['predicted_cover'].iloc[0]
                    if 'probability' in game_row.columns:
                        model_probabilities[model_name] = game_row['probability'].iloc[0]
                    elif 'cover_probability' in game_row.columns:
                        prob = game_row['cover_probability'].iloc[0]
                        model_probabilities[model_name] = prob if prob <= 1.0 else prob / 100.0
        
        # Calculate consensus
        if model_predictions_dict:
            # Count votes for underdog cover
            underdog_votes = sum(1 for pred in model_predictions_dict.values() if pred)
            total_votes = len(model_predictions_dict)
            
            # Consensus prediction (majority vote)
            consensus_cover = underdog_votes > total_votes / 2
            
            # Average probability
            normalized_probs = []
            for prob in model_probabilities.values():
                if prob > 1.0:  # If it's a percentage, convert to decimal
                    normalized_probs.append(prob / 100.0)
                else:
                    normalized_probs.append(prob)
            avg_probability = np.mean(normalized_probs) if normalized_probs else 0.5
            
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
            for model_name, pred in model_predictions_dict.items():
                model_breakdown[model_name] = "Cover" if pred else "No Cover"
            
            consensus_predictions.append({
                'game': game,
                'favorite': favorite,
                'underdog': underdog,
                'spread': spread,
                'consensus_prediction': 'Cover' if consensus_cover else 'No Cover',
                'consensus_probability': avg_probability,
                'confidence': confidence,
                'agreement': agreement,
                'underdog_votes': underdog_votes,
                'total_votes': total_votes,
                'model_breakdown': str(model_breakdown)
            })
    
    return pd.DataFrame(consensus_predictions)

def create_all_consensus():
    """Create consensus predictions for all weeks"""
    
    for week in range(1, 10):
        print(f"\nGenerating consensus for Week {week}...")
        consensus = create_consensus_for_week(week)
        
        if consensus is not None and len(consensus) > 0:
            output_file = f"predictions/week{week}_consensus_predictions.csv"
            consensus.to_csv(output_file, index=False)
            print(f"✅ Saved consensus predictions: {output_file} ({len(consensus)} games)")
        else:
            print(f"⚠️  No consensus generated for Week {week}")

if __name__ == "__main__":
    print("Creating Consensus Predictions for All Weeks")
    print("=" * 80)
    create_all_consensus()
    print("\n✅ COMPLETED: Consensus predictions generated for all weeks")

