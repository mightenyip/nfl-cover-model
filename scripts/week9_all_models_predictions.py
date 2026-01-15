#!/usr/bin/env python3
"""
Week 9 2025: Run all models with updated comprehensive EPA data
"""

import pandas as pd
import numpy as np
import os
import sys
from datetime import datetime

# Add parent directory to path
sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

def load_comprehensive_epa_data():
    """Load the updated comprehensive EPA data"""
    try:
        epa_file = "data/epa/source/comprehensive_epa_data_week8.csv"
        epa_data = pd.read_csv(epa_file)
        print(f"✅ Loaded comprehensive EPA data: {len(epa_data)} teams")
        return epa_data
    except FileNotFoundError:
        print("❌ Comprehensive EPA data not found, using basic EPA data")
        epa_file = "data/epa/source/sumersports_epa_data.csv"
        epa_data = pd.read_csv(epa_file)
        return epa_data

def get_team_mapping():
    """Map full team names to abbreviations used in EPA data"""
    return {
        'Ravens': 'BAL', 'Dolphins': 'MIA', 'Bears': 'CHI', 'Bengals': 'CIN',
        'Vikings': 'MIN', 'Lions': 'DET', 'Panthers': 'CAR', 'Packers': 'GB',
        'Chargers': 'LAC', 'Titans': 'TEN', 'Falcons': 'ATL', 'Patriots': 'NE',
        '49ers': 'SF', 'Giants': 'NYG', 'Colts': 'IND', 'Steelers': 'PIT',
        'Broncos': 'DEN', 'Texans': 'HOU', 'Jaguars': 'JAX', 'Raiders': 'LV',
        'Saints': 'NO', 'Rams': 'LA', 'Chiefs': 'KC', 'Bills': 'BUF',
        'Seahawks': 'SEA', 'Commanders': 'WAS', 'Cardinals': 'ARI', 'Cowboys': 'DAL'
    }

def run_model_a(week9_odds, epa_data):
    """Model A: SumerSports EPA-based predictions"""
    
    print("\n" + "="*80)
    print("MODEL A: SumerSports EPA Predictions")
    print("="*80)
    
    team_mapping = get_team_mapping()
    predictions = []
    
    for _, game in week9_odds.iterrows():
        away_team = game['away_team']
        home_team = game['home_team']
        favorite = game['favorite_team']
        underdog = game['underdog_team']
        spread = game['spread_line']
        
        # Get EPA data for both teams using team mapping
        away_team_abbr = team_mapping.get(away_team, away_team)
        home_team_abbr = team_mapping.get(home_team, home_team)
        away_epa = epa_data[epa_data['team'] == away_team_abbr]
        home_epa = epa_data[epa_data['team'] == home_team_abbr]
        
        if away_epa.empty or home_epa.empty:
            print(f"⚠️ Missing EPA data for {away_team} @ {home_team}")
            continue
        
        # Calculate net EPA difference
        away_net_epa = away_epa['net_epa_per_play'].iloc[0]
        home_net_epa = home_epa['net_epa_per_play'].iloc[0]
        net_epa_diff = away_net_epa - home_net_epa
        
        # Determine if underdog should cover based on EPA advantage
        if favorite == away_team:
            # Away team is favorite, check if home underdog has EPA advantage
            epa_advantage = home_net_epa - away_net_epa
        else:
            # Home team is favorite, check if away underdog has EPA advantage
            epa_advantage = away_net_epa - home_net_epa
        
        # Prediction logic
        if epa_advantage > 0.1:
            predicted_cover = True
            confidence = "HIGH"
            probability = min(0.75, 0.55 + (epa_advantage * 2))
        elif epa_advantage > 0.05:
            predicted_cover = True
            confidence = "MEDIUM"
            probability = 0.60
        elif epa_advantage < -0.1:
            predicted_cover = False
            confidence = "HIGH"
            probability = min(0.75, 0.55 + (abs(epa_advantage) * 2))
        else:
            predicted_cover = True  # Default to underdog
            confidence = "LOW"
            probability = 0.52
        
        predictions.append({
            'game': f"{away_team} @ {home_team}",
            'favorite': favorite,
            'underdog': underdog,
            'spread': spread,
            'predicted_cover': predicted_cover,
            'confidence': confidence,
            'probability': probability,
            'net_epa_diff': net_epa_diff,
            'epa_advantage': epa_advantage
        })
        
        print(f"{away_team} @ {home_team}: {'Cover' if predicted_cover else 'No Cover'} ({probability:.1%}) - EPA Advantage: {epa_advantage:.3f}")
    
    return pd.DataFrame(predictions)

