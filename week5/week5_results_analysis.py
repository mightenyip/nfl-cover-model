#!/usr/bin/env python3
"""
Analyze Week 5 2024 NFL Results and Model Performance
"""

import pandas as pd
import numpy as np
import os
import sys

def load_play_by_play_data():
    """Load the 2025 play-by-play data"""
    
    print("Loading play-by-play data from nflverse...")
    
    try:
        # Load from URL to get latest data
        import requests
        import io
        
        url = "https://github.com/nflverse/nflverse-data/releases/download/pbp/play_by_play_2025.parquet"
        response = requests.get(url, timeout=30)
        response.raise_for_status()
        
        df = pd.read_parquet(io.BytesIO(response.content))
        print(f"✅ Loaded {len(df)} plays from nflverse")
        
        # Filter to regular season only
        df = df[df['season_type'] == 'REG'].copy()
        print(f"   Regular season plays: {len(df)}")
        print(f"   Weeks available: {sorted(df['week'].unique())}")
        
        return df
        
    except Exception as e:
        print(f"❌ Error loading play-by-play data: {e}")
        return None

def extract_week5_scores(df):
    """Extract final scores from Week 5 games"""
    
    print("\n=== Extracting Week 5 Scores ===")
    
    # Filter to Week 5 regular season games
    week5 = df[(df['week'] == 5) & (df['season_type'] == 'REG')].copy()
    
    print(f"Found {len(week5)} plays from Week 5")
    
    # Get unique games
    games = week5.groupby('game_id').agg({
        'away_team': 'first',
        'home_team': 'first',
        'away_score': 'max',
        'home_score': 'max'
    }).reset_index()
    
    print(f"Found {len(games)} games in Week 5")
    
    # Display scores
    print("\nWeek 5 Final Scores:")
    for _, game in games.iterrows():
        away = game['away_team']
        home = game['home_team']
        away_score = int(game['away_score'])
        home_score = int(game['home_score'])
        print(f"  {away} @ {home}: {away_score} - {home_score}")
    
    return games

def load_predictions():
    """Load the Week 5 predictions"""
    
    print("\n=== Loading Predictions ===")
    
    predictions_file = "predictions/week5_predictions_final.csv"
    
    if not os.path.exists(predictions_file):
        print(f"❌ Predictions file not found: {predictions_file}")
        return None
    
    preds = pd.read_csv(predictions_file)
    print(f"✅ Loaded {len(preds)} predictions")
    
    return preds

def determine_cover_result(favorite_score, underdog_score, spread, favorite_team, home_team):
    """
    Determine if the UNDERDOG covered the spread (matching model prediction perspective)
    
    Args:
        favorite_score: Score of the favorite
        underdog_score: Score of the underdog
        spread: The spread (negative number, e.g., -5.5)
        favorite_team: Name of favorite team
        home_team: Name of home team
        
    Returns:
        'Yes' if underdog covered, 'No' if favorite covered
    """
    
    # Calculate the margin (favorite score - underdog score)
    margin = favorite_score - underdog_score
    
    # Spread is typically shown as the favorite's spread (negative number)
    # Underdog covers if favorite doesn't win by more than the spread
    # For example, if favorite is -5.5 and they win by 5, underdog covered
    
    spread_value = abs(spread)
    
    # Underdog covers if the favorite's margin of victory is less than or equal to spread
    # OR if the underdog wins outright
    if margin > spread_value:
        return "No"   # Favorite covered (underdog didn't cover)
    else:
        return "Yes"  # Underdog covered

