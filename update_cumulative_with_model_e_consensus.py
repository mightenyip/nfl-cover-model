"""
Update cumulative performance table with Model E and Consensus data for all weeks
"""

import pandas as pd
import os

def get_model_e_performance(week_num):
    """Get Model E performance for a week"""
    try:
        actual = pd.read_csv(f"data/week{week_num}_ats_results.csv")
        model_e = pd.read_csv(f"models/model_e/model_e_week{week_num}_predictions.csv")
        
        correct = 0
        total = 0
        
        for _, row in actual.iterrows():
            game = row['game']
            e_match = model_e[model_e['game'] == game]
            if len(e_match) > 0:
                total += 1
                if e_match.iloc[0]['predicted_cover'] == row['underdog_covered']:
                    correct += 1
        
        return correct, total
    except:
        if week_num == 9:
            try:
                actual = pd.read_csv(f"data/week{week_num}_actual_results_analysis.csv")
                return actual['model_e_correct'].sum(), len(actual)
            except:
                pass
        return None, None

def get_consensus_performance(week_num):
    """Get Consensus performance for a week"""
    try:
        actual = pd.read_csv(f"data/week{week_num}_ats_results.csv")
        consensus = pd.read_csv(f"predictions/week{week_num}_consensus_predictions.csv")
        
        correct = 0
        total = 0
        
        for _, row in actual.iterrows():
            game = row['game']
            cons_match = consensus[consensus['game'] == game]
            if len(cons_match) > 0:
                total += 1
                consensus_pred = cons_match.iloc[0]['consensus_prediction'] == 'Cover'
                if consensus_pred == row['underdog_covered']:
                    correct += 1
        
        return correct, total
    except:
        if week_num == 9:
            try:
                actual = pd.read_csv(f"data/week{week_num}_actual_results_analysis.csv")
                return actual['consensus_correct'].sum(), len(actual)
            except:
                pass
        return None, None

def update_cumulative():
    """Update cumulative performance with Model E and Consensus"""
    
    # Load existing cumulative data
    df = pd.read_csv("data/cumulative_model_performance.csv")
    
    # Update Model E and Consensus for each week
    for week in range(1, 10):
        e_correct, e_total = get_model_e_performance(week)
        cons_correct, cons_total = get_consensus_performance(week)
        
        if e_correct is not None:
            row_idx = df[df['Week'] == week].index[0]
            df.at[row_idx, 'Model_E_Correct'] = e_correct
            df.at[row_idx, 'Model_E_Accuracy'] = f"{e_correct/e_total*100:.1f}%" if e_total > 0 else "N/A"
        
        if cons_correct is not None:
            row_idx = df[df['Week'] == week].index[0]
            df.at[row_idx, 'Consensus_Correct'] = cons_correct
            df.at[row_idx, 'Consensus_Accuracy'] = f"{cons_correct/cons_total*100:.1f}%" if cons_total > 0 else "N/A"
    
    # Recalculate totals
    total_games = df[df['Week'] != 'TOTAL']['Total_Games'].sum()
    
    # Model E totals
    model_e_rows = df[df['Model_E_Correct'].notna() & (df['Week'] != 'TOTAL')]
    model_e_total = model_e_rows['Model_E_Correct'].sum()
    model_e_games = model_e_rows['Total_Games'].sum()
    model_e_acc = model_e_total / model_e_games * 100 if model_e_games > 0 else 0
    
    # Consensus totals
    consensus_rows = df[df['Consensus_Correct'].notna() & (df['Week'] != 'TOTAL')]
    consensus_total = consensus_rows['Consensus_Correct'].sum()
    consensus_games = consensus_rows['Total_Games'].sum()
    consensus_acc = consensus_total / consensus_games * 100 if consensus_games > 0 else 0
    
    # Update TOTAL row
    total_idx = df[df['Week'] == 'TOTAL'].index[0]
    df.at[total_idx, 'Model_E_Correct'] = model_e_total
    df.at[total_idx, 'Model_E_Accuracy'] = f"{model_e_acc:.1f}%"
    df.at[total_idx, 'Consensus_Correct'] = consensus_total
    df.at[total_idx, 'Consensus_Accuracy'] = f"{consensus_acc:.1f}%"
    
    # Save updated file
    df.to_csv("data/cumulative_model_performance.csv", index=False)
    
    print("Updated cumulative performance with Model E and Consensus data")
    print(f"Model E: {model_e_total}/{model_e_games} ({model_e_acc:.1f}%)")
    print(f"Consensus: {consensus_total}/{consensus_games} ({consensus_acc:.1f}%)")
    
    return df

if __name__ == "__main__":
    update_cumulative()