def run_model_b(week9_odds, epa_data):
    """Model B: Matchup-specific EPA analysis"""
    
    print("\n" + "="*80)
    print("MODEL B: Matchup EPA Analysis")
    print("="*80)
    
    predictions = []
    
    for _, game in week9_odds.iterrows():
        away_team = game['away_team']
        home_team = game['home_team']
        favorite = game['favorite_team']
        underdog = game['underdog_team']
        spread = game['spread_line']
        
        # Get EPA data using team mapping
        team_mapping = get_team_mapping()
        away_team_abbr = team_mapping.get(away_team, away_team)
        home_team_abbr = team_mapping.get(home_team, home_team)
        away_epa = epa_data[epa_data['team'] == away_team_abbr]
        home_epa = epa_data[epa_data['team'] == home_team_abbr]
        
        if away_epa.empty or home_epa.empty:
            continue
        
        # Analyze offensive vs defensive matchups
        if favorite == away_team:
            # Away favorite vs home underdog
            off_epa = away_epa['epa_off_per_play'].iloc[0]
            def_epa_allowed = home_epa['epa_def_allowed_per_play'].iloc[0]
            underdog_off_epa = home_epa['epa_off_per_play'].iloc[0]
            underdog_def_epa = away_epa['epa_def_allowed_per_play'].iloc[0]
        else:
            # Home favorite vs away underdog
            off_epa = home_epa['epa_off_per_play'].iloc[0]
            def_epa_allowed = away_epa['epa_def_allowed_per_play'].iloc[0]
            underdog_off_epa = away_epa['epa_off_per_play'].iloc[0]
            underdog_def_epa = home_epa['epa_def_allowed_per_play'].iloc[0]
        
        # Calculate matchup advantage
        favorite_advantage = off_epa - def_epa_allowed
        underdog_advantage = underdog_off_epa - underdog_def_epa
        
        # Prediction based on matchup analysis
        if underdog_advantage > favorite_advantage + 0.05:
            predicted_cover = True
            confidence = "HIGH"
            probability = 0.65
        elif underdog_advantage > favorite_advantage:
            predicted_cover = True
            confidence = "MEDIUM"
            probability = 0.58
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
            'favorite_advantage': favorite_advantage,
            'underdog_advantage': underdog_advantage
        })
        
        print(f"{away_team} @ {home_team}: {'Cover' if predicted_cover else 'No Cover'} ({probability:.1%}) - Underdog Advantage: {underdog_advantage:.3f}")
    
    return pd.DataFrame(predictions)

def run_model_c_updated(week9_odds):
    """Model C: Updated algorithm with sophisticated rules"""
    
    print("\n" + "="*80)
    print("MODEL C: Updated Algorithm (Sophisticated Rules)")
    print("="*80)
    
    predictions = []
    
    for _, game in week9_odds.iterrows():
        away_team = game['away_team']
        home_team = game['home_team']
        favorite = game['favorite_team']
        underdog = game['underdog_team']
        spread = abs(game['spread_line'])
        total = game['total_line']
        
        predicted_cover = None
        confidence = 'LOW'
        probability = 50.0
        rule_applied = "Default ATS Trend"
        
        # Rule 1: Bet FAVORITE on spread between 1 and 3.5
        if 1.0 <= spread <= 3.5:
            predicted_cover = False  # Favorite covers
            confidence = 'HIGH'
            probability = 65.0
            rule_applied = "Favorite Small Spread Rule (1-3.5)"
        
        # Rule 2: Bet HOME FAVORITE on spreads between 2.5 and 3.5
        elif 2.5 <= spread <= 3.5 and favorite == home_team:
            predicted_cover = False  # Home favorite covers
            confidence = 'HIGH'
            probability = 70.0
            rule_applied = "Home Favorite Spread Rule (2.5-3.5)"
        
        # Rule 3: Bet FAVORITE (spread ≤ 6.5) on games with TOTAL ≥ 46
        elif spread <= 6.5 and total >= 46:
            predicted_cover = False  # Favorite covers
            confidence = 'MEDIUM'
            probability = 60.0
            rule_applied = "High Total + Small Spread Rule"
        
        # Default: Use ATS trends (favor favorites)
        else:
            predicted_cover = False  # Default to favorite covers
            confidence = 'MEDIUM'
            probability = 57.5
            rule_applied = "Default ATS Trend (Favorites 57.5%)"
        
        predictions.append({
            'game': f"{away_team} @ {home_team}",
            'favorite': favorite,
            'underdog': underdog,
            'spread': game['spread_line'],
            'predicted_cover': predicted_cover,
            'confidence': confidence,
            'probability': probability,
            'rule_applied': rule_applied
        })
        
        print(f"{away_team} @ {home_team}: {'Cover' if predicted_cover else 'No Cover'} ({probability:.1%}) - {rule_applied}")
    
    return pd.DataFrame(predictions)