def analyze_model_performance(predictions, actual_results):
    """Compare predictions with actual results and calculate accuracy"""
    
    print("\n=== Analyzing Model Performance ===")
    
    # Team name mapping (from abbreviation to full name)
    team_mapping = {
        'ARI': 'Cardinals', 'ATL': 'Falcons', 'BAL': 'Ravens', 'BUF': 'Bills',
        'CAR': 'Panthers', 'CHI': 'Bears', 'CIN': 'Bengals', 'CLE': 'Browns',
        'DAL': 'Cowboys', 'DEN': 'Broncos', 'DET': 'Lions', 'GB': 'Packers',
        'HOU': 'Texans', 'IND': 'Colts', 'JAX': 'Jaguars', 'KC': 'Chiefs',
        'LA': 'Rams', 'LAC': 'Chargers', 'LV': 'Raiders', 'MIA': 'Dolphins',
        'MIN': 'Vikings', 'NE': 'Patriots', 'NO': 'Saints', 'NYG': 'Giants',
        'NYJ': 'Jets', 'PHI': 'Eagles', 'PIT': 'Steelers', 'SF': '49ers',
        'SEA': 'Seahawks', 'TB': 'Buccaneers', 'TEN': 'Titans', 'WAS': 'Commanders'
    }
    
    # Reverse mapping (full name to abbreviation) - handle both LA and LAR for Rams
    name_to_abbrev = {v: k for k, v in team_mapping.items()}
    
    # For matching, we need to be flexible with Rams abbreviation
    def find_team_abbrev(team_name, away_team, home_team):
        """Find the matching team abbreviation"""
        abbrev = name_to_abbrev.get(team_name)
        if abbrev:
            return abbrev
        # Check if it matches either away or home by name
        if team_mapping.get(away_team) == team_name:
            return away_team
        if team_mapping.get(home_team) == team_name:
            return home_team
        return None
    
    # Create a detailed results dataframe
    results = []
    
    for _, pred_row in predictions.iterrows():
        game = pred_row['Game']
        favorite = pred_row['Favorite']
        underdog = pred_row['Underdog']
        spread = float(pred_row['Spread'])
        
        # Parse game string to get away and home team abbreviations
        if ' @ ' in game:
            away_abbrev, home_abbrev = game.split(' @ ')
            
            # Handle LAR -> LA mapping (predictions use LAR, data uses LA)
            if away_abbrev == 'LAR':
                away_abbrev = 'LA'
            if home_abbrev == 'LAR':
                home_abbrev = 'LA'
            
            # Convert abbreviations to full names for display
            away_full = team_mapping.get(away_abbrev, away_abbrev)
            home_full = team_mapping.get(home_abbrev, home_abbrev)
            
            # Try to find matching game in actual results
            actual_game = None
            for _, result_row in actual_results.iterrows():
                if result_row['away_team'] == away_abbrev and result_row['home_team'] == home_abbrev:
                    actual_game = result_row
                    break
            
            if actual_game is None:
                print(f"⚠️  Could not find game: {game}")
                print(f"   Looking for: away={away_abbrev}, home={home_abbrev}")
                continue
            
            away_score = int(actual_game['away_score'])
            home_score = int(actual_game['home_score'])
            
            # Determine which team is favorite
            if favorite == home_full:
                favorite_score = home_score
                underdog_score = away_score
            else:
                favorite_score = away_score
                underdog_score = home_score
            
            # Determine actual cover result
            actual_cover = determine_cover_result(
                favorite_score, underdog_score, spread, favorite, home_full
            )
            
            # Determine winner
            if away_score > home_score:
                actual_winner = away_full
            elif home_score > away_score:
                actual_winner = home_full
            else:
                actual_winner = "Tie"
            
            # Create final score string
            final_score = f"{away_full} {away_score} - {home_full} {home_score}"
            
            # Check each model's prediction
            result = {
                'Game': game,
                'Favorite': favorite,
                'Underdog': underdog,
                'Spread': spread,
                'Total': pred_row['Total'],
                'Final_Score': final_score,
                'Actual_Cover': actual_cover,
                'Actual_Winner': actual_winner
            }
            
            # Helper function to compare predictions
            # Both models and actual_cover are now from underdog perspective:
            # "Cover" or "Yes" means underdog covered
            # "No Cover" or "No" means favorite covered (underdog didn't cover)
            def check_prediction(model_pred, actual_cover):
                if model_pred == "Cover":
                    return 1 if actual_cover == "Yes" else 0
                elif model_pred == "No Cover":
                    return 1 if actual_cover == "No" else 0
                return 0
            
            # Model A
            if 'Model_A_Pred' in pred_row:
                result['Model_A_Pred'] = pred_row['Model_A_Pred']
                result['Model_A_Conf'] = pred_row['Model_A_Conf']
                result['Model_A_Prob'] = pred_row['Model_A_Prob']
                result['Model_A_Correct'] = check_prediction(pred_row['Model_A_Pred'], actual_cover)
            
            # Model B
            if 'Model_B_Pred' in pred_row:
                result['Model_B_Pred'] = pred_row['Model_B_Pred']
                result['Model_B_Conf'] = pred_row['Model_B_Conf']
                result['Model_B_Prob'] = pred_row['Model_B_Prob']
                result['Model_B_Correct'] = check_prediction(pred_row['Model_B_Pred'], actual_cover)
            
            # Model C
            if 'Model_C_Pred' in pred_row:
                result['Model_C_Pred'] = pred_row['Model_C_Pred']
                result['Model_C_Conf'] = pred_row['Model_C_Conf']
                result['Model_C_Prob'] = pred_row['Model_C_Prob']
                result['Model_C_Correct'] = check_prediction(pred_row['Model_C_Pred'], actual_cover)
            
            # Model D
            if 'Model_D_Pred' in pred_row:
                result['Model_D_Pred'] = pred_row['Model_D_Pred']
                result['Model_D_Conf'] = pred_row['Model_D_Conf']
                result['Model_D_Correct'] = check_prediction(pred_row['Model_D_Pred'], actual_cover)
            
            results.append(result)
    
    results_df = pd.DataFrame(results)
    
    # Save detailed results
    output_file = "week5/week5_model_predictions_vs_reality.csv"
    results_df.to_csv(output_file, index=False)
    print(f"\n✅ Saved detailed results to {output_file}")
    
    return results_df

