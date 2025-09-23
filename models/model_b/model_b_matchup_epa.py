#!/usr/bin/env python3
"""
Model B v2: Matchup-Specific EPA Model
Analyzes rush vs pass EPA matchups between teams
"""

import pandas as pd
import numpy as np
import os
from datetime import datetime

def run_model_b_matchup_epa():
    """Run Model B v2 using matchup-specific EPA analysis"""
    
    print("=== Model B v2: Matchup-Specific EPA Predictions ===")
    print("Analyzing rush vs pass EPA matchups between teams")
    print(f"Data scraped: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}")

    # Load Week 3 schedule and odds
    week3_odds_path = "../../week3/week3_2025_odds.csv"
    week3_odds = pd.read_csv(week3_odds_path)

    # Load the detailed SumerSports EPA data with Pass/Rush breakdown
    scraped_epa_path = "../../detailed_epa_data.csv"
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

    # Using actual EPA/Pass and EPA/Rush data from SumerSports
    print("✅ Using actual EPA/Pass and EPA/Rush data from SumerSports detailed scraper")

    # Merge EPA data with Week 3 odds
    # For underdog team
    week3_data = week3_odds.merge(
        scraped_epa[['team', 'team_name', 'epa_off_per_play', 'epa_def_allowed_per_play', 
                    'epa_pass_off', 'epa_rush_off', 'epa_pass_def_allowed', 'epa_rush_def_allowed']],
        left_on='underdog_abbr',
        right_on='team',
        how='left',
        suffixes=('', '_underdog')
    )
    week3_data.rename(columns={
        'epa_off_per_play': 'underdog_epa_off',
        'epa_def_allowed_per_play': 'underdog_epa_def_allowed',
        'epa_pass_off': 'underdog_epa_pass_off',
        'epa_rush_off': 'underdog_epa_rush_off',
        'epa_pass_def_allowed': 'underdog_epa_pass_def',
        'epa_rush_def_allowed': 'underdog_epa_rush_def'
    }, inplace=True)
    week3_data.drop(columns=['team', 'team_name'], inplace=True)

    # For favorite team
    week3_data = week3_data.merge(
        scraped_epa[['team', 'team_name', 'epa_off_per_play', 'epa_def_allowed_per_play',
                    'epa_pass_off', 'epa_rush_off', 'epa_pass_def_allowed', 'epa_rush_def_allowed']],
        left_on='favorite_abbr',
        right_on='team',
        how='left',
        suffixes=('', '_favorite')
    )
    week3_data.rename(columns={
        'epa_off_per_play': 'favorite_epa_off',
        'epa_def_allowed_per_play': 'favorite_epa_def_allowed',
        'epa_pass_off': 'favorite_epa_pass_off',
        'epa_rush_off': 'favorite_epa_rush_off',
        'epa_pass_def_allowed': 'favorite_epa_pass_def',
        'epa_rush_def_allowed': 'favorite_epa_rush_def'
    }, inplace=True)
    week3_data.drop(columns=['team', 'team_name'], inplace=True)

    # === MATCHUP-SPECIFIC EPA ANALYSIS ===
    
    # Favorite's offensive matchups vs Underdog's defense
    week3_data['fav_pass_vs_underdog_pass_def'] = week3_data['favorite_epa_pass_off'] - week3_data['underdog_epa_pass_def']
    week3_data['fav_rush_vs_underdog_rush_def'] = week3_data['favorite_epa_rush_off'] - week3_data['underdog_epa_rush_def']
    week3_data['fav_pass_vs_underdog_rush_def'] = week3_data['favorite_epa_pass_off'] - week3_data['underdog_epa_rush_def']
    week3_data['fav_rush_vs_underdog_pass_def'] = week3_data['favorite_epa_rush_off'] - week3_data['underdog_epa_pass_def']
    
    # Underdog's offensive matchups vs Favorite's defense
    week3_data['underdog_pass_vs_fav_pass_def'] = week3_data['underdog_epa_pass_off'] - week3_data['favorite_epa_pass_def']
    week3_data['underdog_rush_vs_fav_rush_def'] = week3_data['underdog_epa_rush_off'] - week3_data['favorite_epa_rush_def']
    week3_data['underdog_pass_vs_fav_rush_def'] = week3_data['underdog_epa_pass_off'] - week3_data['favorite_epa_rush_def']
    week3_data['underdog_rush_vs_fav_pass_def'] = week3_data['underdog_epa_rush_off'] - week3_data['favorite_epa_pass_def']
    
    # Overall matchup advantages
    week3_data['favorite_pass_advantage'] = week3_data['fav_pass_vs_underdog_pass_def']
    week3_data['favorite_rush_advantage'] = week3_data['fav_rush_vs_underdog_rush_def']
    week3_data['underdog_pass_advantage'] = week3_data['underdog_pass_vs_fav_pass_def']
    week3_data['underdog_rush_advantage'] = week3_data['underdog_rush_vs_fav_rush_def']
    
    # Net matchup differentials
    week3_data['net_pass_advantage'] = week3_data['favorite_pass_advantage'] - week3_data['underdog_pass_advantage']
    week3_data['net_rush_advantage'] = week3_data['favorite_rush_advantage'] - week3_data['underdog_rush_advantage']
    week3_data['net_matchup_advantage'] = week3_data['net_pass_advantage'] + week3_data['net_rush_advantage']
    
    # Underdog's relative advantages (what we care about for spread betting)
    week3_data['underdog_total_advantage'] = week3_data['underdog_pass_advantage'] + week3_data['underdog_rush_advantage']
    week3_data['favorite_total_advantage'] = week3_data['favorite_pass_advantage'] + week3_data['favorite_rush_advantage']

    # === MODEL B v2 LOGIC ===
    
    # Base probability
    week3_data['cover_probability'] = 0.50

    # Adjust based on underdog's total matchup advantage
    week3_data['cover_probability'] += week3_data['underdog_total_advantage'] * 2.0

    # Adjust based on favorite's total advantage (negative for underdog)
    week3_data['cover_probability'] -= week3_data['favorite_total_advantage'] * 1.5

    # Pass vs Rush balance analysis
    week3_data['pass_rush_balance'] = abs(week3_data['net_pass_advantage'] - week3_data['net_rush_advantage'])
    week3_data['cover_probability'] += week3_data['pass_rush_balance'] * 0.5

    # Spread adjustment (larger spreads favor underdogs slightly)
    week3_data['cover_probability'] += week3_data['spread_line'].abs() * 0.01

    # Cap probabilities
    week3_data['cover_probability'] = week3_data['cover_probability'].clip(0.05, 0.95)

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
    
    week3_data['confidence'] = week3_data['cover_probability'].apply(assign_confidence)
    week3_data['predicted_cover'] = week3_data['cover_probability'] >= 0.5
    
    # Outright win probability
    week3_data['outright_win_probability'] = week3_data['cover_probability'] * 0.65
    week3_data['outright_win_probability'] = week3_data['outright_win_probability'].clip(0.03, 0.80)
    
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

    print(f"\n=== Model B v2 Predictions (Matchup-Specific EPA) ===")
    print(f"Methodology: Rush vs Pass EPA matchup analysis")
    
    # Show detailed matchup analysis for top games
    print(f"\n=== Top Matchup Analysis ===")
    top_games = week3_data.sort_values(by='cover_probability', ascending=False).head(5)
    
    for _, row in top_games.iterrows():
        print(f"\n{row['away_team']} at {row['home_team']}: {row['underdog_team']} +{row['spread_line']}")
        print(f"  Cover Probability: {row['cover_probability']:.1%} ({row['confidence']})")
        print(f"  Underdog Pass Advantage: {row['underdog_pass_advantage']:.3f}")
        print(f"  Underdog Rush Advantage: {row['underdog_rush_advantage']:.3f}")
        print(f"  Underdog Total Advantage: {row['underdog_total_advantage']:.3f}")
        print(f"  Favorite Total Advantage: {row['favorite_total_advantage']:.3f}")
        print(f"  Net Matchup Advantage: {row['net_matchup_advantage']:.3f}")
        print(f"  Pass/Rush Balance: {row['pass_rush_balance']:.3f}")
        print(f"  Prediction: {'Cover' if row['predicted_cover'] else 'No Cover'}")
    
    # Confidence level breakdown
    confidence_counts = week3_data['confidence'].value_counts()
    print(f"\n=== Confidence Level Distribution ===")
    for conf in ['VERY_HIGH', 'HIGH', 'MEDIUM', 'LOW', 'VERY_LOW']:
        count = confidence_counts.get(conf, 0)
        print(f"{conf}: {count} games")

    # Matchup advantage analysis
    print(f"\n=== Matchup Advantage Analysis ===")
    print(f"Average Underdog Advantage: {week3_data['underdog_total_advantage'].mean():.3f}")
    print(f"Average Favorite Advantage: {week3_data['favorite_total_advantage'].mean():.3f}")
    print(f"Average Net Advantage: {week3_data['net_matchup_advantage'].mean():.3f}")

    # Save predictions
    week3_data.to_csv("model_b_v2_week3_predictions.csv", index=False)
    print(f"\n✅ Model B v2 predictions saved to: model_b_v2_week3_predictions.csv")

    # Summary statistics
    print(f"\n=== Model B v2 Summary ===")
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
    run_model_b_matchup_epa()
