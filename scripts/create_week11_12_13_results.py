#!/usr/bin/env python3
"""
Create actual results analysis files for Weeks 11, 12, and 13
Compares actual results with consensus predictions
"""

import pandas as pd
import numpy as np
import os

def calculate_underdog_covered(away_score, home_score, favorite_team, away_team, home_team, spread):
    """Determine if the underdog covered based on scores and spread"""
    
    # Determine which team is the favorite
    if favorite_team == away_team:
        # Favorite is away team
        favorite_score = away_score
        underdog_score = home_score
        # Spread is negative (e.g., -6.5 means favorite by 6.5)
        # Favorite covers if they win by more than abs(spread)
        margin = favorite_score - underdog_score
        if margin > abs(spread):
            return False  # Favorite covered, underdog did not
        elif margin < abs(spread):
            return True   # Underdog covered
        else:
            return None   # Push (exact spread)
    else:
        # Favorite is home team
        favorite_score = home_score
        underdog_score = away_score
        margin = favorite_score - underdog_score
        if margin > abs(spread):
            return False  # Favorite covered, underdog did not
        elif margin < abs(spread):
            return True   # Underdog covered
        else:
            return None   # Push

def create_week_results(week_num, results_data, predictions_file, odds_file):
    """Create results analysis for a week"""
    
    print(f"\n=== Creating Week {week_num} Results Analysis ===")
    
    # Load predictions and odds
    predictions_df = pd.read_csv(predictions_file)
    odds_df = pd.read_csv(odds_file)
    
    results_analysis = []
    
    for game_key, score_data in results_data.items():
        # Find matching prediction
        pred_row = predictions_df[predictions_df['game'] == game_key]
        
        if pred_row.empty:
            print(f"⚠️  No prediction found for {game_key}")
            continue
        
        pred_row = pred_row.iloc[0]
        
        # Find matching odds
        odds_row = odds_df[
            (odds_df['away_team'] == pred_row['away_team']) & 
            (odds_df['home_team'] == pred_row['home_team'])
        ]
        
        if odds_row.empty:
            print(f"⚠️  No odds found for {game_key}")
            continue
        
        odds_row = odds_row.iloc[0]
        
        # Parse scores
        away_score, home_score = score_data['away_score'], score_data['home_score']
        
        # Calculate if underdog covered
        underdog_covered = calculate_underdog_covered(
            away_score, home_score,
            odds_row['favorite_team'],
            odds_row['away_team'],
            odds_row['home_team'],
            odds_row['spread_line']
        )
        
        if underdog_covered is None:
            print(f"⚠️  Push detected for {game_key}")
            continue
        
        # Get consensus prediction
        consensus_pred = pred_row['consensus_prediction'] == 'Cover'
        
        # Calculate if consensus was correct
        consensus_correct = consensus_pred == underdog_covered
        
        # Format score
        score_str = f"{away_score}-{home_score}" if away_score > home_score else f"{home_score}-{away_score}"
        
        results_analysis.append({
            'game': game_key,
            'away_team': odds_row['away_team'],
            'home_team': odds_row['home_team'],
            'favorite_team': odds_row['favorite_team'],
            'underdog_team': odds_row['underdog_team'],
            'spread_line': odds_row['spread_line'],
            'total_line': odds_row['total_line'],
            'score': score_str,
            'away_score': away_score,
            'home_score': home_score,
            'actual_cover': underdog_covered,
            'consensus_prediction': pred_row['consensus_prediction'],
            'consensus_probability': pred_row['consensus_probability'],
            'consensus_correct': consensus_correct,
            'model_a_prediction': pred_row['model_a_prediction'],
            'model_b_prediction': pred_row['model_b_prediction'],
            'model_e_prediction': pred_row['model_e_prediction'],
            'agreement': pred_row['agreement']
        })
    
    df = pd.DataFrame(results_analysis)
    
    # Save to file
    output_file = f"data/actual_results/week{week_num}/week{week_num}_actual_results_analysis.csv"
    df.to_csv(output_file, index=False)
    
    # Calculate summary
    total_games = len(df)
    consensus_correct = df['consensus_correct'].sum()
    consensus_accuracy = consensus_correct / total_games if total_games > 0 else 0
    
    print(f"✅ Saved {len(df)} games to {output_file}")
    print(f"   Consensus: {consensus_correct}/{total_games} correct ({consensus_accuracy:.1%})")
    
    return df

