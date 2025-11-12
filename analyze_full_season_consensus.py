#!/usr/bin/env python3
"""
Analyze consensus performance (AB, AE, BE) across Weeks 1-10
"""

import pandas as pd
import os
import glob

def load_week_results(week_num):
    """Load actual results for a week"""
    results_file = f"data/week{week_num}_ats_results.csv"
    if os.path.exists(results_file):
        return pd.read_csv(results_file)
    return None

def load_individual_model_predictions(week_num):
    """Load individual model predictions and combine them"""
    models = {}
    
    # Try to load Model A
    model_a_files = [
        f"models/model_a/model_a_week{week_num}_predictions.csv",
        f"predictions/model_a_week{week_num}_predictions.csv",
    ]
    for file in model_a_files:
        if os.path.exists(file):
            models['A'] = pd.read_csv(file)
            break
    
    # Try to load Model B
    model_b_files = [
        f"models/model_b/model_b_week{week_num}_predictions.csv",
        f"predictions/model_b_week{week_num}_predictions.csv",
    ]
    for file in model_b_files:
        if os.path.exists(file):
            models['B'] = pd.read_csv(file)
            break
    
    # Try to load Model E
    model_e_files = [
        f"models/model_e/model_e_week{week_num}_predictions.csv",
        f"predictions/model_e_week{week_num}_predictions.csv",
    ]
    for file in model_e_files:
        if os.path.exists(file):
            models['E'] = pd.read_csv(file)
            break
    
    return models

def load_combined_predictions(week_num):
    """Load combined predictions file"""
    combined_files = [
        f"predictions/week{week_num}_all_models_predictions.csv",
        f"week{week_num}/week{week_num}_all_models_comparison.csv",
        f"models/week{week_num}_all_models_predictions.csv",
    ]
    
    for file in combined_files:
        if os.path.exists(file):
            df = pd.read_csv(file)
            # Check if it has the columns we need
            has_a = 'Model_A_Cover' in df.columns or 'model_a_prediction' in df.columns or 'Model_A_Pred' in df.columns
            has_b = 'Model_B_Cover' in df.columns or 'model_b_prediction' in df.columns or 'Model_B_Pred' in df.columns
            has_e = 'Model_E_Cover' in df.columns or 'model_e_prediction' in df.columns or 'Model_E_Pred' in df.columns
            
            if has_a and has_b and has_e:
                return df
    return None

def normalize_predictions(df, week_num):
    """Normalize different prediction formats to a standard format"""
    result = df.copy()
    
    # Create game column if it doesn't exist
    if 'game' not in result.columns:
        if 'Game' in result.columns:
            result['game'] = result['Game']
        elif 'away_team' in result.columns and 'home_team' in result.columns:
            result['game'] = result['away_team'] + ' @ ' + result['home_team']
    
    # Normalize Model A predictions
    if 'Model_A_Cover' in result.columns:
        result['model_a_cover'] = result['Model_A_Cover']
    elif 'model_a_prediction' in result.columns:
        result['model_a_cover'] = result['model_a_prediction'] == 'Cover'
    elif 'Model_A_Pred' in result.columns:
        result['model_a_cover'] = result['Model_A_Pred'] == 'Cover'
    elif 'predicted_cover' in result.columns and 'model' in str(result.columns).lower():
        # Might be a single model file
        pass
    
    # Normalize Model B predictions
    if 'Model_B_Cover' in result.columns:
        result['model_b_cover'] = result['Model_B_Cover']
    elif 'model_b_prediction' in result.columns:
        result['model_b_cover'] = result['model_b_prediction'] == 'Cover'
    elif 'Model_B_Pred' in result.columns:
        result['model_b_cover'] = result['Model_B_Pred'] == 'Cover'
    
    # Normalize Model E predictions
    if 'Model_E_Cover' in result.columns:
        result['model_e_cover'] = result['Model_E_Cover']
    elif 'model_e_prediction' in result.columns:
        result['model_e_cover'] = result['model_e_prediction'] == 'Cover'
    elif 'Model_E_Pred' in result.columns:
        result['model_e_cover'] = result['Model_E_Pred'] == 'Cover'
    
    return result

