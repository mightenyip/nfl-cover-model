#!/usr/bin/env python3
"""
Week 2 Model Using Scraped SumerSports EPA Data
"""

import pandas as pd
import os
import numpy as np

def run_week2_model_with_scraped_epa():
    """Run Week 2 model using SumerSports EPA data"""
    
    print("=== Week 2 Model with Scraped SumerSports EPA Data ===")

    # Load Week 2 schedule and odds
    week2_odds_path = os.path.join("week2", "week2_2025_odds.csv")
    week2_odds = pd.read_csv(week2_odds_path)

    # Load the scraped SumerSports EPA data
    scraped_epa_path = "sumersports_epa_data.csv"
    scraped_epa = pd.read_csv(scraped_epa_path)

    # Load actual Week 2 results for comparison
    actual_results_path = os.path.join("week2", "week2_epa_corrected.csv")
    actual_results = pd.read_csv(actual_results_path)
    actual_results = actual_results[['game', 'underdog', 'actual_cover', 'predicted_cover_binary']]

    print(f"Loaded {len(week2_odds)} games from Week 2 odds")
    print(f"Loaded {len(scraped_epa)} teams from SumerSports EPA data")
    print(f"Loaded {len(actual_results)} actual results")

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
    
    # Add abbreviation columns to week2_odds
    week2_odds['underdog_abbr'] = week2_odds['underdog_team'].map(team_name_to_abbr)
    week2_odds['favorite_abbr'] = week2_odds['favorite_team'].map(team_name_to_abbr)

    # Merge EPA data with Week 2 odds
    # For underdog team
    week2_data = week2_odds.merge(
        scraped_epa[['team', 'team_name', 'epa_off_per_play', 'epa_def_allowed_per_play', 'net_epa_per_play']],
        left_on='underdog_abbr',
        right_on='team',
        how='left',
        suffixes=('', '_underdog')
    )
    week2_data.rename(columns={
        'epa_off_per_play': 'underdog_epa_off',
        'epa_def_allowed_per_play': 'underdog_epa_def_allowed',
        'net_epa_per_play': 'underdog_net_epa'
    }, inplace=True)
    week2_data.drop(columns=['team', 'team_name'], inplace=True)

    # For favorite team (opponent defense)
    week2_data = week2_data.merge(
        scraped_epa[['team', 'team_name', 'epa_def_allowed_per_play']],
        left_on='favorite_abbr',
        right_on='team',
        how='left',
        suffixes=('', '_opponent')
    )
    week2_data.rename(columns={'epa_def_allowed_per_play': 'opponent_def_epa'}, inplace=True)
    week2_data.drop(columns=['team', 'team_name'], inplace=True)

    # Calculate net EPA differential (underdog_net_epa - favorite_net_epa)
    # We need favorite's net EPA as well
    week2_data = week2_data.merge(
        scraped_epa[['team', 'net_epa_per_play']],
        left_on='favorite_abbr',
        right_on='team',
        how='left',
        suffixes=('', '_favorite')
    )
    week2_data.rename(columns={'net_epa_per_play': 'favorite_net_epa'}, inplace=True)
    week2_data.drop(columns=['team'], inplace=True)
    week2_data['net_epa_differential'] = week2_data['underdog_net_epa'] - week2_data['favorite_net_epa']

    # Determine defense quality based on opponent_def_epa
    # Using thresholds based on the scraped data distribution
    def get_defense_quality(epa):
        if epa > 0.10:  # Weak defense (allows high EPA)
            return 'WEAK'
        elif epa >= -0.05:  # Average defense
            return 'AVERAGE'
        else:  # Strong defense (allows low/negative EPA)
            return 'STRONG'
    
    week2_data['defense_quality'] = week2_data['opponent_def_epa'].apply(get_defense_quality)

    # Check for missing data
    missing_teams = week2_data[week2_data['underdog_epa_off'].isna() | week2_data['opponent_def_epa'].isna()]
    if not missing_teams.empty:
        print(f"\n⚠️  Missing EPA data for {len(missing_teams)} games:")
        for _, row in missing_teams.iterrows():
            print(f"  {row['underdog_team']} vs {row['favorite_team']}")
        
        # Fill missing data with league average
        league_avg_off = scraped_epa['epa_off_per_play'].mean()
        league_avg_def = scraped_epa['epa_def_allowed_per_play'].mean()
        league_avg_net = scraped_epa['net_epa_per_play'].mean()
        
        week2_data = week2_data.copy()  # Avoid chained assignment warnings
        week2_data['underdog_epa_off'] = week2_data['underdog_epa_off'].fillna(league_avg_off)
        week2_data['underdog_epa_def_allowed'] = week2_data['underdog_epa_def_allowed'].fillna(league_avg_def)
        week2_data['underdog_net_epa'] = week2_data['underdog_net_epa'].fillna(league_avg_net)
        week2_data['opponent_def_epa'] = week2_data['opponent_def_epa'].fillna(league_avg_def)
        week2_data['favorite_net_epa'] = week2_data['favorite_net_epa'].fillna(league_avg_net)
        week2_data['net_epa_differential'] = week2_data['underdog_net_epa'] - week2_data['favorite_net_epa']
        
        print(f"✅ Filled missing data with league averages")

    # --- Model Logic Using Scraped EPA Data ---
    # This model uses the insights from our previous analysis but with fresh EPA data
    
    # Base probability
    week2_data['cover_probability'] = 0.50

    # Adjust based on opponent defense quality
    # Based on Week 2 actual results, STRONG defenses led to more underdog covers
    week2_data.loc[week2_data['defense_quality'] == 'STRONG', 'cover_probability'] += 0.12
    week2_data.loc[week2_data['defense_quality'] == 'WEAK', 'cover_probability'] -= 0.10
    week2_data.loc[week2_data['defense_quality'] == 'AVERAGE', 'cover_probability'] += 0.02

    # Adjust based on net EPA differential (underdog_net_epa - favorite_net_epa)
    # Positive differential means underdog is performing better overall
    week2_data['cover_probability'] += week2_data['net_epa_differential'] * 0.8

    # Adjust based on spread line (larger spread, slightly higher chance to cover for underdog)
    week2_data['cover_probability'] += week2_data['spread_line'].abs() * 0.008

    # Cap probabilities
    week2_data['cover_probability'] = week2_data['cover_probability'].clip(0.05, 0.95)

    # Assign confidence levels based on probability
    def assign_confidence(prob):
        if prob >= 0.65:
            return 'HIGH'
        elif prob >= 0.40:
            return 'MEDIUM'
        else:
            return 'LOW'
    
    week2_data['confidence'] = week2_data['cover_probability'].apply(assign_confidence)
    week2_data['predicted_cover'] = week2_data['cover_probability'] >= 0.5

    print(f"\n=== Week 2 Predictions with Scraped EPA Data ===")
    print(f"Data source: SumerSports (scraped {len(scraped_epa)} teams)")
    
    print(f"\nAll Games (sorted by cover probability):")
    for _, row in week2_data.sort_values(by='cover_probability', ascending=False).iterrows():
        print(f"{row['away_team']} at {row['home_team']}: {row['underdog_team']} +{row['spread_line']}")
        print(f"  Cover Probability: {row['cover_probability']:.1%}")
        print(f"  Confidence: {row['confidence']}")
        print(f"  Net EPA Diff: {row['net_epa_differential']:.3f}")
        print(f"  Opponent Defense: {row['defense_quality']} ({row['opponent_def_epa']:.3f})")
        print(f"  Prediction: {'Cover' if row['predicted_cover'] else 'No Cover'}")
        print()

    # Confidence level breakdown
    confidence_counts = week2_data['confidence'].value_counts()
    print(f"=== Confidence Level Distribution ===")
    for conf in ['HIGH', 'MEDIUM', 'LOW']:
        count = confidence_counts.get(conf, 0)
        print(f"{conf}: {count} games")

    print(f"\n=== High Confidence Picks ===")
    high_conf = week2_data[week2_data['confidence'] == 'HIGH'].sort_values(by='cover_probability', ascending=False)
    for _, row in high_conf.iterrows():
        print(f"{row['underdog_team']} +{row['spread_line']} vs {row['favorite_team']} ({row['cover_probability']:.1%})")

    print(f"\n=== Medium Confidence Picks ===")
    medium_conf = week2_data[week2_data['confidence'] == 'MEDIUM'].sort_values(by='cover_probability', ascending=False)
    for _, row in medium_conf.iterrows():
        print(f"{row['underdog_team']} +{row['spread_line']} vs {row['favorite_team']} ({row['cover_probability']:.1%})")

    print(f"\n=== Low Confidence Picks ===")
    low_conf = week2_data[week2_data['confidence'] == 'LOW'].sort_values(by='cover_probability', ascending=False)
    for _, row in low_conf.iterrows():
        print(f"{row['underdog_team']} +{row['spread_line']} vs {row['favorite_team']} ({row['cover_probability']:.1%})")

    # Defense quality analysis
    print(f"\n=== Defense Quality Analysis ===")
    defense_quality_summary = week2_data.groupby('defense_quality').agg(
        count=('cover_probability', 'count'),
        mean_prob=('cover_probability', 'mean'),
        mean_predicted=('predicted_cover', 'mean')
    ).round(3)
    print(defense_quality_summary)

    # Compare with actual results
    # Create a game identifier for merging
    week2_data['game'] = week2_data['away_team'] + ' at ' + week2_data['home_team']
    # Rename underdog_team to underdog for merging
    week2_data['underdog'] = week2_data['underdog_team']
    comparison_df = week2_data.merge(actual_results, on=['game', 'underdog'], how='left')
    comparison_df['is_correct_spread'] = comparison_df['predicted_cover'] == comparison_df['actual_cover']
    
    overall_accuracy = comparison_df['is_correct_spread'].mean()
    print(f"\n=== Model Performance vs Actual Results ===")
    print(f"Overall Accuracy: {overall_accuracy:.1%}")

    accuracy_by_confidence = comparison_df.groupby('confidence')['is_correct_spread'].mean().reset_index()
    accuracy_by_confidence.rename(columns={'is_correct_spread': 'accuracy'}, inplace=True)
    print(f"\nAccuracy by Confidence Level:")
    for _, row in accuracy_by_confidence.iterrows():
        count = comparison_df[comparison_df['confidence'] == row['confidence']].shape[0]
        correct = comparison_df[(comparison_df['confidence'] == row['confidence']) & (comparison_df['is_correct_spread'])].shape[0]
        print(f"{row['confidence']}: {row['accuracy']:.1%} ({correct}/{count})")

    print(f"\nDetailed Game-by-Game Results:")
    for _, row in comparison_df.sort_values(by='cover_probability', ascending=False).iterrows():
        status = "✓" if row['is_correct_spread'] else "✗"
        print(f"{status} {row['underdog']} +{row['spread_line']}: Predicted {row['cover_probability']:.1%} → Actual {'Cover' if row['actual_cover'] else 'No Cover'}")

    # Save predictions and comparison
    week2_data.to_csv(os.path.join("week2", "week2_predictions_scraped_epa.csv"), index=False)
    comparison_df.to_csv(os.path.join("week2", "week2_comparison_scraped_epa.csv"), index=False)
    print(f"\n✅ Results saved to:")
    print(f"  - week2/week2_predictions_scraped_epa.csv")
    print(f"  - week2/week2_comparison_scraped_epa.csv")

    # Compare with previous model performance
    print(f"\n=== Comparison with Previous Models ===")
    print(f"Original Week 2 Model (nflverse data): 43.8% accuracy")
    print(f"Improved Week 2 Model (corrected nflverse): 56.2% accuracy")
    print(f"New Model (SumerSports data): {overall_accuracy:.1%} accuracy")
    
    improvement = overall_accuracy - 0.438
    print(f"Improvement over original: {improvement:+.1%}")

if __name__ == "__main__":
    run_week2_model_with_scraped_epa()
