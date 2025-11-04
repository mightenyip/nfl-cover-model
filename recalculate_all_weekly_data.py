#!/usr/bin/env python3
"""
Recalculate all weekly actual results analysis from scratch
Uses odds files from schedule/ directory as source of truth
"""

import pandas as pd
import re
import os

# Team abbreviation to full name mapping
ABBR_TO_FULL = {
    'BAL': 'Ravens', 'MIA': 'Dolphins', 'CHI': 'Bears', 'CIN': 'Bengals',
    'MIN': 'Vikings', 'DET': 'Lions', 'CAR': 'Panthers', 'GB': 'Packers',
    'LAC': 'Chargers', 'TEN': 'Titans', 'ATL': 'Falcons', 'NE': 'Patriots',
    'SF': '49ers', 'NYG': 'Giants', 'IND': 'Colts', 'PIT': 'Steelers',
    'DEN': 'Broncos', 'HOU': 'Texans', 'JAX': 'Jaguars', 'LV': 'Raiders',
    'NO': 'Saints', 'LA': 'Rams', 'KC': 'Chiefs', 'BUF': 'Bills',
    'SEA': 'Seahawks', 'WAS': 'Commanders', 'ARI': 'Cardinals', 'DAL': 'Cowboys'
}

def parse_score(score_str):
    """Parse score string like 'BAL 28, MIA 6' or 'PHI 24 - DAL 20' or 'JAX 30, LV 29 (OT)'"""
    # Remove OT notation
    score_clean = re.sub(r'\s*\(OT\)', '', score_str).strip()
    
    # Try pattern: TEAM1 SCORE1, TEAM2 SCORE2
    match = re.match(r'(\w+)\s+(\d+),\s+(\w+)\s+(\d+)', score_clean)
    if match:
        team1_abbr, score1, team2_abbr, score2 = match.groups()
        team1 = ABBR_TO_FULL.get(team1_abbr, team1_abbr)
        team2 = ABBR_TO_FULL.get(team2_abbr, team2_abbr)
        return team1, int(score1), team2, int(score2)
    
    # Try pattern: TEAM1 SCORE1 - TEAM2 SCORE2
    match = re.match(r'(\w+)\s+(\d+)\s+-\s+(\w+)\s+(\d+)', score_clean)
    if match:
        team1_abbr, score1, team2_abbr, score2 = match.groups()
        team1 = ABBR_TO_FULL.get(team1_abbr, team1_abbr)
        team2 = ABBR_TO_FULL.get(team2_abbr, team2_abbr)
        return team1, int(score1), team2, int(score2)
    
    return None, None, None, None

def calculate_underdog_covered(favorite, underdog, spread, score_str):
    """
    Calculate if underdog covered the spread
    
    Args:
        favorite: Name of favorite team
        underdog: Name of underdog team
        spread: Spread line (negative number, e.g., -7.5)
        score_str: Score string like 'BAL 28, MIA 6'
    
    Returns:
        True if underdog covered, False if favorite covered
    """
    team1, score1, team2, score2 = parse_score(score_str)
    if team1 is None:
        return None
    
    # Determine which score belongs to favorite and which to underdog
    if favorite == team1:
        fav_score = score1
        dog_score = score2
    elif favorite == team2:
        fav_score = score2
        dog_score = score1
    else:
        return None
    
    # Calculate margin (favorite score - underdog score)
    margin = fav_score - dog_score
    spread_abs = abs(spread)
    
    # Underdog covers if favorite doesn't win by more than the spread
    # i.e., margin < spread_abs
    if margin < spread_abs:
        return True  # Underdog covered
    elif margin > spread_abs:
        return False  # Favorite covered
    else:
        return None  # Push (exact spread)

