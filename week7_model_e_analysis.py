#!/usr/bin/env python3
"""
Week 7 Model E Performance Analysis
Analyzes how Model E performed in predicting Week 7 outcomes
"""

import pandas as pd
import numpy as np

def analyze_model_e_performance():
    """Analyze Model E performance against actual Week 7 results"""
    
    print("=== Week 7 Model E Performance Analysis ===")
    
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
    
    # Load Model E predictions
    model_e_df = pd.read_csv("models/model_e/model_e_v1_week7_predictions.csv")
    
    print(f"Analyzing Model E predictions for {len(model_e_df)} games...")
    
    # Create results analysis
    results_data = []
    
    for _, row in model_e_df.iterrows():
        game_key = f"{row['away_team']} @ {row['home_team']}"
        actual_cover = actual_results.get(game_key, None)
        
        if actual_cover is None:
            print(f"Warning: No actual result found for {game_key}")
            continue
            
        # Parse Model E predictions
        model_e_pred = row['predicted_cover']
        model_e_correct = model_e_pred == actual_cover
        model_e_confidence = row['confidence']
        model_e_prob = row['cover_probability']
        
        results_data.append({
            'game': game_key,
            'underdog': row['underdog_team'],
            'spread': row['spread_line'],
            'actual_cover': actual_cover,
            'model_e_pred': model_e_pred,
            'model_e_correct': model_e_correct,
            'model_e_confidence': model_e_confidence,
            'model_e_probability': model_e_prob
        })
    
    results_df = pd.DataFrame(results_data)
    
    # Calculate Model E accuracy
    model_e_accuracy = results_df['model_e_correct'].mean()
    
    print(f"\n=== Model E Week 7 Performance ===")
    print(f"Model E Accuracy: {model_e_accuracy:.1%} ({results_df['model_e_correct'].sum()}/{len(results_df)})")
    
    # Compare with other models from previous analysis
    print(f"\n=== Model Comparison (Week 7) ===")
    print(f"Model A: 60.0% (9/15)")
    print(f"Model B v2: 40.0% (6/15)")
    print(f"Model C: 80.0% (12/15)")
    print(f"Model D: 46.7% (7/15)")
    print(f"Model E: {model_e_accuracy:.1%} ({results_df['model_e_correct'].sum()}/{len(results_df)})")
    print(f"Consensus: 80.0% (12/15)")
    
    # Find Model E's ranking
    model_accuracies = {
        'Model C': 0.80,
        'Consensus': 0.80,
        'Model A': 0.60,
        'Model E': model_e_accuracy,
        'Model D': 0.467,
        'Model B v2': 0.40
    }
    
    sorted_models = sorted(model_accuracies.items(), key=lambda x: x[1], reverse=True)
    model_e_rank = next(i for i, (model, acc) in enumerate(sorted_models) if model == 'Model E') + 1
    
    print(f"\n🏆 Model E Ranking: #{model_e_rank} out of 6 models")
    
    # Analyze confidence levels
    confidence_analysis = results_df.groupby('model_e_confidence')['model_e_correct'].agg(['count', 'sum', 'mean'])
    print(f"\n=== Model E Confidence Analysis ===")
    for conf_level in confidence_analysis.index:
        count = confidence_analysis.loc[conf_level, 'count']
        correct = confidence_analysis.loc[conf_level, 'sum']
        accuracy = confidence_analysis.loc[conf_level, 'mean']
        print(f"{conf_level}: {accuracy:.1%} ({correct}/{count})")
    
    # Show high confidence picks
    high_conf_games = results_df[results_df['model_e_confidence'].isin(['HIGH', 'VERY_HIGH'])]
    print(f"\n=== Model E High Confidence Picks ===")
    print(f"High Confidence Games: {len(high_conf_games)}")
    for _, row in high_conf_games.iterrows():
        status = "✅" if row['model_e_correct'] else "❌"
        print(f"  {status} {row['game']}: {row['underdog']} +{row['spread']} ({row['model_e_confidence']}, {row['model_e_probability']:.1%})")
    
    # Detailed game-by-game analysis
    print(f"\n=== Model E Game-by-Game Analysis ===")
    for _, row in results_df.iterrows():
        print(f"\n{row['game']}: {row['underdog']} +{row['spread']}")
        print(f"  Actual: {'Cover' if row['actual_cover'] else 'No Cover'}")
        print(f"  Model E: {'Cover' if row['model_e_pred'] else 'No Cover'} ({row['model_e_confidence']}, {row['model_e_probability']:.1%}) {'✅' if row['model_e_correct'] else '❌'}")
    
    # Analyze the 3 games that actually covered
    actual_covers = results_df[results_df['actual_cover'] == True]
    print(f"\n=== Model E on Actual Underdog Covers ===")
    print(f"Games where underdogs actually covered: {len(actual_covers)}")
    for _, row in actual_covers.iterrows():
        status = "✅" if row['model_e_correct'] else "❌"
        print(f"  {status} {row['game']}: Model E predicted {'Cover' if row['model_e_pred'] else 'No Cover'}")
    
    # Save detailed results
    results_df.to_csv("week7/week7_model_e_performance_analysis.csv", index=False)
    print(f"\n✅ Model E analysis saved to: week7/week7_model_e_performance_analysis.csv")
    
    return results_df

if __name__ == "__main__":
    analyze_model_e_performance()
