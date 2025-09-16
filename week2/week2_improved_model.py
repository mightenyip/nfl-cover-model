#!/usr/bin/env python3
"""
Improved Week 2 model using corrected Week 1+2 EPA data
"""

import pandas as pd
import numpy as np

def load_corrected_epa_data():
    """Load the corrected EPA data with Week 1+2 metrics"""
    return pd.read_csv("week2/corrected_team_epa_week1_week2.csv")

def load_week2_odds():
    """Load Week 2 odds data"""
    return pd.read_csv("week2/week2_2025_odds.csv")

def create_improved_week2_model():
    """Create improved Week 2 predictions using corrected EPA data"""
    
    # Load data
    epa_data = load_corrected_epa_data()
    odds_data = load_week2_odds()
    
    print("=== Improved Week 2 Model Using Corrected EPA Data ===")
    
    # Create team mapping for odds data
    team_mapping = {
        'Cardinals': 'ARI', 'Falcons': 'ATL', 'Ravens': 'BAL', 'Bills': 'BUF',
        'Panthers': 'CAR', 'Bears': 'CHI', 'Bengals': 'CIN', 'Browns': 'CLE',
        'Cowboys': 'DAL', 'Broncos': 'DEN', 'Lions': 'DET', 'Packers': 'GB',
        'Texans': 'HOU', 'Colts': 'IND', 'Jaguars': 'JAX', 'Chiefs': 'KC',
        'Rams': 'LA', 'Chargers': 'LAC', 'Raiders': 'LV', 'Dolphins': 'MIA',
        'Vikings': 'MIN', 'Patriots': 'NE', 'Saints': 'NO', 'Giants': 'NYG',
        'Jets': 'NYJ', 'Eagles': 'PHI', 'Steelers': 'PIT', '49ers': 'SF',
        'Seahawks': 'SEA', 'Buccaneers': 'TB', 'Titans': 'TEN', 'Commanders': 'WAS'
    }
    
    # Reverse mapping for EPA data
    epa_team_mapping = {v: k for k, v in team_mapping.items()}
    
    results = []
    
    for _, game in odds_data.iterrows():
        away_team = game['away_team']
        home_team = game['home_team']
        spread = game['spread_line']
        underdog = game['underdog_team']
        favorite = game['favorite_team']
        
        # Get EPA data for both teams
        underdog_epa = epa_data[epa_data['team'] == team_mapping[underdog]].iloc[0]
        favorite_epa = epa_data[epa_data['team'] == team_mapping[favorite]].iloc[0]
        
        # Calculate key metrics
        underdog_net_epa = underdog_epa['net_epa_per_play']
        favorite_net_epa = favorite_epa['net_epa_per_play']
        net_epa_differential = underdog_net_epa - favorite_net_epa
        
        # Opponent defensive EPA (how good is the defense the underdog is facing)
        opponent_def_epa = favorite_epa['epa_def_allowed_per_play']
        
        # Determine defense quality based on corrected data
        if opponent_def_epa < -0.05:
            defense_quality = "STRONG"
        elif opponent_def_epa > 0.05:
            defense_quality = "WEAK"
        else:
            defense_quality = "AVERAGE"
        
        # Calculate cover probability using improved model
        # Base probability starts at 50%
        base_prob = 0.50
        
        # Adjust for net EPA differential (stronger underdog = higher probability)
        epa_adjustment = net_epa_differential * 0.3  # Scale factor
        
        # Adjust for opponent defense quality (based on corrected Week 1+2 data)
        if defense_quality == "STRONG":
            defense_adjustment = 0.15  # Strong defenses favor underdogs
        elif defense_quality == "WEAK":
            defense_adjustment = -0.10  # Weak defenses favor favorites
        else:
            defense_adjustment = 0.0  # Average defenses neutral
        
        # Adjust for spread size (larger spreads favor underdogs)
        spread_adjustment = min(spread * 0.02, 0.10)  # Cap at 10%
        
        # Calculate final probability
        cover_probability = base_prob + epa_adjustment + defense_adjustment + spread_adjustment
        
        # Ensure probability stays within reasonable bounds
        cover_probability = max(0.20, min(0.80, cover_probability))
        
        # Determine confidence level
        if cover_probability >= 0.65:
            confidence = "HIGH"
        elif cover_probability >= 0.45:
            confidence = "MEDIUM"
        else:
            confidence = "LOW"
        
        # Determine prediction
        predicted_cover = cover_probability > 0.50
        
        result = {
            'game': f"{away_team} at {home_team}",
            'underdog': underdog,
            'favorite': favorite,
            'spread': spread,
            'underdog_net_epa': underdog_net_epa,
            'favorite_net_epa': favorite_net_epa,
            'net_epa_differential': net_epa_differential,
            'opponent_def_epa': opponent_def_epa,
            'defense_quality': defense_quality,
            'cover_probability': cover_probability,
            'confidence': confidence,
            'predicted_cover': predicted_cover,
            'prediction': "Cover" if predicted_cover else "No Cover"
        }
        
        results.append(result)
    
    return pd.DataFrame(results)

