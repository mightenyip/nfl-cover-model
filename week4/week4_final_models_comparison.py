#!/usr/bin/env python3
"""
Week 4 Final Models Comparison - All 4 Models Including Updated Model C
"""

import pandas as pd
import numpy as np
import os

def compare_week4_final_models():
    """Compare all four models for Week 4 including updated Model C"""
    
    print("=== Week 4 Final Models Comparison ===")
    print("Models: A (SumerSports EPA), B v2 (Matchup EPA), C (Original Spread Rules), C Updated (ATS Trends), D (Total Rules)")
    
    # Load all model predictions
    model_a = pd.read_csv("../models/model_a/model_a_week4_predictions.csv")
    model_b = pd.read_csv("../models/model_b/model_b_v2_week4_predictions.csv")
    model_c_original = pd.read_csv("../models/model_c/model_c_week4_predictions.csv")
    model_c_updated = pd.read_csv("../models/model_c/model_c_week4_updated_predictions.csv")
    model_d = pd.read_csv("../models/model_d/model_d_week4_predictions.csv")
    
    # Create comprehensive comparison DataFrame
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
        'Model_C_Orig': model_c_original['predicted_cover'].map({True: 'Cover', False: 'No Cover'}),
        'Model_C_Orig_Conf': model_c_original['confidence'],
        'Model_C_Updated': model_c_updated['predicted_cover'].map({True: 'Cover', False: 'No Cover'}),
        'Model_C_Updated_Conf': model_c_updated['confidence'],
        'Model_C_Updated_Prob': model_c_updated['probability'].round(3),
        'Model_D': model_d['predicted_cover'].map({True: 'Cover', False: 'No Cover'}),
        'Model_D_Conf': model_d['confidence']
    })
    
    print("\n=== Week 4 Final Model Predictions Comparison ===")
    print(comparison.to_string(index=False))
    
    # Model summary statistics
    print(f"\n=== Model Prediction Counts ===")
    print(f"Model A (Cover/No Cover): {sum(model_a['predicted_cover'])}/{sum(~model_a['predicted_cover'])}")
    print(f"Model B v2 (Cover/No Cover): {sum(model_b['predicted_cover'])}/{sum(~model_b['predicted_cover'])}")
    print(f"Model C Original (Cover/No Cover): {sum(model_c_original['predicted_cover'])}/{sum(~model_c_original['predicted_cover'])}")
    print(f"Model C Updated (Cover/No Cover): {sum(model_c_updated['predicted_cover'])}/{sum(~model_c_updated['predicted_cover'])}")
    print(f"Model D (Cover/No Cover): {sum(model_d['predicted_cover'])}/{sum(~model_d['predicted_cover'])}")
    
    # Find consensus games (all models agree)
    consensus_cover = comparison[
        (comparison['Model_A'] == 'Cover') & 
        (comparison['Model_B'] == 'Cover') & 
        (comparison['Model_C_Updated'] == 'Cover') & 
        (comparison['Model_D'] == 'Cover')
    ]
    
    consensus_no_cover = comparison[
        (comparison['Model_A'] == 'No Cover') & 
        (comparison['Model_B'] == 'No Cover') & 
        (comparison['Model_C_Updated'] == 'No Cover') & 
        (comparison['Model_D'] == 'No Cover')
    ]
    
    print(f"\n=== Consensus Predictions (4 Models) ===")
    print(f"All Models Predict COVER ({len(consensus_cover)} games):")
    for _, row in consensus_cover.iterrows():
        print(f"  {row['Game']}: {row['Underdog']} +{row['Spread']}")
    
    print(f"\nAll Models Predict NO COVER ({len(consensus_no_cover)} games):")
    for _, row in consensus_no_cover.iterrows():
        print(f"  {row['Game']}: {row['Underdog']} +{row['Spread']}")
    
    # High confidence predictions by model
    print(f"\n=== High Confidence Predictions by Model ===")
    
    # Model A High Confidence
    high_conf_a = model_a[model_a['confidence'].isin(['HIGH', 'VERY_HIGH'])]
    print(f"\nModel A High Confidence ({len(high_conf_a)} games):")
    for _, row in high_conf_a.iterrows():
        print(f"  {row['away_team']} @ {row['home_team']}: {row['underdog_team']} +{row['spread_line']} - {'Cover' if row['predicted_cover'] else 'No Cover'} ({row['confidence']}, {row['cover_probability']:.1%})")
    
    # Model B High Confidence
    high_conf_b = model_b[model_b['confidence'].isin(['HIGH', 'VERY_HIGH'])]
    print(f"\nModel B v2 High Confidence ({len(high_conf_b)} games):")
    for _, row in high_conf_b.iterrows():
        print(f"  {row['away_team']} @ {row['home_team']}: {row['underdog_team']} +{row['spread_line']} - {'Cover' if row['predicted_cover'] else 'No Cover'} ({row['confidence']}, {row['cover_probability']:.1%})")
    
    # Model C Updated High Confidence
    high_conf_c = model_c_updated[model_c_updated['confidence'] == 'HIGH']
    print(f"\nModel C Updated High Confidence ({len(high_conf_c)} games):")
    for _, row in high_conf_c.iterrows():
        print(f"  {row['away_team']} @ {row['home_team']}: {row['underdog_team']} +{row['spread_line']} - {'Cover' if row['predicted_cover'] else 'No Cover'} ({row['confidence']}, {row['probability']:.1%})")
    
    # Model D High Confidence
    high_conf_d = model_d[model_d['confidence'] == 'HIGH']
    print(f"\nModel D High Confidence ({len(high_conf_d)} games):")
    for _, row in high_conf_d.iterrows():
        print(f"  {row['away_team']} @ {row['home_team']}: {row['underdog_team']} +{row['spread_line']} - {'Cover' if row['predicted_cover'] else 'No Cover'} ({row['confidence']})")
    
    # Model comparison summary
    print(f"\n=== Model Comparison Summary ===")
    print(f"Model A (SumerSports EPA): Balanced approach, 4 high confidence picks")
    print(f"Model B v2 (Matchup EPA): Extremely bullish on underdogs, 9 high confidence picks")
    print(f"Model C Original (Spread Rules): All underdogs (rule-based default)")
    print(f"Model C Updated (ATS Trends): Data-driven, 11 high confidence picks, favorite-heavy")
    print(f"Model D (Total Rules): Total-based rules, 14 high confidence picks")
    
    # Save comprehensive comparison
    comparison.to_csv("week4_final_models_comparison.csv", index=False)
    print(f"\n✅ Final Week 4 comparison saved to: week4_final_models_comparison.csv")
    
    return comparison

if __name__ == "__main__":
    compare_week4_final_models()
