#!/usr/bin/env python3
"""
Generate Week 10 Predictions for Models A, B, and E
Using Week10_EPA.csv data
"""

import pandas as pd
import numpy as np
from datetime import datetime

def get_team_mapping():
    """Map team names to abbreviations"""
    return {
        'Raiders': 'LV', 'Broncos': 'DEN', 'Falcons': 'ATL', 'Colts': 'IND',
        'Giants': 'NYG', 'Bears': 'CHI', 'Bills': 'BUF', 'Dolphins': 'MIA',
        'Ravens': 'BAL', 'Vikings': 'MIN', 'Browns': 'CLE', 'Jets': 'NYJ',
        'Patriots': 'NE', 'Buccaneers': 'TB', 'Saints': 'NO', 'Panthers': 'CAR',
        'Jaguars': 'JAX', 'Texans': 'HOU', 'Cardinals': 'ARI', 'Seahawks': 'SEA',
        'Rams': 'LA', '49ers': 'SF', 'Lions': 'DET', 'Commanders': 'WAS',
        'Steelers': 'PIT', 'Chargers': 'LAC', 'Eagles': 'PHI', 'Packers': 'GB',
        'Bengals': 'CIN', 'Titans': 'TEN', 'Chiefs': 'KC', 'Cowboys': 'DAL'
    }

def run_model_a(week10_odds, epa_data):
    """Model A: Net EPA/Matchup EPA inverse analysis"""
    
    print("\n" + "="*80)
    print("MODEL A: Net EPA/Matchup EPA Predictions")
    print("="*80)
    
    team_mapping = get_team_mapping()
    predictions = []
    
    for _, game in week10_odds.iterrows():
        away_team = game['away_team']
        home_team = game['home_team']
        favorite = game['favorite_team']
        underdog = game['underdog_team']
        spread = abs(game['spread_line'])
        
        # Convert to abbreviations
        away_abbr = team_mapping.get(away_team, away_team)
        home_abbr = team_mapping.get(home_team, home_team)
        fav_abbr = team_mapping.get(favorite, favorite)
        dog_abbr = team_mapping.get(underdog, underdog)
        
        # Get EPA data
        away_data = epa_data[epa_data['team'] == away_abbr]
        home_data = epa_data[epa_data['team'] == home_abbr]
        
        if len(away_data) == 0 or len(home_data) == 0:
            print(f"⚠️  Missing EPA data for {away_team} ({away_abbr}) or {home_team} ({home_abbr})")
            continue
        
        # Extract EPA values
        away_off_epa = away_data['epa_off_per_play'].iloc[0]
        away_def_epa = away_data['epa_def_allowed_per_play'].iloc[0]
        home_off_epa = home_data['epa_off_per_play'].iloc[0]
        home_def_epa = home_data['epa_def_allowed_per_play'].iloc[0]
        
        # Calculate net EPA
        away_net_epa = away_off_epa - away_def_epa
        home_net_epa = home_off_epa - home_def_epa
        net_epa_diff = away_net_epa - home_net_epa
        
        # Determine opponent defense quality (favorite's defense)
        if favorite == away_team:
            opponent_def_epa = home_def_epa
        else:
            opponent_def_epa = away_def_epa
        
        # 5-tier defense classification
        if opponent_def_epa <= -0.1:
            defense_quality = "ELITE"
        elif opponent_def_epa <= -0.05:
            defense_quality = "STRONG"
        elif opponent_def_epa <= 0.05:
            defense_quality = "AVERAGE"
        elif opponent_def_epa <= 0.1:
            defense_quality = "WEAK"
        else:
            defense_quality = "POOR"
        
        # Model A logic
        cover_prob = 0.50
        
        # Defense quality adjustments
        if defense_quality == "ELITE":
            cover_prob += 0.12
        elif defense_quality == "STRONG":
            cover_prob += 0.12
        elif defense_quality == "AVERAGE":
            cover_prob += 0.02
        elif defense_quality == "WEAK":
            cover_prob -= 0.10
        else:  # POOR
            cover_prob -= 0.15
        
        # Net EPA differential adjustment
        net_diff = net_epa_diff
        if net_diff > 0.10:
            cover_prob += 0.15
        elif net_diff > 0.05:
            cover_prob += 0.10
        elif net_diff < -0.10:
            cover_prob -= 0.15
        elif net_diff < -0.05:
            cover_prob -= 0.10
        
        # Spread adjustment
        cover_prob += spread * 0.008
        
        # Clamp probability
        cover_prob = max(0.05, min(0.95, cover_prob))
        
        # Determine prediction and confidence
        if cover_prob >= 0.70:
            pred = "Cover"
            conf = "HIGH"
        elif cover_prob >= 0.60:
            pred = "Cover"
            conf = "MEDIUM"
        elif cover_prob >= 0.50:
            pred = "Cover"
            conf = "MEDIUM"
        elif cover_prob >= 0.40:
            pred = "No Cover"
            conf = "MEDIUM"
        else:
            pred = "No Cover"
            conf = "HIGH"
        
        predictions.append({
            'game': f"{away_team} @ {home_team}",
            'favorite': favorite,
            'underdog': underdog,
            'spread': game['spread_line'],
            'predicted_cover': pred == "Cover",
            'probability': round(cover_prob, 3),
            'confidence': conf,
            'defense_quality': defense_quality,
            'net_epa_differential': round(net_epa_diff, 3)
        })
        
        print(f"{away_team} @ {home_team}: {pred} ({cover_prob:.1%}, {conf}) - {defense_quality} defense")
    
    return pd.DataFrame(predictions)

