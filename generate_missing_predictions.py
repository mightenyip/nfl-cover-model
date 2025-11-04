#!/usr/bin/env python3
"""
Generate missing model predictions for Weeks 2 and 4
Runs Models B, C, and D for weeks that are missing predictions
"""

import pandas as pd
import numpy as np
import os
import sys

# Add scripts directory to path
sys.path.append('scripts')

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

def run_model_b(week_odds, epa_data, week_num):
    """Run Model B predictions"""
    team_mapping = get_team_mapping()
    predictions = []
    
    for idx, row in week_odds.iterrows():
        away_team = row['away_team']
        home_team = row['home_team']
        favorite = row['favorite_team']
        underdog = row['underdog_team']
        spread = row['spread_line']
        
        away_abbr = team_mapping.get(away_team, away_team)
        home_abbr = team_mapping.get(home_team, home_team)
        
        away_epa = epa_data[epa_data['team'] == away_abbr]
        home_epa = epa_data[epa_data['team'] == home_abbr]
        
        if away_epa.empty or home_epa.empty:
            continue
        
        away_off = away_epa['epa_off_per_play'].iloc[0]
        away_def = away_epa['epa_def_allowed_per_play'].iloc[0]
        home_off = home_epa['epa_off_per_play'].iloc[0]
        home_def = home_epa['epa_def_allowed_per_play'].iloc[0]
        
        away_net = away_off - away_def
        home_net = home_off - home_def
        
        # Determine opponent defense quality
        if favorite == away_team:
            opponent_def_epa = home_def
        else:
            opponent_def_epa = away_def
        
        # 5-tier defense classification
        if opponent_def_epa <= -0.1:
            defense_quality = "ELITE"
            def_multiplier = 0.7
        elif opponent_def_epa <= -0.05:
            defense_quality = "STRONG"
            def_multiplier = 0.85
        elif opponent_def_epa <= 0.05:
            defense_quality = "AVERAGE"
            def_multiplier = 1.0
        elif opponent_def_epa <= 0.1:
            defense_quality = "WEAK"
            def_multiplier = 1.15
        else:
            defense_quality = "POOR"
            def_multiplier = 1.3
        
        # Calculate cover probability
        base_prob = 0.50
        
        # Net EPA differential adjustment
        if favorite == away_team:
            net_diff = home_net - away_net
        else:
            net_diff = away_net - home_net
        
        epa_adjustment = net_diff * 0.3 * def_multiplier
        prob = base_prob + epa_adjustment
        
        # Spread adjustment
        if abs(spread) > 7:
            prob += 0.05
        
        prob = max(0.01, min(0.99, prob))
        predicted_cover = prob > 0.5
        
        predictions.append({
            'game': f"{away_team} @ {home_team}",
            'favorite': favorite,
            'underdog': underdog,
            'spread': spread,
            'predicted_cover': predicted_cover,
            'probability': prob,
            'confidence': 'HIGH' if abs(prob - 0.5) > 0.15 else 'MEDIUM',
            'defense_quality': defense_quality
        })
    
    return pd.DataFrame(predictions)

def run_model_c(week_odds, week_num):
    """Run Model C predictions using ATS trends"""
    predictions = []
    
    for idx, row in week_odds.iterrows():
        away_team = row['away_team']
        home_team = row['home_team']
        favorite = row['favorite_team']
        underdog = row['underdog_team']
        spread = row['spread_line']
        total = row.get('total_line', 45)
        
        favorite_is_home = favorite == home_team
        favorite_is_away = favorite == away_team
        
        # Model C rules based on spread and location
        if favorite_is_away:
            # Away favorites - 60% ATS success rate
            if abs(spread) <= 3.5:
                predicted_cover = False  # Favorite covers
                probability = 0.60
                confidence = 'HIGH'
            else:
                predicted_cover = False
                probability = 0.575
                confidence = 'MEDIUM'
        else:
            # Home favorites
            if abs(spread) <= 3.5:
                predicted_cover = False
                probability = 0.648
                confidence = 'VERY_HIGH'
            elif abs(spread) > 7:
                predicted_cover = True  # Underdog covers
                probability = 0.60
                confidence = 'MEDIUM'
            else:
                predicted_cover = False
                probability = 0.648
                confidence = 'HIGH'
        
        predictions.append({
            'game': f"{away_team} @ {home_team}",
            'favorite': favorite,
            'underdog': underdog,
            'spread': spread,
            'predicted_cover': predicted_cover,
            'probability': probability,
            'confidence': confidence
        })
    
    return pd.DataFrame(predictions)

