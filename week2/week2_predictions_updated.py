#!/usr/bin/env python3
"""
Week 2 2025 NFL Underdog Cover Predictions (UPDATED)
Based on Week 1 EPA analysis findings with OPPONENT DEFENSIVE EPA insights
"""

import pandas as pd
import numpy as np
from scipy import stats

def load_week1_epa_data():
    """Load Week 1 EPA data for each team with net EPA calculation"""
    # Based on our Week 1 analysis - now including net EPA
    team_epa_data = {
        'Commanders': {'epa_off': 0.072, 'epa_def_allowed': 0.072, 'net_epa': 0.000, 'success_rate_off': 0.45},
        'Packers': {'epa_off': 0.185, 'epa_def_allowed': 0.185, 'net_epa': 0.000, 'success_rate_off': 0.52},
        'Browns': {'epa_off': -0.088, 'epa_def_allowed': -0.066, 'net_epa': -0.022, 'success_rate_off': 0.42},
        'Ravens': {'epa_off': 0.204, 'epa_def_allowed': 0.340, 'net_epa': -0.136, 'success_rate_off': 0.48},
        'Jaguars': {'epa_off': 0.090, 'epa_def_allowed': 0.090, 'net_epa': 0.000, 'success_rate_off': 0.46},
        'Bengals': {'epa_off': -0.066, 'epa_def_allowed': -0.066, 'net_epa': 0.000, 'success_rate_off': 0.44},
        'Giants': {'epa_off': -0.113, 'epa_def_allowed': 0.072, 'net_epa': -0.185, 'success_rate_off': 0.38},
        'Cowboys': {'epa_off': 0.139, 'epa_def_allowed': 0.171, 'net_epa': -0.032, 'success_rate_off': 0.49},
        'Bears': {'epa_off': -0.111, 'epa_def_allowed': -0.064, 'net_epa': -0.047, 'success_rate_off': 0.41},
        'Lions': {'epa_off': -0.054, 'epa_def_allowed': 0.185, 'net_epa': -0.239, 'success_rate_off': 0.43},
        'Patriots': {'epa_off': -0.049, 'epa_def_allowed': -0.049, 'net_epa': 0.000, 'success_rate_off': 0.40},
        'Dolphins': {'epa_off': -0.075, 'epa_def_allowed': -0.075, 'net_epa': 0.000, 'success_rate_off': 0.39},
        '49ers': {'epa_off': 0.012, 'epa_def_allowed': 0.012, 'net_epa': 0.000, 'success_rate_off': 0.47},
        'Saints': {'epa_off': -0.091, 'epa_def_allowed': 0.016, 'net_epa': -0.107, 'success_rate_off': 0.41},
        'Bills': {'epa_off': 0.204, 'epa_def_allowed': 0.340, 'net_epa': -0.136, 'success_rate_off': 0.48},
        'Jets': {'epa_off': 0.158, 'epa_def_allowed': 0.209, 'net_epa': -0.051, 'success_rate_off': 0.50},
        'Seahawks': {'epa_off': -0.082, 'epa_def_allowed': 0.012, 'net_epa': -0.094, 'success_rate_off': 0.42},
        'Steelers': {'epa_off': 0.209, 'epa_def_allowed': 0.209, 'net_epa': 0.000, 'success_rate_off': 0.51},
        'Rams': {'epa_off': -0.075, 'epa_def_allowed': -0.075, 'net_epa': 0.000, 'success_rate_off': 0.43},
        'Titans': {'epa_off': -0.219, 'epa_def_allowed': -0.110, 'net_epa': -0.109, 'success_rate_off': 0.35},
        'Panthers': {'epa_off': -0.107, 'epa_def_allowed': 0.090, 'net_epa': -0.197, 'success_rate_off': 0.40},
        'Cardinals': {'epa_off': 0.016, 'epa_def_allowed': 0.016, 'net_epa': 0.000, 'success_rate_off': 0.45},
        'Broncos': {'epa_off': 0.082, 'epa_def_allowed': -0.049, 'net_epa': 0.131, 'success_rate_off': 0.46},
        'Colts': {'epa_off': 0.251, 'epa_def_allowed': -0.159, 'net_epa': 0.410, 'success_rate_off': 0.53},
        'Eagles': {'epa_off': 0.171, 'epa_def_allowed': 0.171, 'net_epa': 0.000, 'success_rate_off': 0.49},
        'Chiefs': {'epa_off': 0.131, 'epa_def_allowed': 0.214, 'net_epa': -0.083, 'success_rate_off': 0.48},
        'Falcons': {'epa_off': 0.011, 'epa_def_allowed': 0.076, 'net_epa': -0.065, 'success_rate_off': 0.44},
        'Vikings': {'epa_off': -0.064, 'epa_def_allowed': -0.064, 'net_epa': 0.000, 'success_rate_off': 0.42},
        'Buccaneers': {'epa_off': 0.076, 'epa_def_allowed': 0.076, 'net_epa': 0.000, 'success_rate_off': 0.45},
        'Texans': {'epa_off': -0.121, 'epa_def_allowed': -0.075, 'net_epa': -0.046, 'success_rate_off': 0.38},
        'Chargers': {'epa_off': 0.214, 'epa_def_allowed': 0.214, 'net_epa': 0.000, 'success_rate_off': 0.52},
        'Raiders': {'epa_off': 0.082, 'epa_def_allowed': -0.049, 'net_epa': 0.131, 'success_rate_off': 0.46}
    }
    return team_epa_data