def run_model_d(week9_odds):
    """Model D: Total-based rules"""
    
    print("\n" + "="*80)
    print("MODEL D: Total-Based Rules")
    print("="*80)
    
    predictions = []
    
    for _, game in week9_odds.iterrows():
        away_team = game['away_team']
        home_team = game['home_team']
        favorite = game['favorite_team']
        underdog = game['underdog_team']
        spread = game['spread_line']
        total = game['total_line']
        
        # Total-based prediction logic
        if total >= 50:
            predicted_cover = True  # Underdog covers in high-scoring games
            confidence = "HIGH"
            probability = 0.65
            rule_applied = "High Total Rule (≥50)"
        elif total >= 47:
            predicted_cover = True
            confidence = "MEDIUM"
            probability = 0.58
            rule_applied = "Medium-High Total Rule (47-49)"
        elif total <= 42:
            predicted_cover = False  # Favorite covers in low-scoring games
            confidence = "HIGH"
            probability = 0.65
            rule_applied = "Low Total Rule (≤42)"
        else:
            predicted_cover = True  # Default to underdog
            confidence = "LOW"
            probability = 0.52
            rule_applied = "Default Underdog Rule"
        
        predictions.append({
            'game': f"{away_team} @ {home_team}",
            'favorite': favorite,
            'underdog': underdog,
            'spread': spread,
            'predicted_cover': predicted_cover,
            'confidence': confidence,
            'probability': probability,
            'rule_applied': rule_applied
        })
        
        print(f"{away_team} @ {home_team}: {'Cover' if predicted_cover else 'No Cover'} ({probability:.1%}) - {rule_applied}")
    
    return pd.DataFrame(predictions)

def run_model_e(week9_odds, epa_data):
    """Model E: Advanced EPA metrics (Pass/Rush EPA)"""
    
    print("\n" + "="*80)
    print("MODEL E: Advanced EPA Metrics")
    print("="*80)
    
    predictions = []
    
    for _, game in week9_odds.iterrows():
        away_team = game['away_team']
        home_team = game['home_team']
        favorite = game['favorite_team']
        underdog = game['underdog_team']
        spread = game['spread_line']
        
        # Get EPA data using team mapping
        team_mapping = get_team_mapping()
        away_team_abbr = team_mapping.get(away_team, away_team)
        home_team_abbr = team_mapping.get(home_team, home_team)
        away_epa = epa_data[epa_data['team'] == away_team_abbr]
        home_epa = epa_data[epa_data['team'] == home_team_abbr]
        
        if away_epa.empty or home_epa.empty:
            continue
        
        # Analyze pass vs rush EPA
        if favorite == away_team:
            fav_pass_epa = away_epa['epa_off_per_pass'].iloc[0]
            fav_rush_epa = away_epa['epa_off_per_rush'].iloc[0]
            underdog_pass_epa = home_epa['epa_off_per_pass'].iloc[0]
            underdog_rush_epa = home_epa['epa_off_per_rush'].iloc[0]
        else:
            fav_pass_epa = home_epa['epa_off_per_pass'].iloc[0]
            fav_rush_epa = home_epa['epa_off_per_rush'].iloc[0]
            underdog_pass_epa = away_epa['epa_off_per_pass'].iloc[0]
            underdog_rush_epa = away_epa['epa_off_per_rush'].iloc[0]
        
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
        
        print(f"{away_team} @ {home_team}: {'Cover' if predicted_cover else 'No Cover'} ({probability:.1%}) - Efficiency Diff: {efficiency_diff:.3f}")
    
    return pd.DataFrame(predictions)

