#!/usr/bin/env python3
"""
Week 3 SumerSports Model - Using the same methodology that achieved 81.2% accuracy in Week 2
"""

import pandas as pd
import numpy as np
import os

def run_week3_sumersports_model():
    """Run Week 3 model using SumerSports EPA data with the proven methodology"""
    
    print("=== Week 3 SumerSports Model Predictions ===")
    print("Using methodology that achieved 81.2% accuracy in Week 2")

    # Load Week 3 schedule and odds
    week3_odds_path = "../../week3/week3_2025_odds.csv"
    week3_odds = pd.read_csv(week3_odds_path)

    # Load the SumerSports EPA data
    scraped_epa_path = "../../data/sumersports_epa_data.csv"
    scraped_epa = pd.read_csv(scraped_epa_path)

    print(f"Loaded {len(week3_odds)} games from Week 3 odds")
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
    # We need favorite's net EPA as well
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

    # Determine defense quality based on opponent_def_epa
    # Using the same thresholds that worked in Week 2
    def get_defense_quality(epa):
        if epa > 0.10:  # Weak defense (allows high EPA)
            return 'WEAK'
        elif epa >= -0.05:  # Average defense
            return 'AVERAGE'
        else:  # Strong defense (allows low/negative EPA)
            return 'STRONG'
    
    week3_data['defense_quality'] = week3_data['opponent_def_epa'].apply(get_defense_quality)

    # Check for missing data
    missing_teams = week3_data[week3_data['underdog_epa_off'].isna() | week3_data['opponent_def_epa'].isna()]
    if not missing_teams.empty:
        print(f"\n⚠️  Missing EPA data for {len(missing_teams)} games:")
        for _, row in missing_teams.iterrows():
            print(f"  {row['underdog_team']} vs {row['favorite_team']}")
        
        # Fill missing data with league average
        league_avg_off = scraped_epa['epa_off_per_play'].mean()
        league_avg_def = scraped_epa['epa_def_allowed_per_play'].mean()
        league_avg_net = scraped_epa['net_epa_per_play'].mean()
        
        week3_data = week3_data.copy()  # Avoid chained assignment warnings
        week3_data['underdog_epa_off'] = week3_data['underdog_epa_off'].fillna(league_avg_off)
        week3_data['underdog_epa_def_allowed'] = week3_data['underdog_epa_def_allowed'].fillna(league_avg_def)
        week3_data['underdog_net_epa'] = week3_data['underdog_net_epa'].fillna(league_avg_net)
        week3_data['opponent_def_epa'] = week3_data['opponent_def_epa'].fillna(league_avg_def)
        week3_data['favorite_net_epa'] = week3_data['favorite_net_epa'].fillna(league_avg_net)
        week3_data['net_epa_differential'] = week3_data['underdog_net_epa'] - week3_data['favorite_net_epa']
        
        print(f"✅ Filled missing data with league averages")

    # --- Model Logic Using Same Methodology as Week 2 ---
    # This model uses the exact same logic that achieved 81.2% accuracy
    
    # Base probability
    week3_data['cover_probability'] = 0.50

    # Adjust based on opponent defense quality
    # Based on Week 2 results, STRONG defenses led to more underdog covers
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

    print(f"\n=== Week 3 Underdog Cover Predictions ===")
    print(f"Data source: SumerSports (using proven methodology)")
    
    print(f"\nAll Games (sorted by cover probability):")
    for _, row in week3_data.sort_values(by='cover_probability', ascending=False).iterrows():
        print(f"{row['away_team']} at {row['home_team']}: {row['underdog_team']} +{row['spread_line']}")
        print(f"  Cover Probability: {row['cover_probability']:.1%}")
        print(f"  Confidence: {row['confidence']}")
        print(f"  Net EPA Diff: {row['net_epa_differential']:.3f}")
        print(f"  Opponent Defense: {row['defense_quality']} ({row['opponent_def_epa']:.3f})")
        print(f"  Prediction: {'Cover' if row['predicted_cover'] else 'No Cover'}")
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

    # Defense quality analysis
    print(f"\n=== Defense Quality Analysis ===")
    defense_quality_summary = week3_data.groupby('defense_quality').agg(
        count=('cover_probability', 'count'),
        mean_prob=('cover_probability', 'mean'),
        mean_predicted=('predicted_cover', 'mean')
    ).round(3)
    print(defense_quality_summary)

    # Save predictions
    week3_data.to_csv("model_a_week3_predictions.csv", index=False)
    print(f"\n✅ Predictions saved to: model_a_week3_predictions.csv")

    return week3_data

if __name__ == "__main__":
    run_model_a_sumersports()
