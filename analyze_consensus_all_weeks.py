"""
Analyze consensus predictions against actual results for all weeks
"""

import pandas as pd
import os

def analyze_consensus_week(week_num):
    """Analyze consensus predictions for a specific week"""
    
    # Load actual results
    actual_results = None
    try:
        actual_results = pd.read_csv(f"data/week{week_num}_ats_results.csv")
    except:
        if week_num == 9:
            try:
                actual_results = pd.read_csv(f"data/week{week_num}_actual_results_analysis.csv")
            except:
                return None
        else:
            return None
    
    # Load consensus predictions
    try:
        consensus = pd.read_csv(f"predictions/week{week_num}_consensus_predictions.csv")
    except:
        return None
    
    results_data = []
    
    for _, actual in actual_results.iterrows():
        game_name = actual['game']
        
        cons_match = consensus[consensus['game'] == game_name]
        if len(cons_match) == 0:
            continue
        
        consensus_pred_str = cons_match.iloc[0]['consensus_prediction']
        consensus_pred = consensus_pred_str == 'Cover'
        
        # Try different column names for actual cover
        if 'underdog_covered' in actual:
            actual_cover = actual['underdog_covered']
        elif 'actual_cover' in actual:
            actual_cover = actual['actual_cover']
        else:
            continue
        
        consensus_correct = consensus_pred == actual_cover
        
        results_data.append({
            'game': game_name,
            'actual_cover': actual_cover,
            'consensus_pred': consensus_pred,
            'consensus_correct': consensus_correct
        })
    
    df = pd.DataFrame(results_data)
    
    if len(df) == 0:
        return None
    
    total = len(df)
    correct = df['consensus_correct'].sum()
    
    print(f"Week {week_num}: Consensus {correct}/{total} ({correct/total*100:.1f}%)")
    
    return {
        'week': week_num,
        'total': total,
        'correct': correct
    }

if __name__ == "__main__":
    print("Analyzing Consensus Performance for All Weeks")
    print("=" * 60)
    
    all_results = []
    for week in range(1, 10):
        result = analyze_consensus_week(week)
        if result:
            all_results.append(result)
    
    print("\n" + "=" * 60)
    print("Summary:")
    total_correct = sum(r['correct'] for r in all_results)
    total_games = sum(r['total'] for r in all_results)
    print(f"Overall: {total_correct}/{total_games} ({total_correct/total_games*100:.1f}%)")

