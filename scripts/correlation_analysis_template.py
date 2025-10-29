#!/usr/bin/env python3
"""
Template for analyzing correlation between matchup EPA differences and spread performance
"""

import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
import seaborn as sns
from scipy import stats

def analyze_matchup_epa_correlation(df):
    """
    Analyze correlation between matchup EPA differences and spread performance
    
    Parameters:
    df: DataFrame with columns:
        - matchupEPA_diff: matchupEPA_favorite - matchupEPA_underdog
        - margin_vs_spread: actual_game_margin - spread
        - actual_margin: actual game margin (favorite - underdog)
        - spread: betting spread
        - game: game identifier
    """
    
    print("=== Matchup EPA Correlation Analysis ===")
    print("=" * 50)
    
    # Calculate correlation
    correlation = df['matchupEPA_diff'].corr(df['margin_vs_spread'])
    
    print(f"Correlation between Matchup EPA Diff and Margin vs Spread: {correlation:.3f}")
    print()
    
    # Interpretation
    if correlation > 0.3:
        print("✅ STRONG POSITIVE CORRELATION")
        print("   Favorites with higher matchup EPA differences tend to outperform their spreads")
        print("   Model X can predict which favorites will cover")
    elif correlation > 0.1:
        print("✅ MODERATE POSITIVE CORRELATION")
        print("   Some relationship between matchup EPA and spread performance")
    elif correlation > -0.1:
        print("⚠️  WEAK CORRELATION")
        print("   Little relationship between matchup EPA and spread performance")
    elif correlation > -0.3:
        print("⚠️  MODERATE NEGATIVE CORRELATION")
        print("   Favorites with higher matchup EPA differences tend to underperform spreads")
        print("   Market might be overpricing matchup advantages")
    else:
        print("❌ STRONG NEGATIVE CORRELATION")
        print("   Strong favorites with matchup advantages tend to underperform")
        print("   Market is significantly overpricing matchup advantages")
    
    print()
    
    # Statistical significance
    n = len(df)
    if n >= 3:  # Need at least 3 data points
        t_stat, p_value = stats.pearsonr(df['matchupEPA_diff'], df['margin_vs_spread'])
        print(f"Statistical Significance:")
        print(f"  Sample size: {n}")
        print(f"  t-statistic: {t_stat:.3f}")
        print(f"  p-value: {p_value:.3f}")
        
        if p_value < 0.05:
            print("  ✅ Statistically significant (p < 0.05)")
        elif p_value < 0.10:
            print("  ⚠️  Marginally significant (p < 0.10)")
        else:
            print("  ❌ Not statistically significant (p >= 0.10)")
    
    print()
    
    # Summary statistics
    print("Summary Statistics:")
    print(f"  Average Matchup EPA Diff: {df['matchupEPA_diff'].mean():.3f}")
    print(f"  Average Margin vs Spread: {df['margin_vs_spread'].mean():.3f}")
    print(f"  Standard Deviation EPA Diff: {df['matchupEPA_diff'].std():.3f}")
    print(f"  Standard Deviation Margin vs Spread: {df['margin_vs_spread'].std():.3f}")
    
    print()
    
    # Top and bottom performers
    print("Games with Highest Matchup EPA Differences:")
    top_epa = df.nlargest(3, 'matchupEPA_diff')
    for _, row in top_epa.iterrows():
        print(f"  {row['game']}: EPA Diff {row['matchupEPA_diff']:.3f}, Margin vs Spread {row['margin_vs_spread']:.1f}")
    
    print()
    print("Games with Lowest Matchup EPA Differences:")
    bottom_epa = df.nsmallest(3, 'matchupEPA_diff')
    for _, row in bottom_epa.iterrows():
        print(f"  {row['game']}: EPA Diff {row['matchupEPA_diff']:.3f}, Margin vs Spread {row['margin_vs_spread']:.1f}")
    
    return correlation

def create_prediction_model(df):
    """
    Create a simple linear model to predict margin vs spread from matchup EPA difference
    """
    print("\n=== Prediction Model ===")
    print("=" * 30)
    
    # Simple linear regression
    from sklearn.linear_model import LinearRegression
    from sklearn.metrics import r2_score, mean_squared_error
    
    X = df[['matchupEPA_diff']]
    y = df['margin_vs_spread']
    
    model = LinearRegression()
    model.fit(X, y)
    
    # Predictions
    y_pred = model.predict(X)
    r2 = r2_score(y, y_pred)
    mse = mean_squared_error(y, y_pred)
    
    print(f"Linear Model: margin_vs_spread = {model.intercept_:.3f} + {model.coef_[0]:.3f} * matchupEPA_diff")
    print(f"R² Score: {r2:.3f}")
    print(f"Mean Squared Error: {mse:.3f}")
    print()
    print("Model Interpretation:")
    print(f"  For every 0.1 increase in matchup EPA difference,")
    print(f"  expected margin vs spread changes by {model.coef_[0] * 0.1:.3f} points")
    
    return model

def example_usage():
    """
    Example of how to use this analysis with historical data
    """
    print("\n=== Example Usage ===")
    print("=" * 20)
    print("To use this analysis with historical data:")
    print()
    print("1. Load historical game results:")
    print("   df = pd.read_csv('historical_games_with_results.csv')")
    print()
    print("2. Calculate matchup EPA differences:")
    print("   df['matchupEPA_diff'] = df['fav_matchup_epa'] - df['dog_matchup_epa']")
    print()
    print("3. Calculate margin vs spread:")
    print("   df['margin_vs_spread'] = df['actual_margin'] - df['spread']")
    print()
    print("4. Run correlation analysis:")
    print("   correlation = analyze_matchup_epa_correlation(df)")
    print()
    print("5. Create prediction model:")
    print("   model = create_prediction_model(df)")
    print()
    print("6. Use model for future predictions:")
    print("   future_epa_diff = 0.2  # Example")
    print("   predicted_margin_vs_spread = model.predict([[future_epa_diff]])[0]")
    print("   print(f'Predicted margin vs spread: {predicted_margin_vs_spread:.1f}')")

if __name__ == "__main__":
    example_usage()
