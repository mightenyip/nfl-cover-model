#!/usr/bin/env python3
"""
Analyze Week 15 majority consensus performance
Specifically: Majority (A, B), Majority (B, E), and Majority (A, E)
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
    'Colts @ Seahawks': True,       # Underdog covered (Seahawks won by 2, didn't cover -13.5)
    'Vikings @ Cowboys': True,      # Underdog covered
    'Dolphins @ Steelers': False,    # Favorite covered
}

# Load predictions
predictions_df = pd.read_csv('predictions/week15_predictions_final.csv')

print("="*80)
print("WEEK 15 MAJORITY CONSENSUS PERFORMANCE ANALYSIS")
print("="*80)
print()

# Filter for majority consensus games
majority_ab = predictions_df[predictions_df['agreement'] == 'Majority (A, B)']
majority_be = predictions_df[predictions_df['agreement'] == 'Majority (B, E)']
majority_ae = predictions_df[predictions_df['agreement'] == 'Majority (A, E)']

print("="*80)
print("MAJORITY (A, B) - Model A and B Agreed")
print("="*80)
if len(majority_ab) > 0:
    print(f"\nTotal games: {len(majority_ab)}")
    print()
    correct = 0
    for _, row in majority_ab.iterrows():
        game = row['game']
        consensus_pred = row['consensus_prediction'] == 'Cover'
        actual = actual_results.get(game)
        if actual is not None:
            is_correct = consensus_pred == actual
            correct += is_correct
            status = "✅" if is_correct else "❌"
            print(f"{status} {game}")
            print(f"   Prediction: {'Underdog Cover' if consensus_pred else 'Favorite Cover'}")
            print(f"   Actual: {'Underdog Covered' if actual else 'Favorite Covered'}")
            print(f"   Model A: {row['model_a_prediction']} ({row['model_a_probability']:.1%})")
            print(f"   Model B: {row['model_b_prediction']} ({row['model_b_probability']:.1%})")
            print()
    accuracy = correct / len(majority_ab) * 100 if len(majority_ab) > 0 else 0
    print(f"Accuracy: {correct}/{len(majority_ab)} = {accuracy:.1f}%")
else:
    print("No games with Majority (A, B) consensus")

print()
print("="*80)
print("MAJORITY (B, E) - Model B and E Agreed")
print("="*80)
if len(majority_be) > 0:
    print(f"\nTotal games: {len(majority_be)}")
    print()
    correct = 0
    for _, row in majority_be.iterrows():
        game = row['game']
        consensus_pred = row['consensus_prediction'] == 'Cover'
        actual = actual_results.get(game)
        if actual is not None:
            is_correct = consensus_pred == actual
            correct += is_correct
            status = "✅" if is_correct else "❌"
            print(f"{status} {game}")
            print(f"   Prediction: {'Underdog Cover' if consensus_pred else 'Favorite Cover'}")
            print(f"   Actual: {'Underdog Covered' if actual else 'Favorite Covered'}")
            print(f"   Model B: {row['model_b_prediction']} ({row['model_b_probability']:.1%})")
            print(f"   Model E: {row['model_e_prediction']} ({row['model_e_probability']:.1%})")
            print()
    accuracy = correct / len(majority_be) * 100 if len(majority_be) > 0 else 0
    print(f"Accuracy: {correct}/{len(majority_be)} = {accuracy:.1f}%")
else:
    print("No games with Majority (B, E) consensus")

print()
print("="*80)
print("MAJORITY (A, E) - Model A and E Agreed")
print("="*80)
if len(majority_ae) > 0:
    print(f"\nTotal games: {len(majority_ae)}")
    print()
    correct = 0
    for _, row in majority_ae.iterrows():
        game = row['game']
        consensus_pred = row['consensus_prediction'] == 'Cover'
        actual = actual_results.get(game)
        if actual is not None:
            is_correct = consensus_pred == actual
            correct += is_correct
            status = "✅" if is_correct else "❌"
            print(f"{status} {game}")
            print(f"   Prediction: {'Underdog Cover' if consensus_pred else 'Favorite Cover'}")
            print(f"   Actual: {'Underdog Covered' if actual else 'Favorite Covered'}")
            print(f"   Model A: {row['model_a_prediction']} ({row['model_a_probability']:.1%})")
            print(f"   Model E: {row['model_e_prediction']} ({row['model_e_probability']:.1%})")
            print()
    accuracy = correct / len(majority_ae) * 100 if len(majority_ae) > 0 else 0
    print(f"Accuracy: {correct}/{len(majority_ae)} = {accuracy:.1f}%")
else:
    print("No games with Majority (A, E) consensus")

print()
print("="*80)
print("SUMMARY")
print("="*80)
print(f"Majority (A, B): {len(majority_ab)} games")
print(f"Majority (B, E): {len(majority_be)} games")
print(f"Majority (A, E): {len(majority_ae)} games")



