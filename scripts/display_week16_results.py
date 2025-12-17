#!/usr/bin/env python3
"""
Display Week 16 predictions in a formatted table
"""

import pandas as pd

# Load the predictions
df = pd.read_csv("week16_predictions_final.csv")

print("="*120)
print("WEEK 16 2025 PREDICTIONS - MODEL RESULTS")
print("="*120)
print()

# Display in a clean table format
for idx, row in df.iterrows():
    game = row['game']
    spread = row['spread_line']
    favorite = row['favorite_team']
    underdog = row['underdog_team']
    
    # Format spread
    if spread < 0:
        spread_str = f"{favorite} {spread}"
    else:
        spread_str = f"{underdog} +{spread}"
    
    print(f"{idx+1:2d}. {game:30s} | Spread: {spread_str:20s}")
    print(f"    {'-'*100}")
    
    # Model A
    ma_pred = row['model_a_prediction']
    ma_prob = row['model_a_probability']
    ma_conf = row['model_a_confidence']
    print(f"    Model A: {ma_pred:8s} | Probability: {ma_prob:.1%} | Confidence: {ma_conf}")
    
    # Model B
    mb_pred = row['model_b_prediction']
    mb_prob = row['model_b_probability']
    mb_conf = row['model_b_confidence']
    print(f"    Model B: {mb_pred:8s} | Probability: {mb_prob:.1%} | Confidence: {mb_conf}")
    
    # Model E
    me_pred = row['model_e_prediction']
    me_prob = row['model_e_probability']
    me_conf = row['model_e_confidence']
    print(f"    Model E: {me_pred:8s} | Probability: {me_prob:.1%} | Confidence: {me_conf}")
    
    # Consensus
    consensus = row['consensus_prediction']
    consensus_prob = row['consensus_probability']
    agreement = row['agreement']
    print(f"    {'→ CONSENSUS:':15s} {consensus:8s} | Probability: {consensus_prob:.1%} | {agreement}")
    print()

print("="*120)
print("SUMMARY")
print("="*120)
print(f"Total Games: {len(df)}")
print(f"Consensus Cover: {(df['consensus_prediction'] == 'Cover').sum()}")
print(f"Consensus No Cover: {(df['consensus_prediction'] == 'No Cover').sum()}")
print()
print("Agreement Breakdown:")
print(df['agreement'].value_counts().to_string())

