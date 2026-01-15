#!/usr/bin/env python3
"""
Analyze consensus performance (AB, AE, BE) across Weeks 1-10
Using individual model prediction files
"""

import pandas as pd
import os

def load_week_results(week_num):
    """Load actual results for a week"""
    results_file = f"data/ats_results/week{week_num}/week{week_num}_ats_results.csv"
    if os.path.exists(results_file):
        return pd.read_csv(results_file)
    return None

def load_individual_models(week_num):
    """Load individual model predictions"""
    models = {}
    
    # Model A
    model_a_files = [
        f"models/model_a/model_a_week{week_num}_predictions.csv",
        f"predictions/model_a_week{week_num}_predictions.csv",
    ]
    for file in model_a_files:
        if os.path.exists(file):
            models['A'] = pd.read_csv(file)
            break
    
    # Model B
    model_b_files = [
        f"models/model_b/model_b_week{week_num}_predictions.csv",
        f"models/model_b/model_b_v2_week{week_num}_predictions.csv",
        f"predictions/model_b_week{week_num}_predictions.csv",
    ]
    for file in model_b_files:
        if os.path.exists(file):
            models['B'] = pd.read_csv(file)
            break
    
    # Model E
    model_e_files = [
        f"models/model_e/model_e_week{week_num}_predictions.csv",
        f"predictions/model_e_week{week_num}_predictions.csv",
    ]
    for file in model_e_files:
        if os.path.exists(file):
            models['E'] = pd.read_csv(file)
            break
    
    return models

def analyze_week(week_num):
    """Analyze a single week"""
    results = load_week_results(week_num)
    models = load_individual_models(week_num)
    
    if results is None:
        return None
    
    if len(models) < 2:  # Need at least 2 models
        return None
    
    # Combine models
    combined = None
    
    for model_name, model_df in models.items():
        if 'game' not in model_df.columns:
            continue
        
        model_cols = model_df[['game', 'predicted_cover']].copy()
        model_cols = model_cols.rename(columns={'predicted_cover': f'model_{model_name.lower()}_cover'})
        
        if combined is None:
            combined = model_cols
        else:
            combined = combined.merge(model_cols, on='game', how='outer')
    
    if combined is None or len(combined) == 0:
        return None
    
    # Merge with results
    merged = combined.merge(
        results[['game', 'underdog_covered']],
        on='game',
        how='inner'
    )
    
    if len(merged) == 0:
        return None
    
    # Calculate consensus
    week_result = {
        'week': week_num,
        'total_games': len(merged),
    }
    
    # AB consensus
    if 'model_a_cover' in merged.columns and 'model_b_cover' in merged.columns:
        ab_consensus = merged[
            (merged['model_a_cover'] == merged['model_b_cover'])
        ]
        ab_correct = (ab_consensus['model_a_cover'] == ab_consensus['underdog_covered']).sum()
        ab_total = len(ab_consensus)
        week_result.update({
            'ab_agree': ab_total,
            'ab_correct': ab_correct,
            'ab_accuracy': ab_correct / ab_total if ab_total > 0 else 0,
        })
    
    # AE consensus
    if 'model_a_cover' in merged.columns and 'model_e_cover' in merged.columns:
        ae_consensus = merged[
            (merged['model_a_cover'] == merged['model_e_cover'])
        ]
        ae_correct = (ae_consensus['model_a_cover'] == ae_consensus['underdog_covered']).sum()
        ae_total = len(ae_consensus)
        week_result.update({
            'ae_agree': ae_total,
            'ae_correct': ae_correct,
            'ae_accuracy': ae_correct / ae_total if ae_total > 0 else 0,
        })
    
    # BE consensus
    if 'model_b_cover' in merged.columns and 'model_e_cover' in merged.columns:
        be_consensus = merged[
            (merged['model_b_cover'] == merged['model_e_cover'])
        ]
        be_correct = (be_consensus['model_b_cover'] == be_consensus['underdog_covered']).sum()
        be_total = len(be_consensus)
        week_result.update({
            'be_agree': be_total,
            'be_correct': be_correct,
            'be_accuracy': be_correct / be_total if be_total > 0 else 0,
        })
    
    return week_result

