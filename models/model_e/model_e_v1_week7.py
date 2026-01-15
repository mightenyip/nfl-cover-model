#!/usr/bin/env python3
"""
Model E v1 Week 7: Additive EPA Framework
Uses Offensive EPA + Defensive EPA Allowed = Expected Performance
Based on Model B v2 framework but with additive logic
"""

import pandas as pd
import numpy as np
from datetime import datetime

def run_model_e_v1_week7():
    """Run Model E v1 for Week 7 with additive EPA framework"""
    
    print("=== Week 7 Model E v1: Additive EPA Framework ===")
    print("Using Offensive EPA + Defensive EPA Allowed = Expected Performance")
    
    # Team name to abbreviation mapping
    team_mapping = {
        'Steelers': 'PIT', 'Bengals': 'CIN', 'Rams': 'LA', 'Jaguars': 'JAX',
        'Saints': 'NO', 'Bears': 'CHI', 'Dolphins': 'MIA', 'Browns': 'CLE',
        'Patriots': 'NE', 'Titans': 'TEN', 'Falcons': 'ATL', 'Buccaneers': 'TB',
        'Eagles': 'PHI', 'Giants': 'NYG', 'Packers': 'GB', 'Panthers': 'CAR',
        'Raiders': 'LV', 'Texans': 'HOU', 'Colts': 'IND', 'Commanders': 'WAS',
        'Chiefs': 'KC', 'Broncos': 'DEN', 'Cardinals': 'ARI', 'Chargers': 'LAC',
        'Cowboys': 'DAL', 'Jets': 'NYJ', 'Lions': 'DET', 'Seahawks': 'SEA',
        'Vikings': 'MIN', '49ers': 'SF'
    }
    
    # Load the EPA data
    epa_data_path = "../../data/epa/processed/detailed_epa_data_current.csv"
    week7_odds_path = "../../schedule/week7_2025_odds.csv"
    
    try:
        epa_data = pd.read_csv(epa_data_path)
        week7_odds = pd.read_csv(week7_odds_path)
        print(f"✅ Loaded EPA data for {len(epa_data)} teams")
        print(f"✅ Loaded Week 7 odds for {len(week7_odds)} games")
    except FileNotFoundError as e:
        print(f"❌ Error loading data: {e}")
        return
    
    # Display EPA data summary
    print(f"\n=== EPA Data Summary ===")
    print(f"Last Updated: {epa_data['last_updated'].iloc[0]}")
    print(f"Data Source: {epa_data['source'].iloc[0]}")
    
    # Process each game
    predictions = []
    
    for _, game in week7_odds.iterrows():
        away_team = game['away_team']
        home_team = game['home_team']
        spread_line = game['spread_line']
        total_line = game['total_line']
        
        # Determine favorite and underdog
        if spread_line > 0:
            favorite_team = home_team
            underdog_team = away_team
            underdog_abbr = team_mapping[away_team]
            favorite_abbr = team_mapping[home_team]
        else:
            favorite_team = away_team
            underdog_team = home_team
            underdog_abbr = team_mapping[home_team]
            favorite_abbr = team_mapping[away_team]
            spread_line = abs(spread_line)
        
        # Get EPA data for both teams
        underdog_data = epa_data[epa_data['team'] == underdog_abbr].iloc[0]
        favorite_data = epa_data[epa_data['team'] == favorite_abbr].iloc[0]
        
        # Extract EPA metrics
        underdog_metrics = {
            'epa_off': underdog_data['epa_off_per_play'],
            'epa_def_allowed': underdog_data['epa_def_allowed_per_play'],
            'epa_pass_off': underdog_data['epa_pass_off'],
            'epa_rush_off': underdog_data['epa_rush_off'],
            'epa_pass_def': underdog_data['epa_pass_def_allowed'],
            'epa_rush_def': underdog_data['epa_rush_def_allowed']
        }
        
        favorite_metrics = {
            'epa_off': favorite_data['epa_off_per_play'],
            'epa_def_allowed': favorite_data['epa_def_allowed_per_play'],
            'epa_pass_off': favorite_data['epa_pass_off'],
            'epa_rush_off': favorite_data['epa_rush_off'],
            'epa_pass_def': favorite_data['epa_pass_def_allowed'],
            'epa_rush_def': favorite_data['epa_rush_def_allowed']
        }
        
        # Model E: Additive EPA Framework
        # Expected Performance = Offensive EPA + Defensive EPA Allowed
        
        # Underdog expected performance vs Favorite defense
        underdog_expected_pass = underdog_metrics['epa_pass_off'] + favorite_metrics['epa_pass_def']
        underdog_expected_rush = underdog_metrics['epa_rush_off'] + favorite_metrics['epa_rush_def']
        underdog_expected_total = underdog_expected_pass + underdog_expected_rush
        
        # Favorite expected performance vs Underdog defense  
        favorite_expected_pass = favorite_metrics['epa_pass_off'] + underdog_metrics['epa_pass_def']
        favorite_expected_rush = favorite_metrics['epa_rush_off'] + underdog_metrics['epa_rush_def']
        favorite_expected_total = favorite_expected_pass + favorite_expected_rush
        
        # Calculate advantages using additive framework
        pass_advantage = favorite_expected_pass - underdog_expected_pass
        rush_advantage = favorite_expected_rush - underdog_expected_rush
        total_advantage = favorite_expected_total - underdog_expected_total
        
        # Calculate cover probability based on total advantage
        # Higher advantage = higher probability of covering
        cover_probability = 0.5 + (total_advantage * 0.15)  # Scale factor
        cover_probability = max(0.1, min(0.9, cover_probability))  # Clamp between 0.1 and 0.9
        
        # Confidence based on magnitude of advantages
        confidence = "LOW"
        if abs(total_advantage) > 0.4:
            confidence = "VERY_HIGH"
        elif abs(total_advantage) > 0.25:
            confidence = "HIGH"
        elif abs(total_advantage) > 0.15:
            confidence = "MEDIUM"
        
        # Predict cover
        predicted_cover = cover_probability > 0.5
        
        # Outright win probability
        outright_win_probability = 0.5 + (total_advantage * 0.12)
        outright_win_probability = max(0.1, min(0.9, outright_win_probability))
        
        # Outright win confidence
        outright_confidence = "LOW"
        if abs(outright_win_probability - 0.5) > 0.25:
            outright_confidence = "HIGH"
        elif abs(outright_win_probability - 0.5) > 0.15:
            outright_confidence = "MEDIUM"
        
        predicted_outright_win = outright_win_probability > 0.5
        
        # Store prediction
        prediction = {
            'away_team': away_team,
            'home_team': home_team,
            'favorite_team': favorite_team,
            'underdog_team': underdog_team,
            'spread_line': game['spread_line'],
            'total_line': total_line,
            'underdog_abbr': underdog_abbr,
            'favorite_abbr': favorite_abbr,
            
            # EPA metrics
            'underdog_epa_pass_off': underdog_metrics['epa_pass_off'],
            'underdog_epa_rush_off': underdog_metrics['epa_rush_off'],
            'underdog_epa_pass_def': underdog_metrics['epa_pass_def'],
            'underdog_epa_rush_def': underdog_metrics['epa_rush_def'],
            'favorite_epa_pass_off': favorite_metrics['epa_pass_off'],
            'favorite_epa_rush_off': favorite_metrics['epa_rush_off'],
            'favorite_epa_pass_def': favorite_metrics['epa_pass_def'],
            'favorite_epa_rush_def': favorite_metrics['epa_rush_def'],
            
            # Expected performance (additive framework)
            'underdog_expected_pass': underdog_expected_pass,
            'underdog_expected_rush': underdog_expected_rush,
            'underdog_expected_total': underdog_expected_total,
            'favorite_expected_pass': favorite_expected_pass,
            'favorite_expected_rush': favorite_expected_rush,
            'favorite_expected_total': favorite_expected_total,
            
            # Advantages
            'pass_advantage': pass_advantage,
            'rush_advantage': rush_advantage,
            'total_advantage': total_advantage,
            
            # Predictions
            'cover_probability': cover_probability,
            'confidence': confidence,
            'predicted_cover': predicted_cover,
            'outright_win_probability': outright_win_probability,
            'outright_confidence': outright_confidence,
            'predicted_outright_win': predicted_outright_win
        }
        
        predictions.append(prediction)
        
        # Display game analysis
        print(f"\n=== {away_team} @ {home_team} ===")
        print(f"Spread: {game['spread_line']}, Total: {total_line}")
        print(f"Favorite: {favorite_team}, Underdog: {underdog_team}")
        print()
        print(f"Expected Performance (Additive Framework):")
        print(f"  Underdog: Pass {underdog_expected_pass:.3f}, Rush {underdog_expected_rush:.3f}, Total {underdog_expected_total:.3f}")
        print(f"  Favorite: Pass {favorite_expected_pass:.3f}, Rush {favorite_expected_rush:.3f}, Total {favorite_expected_total:.3f}")
        print(f"  Total Advantage: {total_advantage:.3f}")
        print(f"  Cover Probability: {cover_probability:.3f} ({confidence})")
        print(f"  Predicted Cover: {'YES' if predicted_cover else 'NO'}")
    
    # Save predictions
    predictions_df = pd.DataFrame(predictions)
    predictions_df.to_csv('model_e_v1_week7_predictions.csv', index=False)
    print(f"\n✅ Saved Week 7 predictions to model_e_v1_week7_predictions.csv")
    
    # Summary
    print(f"\n=== Week 7 Predictions Summary ===")
    print(f"Total Games: {len(predictions)}")
    print(f"Predicted Covers: {sum(p['predicted_cover'] for p in predictions)}")
    print(f"Predicted Outright Wins: {sum(p['predicted_outright_win'] for p in predictions)}")
    
    # High confidence predictions
    high_conf = [p for p in predictions if p['confidence'] in ['HIGH', 'VERY_HIGH']]
    print(f"High Confidence Predictions: {len(high_conf)}")
    
    return predictions_df

if __name__ == "__main__":
    run_model_e_v1_week7()
