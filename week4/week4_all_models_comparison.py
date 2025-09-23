#!/usr/bin/env python3
"""
Week 4 All Models Comparison
"""

import pandas as pd
import numpy as np
import os

def compare_week4_models():
    """Compare all four models for Week 4 predictions"""
    
    print("=== Week 4 All Models Comparison ===")
    
    # Load all model predictions
    model_a = pd.read_csv("../models/model_a/model_a_week4_predictions.csv")
    model_b = pd.read_csv("../models/model_b/model_b_v2_week4_predictions.csv")
    model_c = pd.read_csv("../models/model_c/model_c_week4_predictions.csv")
    model_d = pd.read_csv("../models/model_d/model_d_week4_predictions.csv")
    
    # Create comparison DataFrame
    comparison = pd.DataFrame({
        'Game': model_a['away_team'] + ' @ ' + model_a['home_team'],
        'Underdog': model_a['underdog_team'],
        'Spread': model_a['spread_line'],
        'Total': model_a['total_line'],
        'Model_A': model_a['predicted_cover'].map({True: 'Cover', False: 'No Cover'}),
        'Model_A_Conf': model_a['confidence'],
        'Model_A_Prob': model_a['cover_probability'].round(3),
        'Model_B': model_b['predicted_cover'].map({True: 'Cover', False: 'No Cover'}),
        'Model_B_Conf': model_b['confidence'],
        'Model_B_Prob': model_b['cover_probability'].round(3),
        'Model_C': model_c['predicted_cover'].map({True: 'Cover', False: 'No Cover'}),
        'Model_C_Conf': model_c['confidence'],
        'Model_D': model_d['predicted_cover'].map({True: 'Cover', False: 'No Cover'}),
        'Model_D_Conf': model_d['confidence']
    })
    
    print("\n=== Week 4 Model Predictions Comparison ===")
    print(comparison.to_string(index=False))
    
    # Count predictions by model
    print(f"\n=== Prediction Counts ===")
    print(f"Model A (Cover/No Cover): {sum(model_a['predicted_cover'])}/{sum(~model_a['predicted_cover'])}")
    print(f"Model B (Cover/No Cover): {sum(model_b['predicted_cover'])}/{sum(~model_b['predicted_cover'])}")
    print(f"Model C (Cover/No Cover): {sum(model_c['predicted_cover'])}/{sum(~model_c['predicted_cover'])}")
    print(f"Model D (Cover/No Cover): {sum(model_d['predicted_cover'])}/{sum(~model_d['predicted_cover'])}")
    
    # Find consensus games
    consensus_cover = comparison[
        (comparison['Model_A'] == 'Cover') & 
        (comparison['Model_B'] == 'Cover') & 
        (comparison['Model_C'] == 'Cover') & 
        (comparison['Model_D'] == 'Cover')
    ]
    
    consensus_no_cover = comparison[
        (comparison['Model_A'] == 'No Cover') & 
        (comparison['Model_B'] == 'No Cover') & 
        (comparison['Model_C'] == 'No Cover') & 
        (comparison['Model_D'] == 'No Cover')
    ]
    
    print(f"\n=== Consensus Predictions ===")
    print(f"All Models Predict COVER ({len(consensus_cover)} games):")
    for _, row in consensus_cover.iterrows():
        print(f"  {row['Game']}: {row['Underdog']} +{row['Spread']}")
    
    print(f"\nAll Models Predict NO COVER ({len(consensus_no_cover)} games):")
    for _, row in consensus_no_cover.iterrows():
        print(f"  {row['Game']}: {row['Underdog']} +{row['Spread']}")
    
    # Find disagreements
    disagreements = comparison[
        ~((comparison['Model_A'] == comparison['Model_B']) & 
          (comparison['Model_B'] == comparison['Model_C']) & 
          (comparison['Model_C'] == comparison['Model_D']))
    ]
    
    print(f"\n=== Model Disagreements ({len(disagreements)} games) ===")
    for _, row in disagreements.iterrows():
        print(f"{row['Game']}: {row['Underdog']} +{row['Spread']}")
        print(f"  A: {row['Model_A']} ({row['Model_A_Conf']})")
        print(f"  B: {row['Model_B']} ({row['Model_B_Conf']})")
        print(f"  C: {row['Model_C']} ({row['Model_C_Conf']})")
        print(f"  D: {row['Model_D']} ({row['Model_D_Conf']})")
        print()
    
    # High confidence predictions
    print("=== High Confidence Predictions ===")
    
    high_conf_a = model_a[model_a['confidence'].isin(['HIGH', 'VERY_HIGH'])]
    high_conf_b = model_b[model_b['confidence'].isin(['HIGH', 'VERY_HIGH'])]
    
    print(f"\nModel A High Confidence ({len(high_conf_a)} games):")
    for _, row in high_conf_a.iterrows():
        print(f"  {row['away_team']} @ {row['home_team']}: {row['underdog_team']} +{row['spread_line']} - {'Cover' if row['predicted_cover'] else 'No Cover'} ({row['confidence']}, {row['cover_probability']:.1%})")
    
    print(f"\nModel B v2 High Confidence ({len(high_conf_b)} games):")
    for _, row in high_conf_b.iterrows():
        print(f"  {row['away_team']} @ {row['home_team']}: {row['underdog_team']} +{row['spread_line']} - {'Cover' if row['predicted_cover'] else 'No Cover'} ({row['confidence']}, {row['cover_probability']:.1%})")
    
    # Save comparison
    comparison.to_csv("week4_all_models_comparison.csv", index=False)
    print(f"\n✅ Week 4 comparison saved to: week4_all_models_comparison.csv")
    
    return comparison

if __name__ == "__main__":
    compare_week4_models()
