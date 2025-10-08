#!/usr/bin/env python3
"""
Week 6 2025: Run all 4 models and compile predictions
"""

import pandas as pd
import numpy as np
import os
import sys

# Add parent directory to path
sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

def load_epa_data():
    """Load the updated EPA data"""
    # Use the corrected detailed EPA data
    epa_file = "../detailed_epa_data.csv"
    epa_data = pd.read_csv(epa_file)
    return epa_data

def get_team_mapping():
    """Map full team names to abbreviations"""
    return {
        '49ers': 'SF', 'Bears': 'CHI', 'Bengals': 'CIN', 'Bills': 'BUF', 'Broncos': 'DEN',
        'Browns': 'CLE', 'Buccaneers': 'TB', 'Cardinals': 'ARI', 'Chargers': 'LAC', 'Chiefs': 'KC',
        'Colts': 'IND', 'Commanders': 'WAS', 'Cowboys': 'DAL', 'Dolphins': 'MIA', 'Eagles': 'PHI',
        'Falcons': 'ATL', 'Giants': 'NYG', 'Jaguars': 'JAX', 'Jets': 'NYJ', 'Lions': 'DET',
        'Packers': 'GB', 'Panthers': 'CAR', 'Patriots': 'NE', 'Raiders': 'LV', 'Rams': 'LA',
        'Ravens': 'BAL', 'Saints': 'NO', 'Seahawks': 'SEA', 'Steelers': 'PIT', 'Texans': 'HOU',
        'Titans': 'TEN', 'Vikings': 'MIN'
    }

def run_model_a(week6_odds, epa_data):
    """Model A: SumerSports EPA-based predictions"""
    
    print("\n" + "="*80)
    print("MODEL A: SumerSports EPA Predictions")
    print("="*80)
    
    team_mapping = get_team_mapping()
    predictions = []
    
    for _, game in week6_odds.iterrows():
        underdog = game['underdog_team']
        favorite = game['favorite_team']
        spread = abs(game['spread_line'])
        
        # Convert to abbreviations
        underdog_abbr = team_mapping.get(underdog, underdog)
        favorite_abbr = team_mapping.get(favorite, favorite)
        
        # Get EPA data
        underdog_data = epa_data[epa_data['team'] == underdog_abbr]
        favorite_data = epa_data[epa_data['team'] == favorite_abbr]
        
        if len(underdog_data) == 0 or len(favorite_data) == 0:
            print(f"⚠️  Missing EPA data for {underdog} ({underdog_abbr}) or {favorite} ({favorite_abbr})")
            continue
        
        underdog_epa_off = underdog_data['epa_off_per_play'].iloc[0]
        underdog_epa_def = underdog_data['epa_def_allowed_per_play'].iloc[0]
        favorite_epa_off = favorite_data['epa_off_per_play'].iloc[0]
        favorite_epa_def = favorite_data['epa_def_allowed_per_play'].iloc[0]
        
        underdog_net = underdog_epa_off - underdog_epa_def
        favorite_net = favorite_epa_off - favorite_epa_def
        
        # Model A logic
        cover_prob = 0.50
        
        # Defense quality (favorite's defense)
        if favorite_epa_def < -0.05:  # Strong defense
            cover_prob += 0.12
        elif favorite_epa_def > 0.10:  # Weak defense
            cover_prob -= 0.10
        else:  # Average
            cover_prob += 0.02
        
        # Net EPA differential
        net_diff = underdog_net - favorite_net
        if net_diff > 0.10:
            cover_prob += 0.15
        elif net_diff > 0:
            cover_prob += 0.08
        elif net_diff > -0.10:
            cover_prob -= 0.05
        else:
            cover_prob -= 0.15
        
        # Spread adjustment
        if spread >= 10:
            cover_prob += 0.15
        elif spread >= 7:
            cover_prob += 0.10
        elif spread >= 3:
            cover_prob += 0.05
        
        # Home/away adjustment (underdog is away)
        is_underdog_away = game['away_team'] == underdog
        if not is_underdog_away:  # Underdog at home
            cover_prob += 0.08
        
        # Clamp probability
        cover_prob = max(0.05, min(0.95, cover_prob))
        
        # Determine prediction and confidence
        if cover_prob >= 0.65:
            pred = "Cover"
            conf = "HIGH"
        elif cover_prob >= 0.55:
            pred = "Cover"
            conf = "MEDIUM"
        elif cover_prob >= 0.45:
            pred = "No Cover"
            conf = "LOW"
        elif cover_prob >= 0.35:
            pred = "No Cover"
            conf = "MEDIUM"
        else:
            pred = "No Cover"
            conf = "HIGH"
        
        predictions.append({
            'Game': f"{game['away_team']} @ {game['home_team']}",
            'Favorite': favorite,
            'Underdog': underdog,
            'Spread': spread,
            'Model_A_Pred': pred,
            'Model_A_Conf': conf,
            'Model_A_Prob': f"{cover_prob*100:.1f}%"
        })
    
    return pd.DataFrame(predictions)

