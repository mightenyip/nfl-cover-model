#!/usr/bin/env python3
"""
Model E Week 12 Predictions
Generate Model E predictions for Week 12 using additive EPA framework
"""

import pandas as pd
import numpy as np
from datetime import datetime

def load_epa_data():
    """Load the Week 12 EPA data"""
    try:
        epa_df = pd.read_csv("data/Week11_EPA.csv")
        print(f"Loaded EPA data for {len(epa_df)} teams")
        return epa_df
    except FileNotFoundError:
        print("❌ Error: data/Week11_EPA.csv not found")
        return None

def load_week12_odds():
    """Load Week 12 odds"""
    try:
        odds_df = pd.read_csv("schedule/week12_2025_odds.csv")
        print(f"Loaded {len(odds_df)} games from Week 12 odds")
        return odds_df
    except FileNotFoundError:
        print("❌ Error: schedule/week12_2025_odds.csv not found")
        return None

def calculate_model_e_predictions(epa_df, odds_df):
    """Calculate Model E predictions for Week 12 using additive EPA framework"""
    
    print("\n=== Model E Week 12 Predictions ===")
    print("Using additive EPA framework: Offensive EPA + Defensive EPA Allowed = Expected Performance")
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
        total_line = row['total_line']
        
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
        
        # Extract EPA metrics
        underdog_metrics = {
            'epa_pass_off': away_epa['epa_pass_off'].iloc[0] if away_abbr == dog_abbr else home_epa['epa_pass_off'].iloc[0],
            'epa_rush_off': away_epa['epa_rush_off'].iloc[0] if away_abbr == dog_abbr else home_epa['epa_rush_off'].iloc[0],
            'epa_pass_def': away_epa['epa_pass_def_allowed'].iloc[0] if away_abbr == dog_abbr else home_epa['epa_pass_def_allowed'].iloc[0],
            'epa_rush_def': away_epa['epa_rush_def_allowed'].iloc[0] if away_abbr == dog_abbr else home_epa['epa_rush_def_allowed'].iloc[0]
        }
        
        favorite_metrics = {
            'epa_pass_off': away_epa['epa_pass_off'].iloc[0] if away_abbr == fav_abbr else home_epa['epa_pass_off'].iloc[0],
            'epa_rush_off': away_epa['epa_rush_off'].iloc[0] if away_abbr == fav_abbr else home_epa['epa_rush_off'].iloc[0],
            'epa_pass_def': away_epa['epa_pass_def_allowed'].iloc[0] if away_abbr == fav_abbr else home_epa['epa_pass_def_allowed'].iloc[0],
            'epa_rush_def': away_epa['epa_rush_def_allowed'].iloc[0] if away_abbr == fav_abbr else home_epa['epa_rush_def_allowed'].iloc[0]
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
        
        # Spread adjustment: Larger spreads favor underdogs (more points = easier to cover)
        # But adjustment should be modest - spreads are already priced in by bookmakers
        spread_adjustment = abs(spread) * 0.003  # Each point adds ~0.3% to underdog cover probability
        cover_probability += spread_adjustment
        
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
        
        # Create game description
        game_desc = f"{away_team} @ {home_team}"
        if favorite == away_team:
            spread_desc = f"{favorite} {spread}"
        else:
            spread_desc = f"{underdog} +{abs(spread)}"
        
        prediction_text = "Cover" if predicted_cover else "No Cover"
        
        print(f"{game_desc}: {spread_desc}")
        print(f"  Expected Performance:")
        print(f"    Underdog: Pass {underdog_expected_pass:.3f}, Rush {underdog_expected_rush:.3f}, Total {underdog_expected_total:.3f}")
        print(f"    Favorite: Pass {favorite_expected_pass:.3f}, Rush {favorite_expected_rush:.3f}, Total {favorite_expected_total:.3f}")
        print(f"  Total Advantage: {total_advantage:.3f}")
        print(f"  Cover Probability: {cover_probability:.1%} ({confidence})")
        print(f"  Prediction: {prediction_text}")
        print()
        
        predictions.append({
            'game': game_desc,
            'favorite': favorite,
            'underdog': underdog,
            'spread': spread,
            'total_line': total_line,
            'spread_description': spread_desc,
            'underdog_expected_pass': underdog_expected_pass,
            'underdog_expected_rush': underdog_expected_rush,
            'underdog_expected_total': underdog_expected_total,
            'favorite_expected_pass': favorite_expected_pass,
            'favorite_expected_rush': favorite_expected_rush,
            'favorite_expected_total': favorite_expected_total,
            'pass_advantage': pass_advantage,
            'rush_advantage': rush_advantage,
            'total_advantage': total_advantage,
            'cover_probability': cover_probability,
            'confidence': confidence,
            'predicted_cover': predicted_cover,
            'prediction': prediction_text,
            'outright_win_probability': outright_win_probability,
            'outright_confidence': outright_confidence,
            'predicted_outright_win': predicted_outright_win
        })
    
    return predictions

def main():
    """Main function"""
    print("=== Model E Week 12 Predictions ===")
    print("Generating predictions using additive EPA framework")
    print("=" * 60)
    
    # Load data
    epa_df = load_epa_data()
    if epa_df is None:
        return
    
    odds_df = load_week12_odds()
    if odds_df is None:
        return
    
    # Generate predictions
    predictions = calculate_model_e_predictions(epa_df, odds_df)
    
    # Save predictions
    predictions_df = pd.DataFrame(predictions)
    output_file = "models/model_e/model_e_week12_week11epa_predictions.csv"
    predictions_df.to_csv(output_file, index=False)
    
    # Summary
    total_games = len(predictions)
    underdog_covers = sum(1 for p in predictions if p['predicted_cover'])
    favorite_covers = total_games - underdog_covers
    
    print(f"=== Model E Week 12 Summary ===")
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
    for conf in ['VERY_HIGH', 'HIGH', 'MEDIUM', 'LOW']:
        count = confidence_counts.get(conf, 0)
        print(f"  {conf}: {count} games")
    
    print(f"\n✅ Model E Week 12 predictions saved to {output_file}")

if __name__ == "__main__":
    main()

