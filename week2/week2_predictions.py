#!/usr/bin/env python3
"""
Week 2 2025 NFL Underdog Cover Predictions
Based on Week 1 EPA analysis findings
"""

import pandas as pd
import numpy as np
from scipy import stats

def load_week1_epa_data():
    """Load Week 1 EPA data for each team"""
    # Based on our Week 1 analysis
    team_epa_data = {
        'Commanders': {'epa_off': 0.072, 'epa_def_allowed': 0.072, 'success_rate_off': 0.45},
        'Packers': {'epa_off': 0.185, 'epa_def_allowed': 0.185, 'success_rate_off': 0.52},
        'Browns': {'epa_off': -0.088, 'epa_def_allowed': -0.066, 'success_rate_off': 0.42},
        'Ravens': {'epa_off': 0.204, 'epa_def_allowed': 0.340, 'success_rate_off': 0.48},
        'Jaguars': {'epa_off': 0.090, 'epa_def_allowed': 0.090, 'success_rate_off': 0.46},
        'Bengals': {'epa_off': -0.066, 'epa_def_allowed': -0.066, 'success_rate_off': 0.44},
        'Giants': {'epa_off': -0.113, 'epa_def_allowed': 0.072, 'success_rate_off': 0.38},
        'Cowboys': {'epa_off': 0.139, 'epa_def_allowed': 0.171, 'success_rate_off': 0.49},
        'Bears': {'epa_off': -0.111, 'epa_def_allowed': -0.064, 'success_rate_off': 0.41},
        'Lions': {'epa_off': -0.054, 'epa_def_allowed': 0.185, 'success_rate_off': 0.43},
        'Patriots': {'epa_off': -0.049, 'epa_def_allowed': -0.049, 'success_rate_off': 0.40},
        'Dolphins': {'epa_off': -0.075, 'epa_def_allowed': -0.075, 'success_rate_off': 0.39},
        '49ers': {'epa_off': 0.012, 'epa_def_allowed': 0.012, 'success_rate_off': 0.47},
        'Saints': {'epa_off': -0.091, 'epa_def_allowed': 0.016, 'success_rate_off': 0.41},
        'Bills': {'epa_off': 0.204, 'epa_def_allowed': 0.340, 'success_rate_off': 0.48},
        'Jets': {'epa_off': 0.158, 'epa_def_allowed': 0.209, 'success_rate_off': 0.50},
        'Seahawks': {'epa_off': -0.082, 'epa_def_allowed': 0.012, 'success_rate_off': 0.42},
        'Steelers': {'epa_off': 0.209, 'epa_def_allowed': 0.209, 'success_rate_off': 0.51},
        'Rams': {'epa_off': -0.075, 'epa_def_allowed': -0.075, 'success_rate_off': 0.43},
        'Titans': {'epa_off': -0.219, 'epa_def_allowed': -0.110, 'success_rate_off': 0.35},
        'Panthers': {'epa_off': -0.107, 'epa_def_allowed': 0.090, 'success_rate_off': 0.40},
        'Cardinals': {'epa_off': 0.016, 'epa_def_allowed': 0.016, 'success_rate_off': 0.45},
        'Broncos': {'epa_off': 0.082, 'epa_def_allowed': -0.049, 'success_rate_off': 0.46},
        'Colts': {'epa_off': 0.251, 'epa_def_allowed': -0.159, 'success_rate_off': 0.53},
        'Eagles': {'epa_off': 0.171, 'epa_def_allowed': 0.171, 'success_rate_off': 0.49},
        'Chiefs': {'epa_off': 0.131, 'epa_def_allowed': 0.214, 'success_rate_off': 0.48},
        'Falcons': {'epa_off': 0.011, 'epa_def_allowed': 0.076, 'success_rate_off': 0.44},
        'Vikings': {'epa_off': -0.064, 'epa_def_allowed': -0.064, 'success_rate_off': 0.42},
        'Buccaneers': {'epa_off': 0.076, 'epa_def_allowed': 0.076, 'success_rate_off': 0.45},
        'Texans': {'epa_off': -0.121, 'epa_def_allowed': -0.075, 'success_rate_off': 0.38},
        'Chargers': {'epa_off': 0.214, 'epa_def_allowed': 0.214, 'success_rate_off': 0.52},
        'Raiders': {'epa_off': 0.082, 'epa_def_allowed': -0.049, 'success_rate_off': 0.46}
    }
    return team_epa_data