def run_model_b(week10_odds, epa_data):
    """Model B: Weighted pass/rush EPA using NFL league averages"""
    
    print("\n" + "="*80)
    print("MODEL B: Weighted Pass/Rush EPA Predictions")
    print("="*80)
    
    team_mapping = get_team_mapping()
    predictions = []
    
    # NFL league averages: 55.4% pass, 44.6% run
    NFL_AVG_PASS_RATE = 0.554
    NFL_AVG_RUN_RATE = 0.446
    
    for _, game in week10_odds.iterrows():
        away_team = game['away_team']
        home_team = game['home_team']
        favorite = game['favorite_team']
        underdog = game['underdog_team']
        spread = abs(game['spread_line'])
        
        # Convert to abbreviations
        away_abbr = team_mapping.get(away_team, away_team)
        home_abbr = team_mapping.get(home_team, home_team)
        fav_abbr = team_mapping.get(favorite, favorite)
        dog_abbr = team_mapping.get(underdog, underdog)
        
        # Get EPA data
        away_data = epa_data[epa_data['team'] == away_abbr]
        home_data = epa_data[epa_data['team'] == home_abbr]
        
        if len(away_data) == 0 or len(home_data) == 0:
            continue
        
        # Determine which team is favorite and underdog
        if favorite == away_team:
            fav_data = away_data
            dog_data = home_data
        else:
            fav_data = home_data
            dog_data = away_data
        
        # Pass matchup: underdog pass offense vs favorite pass defense
        dog_pass_off = dog_data['epa_pass_off'].iloc[0]
        fav_pass_def = fav_data['epa_pass_def_allowed'].iloc[0]
        pass_matchup = dog_pass_off - fav_pass_def
        
        # Rush matchup: underdog rush offense vs favorite rush defense
        dog_rush_off = dog_data['epa_rush_off'].iloc[0]
        fav_rush_def = fav_data['epa_rush_def_allowed'].iloc[0]
        rush_matchup = dog_rush_off - fav_rush_def
        
        # Combined matchup (weighted by NFL league averages)
        combined_matchup = (pass_matchup * NFL_AVG_PASS_RATE) + (rush_matchup * NFL_AVG_RUN_RATE)
        
        # Favorite advantages
        fav_pass_off = fav_data['epa_pass_off'].iloc[0]
        dog_pass_def = dog_data['epa_pass_def_allowed'].iloc[0]
        fav_pass_advantage = fav_pass_off - dog_pass_def
        
        fav_rush_off = fav_data['epa_rush_off'].iloc[0]
        dog_rush_def = dog_data['epa_rush_def_allowed'].iloc[0]
        fav_rush_advantage = fav_rush_off - dog_rush_def
        
        fav_total_advantage = (fav_pass_advantage * NFL_AVG_PASS_RATE) + (fav_rush_advantage * NFL_AVG_RUN_RATE)
        
        # Model B logic
        cover_prob = 0.50
        
        # Underdog total advantage (positive = good for underdog)
        cover_prob += combined_matchup * 2.0
        
        # Favorite total advantage (negative for underdog)
        cover_prob -= fav_total_advantage * 1.5
        
        # Pass vs Rush balance analysis
        pass_rush_balance = abs(pass_matchup - rush_matchup)
        cover_prob += pass_rush_balance * 0.5
        
        # Spread adjustment
        cover_prob += spread * 0.01
        
        # Clamp probability
        cover_prob = max(0.05, min(0.95, cover_prob))
        
        # Determine prediction and confidence
        if cover_prob >= 0.70:
            pred = "Cover"
            conf = "VERY_HIGH"
        elif cover_prob >= 0.60:
            pred = "Cover"
            conf = "HIGH"
        elif cover_prob >= 0.45:
            pred = "Cover"
            conf = "MEDIUM"
        elif cover_prob >= 0.30:
            pred = "No Cover"
            conf = "LOW"
        else:
            pred = "No Cover"
            conf = "VERY_LOW"
        
        predictions.append({
            'game': f"{away_team} @ {home_team}",
            'favorite': favorite,
            'underdog': underdog,
            'spread': game['spread_line'],
            'predicted_cover': pred == "Cover",
            'probability': round(cover_prob, 3),
            'confidence': conf,
            'combined_matchup': round(combined_matchup, 3),
            'fav_total_advantage': round(fav_total_advantage, 3)
        })
        
        print(f"{away_team} @ {home_team}: {pred} ({cover_prob:.1%}, {conf}) - Matchup: {combined_matchup:.3f}")
    
    return pd.DataFrame(predictions)