def run_model_b(week6_odds, epa_data):
    """Model B: Matchup-specific EPA (pass/rush) predictions"""
    
    print("\n" + "="*80)
    print("MODEL B: Matchup-Specific EPA Predictions")
    print("="*80)
    
    team_mapping = get_team_mapping()
    predictions = []
    
    for _, game in week6_odds.iterrows():
        underdog = game['underdog_team']
        favorite = game['favorite_team']
        spread = abs(game['spread_line'])
        
        # Convert to abbreviations
        underdog_abbr = team_mapping.get(underdog, underdog)
        favorite_abbr = team_mapping.get(favorite, favorite)
        
        # Get EPA data
        underdog_data = epa_data[epa_data['team'] == underdog_abbr]
        favorite_data = epa_data[epa_data['team'] == favorite_abbr]
        
        if len(underdog_data) == 0 or len(favorite_data) == 0:
            continue
        
        # Pass matchup
        underdog_pass_off = underdog_data['epa_pass_off'].iloc[0]
        favorite_pass_def = favorite_data['epa_pass_def_allowed'].iloc[0]
        pass_matchup = underdog_pass_off - favorite_pass_def
        
        # Rush matchup
        underdog_rush_off = underdog_data['epa_rush_off'].iloc[0]
        favorite_rush_def = favorite_data['epa_rush_def_allowed'].iloc[0]
        rush_matchup = underdog_rush_off - favorite_rush_def
        
        # Combined matchup (weighted: 60% pass, 40% rush)
        combined_matchup = (pass_matchup * 0.6) + (rush_matchup * 0.4)
        
        # Model B logic
        cover_prob = 0.50
        
        # Matchup-based adjustments
        if combined_matchup > 0.25:
            cover_prob += 0.25
        elif combined_matchup > 0.15:
            cover_prob += 0.18
        elif combined_matchup > 0.05:
            cover_prob += 0.10
        elif combined_matchup < -0.15:
            cover_prob -= 0.20
        elif combined_matchup < -0.05:
            cover_prob -= 0.12
        
        # Spread adjustment
        if spread >= 10:
            cover_prob += 0.20
        elif spread >= 7:
            cover_prob += 0.15
        elif spread >= 3:
            cover_prob += 0.08
        
        # Clamp
        cover_prob = max(0.05, min(0.95, cover_prob))
        
        # Determine prediction and confidence
        if cover_prob >= 0.80:
            pred = "Cover"
            conf = "VERY_HIGH"
        elif cover_prob >= 0.65:
            pred = "Cover"
            conf = "HIGH"
        elif cover_prob >= 0.55:
            pred = "Cover"
            conf = "MEDIUM"
        elif cover_prob >= 0.45:
            pred = "No Cover"
            conf = "LOW"
        elif cover_prob >= 0.30:
            pred = "No Cover"
            conf = "MEDIUM"
        else:
            pred = "No Cover"
            conf = "VERY_HIGH"
        
        predictions.append({
            'Game': f"{game['away_team']} @ {game['home_team']}",
            'Model_B_Pred': pred,
            'Model_B_Conf': conf,
            'Model_B_Prob': f"{cover_prob*100:.1f}%"
        })
    
    return pd.DataFrame(predictions)

def run_model_c(week6_odds):
    """Model C: Spread-based rules"""
    
    print("\n" + "="*80)
    print("MODEL C: Spread-Based Rules Predictions")
    print("="*80)
    
    predictions = []
    
    for _, game in week6_odds.iterrows():
        spread = abs(game['spread_line'])
        
        # Model C logic: Simple spread-based rules
        if spread >= 10:
            pred = "No Cover"
            conf = "MEDIUM"
            prob = 55.0
        elif spread >= 7:
            pred = "No Cover"
            conf = "MEDIUM"
            prob = 55.0
        elif spread >= 3.5:
            pred = "No Cover"
            conf = "HIGH"
            prob = 60.0
        else:
            pred = "No Cover"
            conf = "MEDIUM"
            prob = 53.8
        
        predictions.append({
            'Game': f"{game['away_team']} @ {game['home_team']}",
            'Model_C_Pred': pred,
            'Model_C_Conf': conf,
            'Model_C_Prob': f"{prob:.1f}%"
        })
    
    return pd.DataFrame(predictions)

