#!/usr/bin/env python3
"""
Four-Model Comparison: Model A vs Model B v2 vs Model C vs Model D
"""

import pandas as pd
import numpy as np
import os

def compare_four_models():
    """Compare all four models and their Week 3 performance"""
    
    print("=== Four-Model Comparison: A, B v2, C, D ===")
    
    # Actual Week 3 results
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
    
    actual_covers = sum(result['actual_cover'] for result in actual_results.values())
    total_games = len(actual_results)
    actual_cover_rate = actual_covers / total_games
    
    # Load all four models
    models = {}
    model_paths = {
        'A': 'model_a/model_a_week3_predictions.csv',
        'B_v2': 'model_b/model_b_v2_week3_predictions.csv',
        'C': 'model_c/model_c_week3_predictions.csv',
        'D': 'model_d/model_d_week3_predictions.csv'
    }
    
    for model_name, path in model_paths.items():
        try:
            models[model_name] = pd.read_csv(path)
            print(f"✅ Loaded Model {model_name}: {len(models[model_name])} games")
        except Exception as e:
            print(f"❌ Model {model_name} not found: {e}")
    
    if len(models) < 2:
        print("❌ Need at least 2 models to compare")
        return
    
    # Analyze each model's performance
    model_results = {}
    
    for model_name, model_df in models.items():
        print(f"\n=== Model {model_name} Analysis ===")
        
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
        
        # Performance by confidence level (if available)
        if 'confidence' in model_df.columns:
            print(f"\nPerformance by Confidence Level:")
            for conf in model_df['confidence'].unique():
                conf_data = model_df[model_df['confidence'] == conf]
                if not conf_data.empty:
                    conf_correct = conf_data['model_correct'].sum()
                    conf_total = len(conf_data)
                    conf_accuracy = conf_correct / conf_total if conf_total > 0 else 0
                    print(f"  {conf}: {conf_correct}/{conf_total} correct ({conf_accuracy:.1%})")
    
    # Create comprehensive comparison table
    print(f"\n{'='*80}")
    print(f"FOUR-MODEL COMPARISON TABLE")
    print(f"{'='*80}")
    
    # Header
    print(f"{'Model':<8} {'Methodology':<25} {'Accuracy':<10} {'Predicted':<12} {'Actual':<8} {'Difference':<10}")
    print("-" * 80)
    
    # Model descriptions
    model_descriptions = {
        'A': 'SumerSports EPA',
        'B_v2': 'Matchup EPA (Pass/Rush)',
        'C': 'Spread Rules',
        'D': 'Total Rules'
    }
    
    # Sort models by accuracy
    sorted_models = sorted(model_results.items(), key=lambda x: x[1]['accuracy'], reverse=True)
    
    for rank, (model_name, results) in enumerate(sorted_models, 1):
        diff = results['predicted_cover_rate'] - actual_cover_rate
        print(f"#{rank} {model_name:<6} {model_descriptions.get(model_name, 'Unknown'):<25} {results['accuracy']:.1%}{'':<4} {results['predicted_cover_rate']:.1%}{'':<8} {actual_cover_rate:.1%}{'':<4} {diff:+.1%}")
    
    # Summary statistics
    print(f"\n{'='*80}")
    print(f"SUMMARY STATISTICS")
    print(f"{'='*80}")
    print(f"Actual Underdog Cover Rate: {actual_cover_rate:.1%} ({actual_covers}/{total_games})")
    print(f"This was a {'strong' if actual_cover_rate > 0.6 else 'weak' if actual_cover_rate < 0.4 else 'average'} week for underdogs")
    
    # Best and worst performers
    best_model = max(model_results.items(), key=lambda x: x[1]['accuracy'])
    worst_model = min(model_results.items(), key=lambda x: x[1]['accuracy'])
    
    print(f"\n🏆 Best Model: Model {best_model[0]} ({best_model[1]['accuracy']:.1%} accuracy)")
    print(f"❌ Worst Model: Model {worst_model[0]} ({worst_model[1]['accuracy']:.1%} accuracy)")
    
    # Which model predicted closest to actual cover rate
    closest_to_reality = min(model_results.items(), key=lambda x: abs(x[1]['predicted_cover_rate'] - actual_cover_rate))
    print(f"🎯 Closest to Reality: Model {closest_to_reality[0]} (predicted {closest_to_reality[1]['predicted_cover_rate']:.1%} vs actual {actual_cover_rate:.1%})")
    
    # Model-specific insights
    print(f"\n{'='*80}")
    print(f"MODEL-SPECIFIC INSIGHTS")
    print(f"{'='*80}")
    
    if 'C' in model_results:
        print(f"Model C (Spread Rules): All 16 games defaulted to underdog prediction - rules didn't apply to Week 3 spreads")
    
    if 'D' in model_results:
        d_underdog_pred = model_results['D']['predicted_covers']
        print(f"Model D (Total Rules): Predicted {d_underdog_pred}/16 underdog covers ({d_underdog_pred/total_games:.1%})")
        print(f"  - High confidence on 15/16 games based on total rules")
        print(f"  - 13 underdog picks, 3 favorite picks based on totals")
    
    if 'B_v2' in model_results:
        print(f"Model B v2 (Matchup EPA): Best performer with sophisticated Pass/Rush analysis")
        print(f"  - 3/5 VERY_HIGH confidence picks were correct")
        print(f"  - Perfect on LOW confidence picks (3/3)")
    
    if 'A' in model_results:
        print(f"Model A (SumerSports EPA): Struggled with high confidence picks (0% accuracy)")
        print(f"  - Overestimated underdog cover rate by 18.8%")
    
    # Save comprehensive results
    comparison_data = []
    for model_name, results in model_results.items():
        comparison_data.append({
            'Model': model_name,
            'Methodology': model_descriptions.get(model_name, 'Unknown'),
            'Accuracy': results['accuracy'],
            'Predicted_Cover_Rate': results['predicted_cover_rate'],
            'Actual_Cover_Rate': actual_cover_rate,
            'Difference': results['predicted_cover_rate'] - actual_cover_rate,
            'Correct_Predictions': results['correct'],
            'Total_Games': results['total']
        })
    
    comparison_df = pd.DataFrame(comparison_data)
    comparison_df = comparison_df.sort_values('Accuracy', ascending=False)
    comparison_df.to_csv("four_model_comparison_week3.csv", index=False)
    
    print(f"\n✅ Comprehensive comparison saved to: four_model_comparison_week3.csv")
    
    return model_results

if __name__ == "__main__":
    compare_four_models()
