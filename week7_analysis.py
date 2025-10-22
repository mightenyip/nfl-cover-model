#!/usr/bin/env python3
"""
Week 7 Model Performance Analysis
Analyzes how all models performed in predicting Week 7 outcomes
"""

import pandas as pd
import numpy as np

def analyze_week7_performance():
    """Analyze Week 7 model performance against actual results"""
    
    print("=== Week 7 Model Performance Analysis ===")
    
    # Actual Week 7 results (underdog covers)
    actual_results = {
        'Steelers @ Bengals': False,  # Bengals covered (+5.5) - WON 33-31
        'Rams @ Jaguars': False,      # Jaguars did not cover (+3) - LOST 35-7
        'Saints @ Bears': False,      # Saints did not cover (+5.5) - LOST 26-14
        'Dolphins @ Browns': False,   # Dolphins did not cover (+2.5) - LOST 31-6
        'Patriots @ Titans': False,   # Titans did not cover (+7) - LOST 31-13
        'Raiders @ Chiefs': False,    # Raiders did not cover (+11.5) - LOST 31-0
        'Eagles @ Vikings': False,    # Vikings did not cover (+2.5) - LOST 28-22
        'Panthers @ Jets': False,     # Jets did not cover (+1.5) - LOST 13-6
        'Giants @ Broncos': True,     # Giants covered (+7) - LOST 33-32
        'Colts @ Chargers': True,     # Colts covered (+1.5) - WON 38-24
        'Commanders @ Cowboys': False, # Cowboys did not cover (+2.5) - LOST 44-22
        'Packers @ Cardinals': True,  # Cardinals covered (+6.5) - LOST 27-23
        'Falcons @ 49ers': False,     # Falcons did not cover (+2.5) - LOST 20-10
        'Buccaneers @ Lions': False,  # Buccaneers did not cover (+4.5) - LOST 24-9
        'Texans @ Seahawks': False    # Texans did not cover (+3.5) - LOST 27-19
    }
    
    # Load model predictions
    comparison_df = pd.read_csv("week7/week7_all_models_comparison.csv")
    
    print(f"Analyzing {len(comparison_df)} games...")
    
    # Create results analysis
    results_data = []
    
    for _, row in comparison_df.iterrows():
        game_key = f"{row['away_team']} @ {row['home_team']}"
        actual_cover = actual_results.get(game_key, None)
        
        if actual_cover is None:
            print(f"Warning: No actual result found for {game_key}")
            continue
            
        # Parse model predictions (Cover = True, No Cover = False)
        model_a_pred = row['model_a_prediction'] == 'Cover'
        model_b_pred = row['model_b_prediction'] == 'Cover'
        model_c_pred = row['model_c_prediction'] == 'Cover'
        model_d_pred = row['model_d_prediction'] == 'Cover'
        
        # Calculate accuracy for each model
        model_a_correct = model_a_pred == actual_cover
        model_b_correct = model_b_pred == actual_cover
        model_c_correct = model_c_pred == actual_cover
        model_d_correct = model_d_pred == actual_cover
        
        # Consensus prediction
        consensus_pred = row['consensus'] == 'UNDERDOG'
        consensus_correct = consensus_pred == actual_cover
        
        results_data.append({
            'game': game_key,
            'underdog': row['underdog_team'],
            'spread': row['spread_line'],
            'actual_cover': actual_cover,
            'model_a_pred': model_a_pred,
            'model_a_correct': model_a_correct,
            'model_b_pred': model_b_pred,
            'model_b_correct': model_b_correct,
            'model_c_pred': model_c_pred,
            'model_c_correct': model_c_correct,
            'model_d_pred': model_d_pred,
            'model_d_correct': model_d_correct,
            'consensus_pred': consensus_pred,
            'consensus_correct': consensus_correct,
            'agreement': row['agreement']
        })
    
    results_df = pd.DataFrame(results_data)
    
    # Calculate overall accuracy
    model_a_accuracy = results_df['model_a_correct'].mean()
    model_b_accuracy = results_df['model_b_correct'].mean()
    model_c_accuracy = results_df['model_c_correct'].mean()
    model_d_accuracy = results_df['model_d_correct'].mean()
    consensus_accuracy = results_df['consensus_correct'].mean()
    
    print(f"\n=== Week 7 Model Accuracy ===")
    print(f"Model A: {model_a_accuracy:.1%} ({results_df['model_a_correct'].sum()}/{len(results_df)})")
    print(f"Model B v2: {model_b_accuracy:.1%} ({results_df['model_b_correct'].sum()}/{len(results_df)})")
    print(f"Model C: {model_c_accuracy:.1%} ({results_df['model_c_correct'].sum()}/{len(results_df)})")
    print(f"Model D: {model_d_accuracy:.1%} ({results_df['model_d_correct'].sum()}/{len(results_df)})")
    print(f"Consensus: {consensus_accuracy:.1%} ({results_df['consensus_correct'].sum()}/{len(results_df)})")
    
    # Find best performing model
    accuracies = {
        'Model A': model_a_accuracy,
        'Model B v2': model_b_accuracy,
        'Model C': model_c_accuracy,
        'Model D': model_d_accuracy,
        'Consensus': consensus_accuracy
    }
    
    best_model = max(accuracies, key=accuracies.get)
    print(f"\n🏆 Best Performing Model: {best_model} ({accuracies[best_model]:.1%})")
    
    # Analyze actual underdog covers
    actual_covers = sum(actual_results.values())
    print(f"\n=== Week 7 Actual Results ===")
    print(f"Underdog Covers: {actual_covers}/{len(actual_results)} ({actual_covers/len(actual_results):.1%})")
    
    # Show which underdogs actually covered
    print(f"\nUnderdogs that covered:")
    for game, covered in actual_results.items():
        if covered:
            print(f"  ✅ {game}")
        else:
            print(f"  ❌ {game}")
    
    # Detailed game-by-game analysis
    print(f"\n=== Game-by-Game Analysis ===")
    for _, row in results_df.iterrows():
        print(f"\n{row['game']}: {row['underdog']} +{row['spread']}")
        print(f"  Actual: {'Cover' if row['actual_cover'] else 'No Cover'}")
        print(f"  Model A: {'Cover' if row['model_a_pred'] else 'No Cover'} {'✅' if row['model_a_correct'] else '❌'}")
        print(f"  Model B: {'Cover' if row['model_b_pred'] else 'No Cover'} {'✅' if row['model_b_correct'] else '❌'}")
        print(f"  Model C: {'Cover' if row['model_c_pred'] else 'No Cover'} {'✅' if row['model_c_correct'] else '❌'}")
        print(f"  Model D: {'Cover' if row['model_d_pred'] else 'No Cover'} {'✅' if row['model_d_correct'] else '❌'}")
        print(f"  Consensus: {'Cover' if row['consensus_pred'] else 'No Cover'} {'✅' if row['consensus_correct'] else '❌'}")
    
    # High confidence analysis
    print(f"\n=== High Confidence Picks Performance ===")
    
    # Load original comparison for confidence analysis
    original_df = pd.read_csv("week7/week7_all_models_comparison.csv")
    
    high_conf_games = []
    for _, row in original_df.iterrows():
        high_conf_count = sum([
            row['model_a_confidence'] in ['HIGH', 'VERY_HIGH'],
            row['model_b_confidence'] in ['HIGH', 'VERY_HIGH'],
            row['model_c_confidence'] in ['HIGH', 'VERY_HIGH'],
            row['model_d_confidence'] in ['HIGH', 'VERY_HIGH']
        ])
        
        if high_conf_count >= 2:
            game_key = f"{row['away_team']} @ {row['home_team']}"
            actual_cover = actual_results.get(game_key, None)
            if actual_cover is not None:
                high_conf_games.append({
                    'game': game_key,
                    'consensus': row['consensus'],
                    'actual_cover': actual_cover,
                    'high_conf_count': high_conf_count
                })
    
    print(f"Games with 2+ high confidence models: {len(high_conf_games)}")
    for game in high_conf_games:
        print(f"  {game['game']}: Consensus {game['consensus']}, Actual {'Cover' if game['actual_cover'] else 'No Cover'}")
    
    # Save detailed results
    results_df.to_csv("week7/week7_model_performance_analysis.csv", index=False)
    print(f"\n✅ Detailed analysis saved to: week7/week7_model_performance_analysis.csv")
    
    return results_df

if __name__ == "__main__":
    analyze_week7_performance()
