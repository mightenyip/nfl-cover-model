#!/usr/bin/env python3
"""
Create cumulative consensus performance file for Weeks 1-14
Focus on consensus predictions (Models A, B, E) and actual results
"""

import pandas as pd
import numpy as np
import os

def load_week_predictions(week_num):
    """Load consensus predictions for a week"""
    
    # Try predictions_final.csv first
    predictions_final_file = f"predictions/week{week_num}_predictions_final.csv"
    if os.path.exists(predictions_final_file):
        df = pd.read_csv(predictions_final_file)
        # Convert consensus_prediction to boolean (Cover = True, No Cover = False)
        if 'consensus_prediction' in df.columns:
            df['consensus_cover'] = df['consensus_prediction'] == 'Cover'
            return df
    
    # Try week14 analysis format (has consensus_pred column)
    if week_num == 14:
        week_analysis_file = f"week{week_num}/week{week_num}_model_performance_analysis.csv"
        if os.path.exists(week_analysis_file):
            df = pd.read_csv(week_analysis_file)
            if 'consensus_pred' in df.columns:
                df['consensus_cover'] = df['consensus_pred'] == 'Cover'
                return df
    
    return None

def load_week_actual_results(week_num):
    """Load actual results for a week"""
    
    # Try actual_results_analysis.csv
    results_file = f"data/week{week_num}_actual_results_analysis.csv"
    if os.path.exists(results_file):
        df = pd.read_csv(results_file)
        # Handle actual_cover column (could be True/False, Yes/No, or boolean)
        if 'actual_cover' in df.columns:
            def convert_cover(x):
                if pd.isna(x):
                    return None
                if isinstance(x, bool):
                    return x
                if isinstance(x, str):
                    return x.upper() in ['TRUE', 'YES', 'YES', '✓', '1', 'T']
                return bool(x)
            df['actual_cover'] = df['actual_cover'].apply(convert_cover)
            return df
    
    # Try week performance analysis files
    week_analysis_file = f"week{week_num}/week{week_num}_model_performance_analysis.csv"
    if os.path.exists(week_analysis_file):
        df = pd.read_csv(week_analysis_file)
        if 'actual_cover' in df.columns:
            def convert_cover(x):
                if pd.isna(x):
                    return None
                if isinstance(x, bool):
                    return x
                if isinstance(x, str):
                    return x.upper() in ['TRUE', 'YES', 'YES', '✓', '1', 'T']
                return bool(x)
            df['actual_cover'] = df['actual_cover'].apply(convert_cover)
            return df
    
    # Try week14 analysis format (in week14 folder)
    if week_num == 14:
        week_analysis_file = f"week{week_num}/week{week_num}_model_performance_analysis.csv"
        if os.path.exists(week_analysis_file):
            df = pd.read_csv(week_analysis_file)
            if 'actual_cover' in df.columns:
                def convert_cover(x):
                    if pd.isna(x):
                        return None
                    if isinstance(x, bool):
                        return x
                    if isinstance(x, str):
                        return x.upper() in ['TRUE', 'YES', 'YES', '✓', '1', 'T']
                    return bool(x)
                df['actual_cover'] = df['actual_cover'].apply(convert_cover)
                return df
    
    return None

def merge_predictions_and_results(week_num):
    """Merge predictions and results for a week"""
    
    predictions = load_week_predictions(week_num)
    results = load_week_actual_results(week_num)
    
    # Strategy 1: Use predictions_final.csv and merge with actual results
    if predictions is not None and 'consensus_cover' in predictions.columns:
        if results is not None and 'actual_cover' in results.columns:
            # Merge on game
            if 'game' in predictions.columns and 'game' in results.columns:
                merged = predictions.merge(
                    results[['game', 'actual_cover']],
                    on='game',
                    how='inner'
                )
                # Calculate consensus_correct, but preserve NaN for pushes
                def calc_correct(row):
                    if pd.isna(row['actual_cover']):
                        return None  # Push
                    return row['consensus_cover'] == row['actual_cover']
                merged['consensus_correct'] = merged.apply(calc_correct, axis=1)
                return merged
        # If no results file, we can't determine correctness
        return None
    
    # Strategy 2: Use actual_results_analysis.csv which has consensus_pred and consensus_correct
    if results is not None:
        if 'consensus_correct' in results.columns:
            # Check if consensus_pred exists to get predictions
            if 'consensus_pred' in results.columns:
                # Convert consensus_pred to boolean
                results['consensus_cover'] = results['consensus_pred'].apply(
                    lambda x: True if x in [True, 'True', 'Cover', 'COVER', 'YES', 'Yes', '✓'] 
                    else False if x in [False, 'False', 'No Cover', 'NO COVER', 'NO', 'No', '✗'] 
                    else None
                )
                # Convert consensus_correct to boolean
                results['consensus_correct'] = results['consensus_correct'].apply(
                    lambda x: True if x in [True, 'True', '✓', '1', 'CORRECT'] 
                    else False if x in [False, 'False', '✗', '0', 'INCORRECT'] 
                    else None
                )
                return results
            elif 'consensus_correct' in results.columns:
                # Just has consensus_correct, convert it
                results['consensus_correct'] = results['consensus_correct'].apply(
                    lambda x: True if x in [True, 'True', '✓', '1', 'CORRECT'] 
                    else False if x in [False, 'False', '✗', '0', 'INCORRECT'] 
                    else None
                )
                # Try to reconstruct consensus_pred from model predictions
                if all(col in results.columns for col in ['model_a_pred', 'model_b_pred', 'model_e_pred']):
                    def get_consensus(row):
                        votes = sum([
                            row['model_a_pred'] in [True, 'True', 'Cover', 'COVER'],
                            row['model_b_pred'] in [True, 'True', 'Cover', 'COVER'],
                            row['model_e_pred'] in [True, 'True', 'Cover', 'COVER']
                        ])
                        return votes >= 2
                    results['consensus_cover'] = results.apply(get_consensus, axis=1)
                return results
    
    return None