def run_model_d(week6_odds):
    """Model D: Total-based rules"""
    
    print("\n" + "="*80)
    print("MODEL D: Total-Based Rules Predictions")
    print("="*80)
    
    predictions = []
    
    for _, game in week6_odds.iterrows():
        spread = abs(game['spread_line'])
        total = game['total_line']
        
        # Model D logic: Considers both spread and total
        cover_prob = 0.50
        
        if spread >= 7:
            pred = "Cover"
            conf = "HIGH" if spread >= 10 else "HIGH"
        elif spread >= 3.5:
            pred = "Cover"
            conf = "HIGH"
        elif spread < 3:
            pred = "No Cover"
            conf = "HIGH"
        else:
            pred = "Cover"
            conf = "LOW"
        
        predictions.append({
            'Game': f"{game['away_team']} @ {game['home_team']}",
            'Model_D_Pred': pred,
            'Model_D_Conf': conf
        })
    
    return pd.DataFrame(predictions)

def main():
    """Run all models for Week 6"""
    
    print("="*80)
    print("WEEK 6 2025: ALL MODELS PREDICTIONS")
    print("="*80)
    
    # Load Week 6 odds
    week6_odds = pd.read_csv("../schedule/week6_2025_odds.csv")
    print(f"\nLoaded {len(week6_odds)} games for Week 6")
    
    # Load EPA data
    epa_data = load_epa_data()
    print(f"Loaded EPA data for {len(epa_data)} teams (updated Oct 7, 2025)")
    
    # Run all models
    model_a_preds = run_model_a(week6_odds, epa_data)
    model_b_preds = run_model_b(week6_odds, epa_data)
    model_c_preds = run_model_c(week6_odds)
    model_d_preds = run_model_d(week6_odds)
    
    # Merge all predictions
    all_preds = model_a_preds.copy()
    all_preds = all_preds.merge(model_b_preds, on='Game', how='left')
    all_preds = all_preds.merge(model_c_preds, on='Game', how='left')
    all_preds = all_preds.merge(model_d_preds, on='Game', how='left')
    
    # Add Total to display
    all_preds['Total'] = week6_odds['total_line'].values[:len(all_preds)]
    
    # Reorder columns
    cols = ['Game', 'Favorite', 'Underdog', 'Spread', 'Total',
            'Model_A_Pred', 'Model_A_Conf', 'Model_A_Prob',
            'Model_B_Pred', 'Model_B_Conf', 'Model_B_Prob',
            'Model_C_Pred', 'Model_C_Conf', 'Model_C_Prob',
            'Model_D_Pred', 'Model_D_Conf']
    all_preds = all_preds[cols]
    
    # Save to CSV
    output_file = "week6_all_models_predictions.csv"
    all_preds.to_csv(output_file, index=False)
    print(f"\n✅ Saved all predictions to {output_file}")
    
    # Display summary
    print("\n" + "="*80)
    print("PREDICTIONS SUMMARY")
    print("="*80)
    
    for _, row in all_preds.iterrows():
        print(f"\n{row['Game']}")
        print(f"  Spread: {row['Favorite']} -{row['Spread']} | Total: {row['Total']}")
        print(f"  Model A: {row['Model_A_Pred']} ({row['Model_A_Conf']}, {row['Model_A_Prob']})")
        print(f"  Model B: {row['Model_B_Pred']} ({row['Model_B_Conf']}, {row['Model_B_Prob']})")
        print(f"  Model C: {row['Model_C_Pred']} ({row['Model_C_Conf']}, {row['Model_C_Prob']})")
        print(f"  Model D: {row['Model_D_Pred']} ({row['Model_D_Conf']})")
        
        # Show agreement
        preds = [row['Model_A_Pred'], row['Model_B_Pred'], row['Model_C_Pred'], row['Model_D_Pred']]
        cover_count = preds.count('Cover')
        if cover_count == 4:
            print(f"  ⭐ ALL 4 MODELS AGREE: Cover")
        elif cover_count == 0:
            print(f"  ⭐ ALL 4 MODELS AGREE: No Cover")
        elif cover_count == 3:
            print(f"  ✓ 3 models say Cover")
        elif cover_count == 1:
            print(f"  ✓ 3 models say No Cover")
    
    return all_preds

if __name__ == "__main__":
    main()

