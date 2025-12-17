#!/usr/bin/env python3
"""
Check the EPA calculation logic for Chiefs @ Titans
"""

import pandas as pd

# Load EPA data
epa_df = pd.read_csv("data/Week16_EPA.csv")

# Get Chiefs and Titans data
chiefs = epa_df[epa_df['team'] == 'KC'].iloc[0]
titans = epa_df[epa_df['team'] == 'TEN'].iloc[0]

print("="*80)
print("EPA CALCULATION LOGIC CHECK")
print("="*80)
print()

# Game setup
away_team = "Chiefs"
home_team = "Titans"
favorite = "Chiefs"
underdog = "Titans"

# Current code logic (WRONG):
away_net = chiefs['net_epa_per_play']
home_net = titans['net_epa_per_play']
net_epa_diff_wrong = away_net - home_net

print("CURRENT CODE (using away/home):")
print(f"  away_net (Chiefs): {away_net:.3f}")
print(f"  home_net (Titans): {home_net:.3f}")
print(f"  net_epa_diff = away_net - home_net = {net_epa_diff_wrong:.3f}")
print(f"  Adjustment: {net_epa_diff_wrong * 0.3:.3f} (ADDED to probability)")
print()

# Correct logic (from underdog perspective):
favorite_net = chiefs['net_epa_per_play']
underdog_net = titans['net_epa_per_play']
net_epa_diff_correct = underdog_net - favorite_net

print("CORRECT LOGIC (using favorite/underdog):")
print(f"  favorite_net (Chiefs): {favorite_net:.3f}")
print(f"  underdog_net (Titans): {underdog_net:.3f}")
print(f"  net_epa_diff = underdog_net - favorite_net = {underdog_net:.3f} - {favorite_net:.3f} = {net_epa_diff_correct:.3f}")
print(f"  Adjustment: {net_epa_diff_correct * 0.3:.3f} (ADDED to probability)")
print()

print("="*80)
print("THE ISSUE")
print("="*80)
print()
print("The code uses away/home instead of favorite/underdog!")
print("For Chiefs @ Titans:")
print("  - Away = Chiefs (favorite)")
print("  - Home = Titans (underdog)")
print("  - So away_net - home_net = favorite_net - underdog_net")
print("  - This is the OPPOSITE of what we want!")
print()
print("We need: underdog_net - favorite_net")
print("But we're getting: favorite_net - underdog_net")
print()
print("The sign is flipped, which explains why the probability is so high!")

