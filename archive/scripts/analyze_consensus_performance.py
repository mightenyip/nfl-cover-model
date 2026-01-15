#!/usr/bin/env python3
"""
Analyze consensus performance for Models A, B, E across all weeks
Consensus combinations: AB, AE, BE
"""

import pandas as pd
import glob
import os

def load_week_results(week_num):
    """Load actual results for a week"""
    results_file = f"data/ats_results/week{week_num}/week{week_num}_ats_results.csv"
    if os.path.exists(results_file):
        return pd.read_csv(results_file)
    return None

def load_week_predictions(week_num):
    """Load predictions for a week"""
    # Try different file formats
    pred_files = [
        f"predictions/week{week_num}_all_models_predictions.csv",
        f"predictions/week{week_num}_consensus_abe_predictions.csv",
        f"models/week{week_num}_all_models_predictions.csv",
    ]
    
    for pred_file in pred_files:
        if os.path.exists(pred_file):
            df = pd.read_csv(pred_file)
            # Check if it has the required columns
            if 'Model_A_Cover' in df.columns or 'model_a_prediction' in df.columns:
                return df
    return None

def analyze_consensus_performance():
    """Analyze consensus performance across all weeks"""
    
    print("="*80)
    print("CONSENSUS PERFORMANCE ANALYSIS - MODELS A, B, E")
    print("="*80)
    
    # Find all available weeks
    week_results = {}
    week_predictions = {}
    
    for week_num in range(1, 12):  # Weeks 1-11
        results = load_week_results(week_num)
        predictions = load_week_predictions(week_num)
        
        if results is not None and predictions is not None:
            week_results[week_num] = results
            week_predictions[week_num] = predictions
    
    print(f"\nFound data for weeks: {sorted(week_results.keys())}")
    
    # Track consensus performance
    ab_results = {'correct': 0, 'total': 0}
    ae_results = {'correct': 0, 'total': 0}
    be_results = {'correct': 0, 'total': 0}
    
    all_week_results = []
    
    for week_num in sorted(week_results.keys()):
        results = week_results[week_num]
        predictions = week_predictions[week_num]
        
        # Merge predictions with results
        merged = predictions.merge(
            results[['game', 'underdog_covered']],
            on='game',
            how='inner'
        )
        
        if len(merged) == 0:
            continue
        
        # Calculate consensus for each pair
        # AB consensus (A and B agree)
        ab_consensus = merged[
            (merged['Model_A_Cover'] == merged['Model_B_Cover'])
        ]
        ab_correct = (ab_consensus['Model_A_Cover'] == ab_consensus['underdog_covered']).sum()
        ab_total = len(ab_consensus)
        
        # AE consensus (A and E agree)
        ae_consensus = merged[
            (merged['Model_A_Cover'] == merged['Model_E_Cover'])
        ]
        ae_correct = (ae_consensus['Model_A_Cover'] == ae_consensus['underdog_covered']).sum()
        ae_total = len(ae_consensus)
        
        # BE consensus (B and E agree)
        be_consensus = merged[
            (merged['Model_B_Cover'] == merged['Model_E_Cover'])
        ]
        be_correct = (be_consensus['Model_B_Cover'] == be_consensus['underdog_covered']).sum()
        be_total = len(be_consensus)
        
        # Accumulate totals
        ab_results['correct'] += ab_correct
        ab_results['total'] += ab_total
        ae_results['correct'] += ae_correct
        ae_results['total'] += ae_total
        be_results['correct'] += be_correct
        be_results['total'] += be_total
        
        all_week_results.append({
            'week': week_num,
            'total_games': len(merged),
            'ab_agree': ab_total,
            'ab_correct': ab_correct,
            'ab_accuracy': ab_correct / ab_total if ab_total > 0 else 0,
            'ae_agree': ae_total,
            'ae_correct': ae_correct,
            'ae_accuracy': ae_correct / ae_total if ae_total > 0 else 0,
            'be_agree': be_total,
            'be_correct': be_correct,
            'be_accuracy': be_correct / be_total if be_total > 0 else 0,
        })
    
    # Print weekly breakdown
    print("\n" + "="*80)
    print("WEEKLY BREAKDOWN")
    print("="*80)
    print(f"{'Week':<6} {'Games':<8} {'AB Agree':<10} {'AB Acc':<10} {'AE Agree':<10} {'AE Acc':<10} {'BE Agree':<10} {'BE Acc':<10}")
    print("-"*80)
    
    for result in all_week_results:
        print(f"{result['week']:<6} {result['total_games']:<8} {result['ab_agree']:<10} {result['ab_accuracy']:<10.1%} "
              f"{result['ae_agree']:<10} {result['ae_accuracy']:<10.1%} {result['be_agree']:<10} {result['be_accuracy']:<10.1%}")
    
    # Print overall summary
    print("\n" + "="*80)
    print("OVERALL CONSENSUS PERFORMANCE")
    print("="*80)
    
    ab_acc = ab_results['correct'] / ab_results['total'] if ab_results['total'] > 0 else 0
    ae_acc = ae_results['correct'] / ae_results['total'] if ae_results['total'] > 0 else 0
    be_acc = be_results['correct'] / be_results['total'] if be_results['total'] > 0 else 0
    
    print(f"\n📊 Consensus AB (Models A & B agree):")
    print(f"   Accuracy: {ab_acc:.1%} ({ab_results['correct']}/{ab_results['total']})")
    print(f"   Games with agreement: {ab_results['total']}")
    
    print(f"\n📊 Consensus AE (Models A & E agree):")
    print(f"   Accuracy: {ae_acc:.1%} ({ae_results['correct']}/{ae_results['total']})")
    print(f"   Games with agreement: {ae_results['total']}")
    
    print(f"\n📊 Consensus BE (Models B & E agree):")
    print(f"   Accuracy: {be_acc:.1%} ({be_results['correct']}/{be_results['total']})")
    print(f"   Games with agreement: {be_results['total']}")
    
    # Find best consensus
    consensus_accuracies = {
        'AB': ab_acc,
        'AE': ae_acc,
        'BE': be_acc
    }
    
    best_consensus = max(consensus_accuracies, key=consensus_accuracies.get)
    print(f"\n🏆 Best Consensus: {best_consensus} ({consensus_accuracies[best_consensus]:.1%})")
    
    return all_week_results

if __name__ == "__main__":
    analyze_consensus_performance()

