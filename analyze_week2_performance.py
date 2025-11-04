"""
Analyze Week 2 model performance against actual results
"""

import pandas as pd

def analyze_week2():
    """Analyze Week 2 model performance"""
    
    # Load actual results
    actual_results = pd.read_csv("data/week2_ats_results.csv")
    
    # Load week 2 predictions - try different files
    try:
        predictions = pd.read_csv("week2/improved_week2_predictions.csv")
    except:
        try:
            predictions = pd.read_csv("week2/week2_predictions_scraped_epa.csv")
        except:
            print("Could not find week 2 predictions file")
            return None
    
    # Create mapping
    results_data = []
    
    for _, actual in actual_results.iterrows():
        game_name = actual['game']
        
        # Try to find prediction - week2 files use different formats
        # Try matching by game name
        pred_row = None
        if 'game' in predictions.columns:
            pred_row = predictions[predictions['game'] == game_name]
        elif 'underdog' in predictions.columns:
            # Try matching by underdog and favorite
            parts = game_name.split(' @ ')
            if len(parts) == 2:
                away_team = parts[0]
                home_team = parts[1]
                # Try to find matching prediction
                for _, pred in predictions.iterrows():
                    pred_underdog = pred.get('underdog', '')
                    pred_favorite = pred.get('favorite', '')
                    # Check if teams match
                    if (pred_underdog in game_name or pred_favorite in game_name):
                        if (away_team in pred_underdog or home_team in pred_underdog):
                            pred_row = pd.DataFrame([pred])
                            break
        
        if pred_row is None or len(pred_row) == 0:
            continue
        
        # Get prediction
        if 'predicted_cover' in pred_row.columns:
            predicted_cover = pred_row.iloc[0]['predicted_cover']
        elif 'prediction' in pred_row.columns:
            pred_str = pred_row.iloc[0]['prediction']
            predicted_cover = pred_str == 'Cover' or pred_str == 'True'
        else:
            continue
        
        # Actual result
        actual_cover = actual['underdog_covered']
        
        # Calculate correctness
        correct = predicted_cover == actual_cover
        
        results_data.append({
            'game': game_name,
            'actual_cover': actual_cover,
            'predicted_cover': predicted_cover,
            'correct': correct
        })
    
    df = pd.DataFrame(results_data)
    
    if len(df) == 0:
        print("No matching predictions found for week 2")
        return None
    
    # Calculate totals
    total = len(df)
    correct = df['correct'].sum()
    accuracy = correct / total * 100
    
    print(f"Week 2 Performance:")
    print(f"Total Games: {total}")
    print(f"Correct: {correct}/{total} ({accuracy:.1f}%)")
    
    # Save results
    df.to_csv("data/week2_actual_results_analysis.csv", index=False)
    
    return {
        'week': 2,
        'total': total,
        'model_a': correct,  # Assuming this is Model A since week2 had one main model
        'accuracy': accuracy
    }

if __name__ == "__main__":
    analyze_week2()

