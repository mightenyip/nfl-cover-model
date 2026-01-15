#!/usr/bin/env python3
"""
Analyze Chiefs @ Titans prediction calculation
"""

import pandas as pd

# Load EPA data
epa_df = pd.read_csv("data/epa/week16/Week16_EPA.csv")

# Get Chiefs and Titans data
chiefs = epa_df[epa_df['team'] == 'KC'].iloc[0]
titans = epa_df[epa_df['team'] == 'TEN'].iloc[0]

print("="*80)
print("CHIEFS @ TITANS - EPA DATA ANALYSIS")
print("="*80)
print()

print("KANSAS CITY CHIEFS (KC):")
print(f"  Offensive EPA per play: {chiefs['epa_off_per_play']:.3f}")
print(f"  Defensive EPA allowed per play: {chiefs['epa_def_allowed_per_play']:.3f}")
print(f"  Net EPA: {chiefs['net_epa_per_play']:.3f}")
print()

print("TENNESSEE TITANS (TEN):")
print(f"  Offensive EPA per play: {titans['epa_off_per_play']:.3f}")
print(f"  Defensive EPA allowed per play: {titans['epa_def_allowed_per_play']:.3f}")
print(f"  Net EPA: {titans['net_epa_per_play']:.3f}")
print()

print("="*80)
print("MODEL A CALCULATION")
print("="*80)
print()

# Game details
away_team = "Chiefs"
home_team = "Titans"
favorite = "Chiefs"
underdog = "Titans"
spread = -3.5

# EPA values
away_off_epa = chiefs['epa_off_per_play']
away_def_epa = chiefs['epa_def_allowed_per_play']
home_off_epa = titans['epa_off_per_play']
home_def_epa = titans['epa_def_allowed_per_play']

# Net EPA
away_net_epa = away_off_epa - away_def_epa
home_net_epa = home_off_epa - home_def_epa
net_epa_diff = away_net_epa - home_net_epa

print(f"Chiefs Net EPA: {away_net_epa:.3f}")
print(f"Titans Net EPA: {home_net_epa:.3f}")
print(f"Net EPA Difference (Away - Home): {net_epa_diff:.3f}")
print()

# Opponent defense quality (what the underdog Titans are facing)
opponent_def_epa = home_def_epa  # Titans defense
print(f"Opponent Defense (Titans): {opponent_def_epa:.3f}")

# 5-tier defense classification
if opponent_def_epa <= -0.1:
    defense_quality = "ELITE"
    def_adjustment = -0.15
elif opponent_def_epa <= -0.05:
    defense_quality = "STRONG"
    def_adjustment = -0.08
elif opponent_def_epa <= 0.05:
    defense_quality = "AVERAGE"
    def_adjustment = 0.0
elif opponent_def_epa <= 0.1:
    defense_quality = "WEAK"
    def_adjustment = 0.05
else:
    defense_quality = "POOR"
    def_adjustment = 0.12

print(f"Defense Quality: {defense_quality}")
print(f"Defense Adjustment: {def_adjustment:.3f}")
print()

# Model A calculation
base_prob = 0.5
epa_adjustment = net_epa_diff * 0.3
spread_adjustment = abs(spread) * 0.003

print("Model A Calculation:")
print(f"  Base Probability: {base_prob:.3f}")
print(f"  EPA Adjustment: {net_epa_diff:.3f} * 0.3 = {epa_adjustment:.3f}")
print(f"  Defense Adjustment: {def_adjustment:.3f}")
print(f"  Spread Adjustment: {abs(spread):.1f} * 0.003 = {spread_adjustment:.3f}")
print()

cover_prob = base_prob + epa_adjustment + def_adjustment + spread_adjustment
cover_prob = max(0.1, min(0.9, cover_prob))

print(f"  Final Cover Probability: {cover_prob:.3f} ({cover_prob:.1%})")
print(f"  Prediction: {'Underdog Cover' if cover_prob > 0.5 else 'Favorite Cover'}")
print()

print("="*80)
print("ISSUE IDENTIFIED")
print("="*80)
print()
print("The problem is in the Net EPA Difference calculation:")
print(f"  Net EPA Diff = Away Net - Home Net = {away_net_epa:.3f} - {home_net_epa:.3f} = {net_epa_diff:.3f}")
print()
print("This gives a LARGE positive adjustment (+{:.3f}) because:".format(epa_adjustment))
print("  - Chiefs are much better (net EPA +0.10)")
print("  - Titans are much worse (net EPA -0.24)")
print("  - The difference is huge: 0.34")
print()
print("However, this logic is BACKWARDS for underdog cover predictions!")
print("A large positive net_epa_diff means the favorite (Chiefs) is much better,")
print("which should DECREASE the probability of underdog cover, not increase it.")
print()
print("The model is treating a positive net_epa_diff as favoring the underdog,")
print("when it actually means the favorite is stronger and should cover.")