def analyze_week(week_num):
    """Analyze a single week"""
    results = load_week_results(week_num)
    predictions = load_combined_predictions(week_num)
    
    if results is None or predictions is None:
        return None
    
    # Normalize predictions
    predictions = normalize_predictions(predictions, week_num)
    
    # Check if we have the required columns
    required_cols = ['game', 'model_a_cover', 'model_b_cover', 'model_e_cover']
    if not all(col in predictions.columns for col in required_cols):
        return None
    
    # Merge with results
    merged = predictions.merge(
        results[['game', 'underdog_covered']],
        on='game',
        how='inner'
    )
    
    if len(merged) == 0:
        return None
    
    # Calculate consensus
    # AB consensus (A and B agree)
    ab_consensus = merged[
        (merged['model_a_cover'] == merged['model_b_cover'])
    ]
    ab_correct = (ab_consensus['model_a_cover'] == ab_consensus['underdog_covered']).sum()
    ab_total = len(ab_consensus)
    
    # AE consensus (A and E agree)
    ae_consensus = merged[
        (merged['model_a_cover'] == merged['model_e_cover'])
    ]
    ae_correct = (ae_consensus['model_a_cover'] == ae_consensus['underdog_covered']).sum()
    ae_total = len(ae_consensus)
    
    # BE consensus (B and E agree)
    be_consensus = merged[
        (merged['model_b_cover'] == merged['model_e_cover'])
    ]
    be_correct = (be_consensus['model_b_cover'] == be_consensus['underdog_covered']).sum()
    be_total = len(be_consensus)
    
    return {
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
    }

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
            print(f"Week {week_num}: ✅")
        else:
            print(f"Week {week_num}: ❌ (no data)")
    
    if not all_results:
        print("\n❌ No data found for any weeks")
        return
    
    # Create summary DataFrame
    df = pd.DataFrame(all_results)
    
    # Print weekly breakdown
    print("\n" + "="*80)
    print("WEEKLY BREAKDOWN")
    print("="*80)
    print(f"{'Week':<6} {'Games':<8} {'AB Agree':<10} {'AB Acc':<10} {'AE Agree':<10} {'AE Acc':<10} {'BE Agree':<10} {'BE Acc':<10}")
    print("-"*80)
    
    for _, row in df.iterrows():
        print(f"{int(row['week']):<6} {int(row['total_games']):<8} {int(row['ab_agree']):<10} {row['ab_accuracy']:<10.1%} "
              f"{int(row['ae_agree']):<10} {row['ae_accuracy']:<10.1%} {int(row['be_agree']):<10} {row['be_accuracy']:<10.1%}")
    
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
    print(f"   Total Games with Agreement: {ab_total_agree}")
    print(f"   Correct Predictions: {ab_total_correct}")
    print(f"   Overall Accuracy: {ab_overall_acc:.1%}")
    print(f"   Coverage: {ab_total_agree/total_games:.1%} of all games")
    
    print(f"\n📊 Consensus AE (Models A & E agree):")
    print(f"   Total Games with Agreement: {ae_total_agree}")
    print(f"   Correct Predictions: {ae_total_correct}")
    print(f"   Overall Accuracy: {ae_overall_acc:.1%}")
    print(f"   Coverage: {ae_total_agree/total_games:.1%} of all games")
    
    print(f"\n📊 Consensus BE (Models B & E agree):")
    print(f"   Total Games with Agreement: {be_total_agree}")
    print(f"   Correct Predictions: {be_total_correct}")
    print(f"   Overall Accuracy: {be_overall_acc:.1%}")
    print(f"   Coverage: {be_total_agree/total_games:.1%} of all games")
    
    # Find best consensus
    consensus_accuracies = {
        'AB': ab_overall_acc,
        'AE': ae_overall_acc,
        'BE': be_overall_acc
    }
    
    best_consensus = max(consensus_accuracies, key=consensus_accuracies.get)
    print(f"\n🏆 Best Consensus: {best_consensus} ({consensus_accuracies[best_consensus]:.1%})")
    
    # Save results
    df.to_csv("data/full_season_consensus_performance.csv", index=False)
    print(f"\n✅ Results saved to data/full_season_consensus_performance.csv")
    
    return df

if __name__ == "__main__":
    main()

