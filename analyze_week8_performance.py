"""
Analyze Week 8 model performance against actual results
"""

import pandas as pd

def analyze_week8():
    """Analyze Week 8 model performance"""
    
    # Load actual results
    actual_results = pd.read_csv("data/week8_ats_results.csv")
    
    # Load predictions
    model_a = pd.read_csv("models/model_a/model_a_week8_predictions.csv")
    model_b = pd.read_csv("models/model_b/model_b_week8_predictions.csv")
    model_c = pd.read_csv("models/model_c/model_c_week8_real_ats_predictions.csv")
    model_d = pd.read_csv("models/model_d/model_d_week8_predictions.csv")
    model_e = pd.read_csv("models/model_e/model_e_week8_predictions.csv")
    consensus = pd.read_csv("predictions/week8_consensus_predictions.csv")
    
    # Create mapping from game format
    results_data = []
    
    for _, actual in actual_results.iterrows():
        game_name = actual['game']
        
        # Parse game name to get teams
        parts = game_name.split(' @ ')
        if len(parts) != 2:
            continue
        away_team = parts[0]
        home_team = parts[1]
        
        # Find predictions for this game - try different formats
        model_a_pred = model_a[model_a['game'] == game_name] if 'game' in model_a.columns else pd.DataFrame()
        model_b_pred = model_b[model_b['game'] == game_name] if 'game' in model_b.columns else pd.DataFrame()
        
        # Model C uses away_team/home_team format
        model_c_pred = model_c[(model_c['away_team'] == away_team) & (model_c['home_team'] == home_team)] if 'away_team' in model_c.columns else pd.DataFrame()
        
        model_d_pred = model_d[model_d['game'] == game_name] if 'game' in model_d.columns else pd.DataFrame()
        model_e_pred = model_e[model_e['game'] == game_name] if 'game' in model_e.columns else pd.DataFrame()
        consensus_pred = consensus[consensus['game'] == game_name] if 'game' in consensus.columns else pd.DataFrame()
        
        if len(model_a_pred) == 0:
            continue
        
        # Get predictions
        model_a_cover = model_a_pred.iloc[0]['predicted_cover'] if len(model_a_pred) > 0 and 'predicted_cover' in model_a_pred.columns else None
        model_b_cover = model_b_pred.iloc[0]['predicted_cover'] if len(model_b_pred) > 0 and 'predicted_cover' in model_b_pred.columns else None
        model_c_cover = model_c_pred.iloc[0]['predicted_cover'] if len(model_c_pred) > 0 and 'predicted_cover' in model_c_pred.columns else None
        model_d_cover = model_d_pred.iloc[0]['predicted_cover'] if len(model_d_pred) > 0 and 'predicted_cover' in model_d_pred.columns else None
        model_e_cover = model_e_pred.iloc[0]['predicted_cover'] if len(model_e_pred) > 0 and 'predicted_cover' in model_e_pred.columns else None
        
        # Consensus prediction
        consensus_cover = None
        if len(consensus_pred) > 0:
            consensus_str = consensus_pred.iloc[0]['consensus_prediction']
            consensus_cover = consensus_str == 'Cover'
        
        # Actual result
        actual_cover = actual['underdog_covered']
        
        # Calculate correctness
        model_a_correct = (model_a_cover == actual_cover) if model_a_cover is not None else None
        model_b_correct = (model_b_cover == actual_cover) if model_b_cover is not None else None
        model_c_correct = (model_c_cover == actual_cover) if model_c_cover is not None else None
        model_d_correct = (model_d_cover == actual_cover) if model_d_cover is not None else None
        model_e_correct = (model_e_cover == actual_cover) if model_e_cover is not None else None
        consensus_correct = (consensus_cover == actual_cover) if consensus_cover is not None else None
        
        results_data.append({
            'game': game_name,
            'actual_cover': actual_cover,
            'model_a_pred': model_a_cover,
            'model_a_correct': model_a_correct,
            'model_b_pred': model_b_cover,
            'model_b_correct': model_b_correct,
            'model_c_pred': model_c_cover,
            'model_c_correct': model_c_correct,
            'model_d_pred': model_d_cover,
            'model_d_correct': model_d_correct,
            'model_e_pred': model_e_cover,
            'model_e_correct': model_e_correct,
            'consensus_pred': consensus_cover,
            'consensus_correct': consensus_correct
        })
    
    df = pd.DataFrame(results_data)
    
    # Calculate totals
    total = len(df)
    model_a_correct = df['model_a_correct'].sum()
    model_b_correct = df['model_b_correct'].sum()
    model_c_correct = df['model_c_correct'].sum()
    model_d_correct = df['model_d_correct'].sum()
    model_e_correct = df['model_e_correct'].sum()
    consensus_correct = df['consensus_correct'].sum()
    
    print(f"Week 8 Performance:")
    print(f"Total Games: {total}")
    print(f"Model A: {model_a_correct}/{total} ({model_a_correct/total*100:.1f}%)")
    print(f"Model B: {model_b_correct}/{total} ({model_b_correct/total*100:.1f}%)")
    print(f"Model C: {model_c_correct}/{total} ({model_c_correct/total*100:.1f}%)")
    print(f"Model D: {model_d_correct}/{total} ({model_d_correct/total*100:.1f}%)")
    print(f"Model E: {model_e_correct}/{total} ({model_e_correct/total*100:.1f}%)")
    print(f"Consensus: {consensus_correct}/{total} ({consensus_correct/total*100:.1f}%)")
    
    # Save results
    df.to_csv("data/week8_actual_results_analysis.csv", index=False)
    
    return {
        'week': 8,
        'total': total,
        'model_a': model_a_correct,
        'model_b': model_b_correct,
        'model_c': model_c_correct,
        'model_d': model_d_correct,
        'model_e': model_e_correct,
        'consensus': consensus_correct
    }

if __name__ == "__main__":
    analyze_week8()