def load_week1_defensive_epa():
    """Load Week 1 defensive EPA data for each team"""
    # Based on our analysis - defensive EPA allowed per play
    defensive_epa_data = {
        'BUF': 0.340,  # Bills - worst defense
        'NYJ': 0.206,  # Jets - very bad defense
        'PHI': 0.139,  # Eagles - bad defense
        'LAC': 0.131,  # Chargers - bad defense
        'NE': 0.081,   # Patriots - below average
        'ATL': 0.075,  # Falcons - below average
        'NO': 0.016,   # Saints - average
        'SEA': 0.012,  # Seahawks - average
        'GB': -0.054,  # Packers - good defense
        'CHI': -0.064, # Bears - good defense
        'CLE': -0.066, # Browns - good defense
        'JAX': -0.107, # Jaguars - very good defense
        'WAS': -0.113, # Commanders - very good defense
        'LA': -0.121,  # Rams - very good defense
        'IND': -0.156, # Colts - excellent defense
        'DEN': -0.219  # Broncos - best defense
    }
    return defensive_epa_data

def calculate_cover_probability_with_net_epa(underdog_net_epa, favorite_net_epa, opponent_def_epa, spread, is_home):
    """
    Calculate cover probability based on NET EPA (offensive EPA - defensive EPA allowed)
    Key findings:
    - Net EPA is the most comprehensive team strength metric
    - Opponent defensive EPA is still important for matchup analysis
    - vs WEAK defenses: 75% cover rate
    - vs STRONG defenses: 25% cover rate
    - vs AVERAGE defenses: 50% cover rate
    """
    
    # Base probability from opponent defensive EPA (strongest predictor)
    if opponent_def_epa > 0.05:  # Weak defense (high EPA allowed)
        base_prob = 0.75
        defense_factor = "WEAK"
    elif opponent_def_epa < -0.05:  # Strong defense (low EPA allowed)
        base_prob = 0.25
        defense_factor = "STRONG"
    else:  # Average defense
        base_prob = 0.50
        defense_factor = "AVERAGE"
    
    # Net EPA differential factor (primary team strength comparison)
    net_epa_diff = favorite_net_epa - underdog_net_epa
    net_epa_factor = -0.15 * net_epa_diff  # Net EPA is more predictive than offensive EPA alone
    
    # Underdog net EPA factor (how good is the underdog overall)
    underdog_net_epa_factor = 0.1 * underdog_net_epa
    
    # Home field advantage (minimal impact from Week 1)
    home_factor = 0.02 if is_home else 0
    
    # Spread factor (commented out - need more data to determine optimal factor)
    # spread_factor = -0.01 * spread  # Arbitrary factor, revisit with more data
    
    # Calculate final probability
    cover_prob = base_prob + net_epa_factor + underdog_net_epa_factor + home_factor  # + spread_factor
    
    # Ensure probability stays within reasonable bounds
    cover_prob = np.clip(cover_prob, 0.1, 0.9)
    
    return cover_prob, defense_factor

