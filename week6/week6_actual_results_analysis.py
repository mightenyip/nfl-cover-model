#!/usr/bin/env python3
"""
Week 6 NFL Model Performance Analysis - 2025 Season
Compare model predictions vs actual results from ESPN
"""

import pandas as pd
import numpy as np

# Actual Week 6 2025 Results from ESPN
actual_results = {
    'Eagles @ Giants': {'favorite': 'Eagles', 'underdog': 'Giants', 'spread': 7.5, 'actual_winner': 'Giants', 'actual_score': '17-34', 'underdog_covered': True},
    'Broncos @ Jets': {'favorite': 'Broncos', 'underdog': 'Jets', 'spread': 7.5, 'actual_winner': 'Broncos', 'actual_score': '13-11', 'underdog_covered': True},
    'Cardinals @ Colts': {'favorite': 'Colts', 'underdog': 'Cardinals', 'spread': 6.5, 'actual_winner': 'Colts', 'actual_score': '27-31', 'underdog_covered': True},
    'Chargers @ Dolphins': {'favorite': 'Chargers', 'underdog': 'Dolphins', 'spread': 4.5, 'actual_winner': 'Chargers', 'actual_score': '29-27', 'underdog_covered': True},
    'Patriots @ Saints': {'favorite': 'Patriots', 'underdog': 'Saints', 'spread': 3.5, 'actual_winner': 'Patriots', 'actual_score': '25-19', 'underdog_covered': True},
    'Browns @ Steelers': {'favorite': 'Steelers', 'underdog': 'Browns', 'spread': 5.0, 'actual_winner': 'Steelers', 'actual_score': '9-23', 'underdog_covered': False},
    'Cowboys @ Panthers': {'favorite': 'Cowboys', 'underdog': 'Panthers', 'spread': 3.5, 'actual_winner': 'Panthers', 'actual_score': '27-30', 'underdog_covered': True},
    'Seahawks @ Jaguars': {'favorite': 'Jaguars', 'underdog': 'Seahawks', 'spread': 1.5, 'actual_winner': 'Seahawks', 'actual_score': '20-12', 'underdog_covered': True},
    'Rams @ Ravens': {'favorite': 'Rams', 'underdog': 'Ravens', 'spread': 7.5, 'actual_winner': 'Rams', 'actual_score': '17-3', 'underdog_covered': False},
    'Titans @ Raiders': {'favorite': 'Raiders', 'underdog': 'Titans', 'spread': 4.5, 'actual_winner': 'Raiders', 'actual_score': '10-20', 'underdog_covered': False},
    'Bengals @ Packers': {'favorite': 'Packers', 'underdog': 'Bengals', 'spread': 14.5, 'actual_winner': 'Packers', 'actual_score': '18-27', 'underdog_covered': True},
    '49ers @ Buccaneers': {'favorite': 'Buccaneers', 'underdog': '49ers', 'spread': 3.0, 'actual_winner': 'Buccaneers', 'actual_score': '19-30', 'underdog_covered': True},
    'Lions @ Chiefs': {'favorite': 'Chiefs', 'underdog': 'Lions', 'spread': 2.5, 'actual_winner': 'Chiefs', 'actual_score': '17-30', 'underdog_covered': False},
    'Bills @ Falcons': {'favorite': 'Bills', 'underdog': 'Falcons', 'spread': 4.5, 'actual_winner': 'Falcons', 'actual_score': '14-24', 'underdog_covered': True},
    'Bears @ Commanders': {'favorite': 'Commanders', 'underdog': 'Bears', 'spread': 4.5, 'actual_winner': 'Bears', 'actual_score': '25-24', 'underdog_covered': True}
}

# Model predictions from CSV
model_predictions = pd.read_csv('/Users/mightenyip/Documents/GitHub/nfl-cover-model/models/week6_all_models_predictions.csv')