def create_consensus_predictions(model_predictions):
    """Create consensus predictions from all models"""
    
    print("\n" + "="*80)
    print("CREATING CONSENSUS PREDICTIONS")
    print("="*80)
    
    # Get all games from the first model
    first_model = list(model_predictions.values())[0]
    consensus_predictions = []
    
    for idx, row in first_model.iterrows():
        game = row['game']
        favorite = row['favorite']
        underdog = row['underdog']
        spread = row['spread']
        
        # Collect predictions from all models
        model_predictions_dict = {}
        model_probabilities = {}
        
        for model_name, model_df in model_predictions.items():
            game_row = model_df[model_df['game'] == game]
            if not game_row.empty:
                model_predictions_dict[model_name] = game_row['predicted_cover'].iloc[0]
                model_probabilities[model_name] = game_row['probability'].iloc[0]
        
        # Calculate consensus
        if model_predictions_dict:
            # Count votes for underdog cover
            underdog_votes = sum(1 for pred in model_predictions_dict.values() if pred)
            total_votes = len(model_predictions_dict)
            
            # Consensus prediction (majority vote)
            consensus_cover = underdog_votes > total_votes / 2
            
            # Average probability (normalize percentages to decimals)
            normalized_probs = []
            for prob in model_probabilities.values():
                if prob > 1.0:  # If it's a percentage, convert to decimal
                    normalized_probs.append(prob / 100.0)
                else:
                    normalized_probs.append(prob)
            avg_probability = np.mean(normalized_probs)
            
            # Agreement level
            agreement = max(underdog_votes, total_votes - underdog_votes) / total_votes
            
            # Confidence based on agreement
            if agreement >= 0.8:
                confidence = "HIGH"
            elif agreement >= 0.6:
                confidence = "MEDIUM"
            else:
                confidence = "LOW"
            
            # Model breakdown
            model_breakdown = {}
            for model_name, pred in model_predictions_dict.items():
                model_breakdown[model_name] = "Cover" if pred else "No Cover"
            
            # Get individual model probabilities and predictions
            model_a_prob = model_probabilities.get('Model_A', 0.0)
            model_b_prob = model_probabilities.get('Model_B', 0.0)
            model_c_prob = model_probabilities.get('Model_C', 0.0)
            model_d_prob = model_probabilities.get('Model_D', 0.0)
            model_e_prob = model_probabilities.get('Model_E', 0.0)
            
            # Get individual model predictions
            model_a_pred = model_predictions_dict.get('Model_A', False)
            model_b_pred = model_predictions_dict.get('Model_B', False)
            model_c_pred = model_predictions_dict.get('Model_C', False)
            model_d_pred = model_predictions_dict.get('Model_D', False)
            model_e_pred = model_predictions_dict.get('Model_E', False)
            
            # Normalize Model C probability if it's a percentage
            if model_c_prob > 1.0:
                model_c_prob = model_c_prob / 100.0
            
            consensus_predictions.append({
                'game': game,
                'favorite': favorite,
                'underdog': underdog,
                'spread': spread,
                'consensus_prediction': "Cover" if consensus_cover else "No Cover",
                'consensus_probability': avg_probability,
                'model_a_prediction': "Cover" if model_a_pred else "No Cover",
                'model_a_probability': model_a_prob,
                'model_b_prediction': "Cover" if model_b_pred else "No Cover",
                'model_b_probability': model_b_prob,
                'model_c_prediction': "Cover" if model_c_pred else "No Cover",
                'model_c_probability': model_c_prob,
                'model_d_prediction': "Cover" if model_d_pred else "No Cover",
                'model_d_probability': model_d_prob,
                'model_e_prediction': "Cover" if model_e_pred else "No Cover",
                'model_e_probability': model_e_prob,
                'confidence': confidence,
                'agreement': agreement,
                'underdog_votes': underdog_votes,
                'total_votes': total_votes,
                'model_breakdown': str(model_breakdown)
            })
            
            print(f"{game}:")
            print(f"  Consensus: {'Cover' if consensus_cover else 'No Cover'} ({avg_probability:.1%})")
            print(f"  Agreement: {agreement:.1%} ({confidence})")
            print(f"  Votes: {underdog_votes}/{total_votes} for underdog")
            print(f"  Models: {model_breakdown}")
            print()
    
    return consensus_predictions

