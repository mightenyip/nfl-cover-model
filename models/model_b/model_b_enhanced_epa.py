#!/usr/bin/env python3
"""
Model B: Enhanced EPA Model - Using updated SumerSports data with advanced features
"""

import pandas as pd
import numpy as np
import os
from datetime import datetime

def run_model_b_enhanced_epa():
    """Run Model B using enhanced EPA analysis with updated data"""
    
    print("=== Model B: Enhanced EPA Predictions ===")
    print("Using updated SumerSports data with advanced features")
    print(f"Data scraped: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}")

    # Load Week 3 schedule and odds
    week3_odds_path = "../../week3/week3_2025_odds.csv"
    week3_odds = pd.read_csv(week3_odds_path)

    # Load the updated SumerSports EPA data
    scraped_epa_path = "../../data/sumersports_epa_data.csv"
    scraped_epa = pd.read_csv(scraped_epa_path)

    print(f"Loaded {len(week3_odds)} games from Week 3 odds")
    print(f"Loaded {len(scraped_epa)} teams from updated SumerSports EPA data")

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
    
    # Add abbreviation columns to week3_odds
    week3_odds['underdog_abbr'] = week3_odds['underdog_team'].map(team_name_to_abbr)
    week3_odds['favorite_abbr'] = week3_odds['favorite_team'].map(team_name_to_abbr)

    # Merge EPA data with Week 3 odds
    # For underdog team
    week3_data = week3_odds.merge(
        scraped_epa[['team', 'team_name', 'epa_off_per_play', 'epa_def_allowed_per_play', 'net_epa_per_play']],
        left_on='underdog_abbr',
        right_on='team',
        how='left',
        suffixes=('', '_underdog')
    )
    week3_data.rename(columns={
        'epa_off_per_play': 'underdog_epa_off',
        'epa_def_allowed_per_play': 'underdog_epa_def_allowed',
        'net_epa_per_play': 'underdog_net_epa'
    }, inplace=True)
    week3_data.drop(columns=['team', 'team_name'], inplace=True)

    # For favorite team (opponent defense)
    week3_data = week3_data.merge(
        scraped_epa[['team', 'team_name', 'epa_def_allowed_per_play']],
        left_on='favorite_abbr',
        right_on='team',
        how='left',
        suffixes=('', '_opponent')
    )
    week3_data.rename(columns={'epa_def_allowed_per_play': 'opponent_def_epa'}, inplace=True)
    week3_data.drop(columns=['team', 'team_name'], inplace=True)

    # Calculate net EPA differential (underdog_net_epa - favorite_net_epa)
    week3_data = week3_data.merge(
        scraped_epa[['team', 'net_epa_per_play']],
        left_on='favorite_abbr',
        right_on='team',
        how='left',
        suffixes=('', '_favorite')
    )
    week3_data.rename(columns={'net_epa_per_play': 'favorite_net_epa'}, inplace=True)
    week3_data.drop(columns=['team'], inplace=True)
    week3_data['net_epa_differential'] = week3_data['underdog_net_epa'] - week3_data['favorite_net_epa']

    # === MODEL B: ENHANCED FEATURES ===
    
    # 1. Advanced Defense Quality Classification (3-tier system)
    def get_enhanced_defense_quality(epa):
        if epa < -0.10:  # Elite defense (allows very low EPA)
            return 'ELITE'
        elif epa < -0.05:  # Strong defense
            return 'STRONG'
        elif epa < 0.05:   # Average defense
            return 'AVERAGE'
        elif epa < 0.15:   # Weak defense
            return 'WEAK'
        else:  # Poor defense (allows high EPA)
            return 'POOR'
    
    week3_data['defense_quality'] = week3_data['opponent_def_epa'].apply(get_enhanced_defense_quality)

    # 2. Spread-adjusted EPA analysis
    week3_data['spread_adjusted_epa'] = week3_data['net_epa_differential'] / (week3_data['spread_line'].abs() + 1)
    
    # 3. Relative strength indicator
    week3_data['relative_strength'] = week3_data['underdog_net_epa'] / (week3_data['favorite_net_epa'] + 0.01)

    # 4. Matchup difficulty score
    week3_data['matchup_difficulty'] = (
        week3_data['spread_line'].abs() * 0.1 + 
        (week3_data['opponent_def_epa'] * -1) * 0.5 +  # Negative opponent EPA is good for underdog
        (week3_data['underdog_net_epa'] * -1) * 0.3    # Negative underdog EPA is bad
    )

    # === MODEL B LOGIC ===
    
    # Base probability (slightly higher baseline)
    week3_data['cover_probability'] = 0.52

    # Enhanced defense quality adjustments
    defense_adjustments = {
        'ELITE': 0.18,    # Elite defenses are very hard to score against
        'STRONG': 0.12,   # Strong defenses favor underdogs
        'AVERAGE': 0.03,  # Average defenses slightly favor underdogs
        'WEAK': -0.08,    # Weak defenses favor favorites
        'POOR': -0.15     # Poor defenses heavily favor favorites
    }
    
    for quality, adjustment in defense_adjustments.items():
        week3_data.loc[week3_data['defense_quality'] == quality, 'cover_probability'] += adjustment

    # Net EPA differential adjustment (more aggressive)
    week3_data['cover_probability'] += week3_data['net_epa_differential'] * 1.2

    # Spread-adjusted EPA factor
    week3_data['cover_probability'] += week3_data['spread_adjusted_epa'] * 0.3

    # Relative strength factor
    week3_data['cover_probability'] += (week3_data['relative_strength'] - 1) * 0.1

    # Matchup difficulty adjustment
    week3_data['cover_probability'] -= week3_data['matchup_difficulty'] * 0.05

    # Spread line adjustment (larger spreads = more likely underdog covers)
    week3_data['cover_probability'] += week3_data['spread_line'].abs() * 0.012

    # Cap probabilities
    week3_data['cover_probability'] = week3_data['cover_probability'].clip(0.02, 0.98)

    # Enhanced confidence levels
    def assign_enhanced_confidence(prob):
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
    
    week3_data['confidence'] = week3_data['cover_probability'].apply(assign_enhanced_confidence)
    week3_data['predicted_cover'] = week3_data['cover_probability'] >= 0.5
    
    # Outright win probability (more conservative)
    week3_data['outright_win_probability'] = week3_data['cover_probability'] * 0.65
    week3_data['outright_win_probability'] = week3_data['outright_win_probability'].clip(0.03, 0.80)
    
    # Outright win confidence levels
    def assign_outright_confidence(prob):
        if prob >= 0.50:
            return 'HIGH'
        elif prob >= 0.35:
            return 'MEDIUM'
        elif prob >= 0.20:
            return 'LOW'
        else:
            return 'VERY_LOW'
    
    week3_data['outright_confidence'] = week3_data['outright_win_probability'].apply(assign_outright_confidence)
    week3_data['predicted_outright_win'] = week3_data['outright_win_probability'] >= 0.5

    print(f"\n=== Model B Predictions (Enhanced EPA) ===")
    print(f"Data source: Updated SumerSports EPA (scraped {datetime.now().strftime('%Y-%m-%d %H:%M:%S')})")
    
    # Show key games with detailed analysis
    print(f"\n=== Key Games Analysis ===")
    key_games = week3_data.sort_values(by='cover_probability', ascending=False).head(5)
    for _, row in key_games.iterrows():
        print(f"\n{row['away_team']} at {row['home_team']}: {row['underdog_team']} +{row['spread_line']}")
        print(f"  Cover Probability: {row['cover_probability']:.1%} ({row['confidence']})")
        print(f"  Net EPA Diff: {row['net_epa_differential']:.3f}")
        print(f"  Opponent Defense: {row['defense_quality']} ({row['opponent_def_epa']:.3f})")
        print(f"  Matchup Difficulty: {row['matchup_difficulty']:.3f}")
        print(f"  Prediction: {'Cover' if row['predicted_cover'] else 'No Cover'}")
    
    # Confidence level breakdown
    confidence_counts = week3_data['confidence'].value_counts()
    print(f"\n=== Confidence Level Distribution ===")
    for conf in ['VERY_HIGH', 'HIGH', 'MEDIUM', 'LOW', 'VERY_LOW']:
        count = confidence_counts.get(conf, 0)
        print(f"{conf}: {count} games")

    # Defense quality analysis
    print(f"\n=== Defense Quality Analysis ===")
    defense_quality_summary = week3_data.groupby('defense_quality').agg(
        count=('cover_probability', 'count'),
        mean_prob=('cover_probability', 'mean'),
        mean_predicted=('predicted_cover', 'mean')
    ).round(3)
    print(defense_quality_summary)

    # Top predictions by confidence
    print(f"\n=== Very High Confidence Picks ===")
    very_high = week3_data[week3_data['confidence'] == 'VERY_HIGH'].sort_values(by='cover_probability', ascending=False)
    for _, row in very_high.iterrows():
        print(f"{row['underdog_team']} +{row['spread_line']} vs {row['favorite_team']} ({row['cover_probability']:.1%})")

    print(f"\n=== High Confidence Picks ===")
    high_conf = week3_data[week3_data['confidence'] == 'HIGH'].sort_values(by='cover_probability', ascending=False)
    for _, row in high_conf.iterrows():
        print(f"{row['underdog_team']} +{row['spread_line']} vs {row['favorite_team']} ({row['cover_probability']:.1%})")

    # Save predictions
    week3_data.to_csv("model_b_week3_predictions.csv", index=False)
    print(f"\n✅ Model B predictions saved to: model_b_week3_predictions.csv")

    # Summary statistics
    print(f"\n=== Model B Summary ===")
    print(f"Total games: {len(week3_data)}")
    print(f"Underdog covers predicted: {week3_data['predicted_cover'].sum()}")
    print(f"Favorite covers predicted: {(~week3_data['predicted_cover']).sum()}")
    print(f"Outright wins predicted: {week3_data['predicted_outright_win'].sum()}")
    
    avg_spread = week3_data['spread_line'].mean()
    print(f"Average spread: {avg_spread:.1f} points")
    
    avg_prob = week3_data['cover_probability'].mean()
    print(f"Average cover probability: {avg_prob:.1%}")
    
    avg_outright = week3_data['outright_win_probability'].mean()
    print(f"Average outright win probability: {avg_outright:.1%}")

    return week3_data

if __name__ == "__main__":
    run_model_b_enhanced_epa()