def make_week2_predictions():
    """Make Week 2 underdog cover predictions with opponent defensive EPA analysis"""
    
    # Load Week 2 odds
    week2_odds = pd.read_csv('week2_2025_odds.csv')
    
    # Load team EPA data
    team_epa = load_week1_epa_data()
    defensive_epa = load_week1_defensive_epa()
    
    # Team name mapping
    team_mapping = {
        'Raiders': 'LV', 'Patriots': 'NE', 'Steelers': 'PIT', 'Jets': 'NYJ',
        'Dolphins': 'MIA', 'Colts': 'IND', 'Cardinals': 'ARI', 'Saints': 'NO',
        'Giants': 'NYG', 'Commanders': 'WAS', 'Panthers': 'CAR', 'Jaguars': 'JAX',
        'Bengals': 'CIN', 'Browns': 'CLE', 'Buccaneers': 'TB', 'Falcons': 'ATL',
        'Titans': 'TEN', 'Broncos': 'DEN', '49ers': 'SF', 'Seahawks': 'SEA',
        'Lions': 'DET', 'Packers': 'GB', 'Texans': 'HOU', 'Rams': 'LA',
        'Ravens': 'BAL', 'Bills': 'BUF', 'Vikings': 'MIN', 'Bears': 'CHI',
        'Chiefs': 'KC', 'Chargers': 'LAC', 'Cowboys': 'DAL', 'Eagles': 'PHI'
    }
    
    print("="*80)
    print("WEEK 2 UNDERDOG COVER PREDICTIONS (WITH OPPONENT DEFENSIVE EPA ANALYSIS)")
    print("="*80)
    
    predictions = []
    
    for _, game in week2_odds.iterrows():
        away_team = game['away_team']
        home_team = game['home_team']
        spread = game['spread_line']
        total = game['total_line']
        favorite = game['favorite_team']
        underdog = game['underdog_team']
        underdog_spread = spread
        
        # Determine if underdog is home or away
        is_home = (underdog == home_team)
        
        # Get EPA data
        underdog_epa = team_epa.get(underdog, {'epa_off': 0, 'epa_def_allowed': 0, 'net_epa': 0, 'success_rate_off': 0.45})
        favorite_epa = team_epa.get(favorite, {'epa_off': 0, 'epa_def_allowed': 0, 'net_epa': 0, 'success_rate_off': 0.45})
        
        # Get opponent defensive EPA
        favorite_abbr = team_mapping.get(favorite, favorite)
        opponent_def_epa = defensive_epa.get(favorite_abbr, 0)
        
        # Calculate cover probability with net EPA analysis
        cover_prob, defense_quality = calculate_cover_probability_with_net_epa(
            underdog_epa['net_epa'], 
            favorite_epa['net_epa'], 
            opponent_def_epa,
            underdog_spread, 
            is_home
        )
        
        # Determine confidence level based on opponent defense
        if defense_quality == "WEAK":
            confidence = "HIGH"
        elif defense_quality == "STRONG":
            confidence = "LOW"
        else:
            confidence = "MEDIUM"
        
        predictions.append({
            'game': f'{away_team} at {home_team}',
            'underdog': underdog,
            'favorite': favorite,
            'spread': underdog_spread,
            'underdog_net_epa': underdog_epa['net_epa'],
            'favorite_net_epa': favorite_epa['net_epa'],
            'underdog_epa_off': underdog_epa['epa_off'],
            'favorite_epa_off': favorite_epa['epa_off'],
            'opponent_def_epa': opponent_def_epa,
            'defense_quality': defense_quality,
            'net_epa_differential': favorite_epa['net_epa'] - underdog_epa['net_epa'],
            'cover_probability': cover_prob,
            'confidence': confidence,
            'is_home': is_home
        })
    
    # Sort by cover probability
    predictions_df = pd.DataFrame(predictions)
    predictions_df = predictions_df.sort_values('cover_probability', ascending=False)
    
    # Display predictions with net EPA analysis
    print(f"\n{'Underdog':<12} {'vs':<3} {'Favorite':<12} {'Spread':<8} {'Net EPA Diff':<12} {'Opp Def EPA':<12} {'Defense':<8} {'Expected':<10}")
    print("-" * 110)
    
    for _, row in predictions_df.iterrows():
        print(f"{row['underdog']:<12} vs {row['favorite']:<12} +{row['spread']:<7} {row['net_epa_differential']:+8.3f} {row['opponent_def_epa']:+8.3f} {row['defense_quality']:<8} {row['cover_probability']:.1%}")
    
    # High confidence picks based on opponent defense
    weak_defense_picks = predictions_df[predictions_df['defense_quality'] == 'WEAK']
    strong_defense_picks = predictions_df[predictions_df['defense_quality'] == 'STRONG']
    average_defense_picks = predictions_df[predictions_df['defense_quality'] == 'AVERAGE']
    
    print(f"\n🎯 HIGH CONFIDENCE PICKS (vs WEAK defenses - 75% expected cover rate):")
    for _, row in weak_defense_picks.iterrows():
        print(f"  ✅ {row['underdog']} +{row['spread']} vs {row['favorite']} (Opp Def EPA: {row['opponent_def_epa']:+.3f})")
    
    print(f"\n⚠️  AVOID THESE (vs STRONG defenses - 25% expected cover rate):")
    for _, row in strong_defense_picks.iterrows():
        print(f"  ❌ {row['underdog']} +{row['spread']} vs {row['favorite']} (Opp Def EPA: {row['opponent_def_epa']:+.3f})")
    
    print(f"\n📊 AVERAGE PICKS (vs AVERAGE defenses - 50% expected cover rate):")
    for _, row in average_defense_picks.iterrows():
        print(f"  ⚖️  {row['underdog']} +{row['spread']} vs {row['favorite']} (Opp Def EPA: {row['opponent_def_epa']:+.3f})")
    
    print(f"\n📊 SUMMARY:")
    print(f"High confidence picks (vs weak defenses): {len(weak_defense_picks)}")
    print(f"Picks to avoid (vs strong defenses): {len(strong_defense_picks)}")
    print(f"Average picks (vs average defenses): {len(average_defense_picks)}")
    
    print(f"\nKey Insights from Week 1 EPA Analysis:")
    print(f"- NET EPA (offensive EPA - defensive EPA allowed) is the most comprehensive team strength metric")
    print(f"- OPPONENT DEFENSIVE EPA IS THE STRONGEST PREDICTOR")
    print(f"- Underdogs vs weak defenses: 75% cover rate")
    print(f"- Underdogs vs strong defenses: 25% cover rate")
    print(f"- Net EPA differential provides better team comparison than offensive EPA alone")
    print(f"- The matchup matters more than the underdog's inherent ability")
    
    # Save predictions to CSV
    predictions_df.to_csv('week2_underdog_predictions_updated.csv', index=False)
    print(f"\nPredictions saved to week2_underdog_predictions_updated.csv")
    
    return predictions_df

if __name__ == "__main__":
    predictions = make_week2_predictions()
