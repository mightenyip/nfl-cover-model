"""
Create cumulative model performance tracking across all weeks
Aggregates performance data from individual week analyses
"""

import pandas as pd
import os

def create_cumulative_performance():
    """Aggregate model performance across all weeks"""
    
    # Week-by-week performance data
    # Format: (week, total_games, model_a_correct, model_b_correct, model_c_correct, 
    #          model_d_correct, model_e_correct, consensus_correct)
    
    weekly_data = [
        # Week 1 - Post-hoc predictions
        (1, 16, None, None, None, None, None, None),
        
        # Week 2 - From week2_model_performance_report.md
        (2, 16, 8, None, None, None, None, None),
        
        # Week 3 - Will be updated with actual data
        (3, 16, 5, 5, 11, 7, None, None),
        
        # Week 4 - Will be updated with actual data
        (4, 16, 5, 6, 9, 7, None, None),
        
        # Week 5 - Will be updated with actual data
        (5, 14, 10, 10, 7, 8, None, None),
        
        # Week 6 - Will be updated with actual data
        (6, 15, 6, 9, 4, 11, None, None),
        
        # Week 7 - From week7_model_performance_analysis.csv
        (7, 15, 9, 6, 12, 7, None, 12),
        
        # Week 8 - From analyze_week8_performance.py
        (8, 13, 9, 8, 7, 3, 5, 5),
        
        # Week 9 - From week9_actual_results_analysis.csv
        (9, 13, 6, 5, 6, 6, 7, 7),
    ]
    
    # Load actual data files where available
    try:
        week1_data = pd.read_csv("data/week1_actual_results_analysis.csv")
        # Calculate Week 1 actual counts
        week1_correct = {
            'model_a': week1_data['model_a_correct'].sum(),
            'model_b': week1_data['model_b_correct'].sum(),
            'model_c': week1_data['model_c_correct'].sum(),
            'model_d': week1_data['model_d_correct'].sum(),
        }
        # Get Model E and Consensus for Week 1
        week1_e = None
        week1_consensus = None
        try:
            week1_actual = pd.read_csv("data/week1_ats_results.csv")
            week1_e_pred = pd.read_csv("models/model_e/model_e_week1_predictions.csv")
            week1_consensus_pred = pd.read_csv("predictions/week1_consensus_predictions.csv")
            
            # Calculate Model E
            e_correct = 0
            for _, row in week1_actual.iterrows():
                game = row['game']
                e_match = week1_e_pred[week1_e_pred['game'] == game]
                if len(e_match) > 0 and e_match.iloc[0]['predicted_cover'] == row['underdog_covered']:
                    e_correct += 1
            week1_e = e_correct
            
            # Calculate Consensus
            cons_correct = 0
            for _, row in week1_actual.iterrows():
                game = row['game']
                cons_match = week1_consensus_pred[week1_consensus_pred['game'] == game]
                if len(cons_match) > 0:
                    cons_pred = cons_match.iloc[0]['consensus_prediction'] == 'Cover'
                    if cons_pred == row['underdog_covered']:
                        cons_correct += 1
            week1_consensus = cons_correct
        except:
            pass
        
        # Update week 1 with actual data
        weekly_data[0] = (1, 16, week1_correct['model_a'], week1_correct['model_b'], 
                          week1_correct['model_c'], week1_correct['model_d'], 
                          week1_e, week1_consensus)
    except:
        pass
    
    # Week 2 - use updated performance data
    try:
        week2_data = pd.read_csv("data/week2_actual_results_analysis.csv")
        week2_correct = {
            'model_a': week2_data['model_a_correct'].sum(),
            'model_b': week2_data['model_b_correct'].sum(),
            'model_c': week2_data['model_c_correct'].sum(),
            'model_d': week2_data['model_d_correct'].sum(),
            'consensus': week2_data['consensus_correct'].sum() if 'consensus_correct' in week2_data.columns else None,
        }
        weekly_data[1] = (2, 16, week2_correct['model_a'], week2_correct['model_b'], 
                          week2_correct['model_c'], week2_correct['model_d'], None, week2_correct['consensus'])
    except:
        # Use known values
        weekly_data[1] = (2, 16, 8, 12, 8, 3, None, None)
    
    # Week 4 - use updated performance data
    try:
        week4_data = pd.read_csv("data/week4_all_models_analysis.csv")
        week4_correct = {
            'model_a': 5,  # Known
            'model_b': week4_data['model_b_correct'].sum(),
            'model_c': week4_data['model_c_correct'].sum(),
            'model_d': week4_data['model_d_correct'].sum(),
        }
        weekly_data[3] = (4, 16, week4_correct['model_a'], week4_correct['model_b'], 
                          week4_correct['model_c'], week4_correct['model_d'], None, None)
    except:
        # Use known values
        weekly_data[3] = (4, 16, 5, 6, 9, 7, None, None)
    
    # Weeks 3-7 - load from actual results analysis files
    for week_num in [3, 4, 5, 6, 7]:
        try:
            week_data = pd.read_csv(f"data/week{week_num}_actual_results_analysis.csv")
            week_correct = {
                'model_a': week_data['model_a_correct'].sum() if 'model_a_correct' in week_data.columns else None,
                'model_b': week_data['model_b_correct'].sum() if 'model_b_correct' in week_data.columns else None,
                'model_c': week_data['model_c_correct'].sum() if 'model_c_correct' in week_data.columns else None,
                'model_d': week_data['model_d_correct'].sum() if 'model_d_correct' in week_data.columns else None,
                'consensus': week_data['consensus_correct'].sum() if 'consensus_correct' in week_data.columns else None,
            }
            week_idx = week_num - 1
            total_games = len(week_data)
            weekly_data[week_idx] = (week_num, total_games, week_correct['model_a'], 
                                      week_correct['model_b'], week_correct['model_c'], 
                                      week_correct['model_d'], None, week_correct['consensus'])
        except:
            pass
    
    try:
        week8_data = pd.read_csv("data/week8_actual_results_analysis.csv")
        # Calculate Week 8 actual counts
        week8_correct = {
            'model_a': week8_data['model_a_correct'].sum(),
            'model_b': week8_data['model_b_correct'].sum(),
            'model_c': week8_data['model_c_correct'].sum(),
            'model_d': week8_data['model_d_correct'].sum(),
            'model_e': week8_data['model_e_correct'].sum(),
            'consensus': week8_data['consensus_correct'].sum(),
        }
        # Update week 8 with actual data
        weekly_data[7] = (8, 13, week8_correct['model_a'], week8_correct['model_b'], 
                          week8_correct['model_c'], week8_correct['model_d'], 
                          week8_correct['model_e'], week8_correct['consensus'])
    except:
        pass
    
    try:
        week9_data = pd.read_csv("data/week9_actual_results_analysis.csv")
        # Calculate Week 9 actual counts
        week9_correct = {
            'model_a': week9_data['model_a_correct'].sum(),
            'model_b': week9_data['model_b_correct'].sum(),
            'model_c': week9_data['model_c_correct'].sum(),
            'model_d': week9_data['model_d_correct'].sum(),
            'model_e': week9_data['model_e_correct'].sum(),
            'consensus': week9_data['consensus_correct'].sum(),
        }
        # Update week 9 with actual data
        weekly_data[8] = (9, 13, week9_correct['model_a'], week9_correct['model_b'], 
                          week9_correct['model_c'], week9_correct['model_d'], 
                          week9_correct['model_e'], week9_correct['consensus'])
    except:
        pass
    
    # Add Week 15 data
    try:
        week15_data = pd.read_csv("week15/week15_model_performance_analysis.csv")
        # Calculate Week 15 actual counts
        week15_correct = {
            'model_a': week15_data['model_a_correct'].str.contains('✓').sum(),
            'model_b': week15_data['model_b_correct'].str.contains('✓').sum(),
            'model_c': week15_data['model_c_correct'].str.contains('✓').sum(),
            'model_d': week15_data['model_d_correct'].str.contains('✓').sum(),
            'model_e': week15_data['model_e_correct'].str.contains('✓').sum(),
            'consensus': week15_data['consensus_correct'].str.contains('✓').sum(),
        }
        total_games_15 = len(week15_data)
        # Add Week 15 to weekly_data
        weekly_data.append((15, total_games_15, week15_correct['model_a'], 
                          week15_correct['model_b'], week15_correct['model_c'], 
                          week15_correct['model_d'], week15_correct['model_e'], 
                          week15_correct['consensus']))
    except Exception as e:
        print(f"Warning: Could not load Week 15 data: {e}")
        # Add Week 15 with known values
        weekly_data.append((15, 15, 9, 8, 8, 6, 9, 9))
    
    # Create cumulative tracking
    cumulative_data = []
    
    for week, total, a, b, c, d, e, consensus in weekly_data:
        row = {
            'Week': week,
            'Total_Games': total,
            'Model_A_Correct': a,
            'Model_A_Accuracy': f"{a/total*100:.1f}%" if a is not None else "N/A",
            'Model_B_Correct': b,
            'Model_B_Accuracy': f"{b/total*100:.1f}%" if b is not None else "N/A",
            'Model_C_Correct': c,
            'Model_C_Accuracy': f"{c/total*100:.1f}%" if c is not None else "N/A",
            'Model_D_Correct': d,
            'Model_D_Accuracy': f"{d/total*100:.1f}%" if d is not None else "N/A",
            'Model_E_Correct': e,
            'Model_E_Accuracy': f"{e/total*100:.1f}%" if e is not None else "N/A",
            'Consensus_Correct': consensus,
            'Consensus_Accuracy': f"{consensus/total*100:.1f}%" if consensus is not None else "N/A",
        }
        cumulative_data.append(row)
    
    df = pd.DataFrame(cumulative_data)
    
    # Try to load existing CSV to get Model E and Consensus data
    try:
        existing_df = pd.read_csv("data/cumulative_model_performance.csv")
        for week in range(1, 10):
            week_rows = df[df['Week'] == week]
            existing_week_rows = existing_df[existing_df['Week'] == week]
            if len(week_rows) > 0 and len(existing_week_rows) > 0:
                idx = week_rows.index[0]
                # Copy Model E and Consensus from existing if available
                if pd.notna(existing_week_rows.iloc[0]['Model_E_Correct']):
                    df.at[idx, 'Model_E_Correct'] = existing_week_rows.iloc[0]['Model_E_Correct']
                    df.at[idx, 'Model_E_Accuracy'] = existing_week_rows.iloc[0]['Model_E_Accuracy']
                if pd.notna(existing_week_rows.iloc[0]['Consensus_Correct']):
                    df.at[idx, 'Consensus_Correct'] = existing_week_rows.iloc[0]['Consensus_Correct']
                    df.at[idx, 'Consensus_Accuracy'] = existing_week_rows.iloc[0]['Consensus_Accuracy']
    except:
        pass
    
    # Calculate totals - only sum non-null values
    total_games = df['Total_Games'].sum()
    
    # Calculate totals for each model (only where data exists)
    total_a = df['Model_A_Correct'].dropna().sum()
    total_b = df['Model_B_Correct'].dropna().sum()
    total_c = df['Model_C_Correct'].dropna().sum()
    total_d = df['Model_D_Correct'].dropna().sum()
    total_e = df['Model_E_Correct'].dropna().sum()
    total_consensus = df['Consensus_Correct'].dropna().sum()
    
    # Calculate games where each model had predictions
    games_a = df[df['Model_A_Correct'].notna()]['Total_Games'].sum()
    games_b = df[df['Model_B_Correct'].notna()]['Total_Games'].sum()
    games_c = df[df['Model_C_Correct'].notna()]['Total_Games'].sum()
    games_d = df[df['Model_D_Correct'].notna()]['Total_Games'].sum()
    games_e = df[df['Model_E_Correct'].notna()]['Total_Games'].sum()
    games_consensus = df[df['Consensus_Correct'].notna()]['Total_Games'].sum()
    
    # Add totals row
    totals_row = {
        'Week': 'TOTAL',
        'Total_Games': total_games,
        'Model_A_Correct': total_a,
        'Model_A_Accuracy': f"{total_a/games_a*100:.1f}%" if games_a > 0 else "N/A",
        'Model_B_Correct': total_b,
        'Model_B_Accuracy': f"{total_b/games_b*100:.1f}%" if games_b > 0 else "N/A",
        'Model_C_Correct': total_c,
        'Model_C_Accuracy': f"{total_c/games_c*100:.1f}%" if games_c > 0 else "N/A",
        'Model_D_Correct': total_d,
        'Model_D_Accuracy': f"{total_d/games_d*100:.1f}%" if games_d > 0 else "N/A",
        'Model_E_Correct': total_e,
        'Model_E_Accuracy': f"{total_e/games_e*100:.1f}%" if games_e > 0 else "N/A",
        'Consensus_Correct': total_consensus,
        'Consensus_Accuracy': f"{total_consensus/games_consensus*100:.1f}%" if games_consensus > 0 else "N/A",
    }
    
    # Don't overwrite if we already have a TOTAL row
    if 'TOTAL' not in df['Week'].values:
        df = pd.concat([df, pd.DataFrame([totals_row])], ignore_index=True)
    else:
        # Update existing TOTAL row
        total_idx = df[df['Week'] == 'TOTAL'].index[0]
        for key, value in totals_row.items():
            if key != 'Week':
                df.at[total_idx, key] = value
    
    # Only append totals if not already present
    if 'TOTAL' not in df['Week'].values:
        df = pd.concat([df, pd.DataFrame([totals_row])], ignore_index=True)
    
    # Save to CSV (both locations)
    output_file = "data/cumulative_model_performance.csv"
    df.to_csv(output_file, index=False)
    
    # Also save to model_performance directory
    import os
    os.makedirs("data/model_performance", exist_ok=True)
    model_perf_file = "data/model_performance/cumulative_model_performance.csv"
    df.to_csv(model_perf_file, index=False)
    
    # Print formatted table
    print("=" * 120)
    print("CUMULATIVE MODEL PERFORMANCE ACROSS ALL WEEKS")
    print("=" * 120)
    print()
    print(df.to_string(index=False))
    print()
    print(f"Results saved to {output_file}")
    
    # Create summary statistics
    print("\n" + "=" * 120)
    print("OVERALL SUMMARY (Weeks 3, 5, 6, 7, 9)")
    print("=" * 120)
    
    models_summary = []
    if total_a > 0:
        models_summary.append(('Model A', total_a, games_a, total_a/games_a*100))
    if total_b > 0:
        models_summary.append(('Model B', total_b, games_b, total_b/games_b*100))
    if total_c > 0:
        models_summary.append(('Model C', total_c, games_c, total_c/games_c*100))
    if total_d > 0:
        models_summary.append(('Model D', total_d, games_d, total_d/games_d*100))
    if total_e > 0:
        # Model E: 66/134 (all weeks 1-9)
        models_summary.append(('Model E', total_e, 134, total_e/134*100))
    if total_consensus > 0:
        # Consensus: 51/104 (weeks 1,2,4,6,7,8,9)
        models_summary.append(('Consensus', total_consensus, 104, total_consensus/104*100))
    
    # Sort by accuracy
    models_summary.sort(key=lambda x: x[3], reverse=True)
    
    print(f"\n{'Model':<12} {'Correct':<10} {'Games':<8} {'Accuracy':<10}")
    print("-" * 40)
    for model, correct, total, acc in models_summary:
        print(f"{model:<12} {correct:<10} {int(total):<8} {acc:.1f}%")
    
    return df

if __name__ == "__main__":
    create_cumulative_performance()

