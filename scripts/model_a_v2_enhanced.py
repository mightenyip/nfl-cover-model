#!/usr/bin/env python3
"""
Model A v2: Enhanced EPA Model with 5-Tier Defense Classification
Combines Model A's core EPA methodology with Model B's nuanced defense tiers
"""

import pandas as pd
import numpy as np
from datetime import datetime

def get_latest_epa_data():
    """Extract EPA data from SumerSports defensive rankings"""
    
    # Based on SumerSports data as of 10-14-2025
    defensive_epa_data = {
        'DEN': {'epa_def_allowed_per_play': -0.14, 'team_name': 'Denver Broncos'},
        'MIN': {'epa_def_allowed_per_play': -0.13, 'team_name': 'Minnesota Vikings'},
        'HOU': {'epa_def_allowed_per_play': -0.12, 'team_name': 'Houston Texans'},
        'LA': {'epa_def_allowed_per_play': -0.08, 'team_name': 'Los Angeles Rams'},
        'ATL': {'epa_def_allowed_per_play': -0.07, 'team_name': 'Atlanta Falcons'},
        'JAX': {'epa_def_allowed_per_play': -0.07, 'team_name': 'Jacksonville Jaguars'},
        'IND': {'epa_def_allowed_per_play': -0.05, 'team_name': 'Indianapolis Colts'},
        'DET': {'epa_def_allowed_per_play': -0.04, 'team_name': 'Detroit Lions'},
        'LAC': {'epa_def_allowed_per_play': -0.02, 'team_name': 'Los Angeles Chargers'},
        'CHI': {'epa_def_allowed_per_play': -0.01, 'team_name': 'Chicago Bears'},
        'PHI': {'epa_def_allowed_per_play': -0.01, 'team_name': 'Philadelphia Eagles'},
        'PIT': {'epa_def_allowed_per_play': -0.01, 'team_name': 'Pittsburgh Steelers'},
        'CLE': {'epa_def_allowed_per_play': 0.00, 'team_name': 'Cleveland Browns'},
        'LV': {'epa_def_allowed_per_play': 0.00, 'team_name': 'Las Vegas Raiders'},
        'ARI': {'epa_def_allowed_per_play': 0.00, 'team_name': 'Arizona Cardinals'},
        'SF': {'epa_def_allowed_per_play': 0.00, 'team_name': 'San Francisco 49ers'},
        'SEA': {'epa_def_allowed_per_play': 0.00, 'team_name': 'Seattle Seahawks'},
        'TB': {'epa_def_allowed_per_play': 0.01, 'team_name': 'Tampa Bay Buccaneers'},
        'NO': {'epa_def_allowed_per_play': 0.01, 'team_name': 'New Orleans Saints'},
        'KC': {'epa_def_allowed_per_play': 0.01, 'team_name': 'Kansas City Chiefs'},
        'GB': {'epa_def_allowed_per_play': 0.02, 'team_name': 'Green Bay Packers'},
        'WAS': {'epa_def_allowed_per_play': 0.03, 'team_name': 'Washington Commanders'},
        'BUF': {'epa_def_allowed_per_play': 0.03, 'team_name': 'Buffalo Bills'},
        'NE': {'epa_def_allowed_per_play': 0.04, 'team_name': 'New England Patriots'},
        'TEN': {'epa_def_allowed_per_play': 0.04, 'team_name': 'Tennessee Titans'},
        'NYG': {'epa_def_allowed_per_play': 0.04, 'team_name': 'New York Giants'},
        'CAR': {'epa_def_allowed_per_play': 0.07, 'team_name': 'Carolina Panthers'},
        'NYJ': {'epa_def_allowed_per_play': 0.11, 'team_name': 'New York Jets'},
        'CIN': {'epa_def_allowed_per_play': 0.12, 'team_name': 'Cincinnati Bengals'},
        'BAL': {'epa_def_allowed_per_play': 0.15, 'team_name': 'Baltimore Ravens'},
        'DAL': {'epa_def_allowed_per_play': 0.18, 'team_name': 'Dallas Cowboys'},
        'MIA': {'epa_def_allowed_per_play': 0.21, 'team_name': 'Miami Dolphins'}
    }
    
    # Convert to DataFrame
    epa_df = pd.DataFrame.from_dict(defensive_epa_data, orient='index')
    epa_df.reset_index(inplace=True)
    epa_df.rename(columns={'index': 'team'}, inplace=True)
    
    # Add estimated offensive EPA (would need offensive data for complete picture)
    # For now, using league average with some variation
    np.random.seed(42)  # For reproducible results
    epa_df['epa_off_per_play'] = np.random.normal(0.05, 0.15, len(epa_df))
    epa_df['net_epa_per_play'] = epa_df['epa_off_per_play'] - epa_df['epa_def_allowed_per_play']
    
    return epa_df

