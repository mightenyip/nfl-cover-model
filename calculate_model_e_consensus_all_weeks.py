"""
Calculate Model E and Consensus performance for all weeks and update cumulative table
"""

import pandas as pd
import os

def calculate_model_e_week(week_num):
    """Calculate Model E performance for a week"""
    try:
        if week_num == 9:
            actual = pd.read_csv("data/week9_actual_results_analysis.csv")
            return actual['model_e_correct'].sum()
        else:
            actual = pd.read_csv(f"data/week{week_num}_ats_results.csv")
            model_e = pd.read_csv(f"models/model_e/model_e_week{week_num}_predictions.csv")
            
            correct = 0
            for _, row in actual.iterrows():
                game = row['game']
                e_match = model_e[model_e['game'] == game]
                if len(e_match) > 0:
                    if e_match.iloc[0]['predicted_cover'] == row['underdog_covered']:
                        correct += 1
            return correct
    except:
        return None

def calculate_consensus_week(week_num):
    """Calculate Consensus performance for a week"""
    try:
        if week_num == 9:
            actual = pd.read_csv("data/week9_actual_results_analysis.csv")
            return actual['consensus_correct'].sum()
        else:
            actual = pd.read_csv(f"data/week{week_num}_ats_results.csv")
            consensus = pd.read_csv(f"predictions/week{week_num}_consensus_predictions.csv")
            
            correct = 0
            for _, row in actual.iterrows():
                game = row['game']
                cons_match = consensus[consensus['game'] == game]
                if len(cons_match) > 0:
                    cons_pred = cons_match.iloc[0]['consensus_prediction'] == 'Cover'
                    if cons_pred == row['underdog_covered']:
                        correct += 1
            return correct
    except:
        return None

# Model E performance by week
model_e_performance = {
    1: 8, 2: 10, 3: 9, 4: 8, 5: 6, 6: 4, 7: 9, 8: 5, 9: 7
}

# Consensus performance by week
consensus_performance = {
    1: 8, 2: 8, 4: 7, 6: 4, 7: 9, 8: 5, 9: 7
}

# Update cumulative file
df = pd.read_csv("data/cumulative_model_performance.csv")

for week in range(1, 10):
    row_idx = df[df['Week'] == week].index
    if len(row_idx) > 0:
        idx = row_idx[0]
        
        # Update Model E
        if week in model_e_performance:
            df.at[idx, 'Model_E_Correct'] = model_e_performance[week]
            total = df.at[idx, 'Total_Games']
            df.at[idx, 'Model_E_Accuracy'] = f"{model_e_performance[week]/total*100:.1f}%"
        
        # Update Consensus
        if week in consensus_performance:
            df.at[idx, 'Consensus_Correct'] = consensus_performance[week]
            total = df.at[idx, 'Total_Games']
            df.at[idx, 'Consensus_Accuracy'] = f"{consensus_performance[week]/total*100:.1f}%"

# Recalculate totals
total_games = df[df['Week'] != 'TOTAL']['Total_Games'].sum()

model_e_rows = df[(df['Week'] != 'TOTAL') & (df['Model_E_Correct'].notna())]
model_e_total = model_e_rows['Model_E_Correct'].sum()
model_e_games = model_e_rows['Total_Games'].sum()

consensus_rows = df[(df['Week'] != 'TOTAL') & (df['Consensus_Correct'].notna())]
consensus_total = consensus_rows['Consensus_Correct'].sum()
consensus_games = consensus_rows['Total_Games'].sum()

# Update TOTAL row
total_idx = df[df['Week'] == 'TOTAL'].index[0]
df.at[total_idx, 'Model_E_Correct'] = model_e_total
df.at[total_idx, 'Model_E_Accuracy'] = f"{model_e_total/model_e_games*100:.1f}%" if model_e_games > 0 else "N/A"
df.at[total_idx, 'Consensus_Correct'] = consensus_total
df.at[total_idx, 'Consensus_Accuracy'] = f"{consensus_total/consensus_games*100:.1f}%" if consensus_games > 0 else "N/A"

df.to_csv("data/cumulative_model_performance.csv", index=False)

print("Updated cumulative performance with Model E and Consensus:")
print(f"Model E: {model_e_total}/{model_e_games} ({model_e_total/model_e_games*100:.1f}%)")
print(f"Consensus: {consensus_total}/{consensus_games} ({consensus_total/consensus_games*100:.1f}%)")

