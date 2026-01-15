#!/usr/bin/env python3
"""
Generate Model E predictions for all weeks (1-9)
Model E: Advanced EPA metrics (Pass/Rush EPA efficiency)
"""

import pandas as pd
import numpy as np
import os

def get_team_mapping():
    """Get team name to abbreviation mapping"""
    return {
        '49ers': 'SF', 'Bears': 'CHI', 'Bengals': 'CIN', 'Bills': 'BUF', 'Broncos': 'DEN',
        'Browns': 'CLE', 'Buccaneers': 'TB', 'Cardinals': 'ARI', 'Chargers': 'LAC', 'Chiefs': 'KC',
        'Colts': 'IND', 'Commanders': 'WAS', 'Cowboys': 'DAL', 'Dolphins': 'MIA', 'Eagles': 'PHI',
        'Falcons': 'ATL', 'Giants': 'NYG', 'Jaguars': 'JAX', 'Jets': 'NYJ', 'Lions': 'DET',
        'Packers': 'GB', 'Panthers': 'CAR', 'Patriots': 'NE', 'Raiders': 'LV', 'Rams': 'LA',
        'Ravens': 'BAL', 'Saints': 'NO', 'Seahawks': 'SEA', 'Steelers': 'PIT', 'Texans': 'HOU',
        'Titans': 'TEN', 'Vikings': 'MIN'
    }

def load_epa_data():
    """Load EPA data"""
    try:
        epa_data = pd.read_csv("sumersports_epa_data.csv")
        return epa_data
    except:
        try:
            epa_data = pd.read_csv("detailed_epa_data.csv")
            return epa_data
        except:
            print("Could not load EPA data")
            return None

def run_model_e(week_odds, epa_data, week_num):
    """Run Model E predictions using Pass/Rush EPA efficiency"""
    team_mapping = get_team_mapping()
    predictions = []
    
    for _, game in week_odds.iterrows():
        away_team = game['away_team']
        home_team = game['home_team']
        favorite = game['favorite_team']
        underdog = game['underdog_team']
        spread = game['spread_line']
        
        # Get EPA data using team mapping
        away_team_abbr = team_mapping.get(away_team, away_team)
        home_team_abbr = team_mapping.get(home_team, home_team)
        away_epa = epa_data[epa_data['team'] == away_team_abbr]
        home_epa = epa_data[epa_data['team'] == home_team_abbr]
        
        if away_epa.empty or home_epa.empty:
            continue
        
        # Analyze pass vs rush EPA
        # Try to get pass/rush specific EPA, otherwise use overall
        try:
            if favorite == away_team:
                fav_pass_epa = away_epa['epa_off_per_pass'].iloc[0] if 'epa_off_per_pass' in away_epa.columns else away_epa['epa_off_per_play'].iloc[0]
                fav_rush_epa = away_epa['epa_off_per_rush'].iloc[0] if 'epa_off_per_rush' in away_epa.columns else away_epa['epa_off_per_play'].iloc[0]
                underdog_pass_epa = home_epa['epa_off_per_pass'].iloc[0] if 'epa_off_per_pass' in home_epa.columns else home_epa['epa_off_per_play'].iloc[0]
                underdog_rush_epa = home_epa['epa_off_per_rush'].iloc[0] if 'epa_off_per_rush' in home_epa.columns else home_epa['epa_off_per_play'].iloc[0]
            else:
                fav_pass_epa = home_epa['epa_off_per_pass'].iloc[0] if 'epa_off_per_pass' in home_epa.columns else home_epa['epa_off_per_play'].iloc[0]
                fav_rush_epa = home_epa['epa_off_per_rush'].iloc[0] if 'epa_off_per_rush' in home_epa.columns else home_epa['epa_off_per_play'].iloc[0]
                underdog_pass_epa = away_epa['epa_off_per_pass'].iloc[0] if 'epa_off_per_pass' in away_epa.columns else away_epa['epa_off_per_play'].iloc[0]
                underdog_rush_epa = away_epa['epa_off_per_rush'].iloc[0] if 'epa_off_per_rush' in away_epa.columns else away_epa['epa_off_per_play'].iloc[0]
        except:
            # Fallback to overall EPA
            if favorite == away_team:
                fav_pass_epa = away_epa['epa_off_per_play'].iloc[0]
                fav_rush_epa = away_epa['epa_off_per_play'].iloc[0]
                underdog_pass_epa = home_epa['epa_off_per_play'].iloc[0]
                underdog_rush_epa = home_epa['epa_off_per_play'].iloc[0]
            else:
                fav_pass_epa = home_epa['epa_off_per_play'].iloc[0]
                fav_rush_epa = home_epa['epa_off_per_play'].iloc[0]
                underdog_pass_epa = away_epa['epa_off_per_play'].iloc[0]
                underdog_rush_epa = away_epa['epa_off_per_play'].iloc[0]
        
        # Calculate combined offensive efficiency
        fav_efficiency = (fav_pass_epa + fav_rush_epa) / 2
        underdog_efficiency = (underdog_pass_epa + underdog_rush_epa) / 2
        
        # Prediction based on efficiency comparison
        efficiency_diff = underdog_efficiency - fav_efficiency
        
        if efficiency_diff > 0.1:
            predicted_cover = True
            confidence = "HIGH"
            probability = 0.70
        elif efficiency_diff > 0.05:
            predicted_cover = True
            confidence = "MEDIUM"
            probability = 0.60
        else:
            predicted_cover = False
            confidence = "MEDIUM"
            probability = 0.55
        
        predictions.append({
            'game': f"{away_team} @ {home_team}",
            'favorite': favorite,
            'underdog': underdog,
            'spread': spread,
            'predicted_cover': predicted_cover,
            'confidence': confidence,
            'probability': probability,
            'efficiency_diff': efficiency_diff
        })
    
    return pd.DataFrame(predictions)

def generate_all_weeks():
    """Generate Model E predictions for all weeks"""
    
    epa_data = load_epa_data()
    if epa_data is None:
        print("❌ Could not load EPA data")
        return
    
    weeks = [1, 2, 3, 4, 5, 6, 7]  # Weeks 8 and 9 already have predictions
    
    for week in weeks:
        print(f"\n{'='*80}")
        print(f"GENERATING MODEL E PREDICTIONS FOR WEEK {week}")
        print(f"{'='*80}")
        
        # Load odds
        odds_file = f"schedule/week{week}_2025_odds.csv"
        if not os.path.exists(odds_file):
            print(f"⚠️  {odds_file} not found, skipping Week {week}")
            continue
        
        week_odds = pd.read_csv(odds_file)
        print(f"Loaded {len(week_odds)} games for Week {week}")
        
        # Generate predictions
        model_e = run_model_e(week_odds, epa_data, week)
        
        # Save predictions
        model_e_file = f"models/model_e/model_e_week{week}_predictions.csv"
        os.makedirs(os.path.dirname(model_e_file), exist_ok=True)
        model_e.to_csv(model_e_file, index=False)
        print(f"✅ Saved Model E predictions: {model_e_file} ({len(model_e)} games)")
    
    print(f"\n{'='*80}")
    print("✅ COMPLETED: Model E predictions generated for all weeks")
    print(f"{'='*80}")

if __name__ == "__main__":
    generate_all_weeks()