def calculate_model_accuracy(results_df):
    """Calculate accuracy metrics for each model"""
    
    print("\n=== Model Accuracy Summary ===\n")
    
    models = ['Model_A', 'Model_B', 'Model_C', 'Model_D']
    
    summary = []
    
    for model in models:
        correct_col = f'{model}_Correct'
        
        if correct_col not in results_df.columns:
            continue
        
        total_predictions = len(results_df)
        correct_predictions = results_df[correct_col].sum()
        accuracy = (correct_predictions / total_predictions * 100) if total_predictions > 0 else 0
        
        summary.append({
            'Model': model,
            'Correct': int(correct_predictions),
            'Total': total_predictions,
            'Accuracy': f"{accuracy:.1f}%"
        })
        
        print(f"{model}:")
        print(f"  Correct: {int(correct_predictions)}/{total_predictions}")
        print(f"  Accuracy: {accuracy:.1f}%")
        print()
    
    # Save summary
    summary_df = pd.DataFrame(summary)
    output_file = "week5/week5_model_accuracy_summary.csv"
    summary_df.to_csv(output_file, index=False)
    print(f"✅ Saved accuracy summary to {output_file}")
    
    return summary_df

def main():
    """Main analysis function"""
    
    print("=" * 60)
    print("Week 5 2024 NFL Results and Model Performance Analysis")
    print("=" * 60)
    
    # Load play-by-play data
    pbp_df = load_play_by_play_data()
    
    if pbp_df is None:
        return
    
    # Extract Week 5 scores
    actual_results = extract_week5_scores(pbp_df)
    
    # Load predictions
    predictions = load_predictions()
    
    if predictions is None:
        return
    
    # Analyze model performance
    results_df = analyze_model_performance(predictions, actual_results)
    
    # Calculate accuracy
    accuracy_summary = calculate_model_accuracy(results_df)
    
    print("\n" + "=" * 60)
    print("Analysis Complete!")
    print("=" * 60)

if __name__ == "__main__":
    main()

