#!/usr/bin/env python3
"""
Analyze individual model performance (A, B, E) across Weeks 1-10
"""

import pandas as pd
import os

def load_week_results(week_num):
    """Load actual results for a week"""
    results_file = f"data/ats_results/week{week_num}/week{week_num}_ats_results.csv"
    if os.path.exists(results_file):
        df = pd.read_csv(results_file)
        if 'game' in df.columns and 'underdog_covered' in df.columns:
            return df
    
    alt_results_file = f"data/actual_results/week{week_num}/week{week_num}_actual_results_analysis.csv"
    if os.path.exists(alt_results_file):
        df = pd.read_csv(alt_results_file)
        if 'game' in df.columns and 'actual_cover' in df.columns:
            df = df.rename(columns={'actual_cover': 'underdog_covered'})
            return df
    
    return None

def find_model_file(week_num, model_name):
    """Find model prediction file for a given week"""
    possible_paths = [
        f"models/model_{model_name.lower()}/model_{model_name.lower()}_week{week_num}_predictions.csv",
        f"models/model_{model_name.lower()}/model_{model_name.lower()}_v2_week{week_num}_predictions.csv",
        f"predictions/model_{model_name.lower()}_week{week_num}_predictions.csv",
    ]
    
    for path in possible_paths:
        if os.path.exists(path):
            return path
    return None

def load_model_predictions(week_num, model_name):
    """Load predictions for a specific model"""
    file_path = find_model_file(week_num, model_name)
    if not file_path:
        return None
    
    try:
        df = pd.read_csv(file_path)
        
        # Create game column if needed
        if 'game' not in df.columns:
            if 'away_team' in df.columns and 'home_team' in df.columns:
                df['game'] = df['away_team'] + ' @ ' + df['home_team']
            else:
                return None
        
        # Get predicted_cover column
        cover_col = None
        for col in ['predicted_cover', 'Model_A_Cover', 'Model_B_Cover', 'Model_E_Cover']:
            if col in df.columns:
                cover_col = col
                break
        
        if not cover_col:
            return None
        
        result = df[['game', cover_col]].copy()
        result = result.rename(columns={cover_col: 'predicted_cover'})
        
        # Ensure boolean type
        if result['predicted_cover'].dtype != bool:
            result['predicted_cover'] = result['predicted_cover'].astype(bool)
        
        return result
    except:
        return None

def analyze_model_performance():
    """Analyze individual model performance across all weeks"""
    
    print("="*80)
    print("INDIVIDUAL MODEL PERFORMANCE ANALYSIS - WEEKS 1-10")
    print("Models A, B, E")
    print("="*80)
    
    model_stats = {
        'A': {'correct': 0, 'total': 0, 'weeks': []},
        'B': {'correct': 0, 'total': 0, 'weeks': []},
        'E': {'correct': 0, 'total': 0, 'weeks': []}
    }
    
    weekly_results = []
    
    for week_num in range(1, 11):
        results = load_week_results(week_num)
        if results is None:
            continue
        
        week_stats = {'week': week_num, 'total_games': len(results)}
        
        for model_name in ['A', 'B', 'E']:
            predictions = load_model_predictions(week_num, model_name)
            if predictions is None:
                continue
            
            # Merge with results
            merged = predictions.merge(
                results[['game', 'underdog_covered']],
                on='game',
                how='inner'
            )
            
            if len(merged) == 0:
                continue
            
            # Calculate accuracy
            correct = (merged['predicted_cover'] == merged['underdog_covered']).sum()
            total = len(merged)
            accuracy = correct / total if total > 0 else 0
            
            # Update totals
            model_stats[model_name]['correct'] += correct
            model_stats[model_name]['total'] += total
            model_stats[model_name]['weeks'].append({
                'week': week_num,
                'correct': correct,
                'total': total,
                'accuracy': accuracy
            })
            
            week_stats[f'model_{model_name.lower()}_correct'] = correct
            week_stats[f'model_{model_name.lower()}_total'] = total
            week_stats[f'model_{model_name.lower()}_accuracy'] = accuracy
        
        weekly_results.append(week_stats)
    
    # Print weekly breakdown
    print("\n" + "="*80)
    print("WEEKLY BREAKDOWN")
    print("="*80)
    print(f"{'Week':<6} {'Games':<8} {'Model A':<15} {'Model B':<15} {'Model E':<15}")
    print("-"*80)
    
    for week_stat in weekly_results:
        week = week_stat['week']
        games = week_stat['total_games']
        
        a_str = "N/A"
        if 'model_a_accuracy' in week_stat:
            a_str = f"{week_stat['model_a_correct']}/{week_stat['model_a_total']} ({week_stat['model_a_accuracy']:.1%})"
        
        b_str = "N/A"
        if 'model_b_accuracy' in week_stat:
            b_str = f"{week_stat['model_b_correct']}/{week_stat['model_b_total']} ({week_stat['model_b_accuracy']:.1%})"
        
        e_str = "N/A"
        if 'model_e_accuracy' in week_stat:
            e_str = f"{week_stat['model_e_correct']}/{week_stat['model_e_total']} ({week_stat['model_e_accuracy']:.1%})"
        
        print(f"{week:<6} {games:<8} {a_str:<15} {b_str:<15} {e_str:<15}")
    
    # Print overall summary
    print("\n" + "="*80)
    print("OVERALL PERFORMANCE (WEEKS 1-10)")
    print("="*80)
    
    for model_name in ['A', 'B', 'E']:
        stats = model_stats[model_name]
        if stats['total'] > 0:
            accuracy = stats['correct'] / stats['total']
            print(f"\n📊 Model {model_name}:")
            print(f"   Total Games: {stats['total']}")
            print(f"   Correct Predictions: {stats['correct']}")
            print(f"   Overall Accuracy: {accuracy:.1%}")
            print(f"   Weeks with Data: {len(stats['weeks'])}")
    
    # Find best model
    model_accuracies = {}
    for model_name in ['A', 'B', 'E']:
        if model_stats[model_name]['total'] > 0:
            model_accuracies[model_name] = model_stats[model_name]['correct'] / model_stats[model_name]['total']
    
    if model_accuracies:
        best_model = max(model_accuracies, key=model_accuracies.get)
        print(f"\n🏆 Best Model: Model {best_model} ({model_accuracies[best_model]:.1%})")
        
        # Show ranking
        print(f"\n📈 Model Rankings:")
        sorted_models = sorted(model_accuracies.items(), key=lambda x: x[1], reverse=True)
        for rank, (model, acc) in enumerate(sorted_models, 1):
            print(f"   {rank}. Model {model}: {acc:.1%}")
    
    # Save results
    summary_data = []
    for model_name in ['A', 'B', 'E']:
        stats = model_stats[model_name]
        if stats['total'] > 0:
            summary_data.append({
                'model': model_name,
                'total_games': stats['total'],
                'correct': stats['correct'],
                'accuracy': stats['correct'] / stats['total'],
                'weeks_with_data': len(stats['weeks'])
            })
    
    summary_df = pd.DataFrame(summary_data)
    summary_df.to_csv("data/model_performance/legacy/individual_model_performance_summary.csv", index=False)
    print(f"\n✅ Results saved to data/model_performance/legacy/individual_model_performance_summary.csv")
    
    return model_stats

if __name__ == "__main__":
    analyze_model_performance()