def analyze_model_performance():
    """Analyze how each model performed against actual results"""
    
    results = []
    
    for _, row in model_predictions.iterrows():
        game = row['Game']
        if game not in actual_results:
            continue
            
        actual = actual_results[game]
        
        # Skip games with incomplete results
        if actual['actual_winner'] == 'TBD':
            continue
            
        # Determine if underdog covered
        underdog_covered = actual['underdog_covered']
        
        # Check each model's prediction
        model_a_correct = (row['Model_A_Pred'] == 'Cover') == underdog_covered
        model_b_correct = (row['Model_B_Pred'] == 'Cover') == underdog_covered
        model_c_correct = (row['Model_C_Pred'] == 'Cover') == underdog_covered
        model_d_correct = (row['Model_D_Pred'] == 'Cover') == underdog_covered
        
        results.append({
            'Game': game,
            'Underdog_Covered': underdog_covered,
            'Model_A_Correct': model_a_correct,
            'Model_B_Correct': model_b_correct,
            'Model_C_Correct': model_c_correct,
            'Model_D_Correct': model_d_correct,
            'Model_A_Pred': row['Model_A_Pred'],
            'Model_B_Pred': row['Model_B_Pred'],
            'Model_C_Pred': row['Model_C_Pred'],
            'Model_D_Pred': row['Model_D_Pred'],
            'Actual_Result': f"{actual['actual_winner']} {actual['actual_score']}"
        })
    
    return pd.DataFrame(results)

def calculate_accuracy_metrics(df):
    """Calculate accuracy metrics for each model"""
    
    metrics = {}
    
    for model in ['Model_A', 'Model_B', 'Model_C', 'Model_D']:
        correct_col = f'{model}_Correct'
        total_games = len(df)
        correct_predictions = df[correct_col].sum()
        accuracy = (correct_predictions / total_games) * 100 if total_games > 0 else 0
        
        metrics[model] = {
            'Total_Games': total_games,
            'Correct_Predictions': correct_predictions,
            'Accuracy_Percentage': accuracy
        }
    
    return metrics

def main():
    print("🏈 Week 6 NFL Model Performance Analysis - 2025 Season")
    print("=" * 60)
    
    # Analyze performance
    results_df = analyze_model_performance()
    
    print(f"\n📊 Games with Complete Results: {len(results_df)}")
    print("\n🎯 Game-by-Game Results:")
    print("-" * 100)
    
    for _, row in results_df.iterrows():
        print(f"\n{row['Game']}")
        print(f"  Actual: {row['Actual_Result']} | Underdog Covered: {row['Underdog_Covered']}")
        print(f"  Model A: {row['Model_A_Pred']} {'✅' if row['Model_A_Correct'] else '❌'}")
        print(f"  Model B: {row['Model_B_Pred']} {'✅' if row['Model_B_Correct'] else '❌'}")
        print(f"  Model C: {row['Model_C_Pred']} {'✅' if row['Model_C_Correct'] else '❌'}")
        print(f"  Model D: {row['Model_D_Pred']} {'✅' if row['Model_D_Correct'] else '❌'}")
    
    # Calculate metrics
    metrics = calculate_accuracy_metrics(results_df)
    
    print(f"\n📈 Model Performance Summary:")
    print("-" * 50)
    
    for model, stats in metrics.items():
        print(f"{model}: {stats['Correct_Predictions']}/{stats['Total_Games']} ({stats['Accuracy_Percentage']:.1f}%)")
    
    # Find best performing model
    best_model = max(metrics.keys(), key=lambda x: metrics[x]['Accuracy_Percentage'])
    print(f"\n🏆 Best Performing Model: {best_model} ({metrics[best_model]['Accuracy_Percentage']:.1f}%)")
    
    # Calculate underdog cover rate
    underdog_covers = results_df['Underdog_Covered'].sum()
    total_games = len(results_df)
    underdog_rate = (underdog_covers / total_games) * 100
    print(f"\n📊 Week 6 Underdog Cover Rate: {underdog_covers}/{total_games} ({underdog_rate:.1f}%)")
    
    # Save detailed results
    results_df.to_csv('/Users/mightenyip/Documents/GitHub/nfl-cover-model/week6/week6_actual_performance.csv', index=False)
    print(f"\n💾 Detailed results saved to: week6_actual_performance.csv")

if __name__ == "__main__":
    main()
