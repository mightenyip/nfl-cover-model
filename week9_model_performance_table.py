"""
Week 9 Model Performance Table
Create a formatted table showing each model's predictions and results
"""

import pandas as pd

def create_performance_table():
    """Create a formatted table of model performance"""
    
    # Load the results
    df = pd.read_csv("data/week9_actual_results_analysis.csv")
    
    # Define model columns
    models = ['Model A', 'Model B', 'Model C', 'Model D', 'Model E', 'Consensus']
    model_cols = ['model_a', 'model_b', 'model_c', 'model_d', 'model_e', 'consensus']
    correct_cols = ['model_a_correct', 'model_b_correct', 'model_c_correct', 
                    'model_d_correct', 'model_e_correct', 'consensus_correct']
    
    print("=" * 140)
    print("WEEK 9 MODEL PERFORMANCE TABLE")
    print("=" * 140)
    print()
    
    # Create game-by-game table
    print(f"{'Game':<25} {'Spread':<8} {'Actual':<12} ", end="")
    for model in models:
        print(f"{model:<12}", end="")
    print()
    print("-" * 140)
    
    for _, row in df.iterrows():
        game = row['game']
        spread = row['spread']
        actual = "UNDERDOG ✅" if row['actual_cover'] else "FAVORITE ✅"
        
        # Truncate game name if too long
        if len(game) > 24:
            game = game[:21] + "..."
        
        print(f"{game:<25} {spread:<8} {actual:<12} ", end="")
        
        for i, model_col in enumerate(model_cols):
            pred_col = f"{model_col}_pred"
            correct_col = correct_cols[i]
            
            if row[pred_col] is not None and pd.notna(row[pred_col]):
                pred = "UNDERDOG" if row[pred_col] else "FAVORITE"
                correct = row[correct_col]
                symbol = "✅" if correct else "❌"
                print(f"{pred} {symbol:<4}", end="")
            else:
                print(f"{'N/A':<12}", end="")
        print()
    
    print()
    print("=" * 140)
    print("SUMMARY STATISTICS")
    print("=" * 140)
    print()
    
    # Summary table
    summary_data = []
    for i, model in enumerate(models):
        correct_col = correct_cols[i]
        correct = df[correct_col].sum()
        total = df[correct_col].notna().sum()
        accuracy = (correct / total * 100) if total > 0 else 0
        
        summary_data.append({
            'Model': model,
            'Correct': correct,
            'Total': total,
            'Accuracy': f"{accuracy:.1f}%"
        })
    
    summary_df = pd.DataFrame(summary_data)
    print(summary_df.to_string(index=False))
    print()
    
    # Detailed breakdown
    print("=" * 140)
    print("DETAILED BREAKDOWN")
    print("=" * 140)
    print()
    
    for i, model in enumerate(models):
        correct_col = correct_cols[i]
        pred_col = f"{model_cols[i]}_pred"
        
        correct = df[correct_col].sum()
        total = df[correct_col].notna().sum()
        accuracy = (correct / total * 100) if total > 0 else 0
        
        # Count predictions by type
        underdog_preds = df[pred_col].sum() if df[pred_col].dtype == bool else 0
        favorite_preds = total - underdog_preds
        
        # Count correct by prediction type
        underdog_correct = df[(df[pred_col] == True) & (df[correct_col] == True)].shape[0]
        favorite_correct = df[(df[pred_col] == False) & (df[correct_col] == False)].shape[0]
        
        print(f"{model}:")
        print(f"  Overall: {correct}/{total} ({accuracy:.1f}%)")
        print(f"  Underdog Predictions: {underdog_preds} ({underdog_correct} correct)")
        print(f"  Favorite Predictions: {favorite_preds} ({favorite_correct} correct)")
        print()

if __name__ == "__main__":
    create_performance_table()