def main():
    """Create results for weeks 11, 12, 13"""
    
    # Week 11 results
    week11_results = {
        'Jets @ Patriots': {'away_score': 14, 'home_score': 27},
        'Commanders @ Dolphins': {'away_score': 13, 'home_score': 16},
        'Panthers @ Falcons': {'away_score': 30, 'home_score': 27},
        'Buccaneers @ Bills': {'away_score': 32, 'home_score': 44},
        'Texans @ Titans': {'away_score': 16, 'home_score': 13},
        'Bears @ Vikings': {'away_score': 19, 'home_score': 17},
        'Packers @ Giants': {'away_score': 27, 'home_score': 20},
        'Bengals @ Steelers': {'away_score': 12, 'home_score': 34},
        'Chargers @ Jaguars': {'away_score': 6, 'home_score': 35},
        'Seahawks @ Rams': {'away_score': 19, 'home_score': 21},
        '49ers @ Cardinals': {'away_score': 41, 'home_score': 22},
        'Ravens @ Browns': {'away_score': 23, 'home_score': 16},
        'Chiefs @ Broncos': {'away_score': 19, 'home_score': 22},
        'Lions @ Eagles': {'away_score': 9, 'home_score': 16},
        'Cowboys @ Raiders': {'away_score': 33, 'home_score': 16},
    }
    
    # Week 12 results
    week12_results = {
        'Bills @ Texans': {'away_score': 19, 'home_score': 23},
        'Steelers @ Bears': {'away_score': 28, 'home_score': 31},
        'Patriots @ Bengals': {'away_score': 26, 'home_score': 20},
        'Giants @ Lions': {'away_score': 27, 'home_score': 34},
        'Vikings @ Packers': {'away_score': 6, 'home_score': 23},
        'Seahawks @ Titans': {'away_score': 30, 'home_score': 24},
        'Colts @ Chiefs': {'away_score': 20, 'home_score': 23},
        'Jets @ Ravens': {'away_score': 10, 'home_score': 23},
        'Browns @ Raiders': {'away_score': 24, 'home_score': 10},
        'Jaguars @ Cardinals': {'away_score': 27, 'home_score': 24},
        'Eagles @ Cowboys': {'away_score': 21, 'home_score': 24},
        'Falcons @ Saints': {'away_score': 24, 'home_score': 10},
        'Buccaneers @ Rams': {'away_score': 7, 'home_score': 34},
        'Panthers @ 49ers': {'away_score': 9, 'home_score': 20},
    }
    
    # Week 13 results
    week13_results = {
        'Packers @ Lions': {'away_score': 31, 'home_score': 24},
        'Chiefs @ Cowboys': {'away_score': 28, 'home_score': 31},
        'Bengals @ Ravens': {'away_score': 32, 'home_score': 14},
        'Bears @ Eagles': {'away_score': 24, 'home_score': 15},
        '49ers @ Browns': {'away_score': 26, 'home_score': 8},
        'Jaguars @ Titans': {'away_score': 25, 'home_score': 3},
        'Texans @ Colts': {'away_score': 20, 'home_score': 16},
        'Saints @ Dolphins': {'away_score': 17, 'home_score': 21},
        'Falcons @ Jets': {'away_score': 24, 'home_score': 27},
        'Cardinals @ Buccaneers': {'away_score': 17, 'home_score': 20},
        'Rams @ Panthers': {'away_score': 28, 'home_score': 31},
        'Vikings @ Seahawks': {'away_score': 0, 'home_score': 26},
        'Bills @ Steelers': {'away_score': 26, 'home_score': 7},
        'Raiders @ Chargers': {'away_score': 14, 'home_score': 31},
        'Broncos @ Commanders': {'away_score': 27, 'home_score': 26},
        'Giants @ Patriots': {'away_score': 15, 'home_score': 33},
    }
    
    # Create results for each week
    week11_df = create_week_results(
        11,
        week11_results,
        'predictions/week11_predictions_final.csv',
        'schedule/week11_2025_odds.csv'
    )
    
    week12_df = create_week_results(
        12,
        week12_results,
        'predictions/week12_predictions_final.csv',
        'schedule/week12_2025_odds.csv'
    )
    
    week13_df = create_week_results(
        13,
        week13_results,
        'predictions/week13_predictions_final.csv',
        'schedule/week13_2025_odds.csv'
    )
    
    print("\n" + "="*80)
    print("SUMMARY")
    print("="*80)
    print(f"Week 11: {week11_df['consensus_correct'].sum()}/{len(week11_df)} ({week11_df['consensus_correct'].sum()/len(week11_df):.1%})")
    print(f"Week 12: {week12_df['consensus_correct'].sum()}/{len(week12_df)} ({week12_df['consensus_correct'].sum()/len(week12_df):.1%})")
    print(f"Week 13: {week13_df['consensus_correct'].sum()}/{len(week13_df)} ({week13_df['consensus_correct'].sum()/len(week13_df):.1%})")
    print("="*80)

if __name__ == "__main__":
    main()