def run_model_d(week_odds, week_num):
    """Run Model D predictions using spread-based rules"""
    predictions = []
    
    for idx, row in week_odds.iterrows():
        away_team = row['away_team']
        home_team = row['home_team']
        favorite = row['favorite_team']
        underdog = row['underdog_team']
        spread = row['spread_line']
        total = row.get('total_line', 45)
        
        # Model D rules
        if abs(spread) > 7:
            predicted_cover = True  # Fade large spread
            confidence = "HIGH"
            probability = 0.65
        elif abs(spread) >= 3:
            predicted_cover = True  # Medium spread underdog
            confidence = "MEDIUM"
            probability = 0.55
        else:
            predicted_cover = False  # Small spread favorite
            confidence = "MEDIUM"
            probability = 0.55
        
        predictions.append({
            'game': f"{away_team} @ {home_team}",
            'favorite': favorite,
            'underdog': underdog,
            'spread': spread,
            'predicted_cover': predicted_cover,
            'probability': probability,
            'confidence': confidence
        })
    
    return pd.DataFrame(predictions)

def generate_missing_predictions():
    """Generate predictions for missing weeks"""
    
    missing_weeks = [2, 4]  # Weeks that need Model B, C, D predictions
    
    for week in missing_weeks:
        print(f"\n{'='*80}")
        print(f"GENERATING PREDICTIONS FOR WEEK {week}")
        print(f"{'='*80}")
        
        # Load odds
        odds_file = f"schedule/week{week}_2025_odds.csv"
        if not os.path.exists(odds_file):
            print(f"⚠️  {odds_file} not found, skipping Week {week}")
            continue
        
        week_odds = pd.read_csv(odds_file)
        print(f"Loaded {len(week_odds)} games for Week {week}")
        
        # Load EPA data for Model B
        epa_data = load_epa_data()
        
        # Generate Model B predictions
        if epa_data is not None:
            print(f"\nGenerating Model B predictions...")
            model_b = run_model_b(week_odds, epa_data, week)
            model_b_file = f"models/model_b/model_b_week{week}_predictions.csv"
            os.makedirs(os.path.dirname(model_b_file), exist_ok=True)
            model_b.to_csv(model_b_file, index=False)
            print(f"✅ Saved Model B predictions: {model_b_file}")
        
        # Generate Model C predictions
        print(f"\nGenerating Model C predictions...")
        model_c = run_model_c(week_odds, week)
        model_c_file = f"models/model_c/model_c_week{week}_predictions.csv"
        os.makedirs(os.path.dirname(model_c_file), exist_ok=True)
        model_c.to_csv(model_c_file, index=False)
        print(f"✅ Saved Model C predictions: {model_c_file}")
        
        # Generate Model D predictions
        print(f"\nGenerating Model D predictions...")
        model_d = run_model_d(week_odds, week)
        model_d_file = f"models/model_d/model_d_week{week}_predictions.csv"
        os.makedirs(os.path.dirname(model_d_file), exist_ok=True)
        model_d.to_csv(model_d_file, index=False)
        print(f"✅ Saved Model D predictions: {model_d_file}")
        
        print(f"\n✅ Completed Week {week} predictions")

if __name__ == "__main__":
    generate_missing_predictions()

