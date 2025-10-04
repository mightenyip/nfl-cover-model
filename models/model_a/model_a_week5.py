#!/usr/bin/env python3
"""
Model A Week 5: SumerSports EPA Predictions
"""

import pandas as pd
import numpy as np
import os

def run_model_a_week5():
    """Run Model A for Week 5 using SumerSports EPA data"""
    
    print("=== Week 5 Model A: SumerSports EPA Predictions ===")
    print("Using proven SumerSports EPA methodology")

    # Load Week 5 schedule and odds
    week5_odds_path = "../../schedule/week5_2025_odds.csv"
    week5_odds = pd.read_csv(week5_odds_path)

    # Load the SumerSports EPA data
    scraped_epa_path = "../../data/sumersports_epa_data.csv"
    scraped_epa = pd.read_csv(scraped_epa_path)

    print(f"Loaded {len(week5_odds)} games from Week 5 odds")
    print(f"Loaded {len(scraped_epa)} teams from SumerSports EPA data")

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
    week5_odds['underdog_abbr'] = week5_odds['underdog_team'].map(team_name_to_abbr)
    week5_odds['favorite_abbr'] = week5_odds['favorite_team'].map(team_name_to_abbr)

    # Merge EPA data with Week 5 odds
    # For underdog team
    week5_data = week5_odds.merge(
        scraped_epa[['team', 'team_name', 'epa_off_per_play', 'epa_def_allowed_per_play', 'net_epa_per_play']],
        left_on='underdog_abbr',
        right_on='team',
        how='left',
        suffixes=('', '_underdog')
    )
    week5_data.rename(columns={
        'epa_off_per_play': 'underdog_epa_off',
        'epa_def_allowed_per_play': 'underdog_epa_def_allowed',
        'net_epa_per_play': 'underdog_net_epa'
    }, inplace=True)
    week5_data.drop(columns=['team', 'team_name'], inplace=True)

    # For favorite team (opponent defense)
    week5_data = week5_data.merge(
        scraped_epa[['team', 'team_name', 'epa_def_allowed_per_play']],
        left_on='favorite_abbr',
        right_on='team',
        how='left',
        suffixes=('', '_opponent')
    )
    week5_data.rename(columns={'epa_def_allowed_per_play': 'opponent_def_epa'}, inplace=True)
    week5_data.drop(columns=['team', 'team_name'], inplace=True)

    # Calculate net EPA differential
    week5_data = week5_data.merge(
        scraped_epa[['team', 'net_epa_per_play']],
        left_on='favorite_abbr',
        right_on='team',
        how='left',
        suffixes=('', '_favorite')
    )
    week5_data.rename(columns={'net_epa_per_play': 'favorite_net_epa'}, inplace=True)
    week5_data.drop(columns=['team'], inplace=True)
    week5_data['net_epa_differential'] = week5_data['underdog_net_epa'] - week5_data['favorite_net_epa']

    # Determine defense quality
    def get_defense_quality(epa):
        if epa > 0.10:
            return 'WEAK'
        elif epa >= -0.05:
            return 'AVERAGE'
        else:
            return 'STRONG'
    
    week5_data['defense_quality'] = week5_data['opponent_def_epa'].apply(get_defense_quality)

    # Model A Logic
    week5_data['cover_probability'] = 0.50

    # Defense quality adjustments
    week5_data.loc[week5_data['defense_quality'] == 'STRONG', 'cover_probability'] += 0.12
    week5_data.loc[week5_data['defense_quality'] == 'WEAK', 'cover_probability'] -= 0.10
    week5_data.loc[week5_data['defense_quality'] == 'AVERAGE', 'cover_probability'] += 0.02

    # Net EPA differential
    week5_data['cover_probability'] += week5_data['net_epa_differential'] * 0.8

    # Spread adjustment
    week5_data['cover_probability'] += week5_data['spread_line'].abs() * 0.008

    # Cap probabilities
    week5_data['cover_probability'] = week5_data['cover_probability'].clip(0.05, 0.95)

    # Assign confidence levels
    def assign_confidence(prob):
        if prob >= 0.65:
            return 'HIGH'
        elif prob >= 0.40:
            return 'MEDIUM'
        else:
            return 'LOW'
    
    week5_data['confidence'] = week5_data['cover_probability'].apply(assign_confidence)
    week5_data['predicted_cover'] = week5_data['cover_probability'] >= 0.5

    # Outright win probability
    week5_data['outright_win_probability'] = week5_data['cover_probability'] * 0.7
    week5_data['outright_win_probability'] = week5_data['outright_win_probability'].clip(0.05, 0.85)
    
    def assign_outright_confidence(prob):
        if prob >= 0.45:
            return 'HIGH'
        elif prob >= 0.25:
            return 'MEDIUM'
        else:
            return 'LOW'
    
    week5_data['outright_confidence'] = week5_data['outright_win_probability'].apply(assign_outright_confidence)
    week5_data['predicted_outright_win'] = week5_data['outright_win_probability'] >= 0.5

    print(f"\n=== Week 5 Model A Predictions ===")
    
    # Show predictions
    for _, row in week5_data.sort_values(by='cover_probability', ascending=False).iterrows():
        print(f"{row['away_team']} at {row['home_team']}: {row['underdog_team']} +{row['spread_line']}")
        print(f"  Cover Probability: {row['cover_probability']:.1%} ({row['confidence']})")
        print(f"  Net EPA Diff: {row['net_epa_differential']:.3f}")
        print(f"  Opponent Defense: {row['defense_quality']} ({row['opponent_def_epa']:.3f})")
        print(f"  Prediction: {'Cover' if row['predicted_cover'] else 'No Cover'}")
        print()

    # Save predictions
    week5_data.to_csv("model_a_week5_predictions.csv", index=False)
    print(f"✅ Model A Week 5 predictions saved to: model_a_week5_predictions.csv")

    return week5_data

if __name__ == "__main__":
    run_model_a_week5()
