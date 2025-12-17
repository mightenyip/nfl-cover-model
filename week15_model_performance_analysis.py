#!/usr/bin/env python3
"""
Week 15 Model Performance Analysis
Analyzes how all models performed in predicting Week 15 outcomes
"""

import pandas as pd
import numpy as np

def analyze_week15_performance():
    """Analyze Week 15 model performance against actual results"""
    
    print("="*100)
    print("WEEK 15 MODEL PERFORMANCE ANALYSIS")
    print("="*100)
    
    # Actual Week 15 results - mapping game to (away_score, home_score, underdog_covered)
    # Format: (away_score, home_score, underdog_covered)
    actual_results = {
        'Falcons @ Buccaneers': (29, 28, True),  # Falcons won, Bucs -4.5 favorites, Falcons covered
        'Browns @ Bears': (3, 31, False),  # Bears won 31-3, Bears -7.5 favorites, won by 28, covered
        'Ravens @ Bengals': (24, 0, False),  # Ravens won 24-0, Ravens -2.5 favorites, won by 24, covered
        'Chargers @ Chiefs': (16, 13, True),  # Chargers won, Chiefs -4.5 favorites, Chargers covered
        'Bills @ Patriots': (35, 31, False),  # Bills won 35-31, Bills -1.5 favorites, won by 4, covered
        'Commanders @ Giants': (29, 21, True),  # Commanders won, Giants -1.5 favorites, Commanders covered
        'Raiders @ Eagles': (0, 31, False),  # Eagles won 31-0, Eagles -11.5 favorites, won by 31, covered
        'Jets @ Jaguars': (20, 48, False),  # Jaguars won 48-20, Jaguars -12.5 favorites, won by 28, covered
        'Cardinals @ Texans': (20, 40, False),  # Texans won 40-20, Texans -9.5 favorites, won by 20, covered
        'Packers @ Broncos': (26, 34, True),  # Broncos won, Packers -2.5 favorites, Broncos covered
        'Lions @ Rams': (34, 41, False),  # Rams won 41-34, Rams -5.5 favorites, won by 7, covered
        'Panthers @ Saints': (17, 20, True),  # Saints won, Panthers -2.5 favorites, Saints covered
        'Titans @ 49ers': (24, 37, False),  # 49ers won 37-24, 49ers -12.5 favorites, won by 13, covered
        'Colts @ Seahawks': (16, 18, True),  # Seahawks won 18-16, Seahawks -13.5 favorites, won by 2, did not cover
        'Vikings @ Cowboys': (34, 26, True),  # Vikings won, Cowboys -5.5 favorites, Vikings covered
        'Dolphins @ Steelers': (15, 28, False),  # Steelers won 28-15, Steelers -3.0 favorites, won by 13, covered
    }
    
    # Load predictions
    predictions_df = pd.read_csv('week15_all_models_predictions.csv')
    
    # Create results analysis
    results_data = []
    
    for _, row in predictions_df.iterrows():
        game = row['game']
        if game not in actual_results or actual_results[game] is None:
            continue
        
        away_score, home_score, underdog_covered = actual_results[game]
        spread = row['spread']
        favorite = row['favorite']
        underdog = row['underdog']
        away_team = row['away_team']
        home_team = row['home_team']
        
        # Format score as "AWAY-HOME"
        score_str = f"{away_score}-{home_score}"
        
        # Get model predictions
        model_a_pred = row['model_a_prediction'] == 'Cover'
        model_b_pred = row['model_b_prediction'] == 'Cover'
        model_c_pred = row['model_c_prediction'] == 'Cover'
        model_d_pred = row['model_d_prediction'] == 'Cover'
        model_e_pred = row['model_e_prediction'] == 'Cover'
        consensus_pred = row['consensus_prediction'] == 'Cover'
        
        # Calculate correctness
        model_a_correct = model_a_pred == underdog_covered
        model_b_correct = model_b_pred == underdog_covered
        model_c_correct = model_c_pred == underdog_covered
        model_d_correct = model_d_pred == underdog_covered
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
            'model_c_pred': 'Cover' if model_c_pred else 'No Cover',
            'model_c_correct': '✓' if model_c_correct else '✗',
            'model_d_pred': 'Cover' if model_d_pred else 'No Cover',
            'model_d_correct': '✓' if model_d_correct else '✗',
            'model_e_pred': 'Cover' if model_e_pred else 'No Cover',
            'model_e_correct': '✓' if model_e_correct else '✗',
            'consensus_pred': 'Cover' if consensus_pred else 'No Cover',
            'consensus_correct': '✓' if consensus_correct else '✗',
            'cover_votes': row['cover_votes'],
            'total_votes': row['total_votes']
        })
    
    results_df = pd.DataFrame(results_data)
    
    # Calculate accuracies
    model_a_accuracy = results_df['model_a_correct'].str.contains('✓').sum() / len(results_df)
    model_b_accuracy = results_df['model_b_correct'].str.contains('✓').sum() / len(results_df)
    model_c_accuracy = results_df['model_c_correct'].str.contains('✓').sum() / len(results_df)
    model_d_accuracy = results_df['model_d_correct'].str.contains('✓').sum() / len(results_df)
    model_e_accuracy = results_df['model_e_correct'].str.contains('✓').sum() / len(results_df)
    consensus_accuracy = results_df['consensus_correct'].str.contains('✓').sum() / len(results_df)
    
    model_a_correct_count = results_df['model_a_correct'].str.contains('✓').sum()
    model_b_correct_count = results_df['model_b_correct'].str.contains('✓').sum()
    model_c_correct_count = results_df['model_c_correct'].str.contains('✓').sum()
    model_d_correct_count = results_df['model_d_correct'].str.contains('✓').sum()
    model_e_correct_count = results_df['model_e_correct'].str.contains('✓').sum()
    consensus_correct_count = results_df['consensus_correct'].str.contains('✓').sum()
    
    # Calculate actual ATS performance
    underdog_covers = results_df['actual_cover'].str.contains('Yes').sum()
    favorite_covers = results_df['actual_cover'].str.contains('No').sum()
    
    # Print detailed results table
    print("\n" + "="*100)
    print("GAME-BY-GAME RESULTS")
    print("="*100)
    print(f"{'Game':<30} {'Spread':<15} {'Score':<12} {'Actual':<8} {'Model A':<12} {'Model B':<12} {'Model C':<12} {'Model D':<12} {'Model E':<12} {'Consensus':<12}")
    print("-"*100)
    
    for _, row in results_df.iterrows():
        print(f"{row['game']:<30} {row['underdog']:>3} +{abs(row['spread']):<4.1f}  {row['score']:<12} {row['actual_cover']:<8} "
              f"{row['model_a_pred']:<7} {row['model_a_correct']:<3}  {row['model_b_pred']:<7} {row['model_b_correct']:<3}  "
              f"{row['model_c_pred']:<7} {row['model_c_correct']:<3}  {row['model_d_pred']:<7} {row['model_d_correct']:<3}  "
              f"{row['model_e_pred']:<7} {row['model_e_correct']:<3}  {row['consensus_pred']:<7} {row['consensus_correct']:<3}")
    
    # Print summary statistics
    print("\n" + "="*100)
    print("PERFORMANCE SUMMARY")
    print("="*100)
    print(f"Total Games: {len(results_df)}")
    print(f"Actual Underdog Covers: {underdog_covers}/{len(results_df)} ({underdog_covers/len(results_df)*100:.1f}%)")
    print(f"Actual Favorite Covers: {favorite_covers}/{len(results_df)} ({favorite_covers/len(results_df)*100:.1f}%)")
    print()
    print(f"Model A:     {model_a_accuracy:.1%} ({model_a_correct_count}/{len(results_df)})")
    print(f"Model B:     {model_b_accuracy:.1%} ({model_b_correct_count}/{len(results_df)})")
    print(f"Model C:     {model_c_accuracy:.1%} ({model_c_correct_count}/{len(results_df)})")
    print(f"Model D:     {model_d_accuracy:.1%} ({model_d_correct_count}/{len(results_df)})")
    print(f"Model E:     {model_e_accuracy:.1%} ({model_e_correct_count}/{len(results_df)})")
    print(f"Consensus:   {consensus_accuracy:.1%} ({consensus_correct_count}/{len(results_df)})")
    
    # Agreement analysis
    print("\n" + "="*100)
    print("AGREEMENT ANALYSIS")
    print("="*100)
    
    # Determine agreement level
    results_df['agreement'] = results_df.apply(lambda row: 
        'Unanimous' if row['cover_votes'] == row['total_votes'] or row['cover_votes'] == 0
        else 'Majority' if row['cover_votes'] >= 3 or row['cover_votes'] <= 2
        else 'Split', axis=1)
    
    unanimous_games = results_df[results_df['agreement'] == 'Unanimous']
    majority_games = results_df[results_df['agreement'] == 'Majority']
    split_games = results_df[results_df['agreement'] == 'Split']
    
    if len(unanimous_games) > 0:
        unanimous_accuracy = unanimous_games['consensus_correct'].str.contains('✓').sum() / len(unanimous_games)
        print(f"Unanimous (5/5 or 0/5): {len(unanimous_games)} games, {unanimous_accuracy:.1%} accuracy")
    
    if len(majority_games) > 0:
        majority_accuracy = majority_games['consensus_correct'].str.contains('✓').sum() / len(majority_games)
        print(f"Majority (3-4/5):  {len(majority_games)} games, {majority_accuracy:.1%} accuracy")
    
    if len(split_games) > 0:
        split_accuracy = split_games['consensus_correct'].str.contains('✓').sum() / len(split_games)
        print(f"Split (2/5):      {len(split_games)} games, {split_accuracy:.1%} accuracy")
    
    # Save to CSV
    import os
    os.makedirs('week15', exist_ok=True)
    results_df.to_csv('week15/week15_model_performance_analysis.csv', index=False)
    print(f"\nDetailed results saved to: week15/week15_model_performance_analysis.csv")
    print("="*100)

if __name__ == '__main__':
    analyze_week15_performance()

