#!/usr/bin/env python3
"""
Create Week 16 Predictions Final
Generate predictions using Models A, B, and E, then combine into final CSV
"""

import pandas as pd
import numpy as np
import os
import random

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
    """Load Week 16 EPA data"""
    try:
        epa_df = pd.read_csv("data/epa/week16/Week16_EPA.csv")
        print(f"✅ Loaded EPA data for {len(epa_df)} teams")
        return epa_df
    except FileNotFoundError:
        print("❌ Error: data/epa/week16/Week16_EPA.csv not found")
        return None

def load_week16_odds():
    """Load Week 16 odds"""
    try:
        odds_df = pd.read_csv("schedule/week16_2025_odds.csv")
        print(f"✅ Loaded {len(odds_df)} games from Week 16 odds")
        return odds_df
    except FileNotFoundError:
        print("❌ Error: schedule/week16_2025_odds.csv not found")
        return None

def run_model_a(week16_odds, epa_data):
    """Run Model A predictions"""
    team_mapping = get_team_mapping()
    predictions = []
    
    for idx, row in week16_odds.iterrows():
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
        
        # Calculate from underdog's perspective (underdog_net - favorite_net)
        # Positive means underdog is stronger (more likely to cover)
        if favorite == away_team:
            favorite_net = away_net
            underdog_net = home_net
        else:
            favorite_net = home_net
            underdog_net = away_net
        
        net_epa_diff = underdog_net - favorite_net
        
        # Determine opponent defense quality
        if favorite == away_team:
            opponent_def_epa = home_def
        else:
            opponent_def_epa = away_def
        
        # 5-tier defense classification
        if opponent_def_epa <= -0.1:
            defense_quality = "ELITE"
            def_adjustment = -0.15
        elif opponent_def_epa <= -0.05:
            defense_quality = "STRONG"
            def_adjustment = -0.08
        elif opponent_def_epa <= 0.05:
            defense_quality = "AVERAGE"
            def_adjustment = 0.0
        elif opponent_def_epa <= 0.1:
            defense_quality = "WEAK"
            def_adjustment = 0.05
        else:
            defense_quality = "POOR"
            def_adjustment = 0.12
        
        # Calculate cover probability
        base_prob = 0.5
        epa_adjustment = net_epa_diff * 0.3
        spread_adjustment = abs(spread) * 0.003
        
        cover_prob = base_prob + epa_adjustment + def_adjustment + spread_adjustment
        cover_prob = max(0.1, min(0.9, cover_prob))
        
        predicted_cover = cover_prob > 0.5
        
        # Confidence level
        if cover_prob >= 0.7:
            confidence = "VERY_HIGH"
        elif cover_prob >= 0.6:
            confidence = "HIGH"
        elif cover_prob >= 0.4:
            confidence = "MEDIUM"
        elif cover_prob >= 0.3:
            confidence = "LOW"
        else:
            confidence = "VERY_LOW"
        
        game = f"{away_team} @ {home_team}"
        
        predictions.append({
            'game': game,
            'predicted_cover': predicted_cover,
            'cover_probability': cover_prob,
            'confidence': confidence
        })
    
    return pd.DataFrame(predictions)

def run_model_b(week16_odds, epa_data):
    """Run Model B predictions"""
    team_mapping = get_team_mapping()
    predictions = []
    
    for idx, row in week16_odds.iterrows():
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
#!/usr/bin/env python3
"""
Create Week 16 Predictions Final
Generate predictions using Models A, B, and E, then combine into final CSV
"""

import pandas as pd
import numpy as np
import os
import random

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
    """Load Week 16 EPA data"""
    try:
        epa_df = pd.read_csv("data/epa/week16/Week16_EPA.csv")
        print(f"✅ Loaded EPA data for {len(epa_df)} teams")
        return epa_df
    except FileNotFoundError:
        print("❌ Error: data/epa/week16/Week16_EPA.csv not found")
        return None

def load_week16_odds():
    """Load Week 16 odds"""
    try:
        odds_df = pd.read_csv("schedule/week16_2025_odds.csv")
        print(f"✅ Loaded {len(odds_df)} games from Week 16 odds")
        return odds_df
    except FileNotFoundError:
        print("❌ Error: schedule/week16_2025_odds.csv not found")
        return None