def main():
    """Analyze consensus performance across weeks 1-10"""
    
    print("="*80)
    print("FULL SEASON CONSENSUS PERFORMANCE ANALYSIS - WEEKS 1-10")
    print("Models A, B, E - Consensus Pairs: AB, AE, BE")
    print("="*80)
    
    all_results = []
    
    for week_num in range(1, 11):
        result = analyze_week(week_num)
        if result:
            all_results.append(result)
            print(f"Week {week_num}: ✅ ({result.get('total_games', 0)} games)")
        else:
            print(f"Week {week_num}: ❌ (no data)")
    
    if not all_results:
        print("\n❌ No data found for any weeks")
        return
    
    # Create summary DataFrame
    df = pd.DataFrame(all_results)
    
    # Fill missing values with 0
    for col in ['ab_agree', 'ab_correct', 'ae_agree', 'ae_correct', 'be_agree', 'be_correct']:
        if col not in df.columns:
            df[col] = 0
        df[col] = df[col].fillna(0)
    
    # Calculate accuracies
    for col in ['ab_accuracy', 'ae_accuracy', 'be_accuracy']:
        if col not in df.columns:
            df[col] = 0
    
    # Print weekly breakdown
    print("\n" + "="*80)
    print("WEEKLY BREAKDOWN")
    print("="*80)
    print(f"{'Week':<6} {'Games':<8} {'AB Agree':<10} {'AB Acc':<10} {'AE Agree':<10} {'AE Acc':<10} {'BE Agree':<10} {'BE Acc':<10}")
    print("-"*80)
    
    for _, row in df.iterrows():
        ab_agree = int(row.get('ab_agree', 0))
        ae_agree = int(row.get('ae_agree', 0))
        be_agree = int(row.get('be_agree', 0))
        ab_acc = row.get('ab_accuracy', 0)
        ae_acc = row.get('ae_accuracy', 0)
        be_acc = row.get('be_accuracy', 0)
        
        print(f"{int(row['week']):<6} {int(row['total_games']):<8} {ab_agree:<10} {ab_acc:<10.1%} "
              f"{ae_agree:<10} {ae_acc:<10.1%} {be_agree:<10} {be_acc:<10.1%}")
    
    # Calculate totals
    total_games = df['total_games'].sum()
    ab_total_agree = df['ab_agree'].sum()
    ab_total_correct = df['ab_correct'].sum()
    ae_total_agree = df['ae_agree'].sum()
    ae_total_correct = df['ae_correct'].sum()
    be_total_agree = df['be_agree'].sum()
    be_total_correct = df['be_correct'].sum()
    
    ab_overall_acc = ab_total_correct / ab_total_agree if ab_total_agree > 0 else 0
    ae_overall_acc = ae_total_correct / ae_total_agree if ae_total_agree > 0 else 0
    be_overall_acc = be_total_correct / be_total_agree if be_total_agree > 0 else 0
    
    # Print overall summary
    print("\n" + "="*80)
    print("OVERALL PERFORMANCE (WEEKS 1-10)")
    print("="*80)
    
    print(f"\n📊 Consensus AB (Models A & B agree):")
    print(f"   Total Games with Agreement: {int(ab_total_agree)}")
    print(f"   Correct Predictions: {int(ab_total_correct)}")
    print(f"   Overall Accuracy: {ab_overall_acc:.1%}")
    if total_games > 0:
        print(f"   Coverage: {ab_total_agree/total_games:.1%} of all games")
    
    print(f"\n📊 Consensus AE (Models A & E agree):")
    print(f"   Total Games with Agreement: {int(ae_total_agree)}")
    print(f"   Correct Predictions: {int(ae_total_correct)}")
    print(f"   Overall Accuracy: {ae_overall_acc:.1%}")
    if total_games > 0:
        print(f"   Coverage: {ae_total_agree/total_games:.1%} of all games")
    
    print(f"\n📊 Consensus BE (Models B & E agree):")
    print(f"   Total Games with Agreement: {int(be_total_agree)}")
    print(f"   Correct Predictions: {int(be_total_correct)}")
    print(f"   Overall Accuracy: {be_overall_acc:.1%}")
    if total_games > 0:
        print(f"   Coverage: {be_total_agree/total_games:.1%} of all games")
    
    # Find best consensus
    consensus_accuracies = {}
    if ab_total_agree > 0:
        consensus_accuracies['AB'] = ab_overall_acc
    if ae_total_agree > 0:
        consensus_accuracies['AE'] = ae_overall_acc
    if be_total_agree > 0:
        consensus_accuracies['BE'] = be_overall_acc
    
    if consensus_accuracies:
        best_consensus = max(consensus_accuracies, key=consensus_accuracies.get)
        print(f"\n🏆 Best Consensus: {best_consensus} ({consensus_accuracies[best_consensus]:.1%})")
    
    # Save results
    df.to_csv("data/model_performance/legacy/full_season_consensus_performance.csv", index=False)
    print(f"\n✅ Results saved to data/model_performance/legacy/full_season_consensus_performance.csv")
    
    return df

if __name__ == "__main__":
    main()