def analyze_improved_predictions(df):
    """Analyze the improved predictions"""
    
    print("\n=== Improved Week 2 Predictions ===")
    
    # Sort by cover probability
    df_sorted = df.sort_values('cover_probability', ascending=False)
    
    print("\nAll Games (sorted by cover probability):")
    for _, row in df_sorted.iterrows():
        print(f"{row['game']}: {row['underdog']} +{row['spread']}")
        print(f"  Cover Probability: {row['cover_probability']:.1%}")
        print(f"  Confidence: {row['confidence']}")
        print(f"  Net EPA Diff: {row['net_epa_differential']:.3f}")
        print(f"  Opponent Defense: {row['defense_quality']} ({row['opponent_def_epa']:.3f})")
        print(f"  Prediction: {row['prediction']}")
        print()
    
    # High confidence picks
    high_conf = df[df['confidence'] == 'HIGH']
    print(f"\n=== High Confidence Picks ({len(high_conf)} games) ===")
    for _, row in high_conf.iterrows():
        print(f"{row['underdog']} +{row['spread']} vs {row['favorite']} ({row['cover_probability']:.1%})")
    
    # Medium confidence picks
    medium_conf = df[df['confidence'] == 'MEDIUM']
    print(f"\n=== Medium Confidence Picks ({len(medium_conf)} games) ===")
    for _, row in medium_conf.iterrows():
        print(f"{row['underdog']} +{row['spread']} vs {row['favorite']} ({row['cover_probability']:.1%})")
    
    # Low confidence picks
    low_conf = df[df['confidence'] == 'LOW']
    print(f"\n=== Low Confidence Picks ({len(low_conf)} games) ===")
    for _, row in low_conf.iterrows():
        print(f"{row['underdog']} +{row['spread']} vs {row['favorite']} ({row['cover_probability']:.1%})")
    
    # Defense quality analysis
    print(f"\n=== Defense Quality Analysis ===")
    defense_analysis = df.groupby('defense_quality').agg({
        'cover_probability': ['count', 'mean'],
        'predicted_cover': 'sum'
    }).round(3)
    print(defense_analysis)
    
    return df_sorted

def compare_with_actual_results(predictions_df):
    """Compare improved predictions with actual Week 2 results"""
    
    # Load actual results
    actual_results = pd.read_csv("week2/week2_epa_corrected.csv")
    
    print("\n=== Comparison with Actual Results ===")
    
    # Merge predictions with actual results
    comparison = predictions_df.merge(
        actual_results[['game', 'actual_cover']], 
        on='game', 
        how='left'
    )
    
    # Calculate accuracy
    comparison['correct'] = comparison['predicted_cover'] == comparison['actual_cover']
    
    overall_accuracy = comparison['correct'].mean()
    print(f"Overall Accuracy: {overall_accuracy:.1%}")
    
    # Accuracy by confidence level
    print(f"\nAccuracy by Confidence Level:")
    for conf in ['HIGH', 'MEDIUM', 'LOW']:
        conf_data = comparison[comparison['confidence'] == conf]
        if len(conf_data) > 0:
            acc = conf_data['correct'].mean()
            print(f"{conf}: {acc:.1%} ({conf_data['correct'].sum()}/{len(conf_data)})")
    
    # Show detailed comparison
    print(f"\nDetailed Comparison:")
    for _, row in comparison.iterrows():
        correct_symbol = "✓" if row['correct'] else "✗"
        print(f"{correct_symbol} {row['underdog']} +{row['spread']}: "
              f"Predicted {row['cover_probability']:.1%} → "
              f"Actual {'Cover' if row['actual_cover'] else 'No Cover'}")
    
    return comparison

def main():
    """Main function"""
    
    # Create improved predictions
    predictions = create_improved_week2_model()
    
    # Analyze predictions
    predictions_sorted = analyze_improved_predictions(predictions)
    
    # Compare with actual results
    comparison = compare_with_actual_results(predictions_sorted)
    
    # Save results
    predictions_sorted.to_csv("week2/improved_week2_predictions.csv", index=False)
    comparison.to_csv("week2/improved_week2_comparison.csv", index=False)
    
    print(f"\n✅ Results saved to:")
    print(f"  - week2/improved_week2_predictions.csv")
    print(f"  - week2/improved_week2_comparison.csv")

if __name__ == "__main__":
    main()
