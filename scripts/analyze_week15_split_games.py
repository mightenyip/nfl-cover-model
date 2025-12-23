#!/usr/bin/env python3
"""
Analyze Week 15 split games (1/3 votes)
These are games where 2 models agree and 1 disagrees
"""

import pandas as pd

# Week 15 actual results
actual_results = {
    'Falcons @ Buccaneers': True,   # Underdog covered
    'Browns @ Bears': False,         # Favorite covered
    'Ravens @ Bengals': False,      # Favorite covered
    'Chargers @ Chiefs': True,      # Underdog covered
    'Bills @ Patriots': False,       # Favorite covered
    'Commanders @ Giants': True,    # Underdog covered
    'Raiders @ Eagles': False,       # Favorite covered
    'Jets @ Jaguars': False,        # Favorite covered
    'Cardinals @ Texans': False,    # Favorite covered
    'Packers @ Broncos': True,      # Underdog covered
    'Lions @ Rams': False,          # Favorite covered
    'Panthers @ Saints': True,      # Underdog covered
    'Titans @ 49ers': False,        # Favorite covered
    'Colts @ Seahawks': True,       # Underdog covered
    'Vikings @ Cowboys': True,      # Underdog covered
    'Dolphins @ Steelers': False,    # Favorite covered
}

# Load predictions
predictions_df = pd.read_csv('predictions/week15_predictions_final.csv')

print("="*80)
print("WEEK 15 SPLIT GAMES ANALYSIS (1/3 votes)")
print("Split games = 2 models agree, 1 disagrees")
print("="*80)
print()

# Filter for split games
split_games = predictions_df[predictions_df['agreement'] == 'Split (1/3)']

print(f"Total split games: {len(split_games)}")
print()

# Analyze each split game
results = []

for _, row in split_games.iterrows():
    game = row['game']
    actual = actual_results.get(game)
    
    if actual is None:
        continue
    
    # Get model predictions
    model_a_pred = row['model_a_prediction'] == 'Cover'
    model_b_pred = row['model_b_prediction'] == 'Cover'
    model_e_pred = row['model_e_prediction'] == 'Cover'
    
    # Determine which 2 models agree
    votes = [model_a_pred, model_b_pred, model_e_pred]
    underdog_votes = sum(votes)
    
    if underdog_votes == 1:
        # One model says Cover, two say No Cover
        if model_a_pred:
            agreeing_models = "A"
            disagreeing_models = "B, E"
            majority_pred = False  # No Cover
        elif model_b_pred:
            agreeing_models = "B"
            disagreeing_models = "A, E"
            majority_pred = False
        else:  # model_e_pred
            agreeing_models = "E"
            disagreeing_models = "A, B"
            majority_pred = False
    else:  # underdog_votes == 2
        # Two models say Cover, one says No Cover
        if not model_a_pred:
            agreeing_models = "B, E"
            disagreeing_models = "A"
            majority_pred = True  # Cover
        elif not model_b_pred:
            agreeing_models = "A, E"
            disagreeing_models = "B"
            majority_pred = True
        else:  # not model_e_pred
            agreeing_models = "A, B"
            disagreeing_models = "E"
            majority_pred = True
    
    # Check correctness
    majority_correct = majority_pred == actual
    consensus_correct = (row['consensus_prediction'] == 'Cover') == actual
    
    # Individual model correctness
    model_a_correct = model_a_pred == actual
    model_b_correct = model_b_pred == actual
    model_e_correct = model_e_pred == actual
    
    results.append({
        'game': game,
        'agreeing_models': agreeing_models,
        'disagreeing_models': disagreeing_models,
        'majority_prediction': 'Cover' if majority_pred else 'No Cover',
        'actual': 'Cover' if actual else 'No Cover',
        'majority_correct': majority_correct,
        'consensus_correct': consensus_correct,
        'model_a_correct': model_a_correct,
        'model_b_correct': model_b_correct,
        'model_e_correct': model_e_correct,
        'model_a_pred': 'Cover' if model_a_pred else 'No Cover',
        'model_b_pred': 'Cover' if model_b_pred else 'No Cover',
        'model_e_pred': 'Cover' if model_e_pred else 'No Cover',
    })

results_df = pd.DataFrame(results)

# Print detailed results
print("="*80)
print("DETAILED SPLIT GAME RESULTS")
print("="*80)
print()

for _, r in results_df.iterrows():
    status = "✅" if r['majority_correct'] else "❌"
    print(f"{status} {r['game']}")
    print(f"   Agreeing Models ({r['agreeing_models']}): {r['majority_prediction']}")
    print(f"   Disagreeing Model ({r['disagreeing_models']}): {'Cover' if r['majority_prediction'] == 'No Cover' else 'No Cover'}")
    print(f"   Actual: {r['actual']}")
    print(f"   Majority Correct: {'Yes' if r['majority_correct'] else 'No'}")
    print(f"   Individual Models:")
    print(f"     Model A: {r['model_a_pred']} ({'✅' if r['model_a_correct'] else '❌'})")
    print(f"     Model B: {r['model_b_pred']} ({'✅' if r['model_b_correct'] else '❌'})")
    print(f"     Model E: {r['model_e_pred']} ({'✅' if r['model_e_correct'] else '❌'})")
    print()

# Summary statistics
print("="*80)
print("SUMMARY STATISTICS")
print("="*80)
print()

total = len(results_df)
majority_correct = results_df['majority_correct'].sum()
majority_accuracy = majority_correct / total * 100 if total > 0 else 0

print(f"Total Split Games: {total}")
print(f"Majority (2 models) Correct: {majority_correct}/{total} ({majority_accuracy:.1f}%)")
print()

# Break down by which models agreed
print("Performance by Agreeing Models:")
print()

# A, B agreed
ab_games = results_df[results_df['agreeing_models'] == 'A, B']
if len(ab_games) > 0:
    ab_correct = ab_games['majority_correct'].sum()
    print(f"  Models A & B Agreed: {ab_correct}/{len(ab_games)} correct ({ab_correct/len(ab_games)*100:.1f}%)")

# A, E agreed
ae_games = results_df[results_df['agreeing_models'] == 'A, E']
if len(ae_games) > 0:
    ae_correct = ae_games['majority_correct'].sum()
    print(f"  Models A & E Agreed: {ae_correct}/{len(ae_games)} correct ({ae_correct/len(ae_games)*100:.1f}%)")

# B, E agreed
be_games = results_df[results_df['agreeing_models'] == 'B, E']
if len(be_games) > 0:
    be_correct = be_games['majority_correct'].sum()
    print(f"  Models B & E Agreed: {be_correct}/{len(be_games)} correct ({be_correct/len(be_games)*100:.1f}%)")

# Individual model performance in split games
print()
print("Individual Model Performance in Split Games:")
print()

model_a_correct = results_df['model_a_correct'].sum()
model_b_correct = results_df['model_b_correct'].sum()
model_e_correct = results_df['model_e_correct'].sum()

print(f"  Model A: {model_a_correct}/{total} correct ({model_a_correct/total*100:.1f}%)")
print(f"  Model B: {model_b_correct}/{total} correct ({model_b_correct/total*100:.1f}%)")
print(f"  Model E: {model_e_correct}/{total} correct ({model_e_correct/total*100:.1f}%)")

print()
print("="*80)