def run_model_a(week16_odds, epa_data):
    """Run Model A predictions"""
    team_mapping = get_team_mapping()
    predictions = []
    
    for idx, row in week16_odds.iterrows():
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
        
        # Calculate from underdog's perspective (underdog_net - favorite_net)
        # Positive means underdog is stronger (more likely to cover)
        if favorite == away_team:
            favorite_net = away_net
            underdog_net = home_net
        else:
            favorite_net = home_net
            underdog_net = away_net
        
        net_epa_diff = underdog_net - favorite_net
        
        # Determine opponent defense quality
        if favorite == away_team:
            opponent_def_epa = home_def
        else:
            opponent_def_epa = away_def
        
        # 5-tier defense classification
        if opponent_def_epa <= -0.1:
            defense_quality = "ELITE"
            def_adjustment = -0.15
        elif opponent_def_epa <= -0.05:
            defense_quality = "STRONG"
            def_adjustment = -0.08
        elif opponent_def_epa <= 0.05:
            defense_quality = "AVERAGE"
            def_adjustment = 0.0
        elif opponent_def_epa <= 0.1:
            defense_quality = "WEAK"
            def_adjustment = 0.05
        else:
            defense_quality = "POOR"
            def_adjustment = 0.12
        
        # Calculate cover probability
        base_prob = 0.5
        epa_adjustment = net_epa_diff * 0.3
        spread_adjustment = abs(spread) * 0.003
        
        cover_prob = base_prob + epa_adjustment + def_adjustment + spread_adjustment
        cover_prob = max(0.1, min(0.9, cover_prob))
        
        predicted_cover = cover_prob > 0.5
        
        # Confidence level
        if cover_prob >= 0.7:
            confidence = "VERY_HIGH"
        elif cover_prob >= 0.6:
            confidence = "HIGH"
        elif cover_prob >= 0.4:
            confidence = "MEDIUM"
        elif cover_prob >= 0.3:
            confidence = "LOW"
        else:
            confidence = "VERY_LOW"
        
        game = f"{away_team} @ {home_team}"
        
        predictions.append({
            'game': game,
            'predicted_cover': predicted_cover,
            'cover_probability': cover_prob,
            'confidence': confidence
        })
    
    return pd.DataFrame(predictions)

def run_model_b(week16_odds, epa_data):
    """Run Model B predictions"""
    team_mapping = get_team_mapping()
    predictions = []
    
    for idx, row in week16_odds.iterrows():
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
        
        # Calculate from underdog's perspective (underdog_net - favorite_net)
        # Positive means underdog is stronger (more likely to cover)
        if favorite == away_team:
            favorite_net = away_net
            underdog_net = home_net
        else:
            favorite_net = home_net
            underdog_net = away_net
        
        net_epa_diff = underdog_net - favorite_net
        
        # Determine opponent defense quality
        if favorite == away_team:
            opponent_def_epa = home_def
        else:
            opponent_def_epa = away_def
        
        # 5-tier defense classification with multipliers
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
        
        # Model B methodology
        base_prob = 0.5
        epa_adjustment = net_epa_diff * 0.2
        def_adjustment = (def_multiplier - 1.0) * 0.15
        spread_adjustment = min(abs(spread) * 0.003, 0.05)
        
        cover_prob = base_prob + epa_adjustment + def_adjustment + spread_adjustment
        cover_prob = max(0.1, min(0.9, cover_prob))
        
        predicted_cover = cover_prob > 0.5
        
        # Confidence level (Model B is more conservative)
        if cover_prob >= 0.65:
            confidence = "HIGH"
        elif cover_prob >= 0.55:
            confidence = "MEDIUM"
        elif cover_prob >= 0.45:
            confidence = "MEDIUM"
        else:
            confidence = "LOW"
        
        game = f"{away_team} @ {home_team}"
        
        predictions.append({
            'game': game,
            'predicted_cover': predicted_cover,
            'cover_probability': cover_prob,
            'confidence': confidence
        })
    
    return pd.DataFrame(predictions)

def run_model_e(week16_odds):
    """Run Model E predictions (random baseline)"""
    random.seed(42)
    np.random.seed(42)
    
    predictions = []
    
    for idx, row in week16_odds.iterrows():
        away_team = row['away_team']
        home_team = row['home_team']
        
        # Model E: Random baseline
        predicted_cover = random.choice([True, False])
        probability = random.uniform(0.45, 0.55)
        confidence = random.choice(['LOW', 'MEDIUM'])
        
        game = f"{away_team} @ {home_team}"
        
        predictions.append({
            'game': game,
            'predicted_cover': predicted_cover,
            'cover_probability': probability,
            'confidence': confidence
        })
    
    return pd.DataFrame(predictions)

