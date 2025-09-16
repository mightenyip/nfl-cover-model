#!/usr/bin/env python3
"""
Week 3 2025 NFL Predictions with Jake Browning-adjusted Bengals EPA
"""

import pandas as pd
import os
from datetime import datetime

def run_week3_browning_adjusted():
    print("=== Week 3 2025 NFL Predictions (Browning-Adjusted) ===")
    print("Using SumerSports EPA data with Jake Browning adjustment for Bengals")

    # Load Week 3 schedule and odds
    week3_odds_path = os.path.join("week3", "week3_2025_odds.csv")
    week3_odds = pd.read_csv(week3_odds_path)

    # Load the Browning-adjusted EPA data
    adjusted_epa_path = os.path.join(os.path.dirname(__file__), "..", "sumersports_epa_data_browning_adjusted.csv")
    adjusted_epa = pd.read_csv(adjusted_epa_path)

    print(f"Loaded {len(week3_odds)} games from Week 3 odds")
    print(f"Loaded {len(adjusted_epa)} teams from Browning-adjusted EPA data")

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
        adjusted_epa[['team', 'team_name', 'epa_off_per_play', 'epa_def_allowed_per_play', 'net_epa_per_play']],
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
        adjusted_epa[['team', 'team_name', 'epa_def_allowed_per_play']],
        left_on='favorite_abbr',
        right_on='team',
        how='left',
        suffixes=('', '_opponent')
    )
    week3_data.rename(columns={'epa_def_allowed_per_play': 'opponent_def_epa'}, inplace=True)
    week3_data.drop(columns=['team', 'team_name'], inplace=True)

    # Calculate net EPA differential (underdog_net_epa - favorite_net_epa)
    # We need favorite's net EPA as well
    week3_data = week3_data.merge(
        adjusted_epa[['team', 'net_epa_per_play']],
        left_on='favorite_abbr',
        right_on='team',
        how='left',
        suffixes=('', '_favorite')
    )
    week3_data.rename(columns={'net_epa_per_play': 'favorite_net_epa'}, inplace=True)
    week3_data.drop(columns=['team'], inplace=True)
    week3_data['net_epa_differential'] = week3_data['underdog_net_epa'] - week3_data['favorite_net_epa']

    # Determine defense quality based on opponent_def_epa
    def get_defense_quality(epa):
        if epa > 0.08: # Higher EPA allowed means weaker defense
            return 'WEAK'
        elif epa >= -0.05: # Around league average
            return 'AVERAGE'
        else: # Lower EPA allowed means stronger defense
            return 'STRONG'
    week3_data['defense_quality'] = week3_data['opponent_def_epa'].apply(get_defense_quality)

    # --- Model Logic Using Browning-Adjusted EPA Data ---
    
    # Base probability
    week3_data['cover_probability'] = 0.50

    # Adjust based on opponent defense quality
    # Based on Week 2 actual results, STRONG defenses led to more underdog covers
    week3_data.loc[week3_data['defense_quality'] == 'STRONG', 'cover_probability'] += 0.12
    week3_data.loc[week3_data['defense_quality'] == 'WEAK', 'cover_probability'] -= 0.10
    week3_data.loc[week3_data['defense_quality'] == 'AVERAGE', 'cover_probability'] += 0.02

    # Adjust based on net EPA differential (underdog_net_epa - favorite_net_epa)
    # Positive differential means underdog is performing better overall
    week3_data['cover_probability'] += week3_data['net_epa_differential'] * 0.8

    # Adjust based on spread line (larger spread, slightly higher chance to cover for underdog)
    week3_data['cover_probability'] += week3_data['spread_line'].abs() * 0.008

    # Cap probabilities
    week3_data['cover_probability'] = week3_data['cover_probability'].clip(0.05, 0.95)

    # Assign confidence levels based on probability
    def assign_confidence(prob):
        if prob >= 0.65:
            return 'HIGH'
        elif prob >= 0.40:
            return 'MEDIUM'
        else:
            return 'LOW'
    
    week3_data['confidence'] = week3_data['cover_probability'].apply(assign_confidence)
    week3_data['predicted_cover'] = week3_data['cover_probability'] >= 0.5
    
    # Calculate outright win probability
    week3_data['outright_win_probability'] = week3_data['cover_probability'] * 0.7
    week3_data['outright_win_probability'] = week3_data['outright_win_probability'].clip(0.05, 0.85)
    
    # Assign outright win confidence levels
    def assign_outright_confidence(prob):
        if prob >= 0.45:
            return 'HIGH'
        elif prob >= 0.25:
            return 'MEDIUM'
        else:
            return 'LOW'
    
    week3_data['outright_confidence'] = week3_data['outright_win_probability'].apply(assign_outright_confidence)
    week3_data['predicted_outright_win'] = week3_data['outright_win_probability'] >= 0.5

    print(f"\n=== Week 3 Predictions (Browning-Adjusted) ===")
    print(f"Data source: SumerSports EPA with Jake Browning adjustment")
    
    # Focus on Bengals game
    bengals_game = week3_data[week3_data['underdog_team'] == 'Bengals'].iloc[0]
    print(f"\n=== Bengals vs Vikings (Key Game) ===")
    print(f"Bengals Net EPA: {bengals_game['underdog_net_epa']:.4f}")
    print(f"Vikings Net EPA: {bengals_game['favorite_net_epa']:.4f}")
    print(f"Net EPA Differential: {bengals_game['net_epa_differential']:.4f}")
    print(f"Cover Probability: {bengals_game['cover_probability']:.1%}")
    print(f"Outright Win Probability: {bengals_game['outright_win_probability']:.1%}")
    print(f"Cover Confidence: {bengals_game['confidence']}")
    print(f"Outright Confidence: {bengals_game['outright_confidence']}")
    
    print(f"\nAll Games (sorted by cover probability):")
    for _, row in week3_data.sort_values(by='cover_probability', ascending=False).iterrows():
        print(f"{row['away_team']} at {row['home_team']}: {row['underdog_team']} +{row['spread_line']}")
        print(f"  Cover Probability: {row['cover_probability']:.1%}")
        print(f"  Outright Win Probability: {row['outright_win_probability']:.1%}")
        print(f"  Cover Confidence: {row['confidence']}")
        print(f"  Outright Confidence: {row['outright_confidence']}")
        print(f"  Net EPA Diff: {row['net_epa_differential']:.3f}")
        print(f"  Opponent Defense: {row['defense_quality']} ({row['opponent_def_epa']:.3f})")
        print(f"  Cover Prediction: {'Cover' if row['predicted_cover'] else 'No Cover'}")
        print(f"  Outright Prediction: {'Underdog Wins' if row['predicted_outright_win'] else 'Favorite Wins'}")
        print()

    # Confidence level breakdown
    confidence_counts = week3_data['confidence'].value_counts()
    print(f"=== Confidence Level Distribution ===")
    for conf in ['HIGH', 'MEDIUM', 'LOW']:
        count = confidence_counts.get(conf, 0)
        print(f"{conf}: {count} games")

    print(f"\n=== High Confidence Picks ===")
    high_conf = week3_data[week3_data['confidence'] == 'HIGH'].sort_values(by='cover_probability', ascending=False)
    for _, row in high_conf.iterrows():
        print(f"{row['underdog_team']} +{row['spread_line']} vs {row['favorite_team']} ({row['cover_probability']:.1%})")

    print(f"\n=== Medium Confidence Picks ===")
    medium_conf = week3_data[week3_data['confidence'] == 'MEDIUM'].sort_values(by='cover_probability', ascending=False)
    for _, row in medium_conf.iterrows():
        print(f"{row['underdog_team']} +{row['spread_line']} vs {row['favorite_team']} ({row['cover_probability']:.1%})")

    print(f"\n=== Low Confidence Picks ===")
    low_conf = week3_data[week3_data['confidence'] == 'LOW'].sort_values(by='cover_probability', ascending=False)
    for _, row in low_conf.iterrows():
        print(f"{row['underdog_team']} +{row['spread_line']} vs {row['favorite_team']} ({row['cover_probability']:.1%})")

    # Outright win predictions
    print(f"\n=== Outright Win Predictions ===")
    outright_high = week3_data[week3_data['outright_confidence'] == 'HIGH'].sort_values(by='outright_win_probability', ascending=False)
    if not outright_high.empty:
        print(f"\nHigh Confidence Outright Wins:")
        for _, row in outright_high.iterrows():
            print(f"{row['underdog_team']} vs {row['favorite_team']} ({row['outright_win_probability']:.1%})")
    
    outright_medium = week3_data[week3_data['outright_confidence'] == 'MEDIUM'].sort_values(by='outright_win_probability', ascending=False)
    if not outright_medium.empty:
        print(f"\nMedium Confidence Outright Wins:")
        for _, row in outright_medium.iterrows():
            print(f"{row['underdog_team']} vs {row['favorite_team']} ({row['outright_win_probability']:.1%})")
    
    # Count outright win predictions
    outright_wins_predicted = week3_data['predicted_outright_win'].sum()
    print(f"\nOutright Win Summary:")
    print(f"Underdog outright wins predicted: {outright_wins_predicted}")
    print(f"Favorite outright wins predicted: {len(week3_data) - outright_wins_predicted}")

    # Defense quality analysis
    print(f"\n=== Defense Quality Analysis ===")
    defense_quality_summary = week3_data.groupby('defense_quality').agg(
        count=('cover_probability', 'count'),
        mean_prob=('cover_probability', 'mean'),
        mean_predicted=('predicted_cover', 'mean')
    ).round(3)
    print(defense_quality_summary)

    # Save predictions
    predictions_output_path = os.path.join("week3", "week3_predictions_browning_adjusted.csv")
    week3_data.to_csv(predictions_output_path, index=False)
    print(f"\n✅ Predictions saved to {predictions_output_path}")

    # Summary statistics
    print(f"\n=== Week 3 Summary (Browning-Adjusted) ===")
    print(f"Total games: {len(week3_data)}")
    print(f"Underdog covers predicted: {week3_data['predicted_cover'].sum()}")
    print(f"Favorite covers predicted: {(~week3_data['predicted_cover']).sum()}")
    print(f"Underdog outright wins predicted: {week3_data['predicted_outright_win'].sum()}")
    print(f"Favorite outright wins predicted: {(~week3_data['predicted_outright_win']).sum()}")
    
    avg_spread = week3_data['spread_line'].mean()
    print(f"Average spread: {avg_spread:.1f} points")
    
    avg_prob = week3_data['cover_probability'].mean()
    print(f"Average cover probability: {avg_prob:.1%}")
    
    avg_outright = week3_data['outright_win_probability'].mean()
    print(f"Average outright win probability: {avg_outright:.1%}")

if __name__ == "__main__":
    run_week3_browning_adjusted()
