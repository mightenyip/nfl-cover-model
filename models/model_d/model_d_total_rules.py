#!/usr/bin/env python3
"""
Model D: Total-Based Rules Model
Choose FAVORITE (spread of 6.5 or less) on games with TOTAL OF 46 POINTS OR HIGHER
Choose UNDERDOG in games with TOTAL OF 45.5 POINTS OR BELOW
"""

import pandas as pd
import numpy as np
import os

def run_model_d_total_rules():
    """Run Model D using total-based rules"""
    
    print("=== Model D: Total-Based Rules Predictions ===")
    print("Rule 1: Choose FAVORITE (spread ≤ 6.5) on games with TOTAL ≥ 46 points")
    print("Rule 2: Choose UNDERDOG in games with TOTAL ≤ 45.5 points")
    
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
    
    # Apply Model D Rules
    for idx, row in week3_data.iterrows():
        total = row['total_line']
        spread = row['spread_line']
        
        # Rule 1: Choose FAVORITE (spread ≤ 6.5) on games with TOTAL ≥ 46 points
        if total >= 46.0 and abs(spread) <= 6.5:
            week3_data.at[idx, 'predicted_cover'] = False  # Favorite covers
            week3_data.at[idx, 'cover_probability'] = 0.65
            week3_data.at[idx, 'confidence'] = 'HIGH'
            week3_data.at[idx, 'rule_applied'] = 'High Total + Small Spread = Favorite'
        
        # Rule 2: Choose UNDERDOG in games with TOTAL ≤ 45.5 points
        elif total <= 45.5:
            week3_data.at[idx, 'predicted_cover'] = True  # Underdog covers
            week3_data.at[idx, 'cover_probability'] = 0.60
            week3_data.at[idx, 'confidence'] = 'HIGH'
            week3_data.at[idx, 'rule_applied'] = 'Low Total = Underdog'
        
        # For games that don't match rules, default to underdog
        else:
            week3_data.at[idx, 'predicted_cover'] = True  # Underdog covers
            week3_data.at[idx, 'cover_probability'] = 0.45
            week3_data.at[idx, 'confidence'] = 'LOW'
            week3_data.at[idx, 'rule_applied'] = 'Default Underdog'
    
    print(f"\n=== Model D Predictions ===")
    
    # Show games where rules were applied
    rule_games = week3_data[week3_data['rule_applied'] != 'Default Underdog']
    print(f"\nGames where rules were applied ({len(rule_games)}):")
    for _, row in rule_games.iterrows():
        game = f"{row['away_team']} @ {row['home_team']}"
        total = f"Total: {row['total_line']}"
        spread = f"{row['favorite_team']} {row['spread_line']}" if not row['predicted_cover'] else f"{row['underdog_team']} +{row['spread_line']}"
        predicted = "Favorite Covers" if not row['predicted_cover'] else "Underdog Covers"
        confidence = row['confidence']
        rule = row['rule_applied']
        
        print(f"  {game}: {total}, {spread} - {predicted} ({confidence}) - {rule}")
    
    # Show default predictions
    default_games = week3_data[week3_data['rule_applied'] == 'Default Underdog']
    print(f"\nGames with default underdog prediction ({len(default_games)}):")
    for _, row in default_games.iterrows():
        game = f"{row['away_team']} @ {row['home_team']}"
        total = f"Total: {row['total_line']}"
        spread = f"{row['underdog_team']} +{row['spread_line']}"
        
        print(f"  {game}: {total}, {spread} - Underdog Covers (LOW)")
    
    # Confidence distribution
    confidence_counts = week3_data['confidence'].value_counts()
    print(f"\n=== Confidence Level Distribution ===")
    for conf in ['HIGH', 'MEDIUM', 'LOW']:
        count = confidence_counts.get(conf, 0)
        print(f"{conf}: {count} games")
    
    # Summary statistics
    print(f"\n=== Model D Summary ===")
    print(f"Total games: {len(week3_data)}")
    print(f"Underdog covers predicted: {week3_data['predicted_cover'].sum()}")
    print(f"Favorite covers predicted: {(~week3_data['predicted_cover']).sum()}")
    
    avg_spread = week3_data['spread_line'].mean()
    avg_total = week3_data['total_line'].mean()
    print(f"Average spread: {avg_spread:.1f} points")
    print(f"Average total: {avg_total:.1f} points")
    
    avg_prob = week3_data['cover_probability'].mean()
    print(f"Average cover probability: {avg_prob:.1%}")
    
    # Save predictions
    week3_data.to_csv("model_d_week3_predictions.csv", index=False)
    print(f"\n✅ Model D predictions saved to: model_d_week3_predictions.csv")
    
    return week3_data

if __name__ == "__main__":
    run_model_d_total_rules()
