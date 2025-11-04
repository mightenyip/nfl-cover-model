"""
Finalize cumulative performance with complete Model E and Consensus data
"""

import pandas as pd

# Model E performance by week (from analysis)
model_e_data = {
    1: 8,   # 8/16
    2: 10,  # 10/16
    3: 9,   # 9/16
    4: 8,   # 8/16
    5: 6,   # 6/14
    6: 4,   # 4/15
    7: 9,   # 9/15
    8: 5,   # 5/13
    9: 7    # 7/13
}

# Consensus performance by week
consensus_data = {
    1: 8,   # 8/16
    2: 8,   # 8/16
    4: 7,   # 7/16
    6: 4,   # 4/15
    7: 9,   # 9/15 (or 12 from earlier analysis)
    8: 5,   # 5/13
    9: 7    # 7/13
}

# Update the cumulative CSV
df = pd.read_csv("data/cumulative_model_performance.csv")

# Update Model E for all weeks
for week, correct in model_e_data.items():
    week_rows = df[df['Week'] == week]
    if len(week_rows) > 0:
        idx = week_rows.index[0]
        total = df.at[idx, 'Total_Games']
        df.at[idx, 'Model_E_Correct'] = float(correct)
        df.at[idx, 'Model_E_Accuracy'] = f"{correct/total*100:.1f}%"
        print(f"Week {week}: Updated Model E to {correct}/{total}")

# Update Consensus for all weeks
for week, correct in consensus_data.items():
    week_rows = df[df['Week'] == week]
    if len(week_rows) > 0:
        idx = week_rows.index[0]
        total = df.at[idx, 'Total_Games']
        df.at[idx, 'Consensus_Correct'] = float(correct)
        df.at[idx, 'Consensus_Accuracy'] = f"{correct/total*100:.1f}%"
        print(f"Week {week}: Updated Consensus to {correct}/{total}")

# Update Consensus for all weeks
for week, correct in consensus_data.items():
    week_rows = df[df['Week'] == week]
    if len(week_rows) > 0:
        idx = week_rows.index[0]
        total = df.at[idx, 'Total_Games']
        df.at[idx, 'Consensus_Correct'] = float(correct)
        df.at[idx, 'Consensus_Accuracy'] = f"{correct/total*100:.1f}%"

# Week 7 consensus - use actual data (12/15)
try:
    week7_analysis = pd.read_csv("week7/week7_model_performance_analysis.csv")
    week7_consensus = week7_analysis['consensus_correct'].sum()
    row_idx = df[df['Week'] == 7].index[0]
    df.at[row_idx, 'Consensus_Correct'] = float(week7_consensus)
    df.at[row_idx, 'Consensus_Accuracy'] = f"{week7_consensus/15*100:.1f}%"
    consensus_data[7] = week7_consensus  # Update for totals calculation
except:
    pass

# Recalculate totals
total_games = df[df['Week'] != 'TOTAL']['Total_Games'].sum()

# Model E totals (all weeks 1-9)
model_e_total = sum(model_e_data.values())
# Total games for Model E: 16+16+16+16+14+15+15+13+13 = 134
model_e_games = 134

# Consensus totals (weeks with consensus data)
# Update consensus_data with Week 7 actual (12)
if 7 in consensus_data:
    consensus_data[7] = 12
consensus_total = sum(consensus_data.values())
consensus_games = 16 + 16 + 16 + 15 + 15 + 13 + 13  # Weeks 1,2,4,6,7,8,9

# Update TOTAL row
total_idx = df[df['Week'] == 'TOTAL'].index[0]
df.at[total_idx, 'Model_E_Correct'] = model_e_total
df.at[total_idx, 'Model_E_Accuracy'] = f"{model_e_total/model_e_games*100:.1f}%" if model_e_games > 0 else "N/A"
df.at[total_idx, 'Consensus_Correct'] = consensus_total
df.at[total_idx, 'Consensus_Accuracy'] = f"{consensus_total/consensus_games*100:.1f}%" if consensus_games > 0 else "N/A"

df.to_csv("data/cumulative_model_performance.csv", index=False)

print("=" * 80)
print("UPDATED CUMULATIVE PERFORMANCE WITH MODEL E AND CONSENSUS")
print("=" * 80)
print(f"\nModel E: {model_e_total}/{model_e_games} ({model_e_total/model_e_games*100:.1f}%)")
print(f"Consensus: {consensus_total}/{consensus_games} ({consensus_total/consensus_games*100:.1f}%)")
print(f"\nModel E by week: {model_e_data}")
print(f"Consensus by week: {consensus_data}")

