#!/usr/bin/env python3
"""
Week 10 Model Performance Analysis
Analyzes how all models performed in predicting Week 10 outcomes
"""

import pandas as pd
import numpy as np

def analyze_week10_performance():
    """Analyze Week 10 model performance against actual results"""
    
    print("=== Week 10 Model Performance Analysis ===\n")
    
    # Load actual results
    actual_results_df = pd.read_csv("data/week10_ats_results.csv")
    
    # Create a dictionary for quick lookup
    actual_results = {}
    for _, row in actual_results_df.iterrows():
        actual_results[row['game']] = row['underdog_covered']
    
    # Load model predictions
    predictions_df = pd.read_csv("predictions/week10_all_models_predictions.csv")
    
    print(f"Analyzing {len(predictions_df)} games...\n")
    
    # Create results analysis
    results_data = []
    
    for _, row in predictions_df.iterrows():
        game_key = row['game']
        actual_cover = actual_results.get(game_key, None)
        
        if actual_cover is None:
            print(f"Warning: No actual result found for {game_key}")
            continue
            
        # Parse model predictions (Cover = True, No Cover = False)
        model_a_pred = row['Model_A_Cover'] == True if pd.notna(row['Model_A_Cover']) else False
        model_b_pred = row['Model_B_Cover'] == True if pd.notna(row['Model_B_Cover']) else False
        model_e_pred = row['Model_E_Cover'] == True if pd.notna(row['Model_E_Cover']) else False
        
        # Calculate accuracy for each model
        model_a_correct = model_a_pred == actual_cover
        model_b_correct = model_b_pred == actual_cover
        model_e_correct = model_e_pred == actual_cover
        
        # Get actual result details
        actual_row = actual_results_df[actual_results_df['game'] == game_key].iloc[0]
        
        results_data.append({
            'game': game_key,
            'underdog': row['underdog_team'],
            'spread': row['spread_line'],
            'actual_cover': actual_cover,
            'actual_score': actual_row['final_score'],
            'model_a_pred': model_a_pred,
            'model_a_prob': row['Model_A_Prob'],
            'model_a_conf': row['Model_A_Conf'],
            'model_a_correct': model_a_correct,
            'model_b_pred': model_b_pred,
            'model_b_prob': row['Model_B_Prob'],
            'model_b_conf': row['Model_B_Conf'],
            'model_b_correct': model_b_correct,
            'model_e_pred': model_e_pred,
            'model_e_prob': row['Model_E_Prob'],
            'model_e_conf': row['Model_E_Conf'],
            'model_e_correct': model_e_correct,
        })
    
    results_df = pd.DataFrame(results_data)
    
    # Calculate overall accuracy
    model_a_accuracy = results_df['model_a_correct'].mean()
    model_b_accuracy = results_df['model_b_correct'].mean()
    model_e_accuracy = results_df['model_e_correct'].mean()
    
    # Calculate consensus (majority vote)
    results_df['consensus_pred'] = (
        results_df['model_a_pred'].astype(int) + 
        results_df['model_b_pred'].astype(int) + 
        results_df['model_e_pred'].astype(int)
    ) >= 2
    results_df['consensus_correct'] = results_df['consensus_pred'] == results_df['actual_cover']
    consensus_accuracy = results_df['consensus_correct'].mean()
    
    print(f"=== Week 10 Model Accuracy ===")
    print(f"Model A: {model_a_accuracy:.1%} ({results_df['model_a_correct'].sum()}/{len(results_df)})")
    print(f"Model B: {model_b_accuracy:.1%} ({results_df['model_b_correct'].sum()}/{len(results_df)})")
    print(f"Model E: {model_e_accuracy:.1%} ({results_df['model_e_correct'].sum()}/{len(results_df)})")
    print(f"Consensus (2/3): {consensus_accuracy:.1%} ({results_df['consensus_correct'].sum()}/{len(results_df)})")
    
    # Find best performing model
    accuracies = {
        'Model A': model_a_accuracy,
        'Model B': model_b_accuracy,
        'Model E': model_e_accuracy,
        'Consensus': consensus_accuracy
    }
    
    best_model = max(accuracies, key=accuracies.get)
    print(f"\n🏆 Best Performing Model: {best_model} ({accuracies[best_model]:.1%})")
    
    # Analyze actual underdog covers
    actual_covers = results_df['actual_cover'].sum()
    print(f"\n=== Week 10 Actual Results ===")
    print(f"Underdog Covers: {actual_covers}/{len(results_df)} ({actual_covers/len(results_df):.1%})")
    
    # Show which underdogs actually covered
    print(f"\nUnderdogs that covered:")
    for _, row in results_df.iterrows():
        status = "✅" if row['actual_cover'] else "❌"
        print(f"  {status} {row['game']}: {row['underdog']} +{abs(row['spread'])}")
    
    # Detailed game-by-game analysis
    print(f"\n=== Game-by-Game Analysis ===")
    for _, row in results_df.iterrows():
        print(f"\n{row['game']}: {row['underdog']} +{abs(row['spread'])}")
        print(f"  Score: {row['actual_score']}")
        print(f"  Actual: {'Cover' if row['actual_cover'] else 'No Cover'}")
        print(f"  Model A: {'Cover' if row['model_a_pred'] else 'No Cover'} ({row['model_a_prob']:.1%}, {row['model_a_conf']}) {'✅' if row['model_a_correct'] else '❌'}")
        print(f"  Model B: {'Cover' if row['model_b_pred'] else 'No Cover'} ({row['model_b_prob']:.1%}, {row['model_b_conf']}) {'✅' if row['model_b_correct'] else '❌'}")
        print(f"  Model E: {'Cover' if row['model_e_pred'] else 'No Cover'} ({row['model_e_prob']:.1%}, {row['model_e_conf']}) {'✅' if row['model_e_correct'] else '❌'}")
        print(f"  Consensus: {'Cover' if row['consensus_pred'] else 'No Cover'} {'✅' if row['consensus_correct'] else '❌'}")
    
    # High confidence analysis
    print(f"\n=== High Confidence Picks Performance ===")
    
    high_conf_games = []
    for _, row in results_df.iterrows():
        high_conf_count = sum([
            row['model_a_conf'] in ['HIGH', 'VERY_HIGH'],
            row['model_b_conf'] in ['HIGH', 'VERY_HIGH'],
            row['model_e_conf'] in ['HIGH', 'VERY_HIGH']
        ])
        
        if high_conf_count >= 2:
            high_conf_games.append({
                'game': row['game'],
                'consensus': 'Cover' if row['consensus_pred'] else 'No Cover',
                'actual_cover': row['actual_cover'],
                'high_conf_count': high_conf_count,
                'correct': row['consensus_correct']
            })
    
    if high_conf_games:
        print(f"Games with 2+ high confidence models: {len(high_conf_games)}")
        high_conf_correct = sum([g['correct'] for g in high_conf_games])
        print(f"Consensus accuracy on high confidence games: {high_conf_correct}/{len(high_conf_games)} ({high_conf_correct/len(high_conf_games):.1%})")
        for game in high_conf_games:
            status = "✅" if game['correct'] else "❌"
            print(f"  {status} {game['game']}: Consensus {game['consensus']}, Actual {'Cover' if game['actual_cover'] else 'No Cover'}")
    else:
        print("No games with 2+ high confidence models")
    
    # Model agreement analysis
    print(f"\n=== Model Agreement Analysis ===")
    results_df['agreement'] = (
        (results_df['model_a_pred'] == results_df['model_b_pred']).astype(int) +
        (results_df['model_a_pred'] == results_df['model_e_pred']).astype(int) +
        (results_df['model_b_pred'] == results_df['model_e_pred']).astype(int)
    )
    
    unanimous = results_df[results_df['agreement'] == 3]
    two_agree = results_df[results_df['agreement'] == 2]
    
    if len(unanimous) > 0:
        unanimous_accuracy = unanimous['consensus_correct'].mean()
        print(f"Unanimous predictions (3/3): {len(unanimous)} games, {unanimous_accuracy:.1%} accuracy")
    
    if len(two_agree) > 0:
        two_agree_accuracy = two_agree['consensus_correct'].mean()
        print(f"Majority predictions (2/3): {len(two_agree)} games, {two_agree_accuracy:.1%} accuracy")
    
    # Save detailed results
    output_file = "week10/week10_model_performance_analysis.csv"
    results_df.to_csv(output_file, index=False)
    print(f"\n✅ Detailed analysis saved to: {output_file}")
    
    return results_df

if __name__ == "__main__":
    analyze_week10_performance()

