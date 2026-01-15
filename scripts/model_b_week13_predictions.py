#!/usr/bin/env python3
"""
Model B Week 13 Predictions
Generate Model B predictions for Week 13 using Week13 EPA data
"""

import pandas as pd
import numpy as np
from datetime import datetime

def load_epa_data():
    """Load the Week 13 EPA data"""
    try:
        epa_df = pd.read_csv("data/epa/week13/Week13_EPA.csv")
        print(f"Loaded EPA data for {len(epa_df)} teams")
        return epa_df
    except FileNotFoundError:
        print("❌ Error: data/epa/week13/Week13_EPA.csv not found")
        return None

def load_week13_odds():
    """Load Week 13 odds"""
    try:
        odds_df = pd.read_csv("schedule/week13_2025_odds.csv")
        print(f"Loaded {len(odds_df)} games from Week 13 odds")
        return odds_df
    except FileNotFoundError:
        print("❌ Error: schedule/week13_2025_odds.csv not found")
        return None

def calculate_model_b_predictions(epa_df, odds_df):
    """Calculate Model B predictions for Week 13"""
    
    print("\n=== Model B Week 13 Predictions ===")
    print("Using Week 13 EPA data and 5-tier defense classification")
    print("=" * 60)
    
    # Team name mapping
    team_mapping = {
        '49ers': 'SF', 'Bears': 'CHI', 'Bengals': 'CIN', 'Bills': 'BUF', 'Broncos': 'DEN',
        'Browns': 'CLE', 'Buccaneers': 'TB', 'Cardinals': 'ARI', 'Chargers': 'LAC', 'Chiefs': 'KC',
        'Colts': 'IND', 'Commanders': 'WAS', 'Cowboys': 'DAL', 'Dolphins': 'MIA', 'Eagles': 'PHI',
        'Falcons': 'ATL', 'Giants': 'NYG', 'Jaguars': 'JAX', 'Jets': 'NYJ', 'Lions': 'DET',
        'Packers': 'GB', 'Panthers': 'CAR', 'Patriots': 'NE', 'Raiders': 'LV', 'Rams': 'LA',
        'Ravens': 'BAL', 'Saints': 'NO', 'Seahawks': 'SEA', 'Steelers': 'PIT', 'Texans': 'HOU',
        'Titans': 'TEN', 'Vikings': 'MIN'
    }
    
    predictions = []
    
    for idx, row in odds_df.iterrows():
        away_team = row['away_team']
        home_team = row['home_team']
        favorite = row['favorite_team']
        underdog = row['underdog_team']
        spread = row['spread_line']
        
        # Get team abbreviations
        away_abbr = team_mapping.get(away_team, away_team)
        home_abbr = team_mapping.get(home_team, home_team)
        fav_abbr = team_mapping.get(favorite, favorite)
        dog_abbr = team_mapping.get(underdog, underdog)
        
        # Get EPA data for both teams
        away_epa = epa_df[epa_df['team'] == away_abbr]
        home_epa = epa_df[epa_df['team'] == home_abbr]
        
        if away_epa.empty or home_epa.empty:
            print(f"⚠️ Missing EPA data for {away_team} ({away_abbr}) or {home_team} ({home_abbr})")
            continue
        
        # Extract EPA values
        away_off_epa = away_epa['epa_off_per_play'].iloc[0]
        away_def_epa = away_epa['epa_def_allowed_per_play'].iloc[0]
        home_off_epa = home_epa['epa_off_per_play'].iloc[0]
        home_def_epa = home_epa['epa_def_allowed_per_play'].iloc[0]
        
        # Calculate net EPA difference
        away_net_epa = away_off_epa - away_def_epa
        home_net_epa = home_off_epa - home_def_epa
#!/usr/bin/env python3
"""
Model B Week 13 Predictions
Generate Model B predictions for Week 13 using Week13 EPA data
"""

import pandas as pd
import numpy as np
from datetime import datetime

def load_epa_data():
    """Load the Week 13 EPA data"""
    try:
        epa_df = pd.read_csv("data/epa/week13/Week13_EPA.csv")
        print(f"Loaded EPA data for {len(epa_df)} teams")
        return epa_df
    except FileNotFoundError:
        print("❌ Error: data/epa/week13/Week13_EPA.csv not found")
        return None

def load_week13_odds():
    """Load Week 13 odds"""
    try:
        odds_df = pd.read_csv("schedule/week13_2025_odds.csv")
        print(f"Loaded {len(odds_df)} games from Week 13 odds")
        return odds_df
    except FileNotFoundError:
        print("❌ Error: schedule/week13_2025_odds.csv not found")
        return None