def create_predictions_final(week16_odds, model_a, model_b, model_e):
    """Create predictions_final CSV combining all models"""
    
    predictions_final = []
    
    for idx, row in week16_odds.iterrows():
        game = f"{row['away_team']} @ {row['home_team']}"
        
        # Find matching predictions from each model
        model_a_pred = model_a[model_a['game'] == game]
        model_b_pred = model_b[model_b['game'] == game]
        model_e_pred = model_e[model_e['game'] == game]
        
        if model_a_pred.empty or model_b_pred.empty or model_e_pred.empty:
            print(f"⚠️ Missing predictions for {game}")
            continue
        
        # Extract predictions and probabilities
        ma_cover = model_a_pred['predicted_cover'].iloc[0]
        ma_prob = model_a_pred['cover_probability'].iloc[0]
        ma_conf = model_a_pred['confidence'].iloc[0]
        
        mb_cover = model_b_pred['predicted_cover'].iloc[0]
        mb_prob = model_b_pred['cover_probability'].iloc[0]
        mb_conf = model_b_pred['confidence'].iloc[0]
        
        me_cover = model_e_pred['predicted_cover'].iloc[0]
        me_prob = model_e_pred['cover_probability'].iloc[0]
        me_conf = model_e_pred['confidence'].iloc[0]
        
        # Count votes for underdog cover
        underdog_votes = sum([ma_cover, mb_cover, me_cover])
        total_votes = 3
        
        # Determine consensus (from underdog-cover perspective)
        consensus_cover = underdog_votes >= 2
        consensus_prediction = "Underdog Cover" if consensus_cover else "Favorite Cover"
        
        # Calculate consensus probability (average of all three)
        consensus_probability = np.mean([ma_prob, mb_prob, me_prob])
        
        # Format consensus votes
        consensus_votes = f"{underdog_votes}/3"
        
        # Determine agreement level
        if underdog_votes == 3:
            agreement = "Unanimous (3/3)"
        elif underdog_votes == 0:
            agreement = "Unanimous (0/3)"
        elif underdog_votes == 2:
            # Two models agree on underdog cover
            if ma_cover and mb_cover:
                agreement = "Majority (A, B)"
            elif ma_cover and me_cover:
                agreement = "Majority (A, E)"
            else:  # mb_cover and me_cover
                agreement = "Majority (B, E)"
        else:  # underdog_votes == 1
            agreement = "Split (1/3)"
        
        # Convert predictions to text (explicit phrasing)
        ma_pred_text = "Underdog Cover" if ma_cover else "Favorite Cover"
        mb_pred_text = "Underdog Cover" if mb_cover else "Favorite Cover"
        me_pred_text = "Underdog Cover" if me_cover else "Favorite Cover"
        
        predictions_final.append({
            'game': game,
            'away_team': row['away_team'],
            'home_team': row['home_team'],
            'favorite_team': row['favorite_team'],
            'underdog_team': row['underdog_team'],
            'spread_line': row['spread_line'],
            'total_line': row['total_line'],
            'consensus_prediction': consensus_prediction,
            'consensus_probability': round(consensus_probability, 3),
            'consensus_votes': consensus_votes,
            'agreement': agreement,
            'model_a_prediction': ma_pred_text,
            'model_a_probability': round(ma_prob, 3),
            'model_a_confidence': ma_conf,
            'model_b_prediction': mb_pred_text,
            'model_b_probability': round(mb_prob, 3),
            'model_b_confidence': mb_conf,
            'model_e_prediction': me_pred_text,
            'model_e_probability': round(me_prob, 3),
            'model_e_confidence': me_conf,
            'underdog_votes': underdog_votes,
            'total_votes': total_votes
        })
    
    return pd.DataFrame(predictions_final)

def main():
    """Main function"""
    print("="*80)
    print("WEEK 16 2025 PREDICTIONS FINAL")
    print("="*80)
    
    # Load data
    week16_odds = load_week16_odds()
    if week16_odds is None:
        return
    
    epa_data = load_epa_data()
    if epa_data is None:
        return
    
    # Generate predictions for each model
    print("\n=== Generating Model A Predictions ===")
    model_a = run_model_a(week16_odds, epa_data)
    print(f"✅ Model A: {len(model_a)} predictions")
    
    print("\n=== Generating Model B Predictions ===")
    model_b = run_model_b(week16_odds, epa_data)
    print(f"✅ Model B: {len(model_b)} predictions")
    
    print("\n=== Generating Model E Predictions ===")
    model_e = run_model_e(week16_odds)
    print(f"✅ Model E: {len(model_e)} predictions")
    
    # Save individual model predictions
    os.makedirs("models/model_a", exist_ok=True)
    os.makedirs("models/model_b", exist_ok=True)
    os.makedirs("models/model_e", exist_ok=True)
    
    model_a.to_csv("models/model_a/model_a_week16_predictions.csv", index=False)
    model_b.to_csv("models/model_b/model_b_week16_predictions.csv", index=False)
    model_e.to_csv("models/model_e/model_e_week16_predictions.csv", index=False)
    
    print("\n✅ Saved individual model predictions")
    
    # Create predictions_final
    print("\n=== Creating Predictions Final ===")
    predictions_final = create_predictions_final(week16_odds, model_a, model_b, model_e)
    
    # Save to predictions folder
    os.makedirs("predictions", exist_ok=True)
    output_file = "predictions/week16_predictions_final.csv"
    predictions_final.to_csv(output_file, index=False)
    
    print(f"\n✅ Created {output_file}")
    print(f"   Total games: {len(predictions_final)}")
    
    # Summary
    consensus_covers = (predictions_final['consensus_prediction'] == 'Cover').sum()
    consensus_no_covers = (predictions_final['consensus_prediction'] == 'No Cover').sum()
    
    print(f"   Consensus: {consensus_covers} Cover, {consensus_no_covers} No Cover")
    
    # Agreement breakdown
    print(f"\n=== Agreement Breakdown ===")
    agreement_counts = predictions_final['agreement'].value_counts()
    for agreement, count in agreement_counts.items():
        print(f"   {agreement}: {count} games")
    
    print(f"\n✅ Week 16 predictions final saved to {output_file}")

if __name__ == "__main__":
    main()