def calculate_cover_probability(underdog_epa_off, favorite_epa_off, spread, is_home):
    """
    Calculate cover probability based on Week 1 EPA findings
    Key factors from Week 1 analysis:
    - Offensive EPA correlation: r = 0.491
    - EPA differential correlation: r = -0.496
    - Home field advantage: 50% vs 37.5%
    """
    
    # Base probability (43.8% from Week 1)
    base_prob = 0.438
    
    # EPA differential factor (strongest predictor)
    epa_diff = favorite_epa_off - underdog_epa_off
    epa_factor = -0.496 * epa_diff  # Negative correlation means underdog advantage when diff is negative
    
    # Offensive EPA factor
    off_epa_factor = 0.491 * underdog_epa_off
    
    # Home field advantage
    home_factor = 0.125 if is_home else 0  # 50% vs 37.5% = 12.5% advantage
    
    # Spread factor (bigger underdogs tend to cover more in Week 1)
    spread_factor = 0.02 * spread  # Slight boost for bigger underdogs
    
    # Calculate final probability
    cover_prob = base_prob + epa_factor + off_epa_factor + home_factor + spread_factor
    
    # Ensure probability stays within reasonable bounds
    cover_prob = np.clip(cover_prob, 0.1, 0.9)
    
    return cover_prob

def make_week2_predictions():
    """Make Week 2 underdog cover predictions"""
    
    # Load Week 2 odds
    week2_odds = pd.read_csv('week2_2025_odds.csv')
    
    # Load team EPA data
    team_epa = load_week1_epa_data()
    
    print("Week 2 2025 NFL Underdog Cover Predictions")
    print("Based on Week 1 EPA Analysis")
    print("=" * 70)
    
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
        underdog_epa = team_epa.get(underdog, {'epa_off': 0, 'epa_def_allowed': 0, 'success_rate_off': 0.45})
        favorite_epa = team_epa.get(favorite, {'epa_off': 0, 'epa_def_allowed': 0, 'success_rate_off': 0.45})
        
        # Calculate cover probability
        cover_prob = calculate_cover_probability(
            underdog_epa['epa_off'], 
            favorite_epa['epa_off'], 
            underdog_spread, 
            is_home
        )
        
        # Determine confidence level
        if cover_prob > 0.6:
            confidence = "HIGH"
        elif cover_prob > 0.5:
            confidence = "MEDIUM"
        else:
            confidence = "LOW"
        
        predictions.append({
            'game': f'{away_team} at {home_team}',
            'underdog': underdog,
            'favorite': favorite,
            'spread': underdog_spread,
            'underdog_epa_off': underdog_epa['epa_off'],
            'favorite_epa_off': favorite_epa['epa_off'],
            'epa_differential': favorite_epa['epa_off'] - underdog_epa['epa_off'],
            'cover_probability': cover_prob,
            'confidence': confidence,
            'is_home': is_home
        })
    
    # Sort by cover probability
    predictions_df = pd.DataFrame(predictions)
    predictions_df = predictions_df.sort_values('cover_probability', ascending=False)
    
    print(f"{'Game':<25} {'Underdog':<12} {'Spread':<7} {'EPA Diff':<8} {'Prob':<6} {'Conf':<6}")
    print("-" * 70)
    
    for _, pred in predictions_df.iterrows():
        print(f"{pred['game']:<25} {pred['underdog']:<12} +{pred['spread']:<6.1f} {pred['epa_differential']:<8.3f} {pred['cover_probability']:<6.1%} {pred['confidence']:<6}")
    
    print("\n" + "=" * 70)
    print("TOP 5 UNDERDOG PICKS:")
    print("=" * 70)
    
    top_5 = predictions_df.head(5)
    for i, (_, pred) in enumerate(top_5.iterrows(), 1):
        print(f"{i}. {pred['underdog']} (+{pred['spread']:.1f}) vs {pred['favorite']}")
        print(f"   Cover Probability: {pred['cover_probability']:.1%}")
        print(f"   EPA Advantage: {pred['epa_differential']:.3f}")
        print(f"   Confidence: {pred['confidence']}")
        print()
    
    # Save predictions to CSV
    predictions_df.to_csv('week2_underdog_predictions.csv', index=False)
    print("Predictions saved to week2_underdog_predictions.csv")
    
    return predictions_df

if __name__ == "__main__":
    predictions = make_week2_predictions()
