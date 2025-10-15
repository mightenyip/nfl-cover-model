#!/usr/bin/env python3
"""
Week 7 All Models Comparison
Compares predictions from Model A, Model B v2, Model C, and Model D
"""

import pandas as pd
import numpy as np
import os

def create_week7_comparison():
    """Create comprehensive comparison of all four models for Week 7"""
    
    print("=== Week 7 All Models Comparison ===")
    print("Loading predictions from all four models...")

    # Load all model predictions
    model_a_path = "model_a/model_a_week7_predictions.csv"
    model_b_path = "model_b/model_b_v2_week7_predictions.csv"
    model_c_path = "model_c/model_c_week7_predictions.csv"
    model_d_path = "model_d/model_d_week7_predictions.csv"

    # Check if all files exist
    files_exist = all(os.path.exists(path) for path in [model_a_path, model_b_path, model_c_path, model_d_path])
    
    if not files_exist:
        print("Error: Not all prediction files found. Please run all models first.")
        return None

    # Load predictions
    model_a = pd.read_csv(model_a_path)
    model_b = pd.read_csv(model_b_path)
    model_c = pd.read_csv(model_c_path)
    model_d = pd.read_csv(model_d_path)

    print(f"Loaded predictions:")
    print(f"  Model A: {len(model_a)} games")
    print(f"  Model B v2: {len(model_b)} games")
    print(f"  Model C: {len(model_c)} games")
    print(f"  Model D: {len(model_d)} games")

    # Create comparison DataFrame
    comparison_data = []

    for i in range(len(model_a)):
        # Get game info from any model (they should all have the same games)
        away_team = model_a.iloc[i]['away_team']
        home_team = model_a.iloc[i]['home_team']
        favorite_team = model_a.iloc[i]['favorite_team']
        underdog_team = model_a.iloc[i]['underdog_team']
        spread_line = model_a.iloc[i]['spread_line']
        total_line = model_a.iloc[i]['total_line']

        # Get predictions from each model
        model_a_pred = model_a.iloc[i]['predicted_cover']
        model_b_pred = model_b.iloc[i]['predicted_cover']
        model_c_pred = model_c.iloc[i]['predicted_cover']
        model_d_pred = model_d.iloc[i]['predicted_cover']

        # Get confidence levels
        model_a_conf = model_a.iloc[i]['confidence']
        model_b_conf = model_b.iloc[i]['confidence']
        model_c_conf = model_c.iloc[i]['confidence']
        model_d_conf = model_d.iloc[i]['confidence']

        # Get probabilities
        model_a_prob = model_a.iloc[i]['cover_probability']
        model_b_prob = model_b.iloc[i]['cover_probability']
        model_c_prob = model_c.iloc[i]['probability']

        # Count agreement
        predictions = [model_a_pred, model_b_pred, model_c_pred, model_d_pred]
        cover_count = sum(predictions)
        agreement = f"{cover_count}/4 models predict UNDERDOG cover"

        comparison_data.append({
            'away_team': away_team,
            'home_team': home_team,
            'favorite_team': favorite_team,
            'underdog_team': underdog_team,
            'spread_line': spread_line,
            'total_line': total_line,
            'model_a_prediction': 'Cover' if model_a_pred else 'No Cover',
            'model_a_confidence': model_a_conf,
            'model_a_probability': f"{model_a_prob:.1%}",
            'model_b_prediction': 'Cover' if model_b_pred else 'No Cover',
            'model_b_confidence': model_b_conf,
            'model_b_probability': f"{model_b_prob:.1%}",
            'model_c_prediction': 'Cover' if model_c_pred else 'No Cover',
            'model_c_confidence': model_c_conf,
            'model_c_probability': f"{model_c_prob:.1%}",
            'model_d_prediction': 'Cover' if model_d_pred else 'No Cover',
            'model_d_confidence': model_d_conf,
            'agreement': agreement,
            'consensus': 'UNDERDOG' if cover_count >= 3 else 'FAVORITE' if cover_count <= 1 else 'SPLIT'
        })

    # Create comparison DataFrame
    comparison_df = pd.DataFrame(comparison_data)

    print(f"\n=== Week 7 Model Predictions Comparison ===")
    print(f"Total Games: {len(comparison_df)}")
    
    # Summary by consensus
    consensus_summary = comparison_df['consensus'].value_counts()
    print(f"\nConsensus Summary:")
    for consensus, count in consensus_summary.items():
        print(f"  {consensus}: {count} games ({count/len(comparison_df):.1%})")

    # Show all predictions
    print(f"\n=== Detailed Predictions ===")
    for _, row in comparison_df.iterrows():
        print(f"\n{row['away_team']} at {row['home_team']}: {row['underdog_team']} +{row['spread_line']} (Total: {row['total_line']})")
        print(f"  Model A: {row['model_a_prediction']} ({row['model_a_confidence']}, {row['model_a_probability']})")
        print(f"  Model B v2: {row['model_b_prediction']} ({row['model_b_confidence']}, {row['model_b_probability']})")
        print(f"  Model C: {row['model_c_prediction']} ({row['model_c_confidence']}, {row['model_c_probability']})")
        print(f"  Model D: {row['model_d_prediction']} ({row['model_d_confidence']})")
        print(f"  Agreement: {row['agreement']} | Consensus: {row['consensus']}")

    # High confidence picks analysis
    print(f"\n=== High Confidence Analysis ===")
    
    # Model A high confidence
    model_a_high = comparison_df[comparison_df['model_a_confidence'].isin(['HIGH', 'VERY_HIGH'])]
    print(f"Model A High Confidence: {len(model_a_high)} games")
    
    # Model B high confidence
    model_b_high = comparison_df[comparison_df['model_b_confidence'].isin(['HIGH', 'VERY_HIGH'])]
    print(f"Model B v2 High Confidence: {len(model_b_high)} games")
    
    # Model C high confidence
    model_c_high = comparison_df[comparison_df['model_c_confidence'].isin(['HIGH', 'VERY_HIGH'])]
    print(f"Model C High Confidence: {len(model_c_high)} games")
    
    # Model D high confidence
    model_d_high = comparison_df[comparison_df['model_d_confidence'].isin(['HIGH', 'VERY_HIGH'])]
    print(f"Model D High Confidence: {len(model_d_high)} games")

    # Show high confidence picks with consensus
    print(f"\n=== High Confidence Picks with Consensus ===")
    high_conf_games = []
    
    for _, row in comparison_df.iterrows():
        high_conf_count = sum([
            row['model_a_confidence'] in ['HIGH', 'VERY_HIGH'],
            row['model_b_confidence'] in ['HIGH', 'VERY_HIGH'],
            row['model_c_confidence'] in ['HIGH', 'VERY_HIGH'],
            row['model_d_confidence'] in ['HIGH', 'VERY_HIGH']
        ])
        
        if high_conf_count >= 2:  # At least 2 models with high confidence
            high_conf_games.append(row)

    for game in high_conf_games:
        print(f"{game['away_team']} at {game['home_team']}: {game['underdog_team']} +{game['spread_line']}")
        print(f"  Consensus: {game['consensus']} | Agreement: {game['agreement']}")

    # Save comparison
    comparison_df.to_csv("week7_all_models_comparison.csv", index=False)
    print(f"\n✅ Week 7 all models comparison saved to: week7_all_models_comparison.csv")

    return comparison_df

if __name__ == "__main__":
    create_week7_comparison()
