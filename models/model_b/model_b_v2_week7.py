#!/usr/bin/env python3
"""
Model B v2 Week 7: Matchup-Specific EPA Predictions
Uses updated EPA data with Pass/Rush breakdowns
"""

import pandas as pd
import numpy as np
from datetime import datetime

def run_model_b_v2_week7():
    """Run Model B v2 for Week 7 with updated EPA data"""
    
    print("=== Week 7 Model B v2: Matchup-Specific EPA Predictions ===")
    print("Analyzing rush vs pass EPA matchups between teams")
    
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
    
    # Load the detailed SumerSports EPA data with Pass/Rush breakdown
    epa_data_path = "../../data/detailed_epa_data.csv"
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
    print(f"\n=== Updated EPA Data Summary ===")
    print(f"Last Updated: {epa_data['last_updated'].iloc[0]}")
    print(f"Data Source: {epa_data['source'].iloc[0]}")
    
    # Show top 5 teams by net EPA
    top_teams = epa_data.nlargest(5, 'net_epa_per_play')[['team_name', 'net_epa_per_play', 'net_epa_pass', 'net_epa_rush']]
    print(f"\nTop 5 Teams by Net EPA:")
    print(top_teams.to_string(index=False))
    
    # Show top 5 defensive teams
    top_def = epa_data.nsmallest(5, 'epa_def_allowed_per_play')[['team_name', 'epa_def_allowed_per_play', 'epa_pass_def_allowed', 'epa_rush_def_allowed']]
    print(f"\nTop 5 Defensive Teams (Lowest EPA Allowed):")
    print(top_def.to_string(index=False))
    
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
        
        # Calculate matchup advantages
        fav_pass_vs_underdog_pass_def = favorite_metrics['epa_pass_off'] - underdog_metrics['epa_pass_def']
        fav_rush_vs_underdog_rush_def = favorite_metrics['epa_rush_off'] - underdog_metrics['epa_rush_def']
        underdog_pass_vs_fav_pass_def = underdog_metrics['epa_pass_off'] - favorite_metrics['epa_pass_def']
        underdog_rush_vs_fav_rush_def = underdog_metrics['epa_rush_off'] - favorite_metrics['epa_rush_def']
        
        # Calculate advantages
        favorite_pass_advantage = fav_pass_vs_underdog_pass_def
        favorite_rush_advantage = fav_rush_vs_underdog_rush_def
        underdog_pass_advantage = underdog_pass_vs_fav_pass_def
        underdog_rush_advantage = underdog_rush_vs_fav_rush_def
        
        # Net advantages
        net_pass_advantage = favorite_pass_advantage - underdog_pass_advantage
        net_rush_advantage = favorite_rush_advantage - underdog_rush_advantage
        net_matchup_advantage = net_pass_advantage + net_rush_advantage
        
        # Total advantages
        underdog_total_advantage = underdog_pass_advantage + underdog_rush_advantage
        favorite_total_advantage = favorite_pass_advantage + favorite_rush_advantage
        
        # Calculate cover probability (simplified)
        # Higher net advantage = higher probability of covering
        cover_probability = 0.5 + (net_matchup_advantage * 0.1)  # Scale factor
        cover_probability = max(0.1, min(0.9, cover_probability))  # Clamp between 0.1 and 0.9
        
        # Pass/Rush balance
        pass_rush_balance = abs(net_pass_advantage - net_rush_advantage)
        
        # Confidence based on magnitude of advantages
        confidence = "LOW"
        if abs(net_matchup_advantage) > 0.3:
            confidence = "VERY_HIGH"
        elif abs(net_matchup_advantage) > 0.2:
            confidence = "HIGH"
        elif abs(net_matchup_advantage) > 0.1:
            confidence = "MEDIUM"
        
        # Predict cover
        predicted_cover = cover_probability > 0.5
        
        # Outright win probability
        outright_win_probability = 0.5 + (net_matchup_advantage * 0.15)
        outright_win_probability = max(0.1, min(0.9, outright_win_probability))
        
        # Outright win confidence
        outright_confidence = "LOW"
        if abs(outright_win_probability - 0.5) > 0.3:
            outright_confidence = "HIGH"
        elif abs(outright_win_probability - 0.5) > 0.2:
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
            'underdog_epa_off': underdog_metrics['epa_off'],
            'underdog_epa_def_allowed': underdog_metrics['epa_def_allowed'],
            'underdog_epa_pass_off': underdog_metrics['epa_pass_off'],
            'underdog_epa_rush_off': underdog_metrics['epa_rush_off'],
            'underdog_epa_pass_def': underdog_metrics['epa_pass_def'],
            'underdog_epa_rush_def': underdog_metrics['epa_rush_def'],
            'favorite_epa_off': favorite_metrics['epa_off'],
            'favorite_epa_def_allowed': favorite_metrics['epa_def_allowed'],
            'favorite_epa_pass_off': favorite_metrics['epa_pass_off'],
            'favorite_epa_rush_off': favorite_metrics['epa_rush_off'],
            'favorite_epa_pass_def': favorite_metrics['epa_pass_def'],
            'favorite_epa_rush_def': favorite_metrics['epa_rush_def'],
            'fav_pass_vs_underdog_pass_def': fav_pass_vs_underdog_pass_def,
            'fav_rush_vs_underdog_rush_def': fav_rush_vs_underdog_rush_def,
            'underdog_pass_vs_fav_pass_def': underdog_pass_vs_fav_pass_def,
            'underdog_rush_vs_fav_rush_def': underdog_rush_vs_fav_rush_def,
            'favorite_pass_advantage': favorite_pass_advantage,
            'favorite_rush_advantage': favorite_rush_advantage,
            'underdog_pass_advantage': underdog_pass_advantage,
            'underdog_rush_advantage': underdog_rush_advantage,
            'net_pass_advantage': net_pass_advantage,
            'net_rush_advantage': net_rush_advantage,
            'net_matchup_advantage': net_matchup_advantage,
            'underdog_total_advantage': underdog_total_advantage,
            'favorite_total_advantage': favorite_total_advantage,
            'cover_probability': cover_probability,
            'pass_rush_balance': pass_rush_balance,
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
        print(f"Net Matchup Advantage: {net_matchup_advantage:.3f}")
        print(f"Cover Probability: {cover_probability:.3f} ({confidence})")
        print(f"Predicted Cover: {'YES' if predicted_cover else 'NO'}")
        print(f"Outright Win Probability: {outright_win_probability:.3f} ({outright_confidence})")
        print(f"Predicted Outright Win: {'YES' if predicted_outright_win else 'NO'}")
    
    # Save predictions
    predictions_df = pd.DataFrame(predictions)
    predictions_df.to_csv('model_b_v2_week7_predictions.csv', index=False)
    print(f"\n✅ Saved Week 7 predictions to model_b_v2_week7_predictions.csv")
    
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
    run_model_b_v2_week7()
