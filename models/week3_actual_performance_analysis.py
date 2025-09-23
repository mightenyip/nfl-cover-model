#!/usr/bin/env python3
"""
Week 3 Actual Performance Analysis - All Three Models
"""

import pandas as pd
import numpy as np

def analyze_week3_actual_performance():
    """Analyze how all three models actually performed in Week 3"""
    
    print("=== Week 3 Actual Performance Analysis ===")
    print("All Three Models vs Actual Results")
    
    # Actual Week 3 results (from performance summary)
    actual_results = {
        ('Dolphins', 'Bills'): {'spread': 12.5, 'underdog': 'Dolphins', 'actual_cover': True},
        ('Falcons', 'Panthers'): {'spread': 5.5, 'underdog': 'Panthers', 'actual_cover': True},
        ('Packers', 'Browns'): {'spread': 8.5, 'underdog': 'Browns', 'actual_cover': True},
        ('Texans', 'Jaguars'): {'spread': 1.5, 'underdog': 'Texans', 'actual_cover': False},
        ('Bengals', 'Vikings'): {'spread': 3.0, 'underdog': 'Bengals', 'actual_cover': False},
        ('Steelers', 'Patriots'): {'spread': 1.5, 'underdog': 'Patriots', 'actual_cover': False},
        ('Rams', 'Eagles'): {'spread': 3.5, 'underdog': 'Rams', 'actual_cover': False},
        ('Jets', 'Buccaneers'): {'spread': 7.0, 'underdog': 'Jets', 'actual_cover': True},
        ('Colts', 'Titans'): {'spread': 3.5, 'underdog': 'Titans', 'actual_cover': False},
        ('Raiders', 'Commanders'): {'spread': 3.5, 'underdog': 'Raiders', 'actual_cover': False},
        ('Broncos', 'Chargers'): {'spread': 2.5, 'underdog': 'Broncos', 'actual_cover': False},
        ('Saints', 'Seahawks'): {'spread': 7.5, 'underdog': 'Saints', 'actual_cover': False},
        ('Cowboys', 'Bears'): {'spread': 1.5, 'underdog': 'Cowboys', 'actual_cover': False},
        ('Cardinals', '49ers'): {'spread': 1.5, 'underdog': 'Cardinals', 'actual_cover': True},
        ('Chiefs', 'Giants'): {'spread': 6.5, 'underdog': 'Giants', 'actual_cover': False},
        ('Lions', 'Ravens'): {'spread': 5.5, 'underdog': 'Lions', 'actual_cover': True}
    }
    
    # Load all three models
    models = {}
    
    # Model A
    try:
        models['A'] = pd.read_csv("model_a/model_a_week3_predictions.csv")
        print(f"✅ Loaded Model A: {len(models['A'])} games")
    except:
        print("❌ Model A not found")
    
    # Model B
    try:
        models['B'] = pd.read_csv("model_b/model_b_week3_predictions.csv")
        print(f"✅ Loaded Model B: {len(models['B'])} games")
    except:
        print("❌ Model B not found")
    
    # Model B v2
    try:
        models['B_v2'] = pd.read_csv("model_b/model_b_v2_week3_predictions.csv")
        print(f"✅ Loaded Model B v2: {len(models['B_v2'])} games")
    except:
        print("❌ Model B v2 not found")
    
    # Calculate actual underdog cover rate
    actual_covers = sum(result['actual_cover'] for result in actual_results.values())
    total_games = len(actual_results)
    actual_cover_rate = actual_covers / total_games
    
    print(f"\n=== Week 3 Reality Check ===")
    print(f"Actual Underdog Cover Rate: {actual_covers}/{total_games} ({actual_cover_rate:.1%})")
    print(f"This was a {'good' if actual_cover_rate > 0.5 else 'bad'} week for underdogs")
    
    # Analyze each model
    model_results = {}
    
    for model_name, model_df in models.items():
        print(f"\n=== Model {model_name} Performance ===")
        
        # Add actual results
        model_df['actual_cover'] = model_df.apply(
            lambda row: actual_results.get((row['away_team'], row['home_team']), {}).get('actual_cover', None), 
            axis=1
        )
        
        # Calculate correctness
        model_df['model_correct'] = model_df['predicted_cover'] == model_df['actual_cover']
        
        # Overall performance
        total_games = len(model_df)
        correct_predictions = model_df['model_correct'].sum()
        accuracy = correct_predictions / total_games
        
        predicted_covers = model_df['predicted_cover'].sum()
        predicted_cover_rate = predicted_covers / total_games
        
        model_results[model_name] = {
            'accuracy': accuracy,
            'correct': correct_predictions,
            'total': total_games,
            'predicted_covers': predicted_covers,
            'predicted_cover_rate': predicted_cover_rate
        }
        
        print(f"Accuracy: {correct_predictions}/{total_games} ({accuracy:.1%})")
        print(f"Predicted Underdog Covers: {predicted_covers}/{total_games} ({predicted_cover_rate:.1%})")
        print(f"Actual Underdog Covers: {actual_covers}/{total_games} ({actual_cover_rate:.1%})")
        
        # Performance by confidence level
        if 'confidence' in model_df.columns:
            print(f"\nPerformance by Confidence Level:")
            for conf in model_df['confidence'].unique():
                conf_data = model_df[model_df['confidence'] == conf]
                if not conf_data.empty:
                    conf_correct = conf_data['model_correct'].sum()
                    conf_total = len(conf_data)
                    conf_accuracy = conf_correct / conf_total if conf_total > 0 else 0
                    print(f"  {conf}: {conf_correct}/{conf_total} correct ({conf_accuracy:.1%})")
        
        # Biggest misses
        misses = model_df[~model_df['model_correct']].sort_values('cover_probability', ascending=False)
        if not misses.empty:
            print(f"\nBiggest Prediction Misses:")
            for _, row in misses.head(3).iterrows():
                game = f"{row['away_team']} @ {row['home_team']}"
                underdog = row['underdog_team']
                spread = f"+{row['spread_line']}"
                predicted = "Cover" if row['predicted_cover'] else "No Cover"
                actual = "Cover" if row['actual_cover'] else "No Cover"
                prob = row['cover_probability']
                confidence = row.get('confidence', 'N/A')
                
                print(f"  {game}: {underdog} {spread} - Predicted {predicted} ({prob:.1%}, {confidence}) but {underdog} {'covered' if actual else 'did not cover'}")
        
        # Success stories
        successes = model_df[model_df['model_correct']].sort_values('cover_probability', ascending=False)
        if not successes.empty:
            print(f"\nCorrect High Confidence Picks:")
            high_conf_successes = successes[successes.get('confidence', '').str.contains('HIGH|VERY_HIGH', na=False)]
            for _, row in high_conf_successes.head(3).iterrows():
                game = f"{row['away_team']} @ {row['home_team']}"
                underdog = row['underdog_team']
                spread = f"+{row['spread_line']}"
                predicted = "Cover" if row['predicted_cover'] else "No Cover"
                prob = row['cover_probability']
                confidence = row.get('confidence', 'N/A')
                
                print(f"  {game}: {underdog} {spread} - Correctly predicted {predicted} ({prob:.1%}, {confidence})")
    
    # Model comparison summary
    print(f"\n=== Model Performance Summary ===")
    print(f"{'Model':<10} {'Accuracy':<10} {'Predicted':<12} {'Actual':<8} {'Difference':<10}")
    print("-" * 55)
    
    for model_name, results in model_results.items():
        diff = results['predicted_cover_rate'] - actual_cover_rate
        print(f"Model {model_name:<6} {results['accuracy']:.1%}{'':<4} {results['predicted_cover_rate']:.1%}{'':<8} {actual_cover_rate:.1%}{'':<4} {diff:+.1%}")
    
    # Find the best performing model
    best_model = max(model_results.items(), key=lambda x: x[1]['accuracy'])
    print(f"\n🏆 Best Performing Model: Model {best_model[0]} ({best_model[1]['accuracy']:.1%} accuracy)")
    
    # Analysis of the week's characteristics
    print(f"\n=== Week 3 Characteristics ===")
    print(f"• Underdog cover rate: {actual_cover_rate:.1%}")
    print(f"• This was a {'strong' if actual_cover_rate > 0.6 else 'weak' if actual_cover_rate < 0.4 else 'average'} week for underdogs")
    print(f"• Models that predicted closer to {actual_cover_rate:.1%} would have performed better")
    
    # Which model was closest to reality?
    closest_to_reality = min(model_results.items(), key=lambda x: abs(x[1]['predicted_cover_rate'] - actual_cover_rate))
    print(f"• Model {closest_to_reality[0]} predicted closest to actual cover rate ({closest_to_reality[1]['predicted_cover_rate']:.1%} vs {actual_cover_rate:.1%})")
    
    return model_results

if __name__ == "__main__":
    analyze_week3_actual_performance()