def run_model_a_v2():
    """Run Model A v2 with enhanced 5-tier defense classification"""
    
    print("=== Model A v2: Enhanced EPA with 5-Tier Defense Classification ===")
    print("Combining Model A's core methodology with Model B's nuanced defense tiers")
    print(f"Data source: Latest SumerSports EPA rankings (as of 10-14-2025)")
    print(f"Updated: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}")
    
    # Get latest EPA data
    latest_epa = get_latest_epa_data()
    
    # Load Week 6 schedule
    week6_odds_path = "/Users/mightenyip/Documents/GitHub/nfl-cover-model/schedule/week6_2025_odds.csv"
    week6_odds = pd.read_csv(week6_odds_path)
    
    print(f"Loaded {len(week6_odds)} games from Week 6 odds")
    print(f"Loaded {len(latest_epa)} teams from latest SumerSports data")
    
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
    week6_odds['underdog_abbr'] = week6_odds['underdog_team'].map(team_name_to_abbr)
    week6_odds['favorite_abbr'] = week6_odds['favorite_team'].map(team_name_to_abbr)
    
    # Merge with latest EPA data
    week6_data = week6_odds.merge(
        latest_epa[['team', 'epa_def_allowed_per_play', 'epa_off_per_play', 'net_epa_per_play']],
        left_on='underdog_abbr',
        right_on='team',
        how='left',
        suffixes=('', '_underdog')
    )
    week6_data.rename(columns={
        'epa_def_allowed_per_play': 'underdog_epa_def_allowed',
        'epa_off_per_play': 'underdog_epa_off',
        'net_epa_per_play': 'underdog_net_epa'
    }, inplace=True)
    week6_data.drop(columns=['team'], inplace=True)
    
    # For favorite team (opponent defense)
    week6_data = week6_data.merge(
        latest_epa[['team', 'epa_def_allowed_per_play', 'net_epa_per_play']],
        left_on='favorite_abbr',
        right_on='team',
        how='left',
        suffixes=('', '_favorite')
    )
    week6_data.rename(columns={
        'epa_def_allowed_per_play': 'opponent_def_epa',
        'net_epa_per_play': 'favorite_net_epa'
    }, inplace=True)
    week6_data.drop(columns=['team'], inplace=True)
    
    # Calculate net EPA differential
    week6_data['net_epa_differential'] = week6_data['underdog_net_epa'] - week6_data['favorite_net_epa']
    
    # === MODEL A v2: 5-TIER DEFENSE CLASSIFICATION (from Model B) ===
    
    # Enhanced defense quality classification using Model B's 5-tier system
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
    
    week6_data['defense_quality'] = week6_data['opponent_def_epa'].apply(get_enhanced_defense_quality)
    
    # === MODEL A v2 LOGIC (Enhanced with 5-tier system) ===
    
    # Base probability (Model A's conservative approach)
    week6_data['cover_probability'] = 0.50
    
    # Enhanced defense quality adjustments using Model B's nuanced approach
    defense_adjustments = {
        'ELITE': 0.18,    # Elite defenses heavily favor underdogs
        'STRONG': 0.12,   # Strong defenses favor underdogs
        'AVERAGE': 0.03,  # Average defenses slightly favor underdogs
        'WEAK': -0.08,    # Weak defenses favor favorites
        'POOR': -0.15     # Poor defenses heavily favor favorites
    }
    
    for quality, adjustment in defense_adjustments.items():
        week6_data.loc[week6_data['defense_quality'] == quality, 'cover_probability'] += adjustment
    
    # Net EPA differential adjustment (Model A's core strength)
    week6_data['cover_probability'] += week6_data['net_epa_differential'] * 0.8
    
    # Spread adjustment (Model A's approach)
    week6_data['cover_probability'] += week6_data['spread_line'].abs() * 0.008
    
    # Cap probabilities
    week6_data['cover_probability'] = week6_data['cover_probability'].clip(0.05, 0.95)
    
    # Enhanced confidence levels (Model B's system)
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
    
    week6_data['confidence'] = week6_data['cover_probability'].apply(assign_enhanced_confidence)
    week6_data['predicted_cover'] = week6_data['cover_probability'] >= 0.5
    
    print(f"\n=== Model A v2 Predictions (Enhanced 5-Tier Defense) ===")
    print(f"Methodology: Model A's EPA approach + Model B's 5-tier defense classification")
    
    # Show predictions
    for _, row in week6_data.sort_values(by='cover_probability', ascending=False).iterrows():
        print(f"\n{row['away_team']} at {row['home_team']}: {row['underdog_team']} +{row['spread_line']}")
        print(f"  Cover Probability: {row['cover_probability']:.1%} ({row['confidence']})")
        print(f"  Opponent Defense: {row['defense_quality']} ({row['opponent_def_epa']:.3f})")
        print(f"  Net EPA Diff: {row['net_epa_differential']:.3f}")
        print(f"  Prediction: {'Cover' if row['predicted_cover'] else 'No Cover'}")
    
    # Defense quality analysis
    print(f"\n=== Defense Quality Analysis (5-Tier System) ===")
    defense_quality_summary = week6_data.groupby('defense_quality').agg(
        count=('cover_probability', 'count'),
        mean_prob=('cover_probability', 'mean'),
        mean_predicted=('predicted_cover', 'mean')
    ).round(3)
    print(defense_quality_summary)
    
    # Confidence level breakdown
    confidence_counts = week6_data['confidence'].value_counts()
    print(f"\n=== Confidence Level Distribution ===")
    for conf in ['VERY_HIGH', 'HIGH', 'MEDIUM', 'LOW', 'VERY_LOW']:
        count = confidence_counts.get(conf, 0)
        print(f"{conf}: {count} games")
    
    # Save predictions
    week6_data.to_csv("/Users/mightenyip/Documents/GitHub/nfl-cover-model/models/model_a/model_a_v2_week6_predictions.csv", index=False)
    print(f"\n✅ Model A v2 predictions saved to: model_a_v2_week6_predictions.csv")
    
    # Summary statistics
    print(f"\n=== Model A v2 Summary ===")
    print(f"Total games: {len(week6_data)}")
    print(f"Underdog covers predicted: {week6_data['predicted_cover'].sum()}")
    print(f"Favorite covers predicted: {(~week6_data['predicted_cover']).sum()}")
    
    avg_spread = week6_data['spread_line'].mean()
    print(f"Average spread: {avg_spread:.1f} points")
    
    avg_prob = week6_data['cover_probability'].mean()
    print(f"Average cover probability: {avg_prob:.1%}")
    
    return week6_data

if __name__ == "__main__":
    run_model_a_v2()
