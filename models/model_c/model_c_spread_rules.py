#!/usr/bin/env python3
"""
Model C: Spread-Based Rules Model
Choose HOME FAVORITE on spreads between -2.5 and -3.5
Choose FAVORITE on spreads between -1 and -3.5
"""

import pandas as pd
import numpy as np
import os

def run_model_c_spread_rules():
    """Run Model C using spread-based rules"""
    
    print("=== Model C: Spread-Based Rules Predictions ===")
    print("Rule 1: Choose HOME FAVORITE on spreads between -2.5 and -3.5")
    print("Rule 2: Choose FAVORITE on spreads between -1 and -3.5")
    
    # Load Week 3 schedule and odds
    week3_odds_path = "../../week3/week3_2025_odds.csv"
    week3_odds = pd.read_csv(week3_odds_path)
    
    print(f"Loaded {len(week3_odds)} games from Week 3 odds")
    
    # Create team name to abbreviation mapping
    team_name_to_abbr = {
        '49ers': 'SF', 'Bears': 'CHI', 'Bengals': 'CIN', 'Bills': 'BUF', 'Broncos': 'DEN',
        'Browns': 'CLE', 'Buccaneers': 'TB', 'Cardinals': 'ARI', 'Chargers': 'LAC', 'Chiefs': 'KC',
        'Colts': 'IND', 'Commanders': 'WAS', 'Cowboys': 'DAL', 'Dolphins': 'MIA', 'Eagles': 'PHI',
        'Falcons': 'ATL', 'Giants': 'NYG', 'Jaguars': 'JAX', 'Jets': 'NYJ', 'Lions': 'DET',
        'Packers': 'GB', 'Panthers': 'CAR', 'Patriots': 'NE', 'Raiders': 'LV', 'Rams': 'LA',
        'Ravens': 'BAL', 'Saints': 'NO', 'Seahawks': 'SEA', 'Steelers': 'PIT', 'Texans': 'HOU',
        'Titans': 'TEN', 'Vikings': 'MIN'
    }
    
    # Add abbreviation columns
    week3_odds['underdog_abbr'] = week3_odds['underdog_team'].map(team_name_to_abbr)
    week3_odds['favorite_abbr'] = week3_odds['favorite_team'].map(team_name_to_abbr)
    
    # Initialize predictions
    week3_data = week3_odds.copy()
    week3_data['cover_probability'] = 0.50  # Default
    week3_data['confidence'] = 'MEDIUM'  # Default
    week3_data['predicted_cover'] = False  # Default to favorite cover
    week3_data['rule_applied'] = 'None'
    
    # Apply Model C Rules
    for idx, row in week3_data.iterrows():
        spread = row['spread_line']
        favorite = row['favorite_team']
        home_team = row['home_team']
        
        # Rule 1: Choose HOME FAVORITE on spreads between -2.5 and -3.5
        if -3.5 <= spread <= -2.5 and favorite == home_team:
            week3_data.at[idx, 'predicted_cover'] = False  # Favorite covers
            week3_data.at[idx, 'cover_probability'] = 0.65
            week3_data.at[idx, 'confidence'] = 'HIGH'
            week3_data.at[idx, 'rule_applied'] = 'Home Favorite -2.5 to -3.5'
        
        # Rule 2: Choose FAVORITE on spreads between -1 and -3.5
        elif -3.5 <= spread <= -1.0:
            week3_data.at[idx, 'predicted_cover'] = False  # Favorite covers
            week3_data.at[idx, 'cover_probability'] = 0.60
            week3_data.at[idx, 'confidence'] = 'HIGH'
            week3_data.at[idx, 'rule_applied'] = 'Favorite -1 to -3.5'
        
        # For spreads outside these ranges, default to underdog
        else:
            week3_data.at[idx, 'predicted_cover'] = True  # Underdog covers
            week3_data.at[idx, 'cover_probability'] = 0.45
            week3_data.at[idx, 'confidence'] = 'LOW'
            week3_data.at[idx, 'rule_applied'] = 'Default Underdog'
    
    print(f"\n=== Model C Predictions ===")
    
    # Show games where rules were applied
    rule_games = week3_data[week3_data['rule_applied'] != 'Default Underdog']
    print(f"\nGames where rules were applied ({len(rule_games)}):")
    for _, row in rule_games.iterrows():
        game = f"{row['away_team']} @ {row['home_team']}"
        spread = f"{row['favorite_team']} {row['spread_line']}"
        predicted = "Favorite Covers" if not row['predicted_cover'] else "Underdog Covers"
        confidence = row['confidence']
        rule = row['rule_applied']
        
        print(f"  {game}: {spread} - {predicted} ({confidence}) - {rule}")
    
    # Show default predictions
    default_games = week3_data[week3_data['rule_applied'] == 'Default Underdog']
    print(f"\nGames with default underdog prediction ({len(default_games)}):")
    for _, row in default_games.iterrows():
        game = f"{row['away_team']} @ {row['home_team']}"
        spread = f"{row['underdog_team']} +{row['spread_line']}"
        
        print(f"  {game}: {spread} - Underdog Covers (LOW)")
    
    # Confidence distribution
    confidence_counts = week3_data['confidence'].value_counts()
    print(f"\n=== Confidence Level Distribution ===")
    for conf in ['HIGH', 'MEDIUM', 'LOW']:
        count = confidence_counts.get(conf, 0)
        print(f"{conf}: {count} games")
    
    # Summary statistics
    print(f"\n=== Model C Summary ===")
    print(f"Total games: {len(week3_data)}")
    print(f"Underdog covers predicted: {week3_data['predicted_cover'].sum()}")
    print(f"Favorite covers predicted: {(~week3_data['predicted_cover']).sum()}")
    
    avg_spread = week3_data['spread_line'].mean()
    print(f"Average spread: {avg_spread:.1f} points")
    
    avg_prob = week3_data['cover_probability'].mean()
    print(f"Average cover probability: {avg_prob:.1%}")
    
    # Save predictions
    week3_data.to_csv("model_c_week3_predictions.csv", index=False)
    print(f"\n✅ Model C predictions saved to: model_c_week3_predictions.csv")
    
    return week3_data

if __name__ == "__main__":
    run_model_c_spread_rules()