def analyze_all_weeks():
    """Analyze consensus performance for weeks 1-14"""
    
    print("="*80)
    print("CONSENSUS PERFORMANCE ANALYSIS - WEEKS 1-14")
    print("="*80)
    print()
    
    weekly_data = []
    
    for week_num in range(1, 15):
        print(f"Processing Week {week_num}...", end=" ")
        
        merged = merge_predictions_and_results(week_num)
        
        if merged is None:
            print("⚠️  No data available")
            continue
        
        # Calculate consensus accuracy
        if 'consensus_correct' in merged.columns:
            # Filter out pushes (None/NaN values)
            non_push_games = merged[merged['consensus_correct'].notna()]
            total_games = len(merged)  # Total games including pushes
            non_push_total = len(non_push_games)  # Games that count toward accuracy
            correct = non_push_games['consensus_correct'].sum() if non_push_total > 0 else 0
            incorrect = non_push_total - correct
            accuracy = correct / non_push_total if non_push_total > 0 else 0
            
            # Count predictions (from all games, including pushes)
            if 'consensus_cover' in merged.columns or 'consensus_prediction' in merged.columns:
                if 'consensus_cover' in merged.columns:
                    cover_predictions = merged['consensus_cover'].sum()
                else:
                    cover_predictions = (merged['consensus_prediction'] == 'Cover').sum()
                no_cover_predictions = total_games - cover_predictions
            else:
                cover_predictions = None
                no_cover_predictions = None
            
            # Count actual results (excluding pushes)
            if 'actual_cover' in merged.columns:
                actual_covers = non_push_games['actual_cover'].sum() if non_push_total > 0 else 0
                actual_no_covers = non_push_total - actual_covers
            else:
                actual_covers = None
                actual_no_covers = None
            
            weekly_data.append({
                'week': week_num,
                'total_games': total_games,
                'consensus_correct': correct,
                'consensus_incorrect': incorrect,
                'consensus_accuracy': accuracy,
                'consensus_cover_predictions': cover_predictions,
                'consensus_no_cover_predictions': no_cover_predictions,
                'actual_covers': actual_covers,
                'actual_no_covers': actual_no_covers,
            })
            
            print(f"✅ {correct}/{total_games} correct ({accuracy:.1%})")
        else:
            print("⚠️  Missing consensus_correct column")
    
    if not weekly_data:
        print("\n❌ No data compiled")
        return None
    
    # Create DataFrame
    df = pd.DataFrame(weekly_data)
    
    # Calculate totals
    total_games = df['total_games'].sum()
    total_correct = df['consensus_correct'].sum()
    total_accuracy = total_correct / total_games if total_games > 0 else 0
    
    # Add totals row
    totals_row = {
        'week': 'TOTAL',
        'total_games': total_games,
        'consensus_correct': total_correct,
        'consensus_incorrect': total_games - total_correct,
        'consensus_accuracy': total_accuracy,
        'consensus_cover_predictions': df['consensus_cover_predictions'].sum() if df['consensus_cover_predictions'].notna().any() else None,
        'consensus_no_cover_predictions': df['consensus_no_cover_predictions'].sum() if df['consensus_no_cover_predictions'].notna().any() else None,
        'actual_covers': df['actual_covers'].sum() if df['actual_covers'].notna().any() else None,
        'actual_no_covers': df['actual_no_covers'].sum() if df['actual_no_covers'].notna().any() else None,
    }
    
    # Append totals
    df = pd.concat([df, pd.DataFrame([totals_row])], ignore_index=True)
    
    # Format accuracy as percentage
    df['consensus_accuracy_pct'] = (df['consensus_accuracy'] * 100).apply(lambda x: f"{x:.1f}%")
    
    # Save to file
    output_file = "data/model_performance/cumulative_model_performance.csv"
    os.makedirs("data/model_performance", exist_ok=True)
    
    # Format for output
    output_df = df[['week', 'total_games', 'consensus_correct', 'consensus_incorrect', 
                    'consensus_accuracy_pct', 'consensus_cover_predictions', 
                    'consensus_no_cover_predictions', 'actual_covers', 'actual_no_covers']].copy()
    
    output_df.columns = ['Week', 'Total_Games', 'Consensus_Correct', 'Consensus_Incorrect',
                         'Consensus_Accuracy', 'Consensus_Cover_Pred', 'Consensus_No_Cover_Pred',
                         'Actual_Covers', 'Actual_No_Covers']
    
    output_df.to_csv(output_file, index=False)
    
    print("\n" + "="*80)
    print("SUMMARY")
    print("="*80)
    print(f"Total Weeks Analyzed: {len(weekly_data)}")
    print(f"Total Games: {total_games}")
    print(f"Consensus Correct: {total_correct}")
    print(f"Consensus Accuracy: {total_accuracy:.1%}")
    print()
    print("Weekly Breakdown:")
    for _, row in df[df['week'] != 'TOTAL'].iterrows():
        print(f"  Week {int(row['week'])}: {int(row['consensus_correct'])}/{int(row['total_games'])} ({row['consensus_accuracy']:.1%})")
    print()
    print(f"✅ Saved to {output_file}")
    
    return output_df

if __name__ == "__main__":
    analyze_all_weeks()