def load_model_predictions(week_num):
    """Load predictions from all models for a week"""
    predictions = {}
    
    # Model A
    try:
        df = pd.read_csv(f'predictions/model_a_week{week_num}_predictions.csv')
        predictions['model_a'] = df
    except:
        pass
    
    # Model B
    try:
        df = pd.read_csv(f'models/model_b/model_b_week{week_num}_predictions.csv')
        predictions['model_b'] = df
    except:
        pass
    
    # Model C
    try:
        df = pd.read_csv(f'models/model_c/model_c_week{week_num}_predictions.csv')
        predictions['model_c'] = df
    except:
        pass
    
    # Model D
    try:
        df = pd.read_csv(f'models/model_d/model_d_week{week_num}_predictions.csv')
        predictions['model_d'] = df
    except:
        pass
    
    # Model E
    try:
        df = pd.read_csv(f'models/model_e/model_e_week{week_num}_predictions.csv')
        predictions['model_e'] = df
    except:
        pass
    
    # Consensus
    try:
        df = pd.read_csv(f'predictions/week{week_num}_consensus_predictions.csv')
        predictions['consensus'] = df
    except:
        pass
    
    return predictions

def get_model_prediction(model_df, game_name):
    """Extract prediction from model dataframe"""
    if model_df is None:
        return None
    
    # Try different column names for game
    if 'game' in model_df.columns:
        match = model_df[model_df['game'] == game_name]
    elif 'Game' in model_df.columns:
        match = model_df[model_df['Game'] == game_name]
    else:
        return None
    
    if len(match) == 0:
        return None
    
    row = match.iloc[0]
    
    # Try different column names for prediction
    if 'predicted_cover' in row:
        return row['predicted_cover']
    elif 'underdog_cover' in row:
        return row['underdog_cover']
    elif 'consensus_prediction' in row:
        return row['consensus_prediction'] == 'Cover'
    else:
        return None