def run_model_e(week10_odds, epa_data):
    """Model E: Advanced EPA metrics (Pass/Rush EPA efficiency)"""
    
    print("\n" + "="*80)
    print("MODEL E: Advanced EPA Metrics (Pass/Rush Efficiency)")
    print("="*80)
    
    team_mapping = get_team_mapping()
    predictions = []
    
    for _, game in week10_odds.iterrows():
        away_team = game['away_team']
        home_team = game['home_team']
        favorite = game['favorite_team']
        underdog = game['underdog_team']
        spread = game['spread_line']
        
        # Get EPA data using team mapping
        away_abbr = team_mapping.get(away_team, away_team)
        home_abbr = team_mapping.get(home_team, home_team)
        
        away_epa = epa_data[epa_data['team'] == away_abbr]
        home_epa = epa_data[epa_data['team'] == home_abbr]
        
        if away_epa.empty or home_epa.empty:
            continue
        
        # Analyze pass vs rush EPA efficiency
        if favorite == away_team:
            fav_pass_epa = away_epa['epa_pass_off'].iloc[0]
            fav_rush_epa = away_epa['epa_rush_off'].iloc[0]
            underdog_pass_epa = home_epa['epa_pass_off'].iloc[0]
            underdog_rush_epa = home_epa['epa_rush_off'].iloc[0]
        else:
            fav_pass_epa = home_epa['epa_pass_off'].iloc[0]
            fav_rush_epa = home_epa['epa_rush_off'].iloc[0]
            underdog_pass_epa = away_epa['epa_pass_off'].iloc[0]
            underdog_rush_epa = away_epa['epa_rush_off'].iloc[0]
        
        # Calculate combined offensive efficiency
        fav_efficiency = (fav_pass_epa + fav_rush_epa) / 2
        underdog_efficiency = (underdog_pass_epa + underdog_rush_epa) / 2
        
        # Efficiency difference (positive = underdog more efficient)
        efficiency_diff = underdog_efficiency - fav_efficiency
        
        # Prediction based on efficiency comparison
        if efficiency_diff > 0.1:
            predicted_cover = True
            confidence = "HIGH"
            probability = 0.70
        elif efficiency_diff > 0.05:
            predicted_cover = True
            confidence = "MEDIUM"
            probability = 0.60
        elif efficiency_diff > -0.05:
            predicted_cover = False
            confidence = "MEDIUM"
            probability = 0.55
        else:
            predicted_cover = False
            confidence = "HIGH"
            probability = 0.65
        
        predictions.append({
            'game': f"{away_team} @ {home_team}",
            'favorite': favorite,
            'underdog': underdog,
            'spread': spread,
            'predicted_cover': predicted_cover,
            'probability': probability,
            'confidence': confidence,
            'efficiency_diff': round(efficiency_diff, 3),
            'fav_efficiency': round(fav_efficiency, 3),
            'underdog_efficiency': round(underdog_efficiency, 3)
        })
        
        print(f"{away_team} @ {home_team}: {'Cover' if predicted_cover else 'No Cover'} ({probability:.1%}, {confidence}) - Efficiency diff: {efficiency_diff:.3f}")
    
    return pd.DataFrame(predictions)