def main():
    """Run all models for Week 9"""
    
    print("="*80)
    print("WEEK 9 2025: ALL MODELS PREDICTIONS")
    print("Using Updated Comprehensive EPA Data")
    print("="*80)
    
    # Load Week 9 odds
    week9_odds = pd.read_csv("schedule/week9_2025_odds.csv")
    print(f"\nLoaded {len(week9_odds)} games for Week 9")
    
    # Load comprehensive EPA data
    epa_data = load_comprehensive_epa_data()
    
    # Run all models
    print("\n" + "="*80)
    print("RUNNING ALL MODELS")
    print("="*80)
    
    model_a_preds = run_model_a(week9_odds, epa_data)
    model_b_preds = run_model_b(week9_odds, epa_data)
    model_c_preds = run_model_c_updated(week9_odds)
    model_d_preds = run_model_d(week9_odds)
    model_e_preds = run_model_e(week9_odds, epa_data)
    
    # Save individual model predictions
    model_predictions = {
        'Model_A': model_a_preds,
        'Model_B': model_b_preds,
        'Model_C': model_c_preds,
        'Model_D': model_d_preds,
        'Model_E': model_e_preds
    }
    
    # Save individual model files
    for model_name, preds in model_predictions.items():
        output_file = f"predictions/{model_name.lower()}_week9_predictions.csv"
        preds.to_csv(output_file, index=False)
        print(f"✅ Saved {model_name} predictions to {output_file}")
    
    # Create consensus predictions
    consensus = create_consensus_predictions(model_predictions)
    
    # Save consensus predictions
    consensus_df = pd.DataFrame(consensus)
    consensus_output = "predictions/week9_consensus_predictions.csv"
    consensus_df.to_csv(consensus_output, index=False)
    
    # Create final predictions file
    final_predictions = []
    for pred in consensus:
        final_predictions.append({
            'game': pred['game'],
            'favorite': pred['favorite'],
            'underdog': pred['underdog'],
            'spread': pred['spread'],
            'consensus_prediction': pred['consensus_prediction'],
            'consensus_probability': pred['consensus_probability'],
            'model_a_prediction': pred['model_a_prediction'],
            'model_a_probability': pred['model_a_probability'],
            'model_b_prediction': pred['model_b_prediction'],
            'model_b_probability': pred['model_b_probability'],
            'model_c_prediction': pred['model_c_prediction'],
            'model_c_probability': pred['model_c_probability'],
            'model_d_prediction': pred['model_d_prediction'],
            'model_d_probability': pred['model_d_probability'],
            'model_e_prediction': pred['model_e_prediction'],
            'model_e_probability': pred['model_e_probability'],
            'confidence': pred['confidence'],
            'agreement': pred['agreement'],
            'underdog_votes': pred['underdog_votes'],
            'total_votes': pred['total_votes'],
            'model_breakdown': pred['model_breakdown']
        })
    
    final_df = pd.DataFrame(final_predictions)
    final_output = "predictions/week9_predictions_final.csv"
    final_df.to_csv(final_output, index=False)
    
    # Summary
    total_games = len(consensus)
    underdog_covers = sum(1 for p in consensus if p['consensus_prediction'] == 'Cover')
    favorite_covers = total_games - underdog_covers
    
    print(f"\n" + "="*80)
    print("WEEK 9 PREDICTIONS SUMMARY")
    print("="*80)
    print(f"Total games: {total_games}")
    print(f"Underdog covers predicted: {underdog_covers}")
    print(f"Favorite covers predicted: {favorite_covers}")
    print(f"Average consensus probability: {np.mean([p['consensus_probability'] for p in consensus]):.1%}")
    
    # Confidence distribution
    confidence_counts = {}
    for p in consensus:
        conf = p['confidence']
        confidence_counts[conf] = confidence_counts.get(conf, 0) + 1
    
    print(f"\nConsensus Confidence Distribution:")
    for conf in ['HIGH', 'MEDIUM', 'LOW']:
        count = confidence_counts.get(conf, 0)
        print(f"  {conf}: {count} games")
    
    print(f"\n✅ Week 9 predictions saved to:")
    print(f"  - {consensus_output}")
    print(f"  - {final_output}")
    print(f"  - Individual model files in predictions/")

if __name__ == "__main__":
    main()