def recalculate_week(week_num):
    """Recalculate all data for a specific week"""
    
    print(f"\n{'='*80}")
    print(f"RECALCULATING WEEK {week_num}")
    print(f"{'='*80}\n")
    
    # Load odds file
    odds_file = f'schedule/week{week_num}_2025_odds.csv'
    if not os.path.exists(odds_file):
        print(f"⚠️  {odds_file} not found, skipping Week {week_num}")
        return None
    
    odds_df = pd.read_csv(odds_file)
    print(f"Loaded {len(odds_df)} games from odds file")
    
    # Load actual results - try different file names
    actual_results = None
    for file_name in [
        f'data/week{week_num}_ats_results.csv',
        f'data/week{week_num}_actual_results_analysis.csv',
        f'data/master_games_results_week{week_num}.csv'
    ]:
        if os.path.exists(file_name):
            actual_results = pd.read_csv(file_name)
            print(f"Loaded actual results from {file_name}")
            break
    
    if actual_results is None:
        print(f"⚠️  No actual results file found for Week {week_num}")
        return None
    
    # Load model predictions
    model_preds = load_model_predictions(week_num)
    print(f"Loaded predictions from {len(model_preds)} models")
    
    # Build results data
    results_data = []
    
    for _, odds_row in odds_df.iterrows():
        away_team = odds_row['away_team']
        home_team = odds_row['home_team']
        favorite = odds_row['favorite_team']
        underdog = odds_row['underdog_team']
        spread = odds_row['spread_line']
        
        game_name = f"{away_team} @ {home_team}"
        
        # Find matching actual result
        actual_match = None
        score = None
        
        # Try to match by game name
        if 'game' in actual_results.columns:
            actual_match = actual_results[actual_results['game'] == game_name]
        elif 'away_team' in actual_results.columns and 'home_team' in actual_results.columns:
            actual_match = actual_results[
                (actual_results['away_team'] == away_team) & 
                (actual_results['home_team'] == home_team)
            ]
        
        if len(actual_match) == 0:
            print(f"⚠️  No actual result found for {game_name}")
            continue
        
        actual_row = actual_match.iloc[0]
        
        # Get score - try multiple formats
        score = None
        if 'score' in actual_row:
            score = actual_row['score']
        elif 'final_score' in actual_row:
            score = actual_row['final_score']
        elif 'away_score' in actual_row and 'home_score' in actual_row:
            # Construct score from away_score and home_score
            away_score = actual_row['away_score']
            home_score = actual_row['home_score']
            # Get abbreviations
            away_abbr = None
            home_abbr = None
            for abbr, full_name in ABBR_TO_FULL.items():
                if full_name == away_team:
                    away_abbr = abbr
                if full_name == home_team:
                    home_abbr = abbr
            
            if away_abbr and home_abbr:
                score = f"{away_abbr} {away_score}, {home_abbr} {home_score}"
        
        if score is None:
            print(f"⚠️  Could not find score for {game_name}")
            continue
        
        # Calculate if underdog covered
        underdog_covered = calculate_underdog_covered(favorite, underdog, spread, score)
        
        if underdog_covered is None:
            print(f"⚠️  Could not calculate cover for {game_name}")
            continue
        
        # Get model predictions
        model_a_pred = get_model_prediction(model_preds.get('model_a'), game_name)
        model_b_pred = get_model_prediction(model_preds.get('model_b'), game_name)
        model_c_pred = get_model_prediction(model_preds.get('model_c'), game_name)
        model_d_pred = get_model_prediction(model_preds.get('model_d'), game_name)
        model_e_pred = get_model_prediction(model_preds.get('model_e'), game_name)
        consensus_pred = get_model_prediction(model_preds.get('consensus'), game_name)
        
        # Calculate correctness
        model_a_correct = (model_a_pred == underdog_covered) if model_a_pred is not None else None
        model_b_correct = (model_b_pred == underdog_covered) if model_b_pred is not None else None
        model_c_correct = (model_c_pred == underdog_covered) if model_c_pred is not None else None
        model_d_correct = (model_d_pred == underdog_covered) if model_d_pred is not None else None
        model_e_correct = (model_e_pred == underdog_covered) if model_e_pred is not None else None
        consensus_correct = (consensus_pred == underdog_covered) if consensus_pred is not None else None
        
        results_data.append({
            'game': game_name,
            'score': score,
            'spread': spread,
            'underdog': underdog,
            'actual_cover': underdog_covered,
            'model_a_pred': model_a_pred,
            'model_a_correct': model_a_correct,
            'model_b_pred': model_b_pred,
            'model_b_correct': model_b_correct,
            'model_c_pred': model_c_pred,
            'model_c_correct': model_c_correct,
            'model_d_pred': model_d_pred,
            'model_d_correct': model_d_correct,
            'model_e_pred': model_e_pred,
            'model_e_correct': model_e_correct,
            'consensus_pred': consensus_pred,
            'consensus_correct': consensus_correct,
        })
    
    # Create DataFrame
    results_df = pd.DataFrame(results_data)
    
    # Save to file
    output_file = f'data/week{week_num}_actual_results_analysis.csv'
    results_df.to_csv(output_file, index=False)
    
    # Print summary
    print(f"\n✅ Saved {len(results_df)} games to {output_file}")
    
    # Calculate and print accuracies
    print("\nModel Accuracies:")
    for model in ['model_a', 'model_b', 'model_c', 'model_d', 'model_e', 'consensus']:
        correct_col = f'{model}_correct'
        if correct_col in results_df.columns:
            correct = results_df[correct_col].dropna().sum()
            total = results_df[correct_col].notna().sum()
            if total > 0:
                acc = correct / total * 100
                print(f"  {model}: {correct}/{total} ({acc:.1f}%)")
    
    return results_df

def main():
    """Recalculate all weeks"""
    print("=" * 80)
    print("RECALCULATING ALL WEEKLY DATA FROM SCRATCH")
    print("=" * 80)
    print("\nUsing odds files from schedule/ directory as source of truth")
    print("Calculating underdog cover based on favorite/underdog from odds file")
    print()
    
    all_results = {}
    
    for week in range(1, 10):
        week_results = recalculate_week(week)
        if week_results is not None:
            all_results[week] = week_results
    
    print(f"\n{'='*80}")
    print("RECALCULATION COMPLETE")
    print(f"{'='*80}")
    print(f"\nRecalculated {len(all_results)} weeks")
    print("\n✅ All weekly data files have been regenerated with correct calculations")

if __name__ == "__main__":
    main()