def main():
    """Main function to generate Week 10 predictions"""
    
    print("="*80)
    print("WEEK 10 2025 PREDICTIONS - MODELS A, B, AND E")
    print("="*80)
    
    # Load Week 10 odds
    week10_odds = pd.read_csv("schedule/week10_2025_odds.csv")
    print(f"\nLoaded {len(week10_odds)} games for Week 10")
    
    # Load Week 10 EPA data
    epa_data = pd.read_csv("data/Week10_EPA.csv")
    print(f"Loaded EPA data for {len(epa_data)} teams")
    
    # Run all three models
    model_a_preds = run_model_a(week10_odds, epa_data)
    model_b_preds = run_model_b(week10_odds, epa_data)
    model_e_preds = run_model_e(week10_odds, epa_data)
    
    # Save individual model predictions
    model_a_preds.to_csv("models/model_a/model_a_week10_predictions.csv", index=False)
    model_b_preds.to_csv("models/model_b/model_b_week10_predictions.csv", index=False)
    model_e_preds.to_csv("models/model_e/model_e_week10_predictions.csv", index=False)
    
    print(f"\n✅ Model A predictions saved to models/model_a/model_a_week10_predictions.csv")
    print(f"✅ Model B predictions saved to models/model_b/model_b_week10_predictions.csv")
    print(f"✅ Model E predictions saved to models/model_e/model_e_week10_predictions.csv")
    
    # Create combined summary
    summary = week10_odds.copy()
    summary['game'] = summary['away_team'] + ' @ ' + summary['home_team']
    
    # Merge predictions
    summary = summary.merge(
        model_a_preds[['game', 'predicted_cover', 'probability', 'confidence']].rename(
            columns={'predicted_cover': 'Model_A_Cover', 'probability': 'Model_A_Prob', 'confidence': 'Model_A_Conf'}
        ),
        on='game', how='left'
    )
    summary = summary.merge(
        model_b_preds[['game', 'predicted_cover', 'probability', 'confidence']].rename(
            columns={'predicted_cover': 'Model_B_Cover', 'probability': 'Model_B_Prob', 'confidence': 'Model_B_Conf'}
        ),
        on='game', how='left'
    )
    summary = summary.merge(
        model_e_preds[['game', 'predicted_cover', 'probability', 'confidence']].rename(
            columns={'predicted_cover': 'Model_E_Cover', 'probability': 'Model_E_Prob', 'confidence': 'Model_E_Conf'}
        ),
        on='game', how='left'
    )
    
    # Save combined summary
    summary.to_csv("predictions/week10_all_models_predictions.csv", index=False)
    print(f"\n✅ Combined predictions saved to predictions/week10_all_models_predictions.csv")
    
    # Print summary statistics
    print("\n" + "="*80)
    print("PREDICTION SUMMARY")
    print("="*80)
    
    a_covers = model_a_preds['predicted_cover'].sum()
    b_covers = model_b_preds['predicted_cover'].sum()
    e_covers = model_e_preds['predicted_cover'].sum()
    total_games = len(model_a_preds)
    
    print(f"\nModel A: {a_covers}/{total_games} underdog covers predicted ({a_covers/total_games:.1%})")
    print(f"Model B: {b_covers}/{total_games} underdog covers predicted ({b_covers/total_games:.1%})")
    print(f"Model E: {e_covers}/{total_games} underdog covers predicted ({e_covers/total_games:.1%})")
    
    print("\n✅ Week 10 predictions complete!")

if __name__ == "__main__":
    main()