def calculate_model_b_predictions(epa_df, odds_df):
    """Calculate Model B predictions for Week 13"""
    
    print("\n=== Model B Week 13 Predictions ===")
    print("Using Week 13 EPA data and 5-tier defense classification")
    print("=" * 60)
    
    # Team name mapping
    team_mapping = {
        '49ers': 'SF', 'Bears': 'CHI', 'Bengals': 'CIN', 'Bills': 'BUF', 'Broncos': 'DEN',
        'Browns': 'CLE', 'Buccaneers': 'TB', 'Cardinals': 'ARI', 'Chargers': 'LAC', 'Chiefs': 'KC',
        'Colts': 'IND', 'Commanders': 'WAS', 'Cowboys': 'DAL', 'Dolphins': 'MIA', 'Eagles': 'PHI',
        'Falcons': 'ATL', 'Giants': 'NYG', 'Jaguars': 'JAX', 'Jets': 'NYJ', 'Lions': 'DET',
        'Packers': 'GB', 'Panthers': 'CAR', 'Patriots': 'NE', 'Raiders': 'LV', 'Rams': 'LA',
        'Ravens': 'BAL', 'Saints': 'NO', 'Seahawks': 'SEA', 'Steelers': 'PIT', 'Texans': 'HOU',
        'Titans': 'TEN', 'Vikings': 'MIN'
    }
    
    predictions = []
    
    for idx, row in odds_df.iterrows():
        away_team = row['away_team']
        home_team = row['home_team']
        favorite = row['favorite_team']
        underdog = row['underdog_team']
        spread = row['spread_line']
        
        # Get team abbreviations
        away_abbr = team_mapping.get(away_team, away_team)
        home_abbr = team_mapping.get(home_team, home_team)
        fav_abbr = team_mapping.get(favorite, favorite)
        dog_abbr = team_mapping.get(underdog, underdog)
        
        # Get EPA data for both teams
        away_epa = epa_df[epa_df['team'] == away_abbr]
        home_epa = epa_df[epa_df['team'] == home_abbr]
        
        if away_epa.empty or home_epa.empty:
            print(f"⚠️ Missing EPA data for {away_team} ({away_abbr}) or {home_team} ({home_abbr})")
            continue
        
        # Extract EPA values
        away_off_epa = away_epa['epa_off_per_play'].iloc[0]
        away_def_epa = away_epa['epa_def_allowed_per_play'].iloc[0]
        home_off_epa = home_epa['epa_off_per_play'].iloc[0]
        home_def_epa = home_epa['epa_def_allowed_per_play'].iloc[0]
        
        # Calculate net EPA difference
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
        
        # Determine opponent defense quality (Model B's 5-tier system)
        if favorite == away_team:
            opponent_def_epa = home_def_epa
        else:
            opponent_def_epa = away_def_epa
        
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
        
        # Model B methodology: Defense-focused approach
        base_prob = 0.5
        
        # EPA adjustment (smaller than Model A)
        epa_adjustment = net_epa_diff * 0.2
        
        # Defense quality adjustment (Model B's key factor)
        def_adjustment = (def_multiplier - 1.0) * 0.15
        
        # Spread size adjustment: Larger spreads favor underdogs (more points = easier to cover)
        # But adjustment should be modest - spreads are already priced in by bookmakers
        spread_adjustment = abs(spread) * 0.003  # Each point adds ~0.3% to underdog cover probability
        spread_adjustment = min(spread_adjustment, 0.05)  # Cap at 5%
        
        # Calculate final probability
        cover_prob = base_prob + epa_adjustment + def_adjustment + spread_adjustment
        cover_prob = max(0.1, min(0.9, cover_prob))  # Clamp between 10% and 90%
        
        # Determine prediction
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
        
        # Create game description
        game_desc = f"{away_team} @ {home_team}"
        if favorite == away_team:
            spread_desc = f"{favorite} {spread}"
        else:
            spread_desc = f"{underdog} +{abs(spread)}"
        
        prediction_text = "Cover" if predicted_cover else "No Cover"
        
        print(f"{game_desc}: {spread_desc}")
        print(f"  Cover Probability: {cover_prob:.1%} ({confidence})")
        print(f"  Defense Quality: {defense_quality} ({opponent_def_epa:.3f})")
        print(f"  Net EPA Diff: {net_epa_diff:.3f}")
        print(f"  Prediction: {prediction_text}")
        print()
        
        predictions.append({
            'game': game_desc,
            'away_team': away_team,
            'home_team': home_team,
            'favorite': favorite,
            'underdog': underdog,
            'spread': spread,
            'spread_description': spread_desc,
            'cover_probability': cover_prob,
            'confidence': confidence,
            'defense_quality': defense_quality,
            'opponent_def_epa': opponent_def_epa,
            'net_epa_diff': net_epa_diff,
            'predicted_cover': predicted_cover,
            'prediction': prediction_text
        })
    
    return predictions

def main():
    """Main function"""
    print("=== Model B Week 13 Predictions ===")
    print("Generating predictions using Week 13 EPA data")
    print("=" * 60)
    
    # Load data
    epa_df = load_epa_data()
    if epa_df is None:
        return
    
    odds_df = load_week13_odds()
    if odds_df is None:
        return
    
    # Generate predictions
    predictions = calculate_model_b_predictions(epa_df, odds_df)
    
    # Save predictions
    predictions_df = pd.DataFrame(predictions)
    output_file = "models/model_b/model_b_week13_predictions.csv"
    predictions_df.to_csv(output_file, index=False)
    
    # Summary
    total_games = len(predictions)
    underdog_covers = sum(1 for p in predictions if p['predicted_cover'])
    favorite_covers = total_games - underdog_covers
    
    print(f"=== Model B Week 13 Summary ===")
    print(f"Total games: {total_games}")
    print(f"Underdog covers predicted: {underdog_covers}")
    print(f"Favorite covers predicted: {favorite_covers}")
    print(f"Average cover probability: {np.mean([p['cover_probability'] for p in predictions]):.1%}")
    
    # Confidence distribution
    confidence_counts = {}
    for p in predictions:
        conf = p['confidence']
        confidence_counts[conf] = confidence_counts.get(conf, 0) + 1
    
    print(f"\nConfidence Distribution:")
    for conf in ['HIGH', 'MEDIUM', 'LOW']:
        count = confidence_counts.get(conf, 0)
        print(f"  {conf}: {count} games")
    
    print(f"\n✅ Model B Week 13 predictions saved to {output_file}")

if __name__ == "__main__":
    main()

