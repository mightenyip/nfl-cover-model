"""
Create post-hoc Week 1 predictions using current model methodology
This generates what the models would have predicted for Week 1 games
"""

import pandas as pd
import sys
import os

# Add scripts directory to path
sys.path.append('scripts')

def load_epa_data():
    """Load EPA data"""
    try:
        epa_data = pd.read_csv("sumersports_epa_data.csv")
        return epa_data
    except:
        print("Could not load EPA data")
        return None

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

def create_model_a_predictions(week1_results, epa_data):
    """Create Model A predictions for Week 1"""
    team_mapping = get_team_mapping()
    predictions = []
    
    for _, game in week1_results.iterrows():
        favorite = game['favorite']
        underdog = game['underdog']
        spread = game['spread']
        
        fav_abbr = team_mapping.get(favorite, favorite)
        dog_abbr = team_mapping.get(underdog, underdog)
        
        # Get EPA data
        fav_epa = epa_data[epa_data['team'] == fav_abbr]
        dog_epa = epa_data[epa_data['team'] == dog_abbr]
        
        if fav_epa.empty or dog_epa.empty:
            continue
        
        fav_off = fav_epa['epa_off_per_play'].iloc[0]
        fav_def = fav_epa['epa_def_allowed_per_play'].iloc[0]
        dog_off = dog_epa['epa_off_per_play'].iloc[0]
        dog_def = dog_epa['epa_def_allowed_per_play'].iloc[0]
        
        fav_net = fav_off - fav_def
        dog_net = dog_off - dog_def
        
        # Model A logic
        prob = 0.50
        
        # Defense quality
        if fav_def < -0.05:
            prob += 0.12
        elif fav_def > 0.10:
            prob -= 0.10
        else:
            prob += 0.02
        
        # Net EPA differential
        net_diff = dog_net - fav_net
        if net_diff > 0.10:
            prob += 0.15
        elif net_diff > 0.05:
            prob += 0.08
        elif net_diff < -0.10:
            prob -= 0.15
        elif net_diff < -0.05:
            prob -= 0.08
        
        # Spread adjustment
        if abs(spread) > 7:
            prob += 0.05
        
        prob = max(0.01, min(0.99, prob))
        predicted_cover = prob > 0.5
        
        predictions.append({
            'game': game['game'],
            'favorite': favorite,
            'underdog': underdog,
            'spread': spread,
            'predicted_cover': predicted_cover,
            'probability': prob
        })
    
    return pd.DataFrame(predictions)

def create_week1_predictions():
    """Create post-hoc Week 1 predictions"""
    
    # Load Week 1 results (for game info)
    week1_results = pd.read_csv("data/week1_ats_results.csv")
    
    # Load EPA data (use most recent available)
    epa_data = load_epa_data()
    if epa_data is None:
        print("Could not load EPA data. Using default predictions.")
        # Fallback: simple predictions based on spread
        predictions = []
        for _, game in week1_results.iterrows():
            spread = abs(game['spread'])
            # Simple heuristic: predict underdog cover if spread > 3
            predicted_cover = spread > 3
            predictions.append({
                'game': game['game'],
                'favorite': game['favorite'],
                'underdog': game['underdog'],
                'spread': game['spread'],
                'predicted_cover': predicted_cover,
                'probability': 0.55 if spread > 3 else 0.45
            })
        return pd.DataFrame(predictions)
    
    # Create Model A predictions
    model_a = create_model_a_predictions(week1_results, epa_data)
    
    # For other models, we'll use simplified versions
    # Model B: Similar to A
    model_b = model_a.copy()
    model_b['probability'] = model_b['probability'] * 0.95  # Slight adjustment
    
    # Model C: Simple spread-based
    model_c = []
    for _, game in week1_results.iterrows():
        spread = abs(game['spread'])
        predicted_cover = spread > 5  # Large spread favor underdog
        model_c.append({
            'game': game['game'],
            'predicted_cover': predicted_cover,
            'probability': 0.60 if spread > 5 else 0.40
        })
    model_c = pd.DataFrame(model_c)
    
    # Model D: Always predict underdog (simplified)
    model_d = []
    for _, game in week1_results.iterrows():
        model_d.append({
            'game': game['game'],
            'predicted_cover': True,
            'probability': 0.52
        })
    model_d = pd.DataFrame(model_d)
    
    # Combine all predictions
    all_predictions = []
    for _, game in week1_results.iterrows():
        game_name = game['game']
        
        model_a_pred = model_a[model_a['game'] == game_name]
        model_b_pred = model_b[model_b['game'] == game_name]
        model_c_pred = model_c[model_c['game'] == game_name]
        model_d_pred = model_d[model_d['game'] == game_name]
        
        if len(model_a_pred) == 0:
            continue
        
        all_predictions.append({
            'game': game_name,
            'actual_cover': game['underdog_covered'],
            'model_a_pred': model_a_pred.iloc[0]['predicted_cover'],
            'model_b_pred': model_b_pred.iloc[0]['predicted_cover'] if len(model_b_pred) > 0 else None,
            'model_c_pred': model_c_pred.iloc[0]['predicted_cover'] if len(model_c_pred) > 0 else None,
            'model_d_pred': model_d_pred.iloc[0]['predicted_cover'] if len(model_d_pred) > 0 else None,
        })
    
    df = pd.DataFrame(all_predictions)
    
    # Calculate correctness
    df['model_a_correct'] = df['model_a_pred'] == df['actual_cover']
    df['model_b_correct'] = (df['model_b_pred'] == df['actual_cover']) & df['model_b_pred'].notna()
    df['model_c_correct'] = (df['model_c_pred'] == df['actual_cover']) & df['model_c_pred'].notna()
    df['model_d_correct'] = (df['model_d_pred'] == df['actual_cover']) & df['model_d_pred'].notna()
    
    # Save results
    df.to_csv("data/week1_actual_results_analysis.csv", index=False)
    
    # Print summary
    total = len(df)
    print(f"Week 1 Post-Hoc Predictions:")
    print(f"Total Games: {total}")
    print(f"Model A: {df['model_a_correct'].sum()}/{total} ({df['model_a_correct'].mean()*100:.1f}%)")
    print(f"Model B: {df['model_b_correct'].sum()}/{total} ({df['model_b_correct'].mean()*100:.1f}%)")
    print(f"Model C: {df['model_c_correct'].sum()}/{total} ({df['model_c_correct'].mean()*100:.1f}%)")
    print(f"Model D: {df['model_d_correct'].sum()}/{total} ({df['model_d_correct'].mean()*100:.1f}%)")
    
    return {
        'week': 1,
        'total': total,
        'model_a': df['model_a_correct'].sum(),
        'model_b': df['model_b_correct'].sum(),
        'model_c': df['model_c_correct'].sum(),
        'model_d': df['model_d_correct'].sum()
    }

if __name__ == "__main__":
    create_week1_predictions()

