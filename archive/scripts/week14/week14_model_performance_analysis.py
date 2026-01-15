#!/usr/bin/env python3
"""
Week 14 Model Performance Analysis
Analyzes how all models performed in predicting Week 14 outcomes
"""

import pandas as pd
import numpy as np

def analyze_week14_performance():
    """Analyze Week 14 model performance against actual results"""
    
    print("="*100)
    print("WEEK 14 MODEL PERFORMANCE ANALYSIS")
    print("="*100)
    
    # Actual Week 14 results - mapping game to (away_score, home_score, underdog_covered)
    # Scores are in format: "AWAY @ HOME: AWAY_SCORE, HOME_SCORE"
    actual_results = {
        'Cowboys @ Lions': (30, 44, False),  # Lions -3 favorites, won 44-30, covered. Underdog did not cover.
        'Seahawks @ Falcons': (37, 9, False),  # Seahawks -7.5 favorites, won 37-9, covered. Underdog did not cover.
        'Bengals @ Bills': (34, 39, True),  # Bills -5.5 favorites, won 39-34, did not cover. Underdog covered.
        'Titans @ Browns': (31, 29, True),  # Browns -3.5 favorites, lost 29-31. Underdog covered.
        'Commanders @ Vikings': (0, 31, False),  # Vikings -1.5 favorites, won 31-0, covered. Underdog did not cover.
        'Dolphins @ Jets': (34, 10, False),  # Dolphins -2.5 favorites, won 34-10, covered. Underdog did not cover.
        'Saints @ Buccaneers': (24, 20, True),  # Buccaneers -8.5 favorites, lost 20-24. Underdog covered.
        'Colts @ Jaguars': (19, 36, True),  # Colts -1.5 favorites, lost 19-36. Underdog covered.
        'Steelers @ Ravens': (27, 22, True),  # Ravens -5.5 favorites, lost 22-27. Underdog covered.
        'Broncos @ Raiders': (24, 17, True),  # Broncos -7.5 favorites, won 24-17, did not cover. Underdog covered.
        'Bears @ Packers': (21, 28, True),  # Packers -6.5 favorites, won 28-21, did not cover. Underdog covered.
        'Rams @ Cardinals': (45, 17, False),  # Rams -8.5 favorites, won 45-17, covered. Underdog did not cover.
        'Texans @ Chiefs': (20, 10, True),  # Chiefs -3.5 favorites, lost 10-20. Underdog covered.
        'Eagles @ Chargers': (19, 22, True),  # Eagles -2.5 favorites, lost 19-22. Underdog covered.
    }
    
    # Load predictions
    predictions_df = pd.read_csv('predictions/week14_predictions_final.csv')
    
    # Create results analysis
    results_data = []
    
    for _, row in predictions_df.iterrows():
        game = row['game']
        if game not in actual_results:
            continue
        
        away_score, home_score, underdog_covered = actual_results[game]
        spread = row['spread_line']
        favorite = row['favorite_team']
        underdog = row['underdog_team']
        away_team = row['away_team']
        home_team = row['home_team']
        
        # Format score as "AWAY-HOME"
        score_str = f"{away_score}-{home_score}"
        
        # Get model predictions
        model_a_pred = row['model_a_prediction'] == 'Cover'
        model_b_pred = row['model_b_prediction'] == 'Cover'
        model_e_pred = row['model_e_prediction'] == 'Cover'
        consensus_pred = row['consensus_prediction'] == 'Cover'
        
        # Calculate correctness
        model_a_correct = model_a_pred == underdog_covered
        model_b_correct = model_b_pred == underdog_covered
        model_e_correct = model_e_pred == underdog_covered
        consensus_correct = consensus_pred == underdog_covered
        
        results_data.append({
            'game': game,
            'underdog': underdog,
            'spread': spread,
            'score': score_str,
            'actual_cover': 'Yes' if underdog_covered else 'No',
            'model_a_pred': 'Cover' if model_a_pred else 'No Cover',
            'model_a_correct': '✓' if model_a_correct else '✗',
            'model_b_pred': 'Cover' if model_b_pred else 'No Cover',
            'model_b_correct': '✓' if model_b_correct else '✗',
            'model_e_pred': 'Cover' if model_e_pred else 'No Cover',
            'model_e_correct': '✓' if model_e_correct else '✗',
            'consensus_pred': 'Cover' if consensus_pred else 'No Cover',
            'consensus_correct': '✓' if consensus_correct else '✗',
            'agreement': row['agreement']
        })
    
    results_df = pd.DataFrame(results_data)
    
    # Calculate accuracies
    model_a_accuracy = results_df['model_a_correct'].str.contains('✓').sum() / len(results_df)
    model_b_accuracy = results_df['model_b_correct'].str.contains('✓').sum() / len(results_df)
    model_e_accuracy = results_df['model_e_correct'].str.contains('✓').sum() / len(results_df)
    consensus_accuracy = results_df['consensus_correct'].str.contains('✓').sum() / len(results_df)
    
    model_a_correct_count = results_df['model_a_correct'].str.contains('✓').sum()
    model_b_correct_count = results_df['model_b_correct'].str.contains('✓').sum()
    model_e_correct_count = results_df['model_e_correct'].str.contains('✓').sum()
    consensus_correct_count = results_df['consensus_correct'].str.contains('✓').sum()
    
    # Print detailed results table
    print("\n" + "="*100)
    print("GAME-BY-GAME RESULTS")
    print("="*100)
    print(f"{'Game':<30} {'Spread':<15} {'Score':<12} {'Actual':<8} {'Model A':<12} {'Model B':<12} {'Model E':<12} {'Consensus':<12}")
    print("-"*100)
    
    for _, row in results_df.iterrows():
        print(f"{row['game']:<30} {row['underdog']:>3} +{abs(row['spread']):<4.1f}  {row['score']:<12} {row['actual_cover']:<8} "
              f"{row['model_a_pred']:<7} {row['model_a_correct']:<3}  {row['model_b_pred']:<7} {row['model_b_correct']:<3}  "
              f"{row['model_e_pred']:<7} {row['model_e_correct']:<3}  {row['consensus_pred']:<7} {row['consensus_correct']:<3}")
    
    # Print summary statistics
    print("\n" + "="*100)
    print("PERFORMANCE SUMMARY")
    print("="*100)
    print(f"Model A:     {model_a_accuracy:.1%} ({model_a_correct_count}/{len(results_df)})")
    print(f"Model B:     {model_b_accuracy:.1%} ({model_b_correct_count}/{len(results_df)})")
    print(f"Model E:     {model_e_accuracy:.1%} ({model_e_correct_count}/{len(results_df)})")
    print(f"Consensus:   {consensus_accuracy:.1%} ({consensus_correct_count}/{len(results_df)})")
    
    # Agreement analysis
    print("\n" + "="*100)
    print("AGREEMENT ANALYSIS")
    print("="*100)
    unanimous_games = results_df[results_df['agreement'].str.contains('Unanimous')]
    majority_games = results_df[results_df['agreement'].str.contains('Majority')]
    split_games = results_df[results_df['agreement'].str.contains('Split')]
    
    if len(unanimous_games) > 0:
        unanimous_accuracy = unanimous_games['consensus_correct'].str.contains('✓').sum() / len(unanimous_games)
        print(f"Unanimous (3/3): {len(unanimous_games)} games, {unanimous_accuracy:.1%} accuracy")
    
    if len(majority_games) > 0:
        majority_accuracy = majority_games['consensus_correct'].str.contains('✓').sum() / len(majority_games)
        print(f"Majority (2/3):  {len(majority_games)} games, {majority_accuracy:.1%} accuracy")
    
    if len(split_games) > 0:
        split_accuracy = split_games['consensus_correct'].str.contains('✓').sum() / len(split_games)
        print(f"Split (1/3):      {len(split_games)} games, {split_accuracy:.1%} accuracy")
    
    # Save to CSV
    results_df.to_csv('week14/week14_model_performance_analysis.csv', index=False)
    print(f"\nDetailed results saved to: week14/week14_model_performance_analysis.csv")
    print("="*100)

if __name__ == '__main__':
    analyze_week14_performance()

