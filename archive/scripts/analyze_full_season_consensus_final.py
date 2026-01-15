#!/usr/bin/env python3
"""
Analyze consensus performance (AB, AE, BE) across Weeks 1-10
Using individual model prediction files directly
"""

import pandas as pd
import os
import glob

def load_week_results(week_num):
    """Load actual results for a week"""
    # Try standard results file first
    results_file = f"data/ats_results/week{week_num}/week{week_num}_ats_results.csv"
    if os.path.exists(results_file):
        df = pd.read_csv(results_file)
        # Ensure it has the columns we need
        if 'game' in df.columns and 'underdog_covered' in df.columns:
            return df
    
    # Try alternative results file (for week 9)
    alt_results_file = f"data/actual_results/week{week_num}/week{week_num}_actual_results_analysis.csv"
    if os.path.exists(alt_results_file):
        df = pd.read_csv(alt_results_file)
        # Check if it has the columns we need
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

def load_comparison_file(week_num):
    """Load comparison file that has all models together"""
    comparison_files = [
        f"week{week_num}/week{week_num}_all_models_comparison.csv",
        f"models/week{week_num}_all_models_predictions.csv",
        f"predictions/week{week_num}_all_models_predictions.csv",
    ]
    
    for file_path in comparison_files:
        if os.path.exists(file_path):
            try:
                df = pd.read_csv(file_path)
                # Check if it has model predictions
                has_a = 'model_a_prediction' in df.columns or 'Model_A_Cover' in df.columns or 'Model_A_Pred' in df.columns
                has_b = 'model_b_prediction' in df.columns or 'Model_B_Cover' in df.columns or 'Model_B_Pred' in df.columns
                has_e = 'model_e_prediction' in df.columns or 'Model_E_Cover' in df.columns or 'Model_E_Pred' in df.columns
                
                if has_a and has_b and has_e:
                    return df
            except:
                pass
    return None

def load_individual_models(week_num):
    """Load individual model predictions"""
    models = {}
    
    # First try to load comparison file
    comparison_df = load_comparison_file(week_num)
    if comparison_df is not None:
        # Extract individual model predictions from comparison file
        if 'game' not in comparison_df.columns:
            if 'away_team' in comparison_df.columns and 'home_team' in comparison_df.columns:
                comparison_df['game'] = comparison_df['away_team'] + ' @ ' + comparison_df['home_team']
        
        # Extract Model A
        if 'model_a_prediction' in comparison_df.columns:
            model_a = comparison_df[['game']].copy()
            model_a['predicted_cover'] = comparison_df['model_a_prediction'] == 'Cover'
            models['A'] = model_a
        elif 'Model_A_Cover' in comparison_df.columns:
            model_a = comparison_df[['game']].copy()
            model_a['predicted_cover'] = comparison_df['Model_A_Cover']
            models['A'] = model_a
        
        # Extract Model B
        if 'model_b_prediction' in comparison_df.columns:
            model_b = comparison_df[['game']].copy()
            model_b['predicted_cover'] = comparison_df['model_b_prediction'] == 'Cover'
            models['B'] = model_b
        elif 'Model_B_Cover' in comparison_df.columns:
            model_b = comparison_df[['game']].copy()
            model_b['predicted_cover'] = comparison_df['Model_B_Cover']
            models['B'] = model_b
        
        # Extract Model E
        if 'model_e_prediction' in comparison_df.columns:
            model_e = comparison_df[['game']].copy()
            model_e['predicted_cover'] = comparison_df['model_e_prediction'] == 'Cover'
            models['E'] = model_e
        elif 'Model_E_Cover' in comparison_df.columns:
            model_e = comparison_df[['game']].copy()
            model_e['predicted_cover'] = comparison_df['Model_E_Cover']
            models['E'] = model_e
    
    # Then try to load individual files for any missing models
    for model in ['a', 'b', 'e']:
        if model.upper() not in models:
            file_path = find_model_file(week_num, model)
            if file_path:
                try:
                    df = pd.read_csv(file_path)
                    # Create game column if it doesn't exist
                    if 'game' not in df.columns:
                        if 'away_team' in df.columns and 'home_team' in df.columns:
                            df['game'] = df['away_team'] + ' @ ' + df['home_team']
                        else:
                            continue
                    
                    # Get predicted_cover column (handle different column names)
                    cover_col = None
                    for col in ['predicted_cover', 'Model_A_Cover', 'Model_B_Cover', 'Model_E_Cover']:
                        if col in df.columns:
                            cover_col = col
                            break
                    
                    if cover_col:
                        model_df = df[['game', cover_col]].copy()
                        model_df = model_df.rename(columns={cover_col: 'predicted_cover'})
                        # Ensure boolean type
                        if model_df['predicted_cover'].dtype != bool:
                            model_df['predicted_cover'] = model_df['predicted_cover'].astype(bool)
                        models[model.upper()] = model_df
                except Exception as e:
                    pass
    
    return models

def analyze_week(week_num):
    """Analyze a single week"""
    results = load_week_results(week_num)
    models = load_individual_models(week_num)
    
    if results is None:
        return None
    
    if len(models) < 2:  # Need at least 2 models
        return None
    
    # Combine models on 'game' column
    combined = None
    
    for model_name, model_df in models.items():
        if 'game' not in model_df.columns:
            continue
        
        # Get predicted_cover column (handle different column names)
        cover_col = None
        for col in ['predicted_cover', 'Model_A_Cover', 'Model_B_Cover', 'Model_E_Cover']:
            if col in model_df.columns:
                cover_col = col
                break
        
        if cover_col is None:
            continue
        
        model_cols = model_df[['game', cover_col]].copy()
        model_cols = model_cols.rename(columns={cover_col: f'model_{model_name.lower()}_cover'})
        
        # Ensure boolean type
        if model_cols[f'model_{model_name.lower()}_cover'].dtype != bool:
            model_cols[f'model_{model_name.lower()}_cover'] = model_cols[f'model_{model_name.lower()}_cover'].astype(bool)
        
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
        if len(ab_consensus) > 0:
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
        if len(ae_consensus) > 0:
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
        if len(be_consensus) > 0:
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
            models_found = []
            if result.get('ab_agree', 0) > 0:
                models_found.append('AB')
            if result.get('ae_agree', 0) > 0:
                models_found.append('AE')
            if result.get('be_agree', 0) > 0:
                models_found.append('BE')
            print(f"Week {week_num}: ✅ ({result.get('total_games', 0)} games, consensus: {', '.join(models_found)})")
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
        df[col] = df[col].fillna(0).astype(int)
    
    # Calculate accuracies
    for col in ['ab_accuracy', 'ae_accuracy', 'be_accuracy']:
        if col not in df.columns:
            df[col] = 0.0
    
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
        
        ab_str = f"{ab_acc:.1%}" if ab_agree > 0 else "N/A"
        ae_str = f"{ae_acc:.1%}" if ae_agree > 0 else "N/A"
        be_str = f"{be_acc:.1%}" if be_agree > 0 else "N/A"
        
        print(f"{int(row['week']):<6} {int(row['total_games']):<8} {ab_agree:<10} {ab_str:<10} "
              f"{ae_agree:<10} {ae_str:<10} {be_agree:<10} {be_str:<10}")
    
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

