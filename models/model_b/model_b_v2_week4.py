#!/usr/bin/env python3
"""
Model B v2 Week 4: Matchup-Specific EPA Predictions
"""

import pandas as pd
import numpy as np
import os

def run_model_b_v2_week4():
    """Run Model B v2 for Week 4 using matchup-specific EPA analysis"""
    
    print("=== Week 4 Model B v2: Matchup-Specific EPA Predictions ===")
    print("Analyzing rush vs pass EPA matchups between teams")

    # Load Week 4 schedule and odds
    week4_odds_path = "../../schedule/week4_2025_odds.csv"
    week4_odds = pd.read_csv(week4_odds_path)

    # Load the detailed SumerSports EPA data with Pass/Rush breakdown
    scraped_epa_path = "../../detailed_epa_data.csv"
    scraped_epa = pd.read_csv(scraped_epa_path)

    print(f"Loaded {len(week4_odds)} games from Week 4 odds")
    print(f"Loaded {len(scraped_epa)} teams from detailed SumerSports EPA data")

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
    week4_odds['underdog_abbr'] = week4_odds['underdog_team'].map(team_name_to_abbr)
    week4_odds['favorite_abbr'] = week4_odds['favorite_team'].map(team_name_to_abbr)

    # Merge EPA data with Week 4 odds
    # For underdog team
    week4_data = week4_odds.merge(
        scraped_epa[['team', 'team_name', 'epa_off_per_play', 'epa_def_allowed_per_play', 
                    'epa_pass_off', 'epa_rush_off', 'epa_pass_def_allowed', 'epa_rush_def_allowed']],
        left_on='underdog_abbr',
        right_on='team',
        how='left',
        suffixes=('', '_underdog')
    )
    week4_data.rename(columns={
        'epa_off_per_play': 'underdog_epa_off',
        'epa_def_allowed_per_play': 'underdog_epa_def_allowed',
        'epa_pass_off': 'underdog_epa_pass_off',
        'epa_rush_off': 'underdog_epa_rush_off',
        'epa_pass_def_allowed': 'underdog_epa_pass_def',
        'epa_rush_def_allowed': 'underdog_epa_rush_def'
    }, inplace=True)
    week4_data.drop(columns=['team', 'team_name'], inplace=True)

    # For favorite team
    week4_data = week4_data.merge(
        scraped_epa[['team', 'team_name', 'epa_off_per_play', 'epa_def_allowed_per_play',
                    'epa_pass_off', 'epa_rush_off', 'epa_pass_def_allowed', 'epa_rush_def_allowed']],
        left_on='favorite_abbr',
        right_on='team',
        how='left',
        suffixes=('', '_favorite')
    )
    week4_data.rename(columns={
        'epa_off_per_play': 'favorite_epa_off',
        'epa_def_allowed_per_play': 'favorite_epa_def_allowed',
        'epa_pass_off': 'favorite_epa_pass_off',
        'epa_rush_off': 'favorite_epa_rush_off',
        'epa_pass_def_allowed': 'favorite_epa_pass_def',
        'epa_rush_def_allowed': 'favorite_epa_rush_def'
    }, inplace=True)
    week4_data.drop(columns=['team', 'team_name'], inplace=True)

    # Matchup-specific EPA analysis
    week4_data['fav_pass_vs_underdog_pass_def'] = week4_data['favorite_epa_pass_off'] - week4_data['underdog_epa_pass_def']
    week4_data['fav_rush_vs_underdog_rush_def'] = week4_data['favorite_epa_rush_off'] - week4_data['underdog_epa_rush_def']
    week4_data['underdog_pass_vs_fav_pass_def'] = week4_data['underdog_epa_pass_off'] - week4_data['favorite_epa_pass_def']
    week4_data['underdog_rush_vs_fav_rush_def'] = week4_data['underdog_epa_rush_off'] - week4_data['favorite_epa_rush_def']
    
    # Overall matchup advantages
    week4_data['favorite_pass_advantage'] = week4_data['fav_pass_vs_underdog_pass_def']
    week4_data['favorite_rush_advantage'] = week4_data['fav_rush_vs_underdog_rush_def']
    week4_data['underdog_pass_advantage'] = week4_data['underdog_pass_vs_fav_pass_def']
    week4_data['underdog_rush_advantage'] = week4_data['underdog_rush_vs_fav_rush_def']
    
    # Net matchup differentials
    week4_data['net_pass_advantage'] = week4_data['favorite_pass_advantage'] - week4_data['underdog_pass_advantage']
    week4_data['net_rush_advantage'] = week4_data['favorite_rush_advantage'] - week4_data['underdog_rush_advantage']
    week4_data['net_matchup_advantage'] = week4_data['net_pass_advantage'] + week4_data['net_rush_advantage']
    
    # Underdog's relative advantages
    week4_data['underdog_total_advantage'] = week4_data['underdog_pass_advantage'] + week4_data['underdog_rush_advantage']
    week4_data['favorite_total_advantage'] = week4_data['favorite_pass_advantage'] + week4_data['favorite_rush_advantage']

    # Model B v2 Logic
    week4_data['cover_probability'] = 0.50

    # Adjust based on underdog's total matchup advantage
    week4_data['cover_probability'] += week4_data['underdog_total_advantage'] * 2.0

    # Adjust based on favorite's total advantage (negative for underdog)
    week4_data['cover_probability'] -= week4_data['favorite_total_advantage'] * 1.5

    # Pass vs Rush balance analysis
    week4_data['pass_rush_balance'] = abs(week4_data['net_pass_advantage'] - week4_data['net_rush_advantage'])
    week4_data['cover_probability'] += week4_data['pass_rush_balance'] * 0.5

    # Spread adjustment
    week4_data['cover_probability'] += week4_data['spread_line'].abs() * 0.01

    # Cap probabilities
    week4_data['cover_probability'] = week4_data['cover_probability'].clip(0.05, 0.95)

    # Enhanced confidence levels
    def assign_confidence(prob):
        if prob >= 0.70:
            return 'VERY_HIGH'
        elif prob >= 0.60:
            return 'HIGH'
        elif prob >= 0.45:
            return 'MEDIUM'
        elif prob >= 0.30:
            return 'LOW'
        else:
            return 'VERY_LOW'
    
    week4_data['confidence'] = week4_data['cover_probability'].apply(assign_confidence)
    week4_data['predicted_cover'] = week4_data['cover_probability'] >= 0.5
    
    # Outright win probability
    week4_data['outright_win_probability'] = week4_data['cover_probability'] * 0.65
    week4_data['outright_win_probability'] = week4_data['outright_win_probability'].clip(0.03, 0.80)
    
    def assign_outright_confidence(prob):
        if prob >= 0.50:
            return 'HIGH'
        elif prob >= 0.35:
            return 'MEDIUM'
        elif prob >= 0.20:
            return 'LOW'
        else:
            return 'VERY_LOW'
    
    week4_data['outright_confidence'] = week4_data['outright_win_probability'].apply(assign_outright_confidence)
    week4_data['predicted_outright_win'] = week4_data['outright_win_probability'] >= 0.5

    print(f"\n=== Week 4 Model B v2 Predictions ===")
    
    # Show detailed matchup analysis for top games
    top_games = week4_data.sort_values(by='cover_probability', ascending=False).head(5)
    
    for _, row in top_games.iterrows():
        print(f"{row['away_team']} at {row['home_team']}: {row['underdog_team']} +{row['spread_line']}")
        print(f"  Cover Probability: {row['cover_probability']:.1%} ({row['confidence']})")
        print(f"  Underdog Pass Advantage: {row['underdog_pass_advantage']:.3f}")
        print(f"  Underdog Rush Advantage: {row['underdog_rush_advantage']:.3f}")
        print(f"  Underdog Total Advantage: {row['underdog_total_advantage']:.3f}")
        print(f"  Net Matchup Advantage: {row['net_matchup_advantage']:.3f}")
        print(f"  Prediction: {'Cover' if row['predicted_cover'] else 'No Cover'}")
        print()

    # Save predictions
    week4_data.to_csv("model_b_v2_week4_predictions.csv", index=False)
    print(f"✅ Model B v2 Week 4 predictions saved to: model_b_v2_week4_predictions.csv")

    return week4_data

if __name__ == "__main__":
    run_model_b_v2_week4()
