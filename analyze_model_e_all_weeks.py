"""
Analyze Model E predictions against actual results for all weeks
"""

import pandas as pd
import os

def analyze_week(week_num):
    """Analyze a specific week's Model E predictions"""
    
    # Load actual results - try different file names
    actual_results = None
    try:
        actual_results = pd.read_csv(f"data/week{week_num}_ats_results.csv")
    except:
        if week_num == 9:
            try:
                actual_results = pd.read_csv(f"data/week{week_num}_actual_results_analysis.csv")
                # Rename actual_cover to underdog_covered for consistency
                if 'actual_cover' in actual_results.columns:
                    actual_results['underdog_covered'] = actual_results['actual_cover']
            except:
                return None
    
    # Load Model E predictions
    try:
        model_e = pd.read_csv(f"models/model_e/model_e_week{week_num}_predictions.csv")
    except:
        return None
    
    results_data = []
    
    for _, actual in actual_results.iterrows():
        game_name = actual['game']
        
        e_match = model_e[model_e['game'] == game_name]
        if len(e_match) == 0:
            continue
        
        model_e_pred = e_match.iloc[0]['predicted_cover']
        actual_cover = actual['underdog_covered']
        
        model_e_correct = model_e_pred == actual_cover
        
        results_data.append({
            'game': game_name,
            'actual_cover': actual_cover,
            'model_e_pred': model_e_pred,
            'model_e_correct': model_e_correct
        })
    
    df = pd.DataFrame(results_data)
    
    if len(df) == 0:
        return None
    
    total = len(df)
    correct = df['model_e_correct'].sum()
    
    print(f"Week {week_num}: Model E {correct}/{total} ({correct/total*100:.1f}%)")
    
    return {
        'week': week_num,
        'total': total,
        'correct': correct
    }

if __name__ == "__main__":
    print("Analyzing Model E Performance for All Weeks")
    print("=" * 60)
    
    all_results = []
    for week in range(1, 10):
        result = analyze_week(week)
        if result:
            all_results.append(result)
    
    print("\n" + "=" * 60)
    print("Summary:")
    total_correct = sum(r['correct'] for r in all_results)
    total_games = sum(r['total'] for r in all_results)
    print(f"Overall: {total_correct}/{total_games} ({total_correct/total_games*100:.1f}%)")

