#!/usr/bin/env python3
"""
Model C Weekly Updater
Automatically update Model C with latest ATS trends and generate predictions
"""

import pandas as pd
import numpy as np
import os
import sys

# Add parent directory to path for imports
sys.path.append(os.path.dirname(os.path.dirname(os.path.dirname(os.path.abspath(__file__)))))

def load_master_ats_data():
    """Load the master ATS trends data"""
    try:
        df = pd.read_csv("data/master_ats_trends.csv")
        return df
    except FileNotFoundError:
        print("❌ Error: master_ats_trends.csv not found")
        print("Please run the ATS data compilation first")
        return None

def calculate_current_trends(df):
    """Calculate current ATS trends from master data"""
    
    print("=== Calculating Current ATS Trends ===")
    
    # Overall performance
    total_games = len(df)
    underdog_covers = df['underdog_covered'].sum()
    favorite_covers = total_games - underdog_covers
    
    overall_underdog_rate = underdog_covers / total_games * 100
    overall_favorite_rate = favorite_covers / total_games * 100
    
    print(f"Overall: {underdog_covers}/{total_games} underdog covers ({overall_underdog_rate:.1f}%)")
    
    # Category analysis
    categories = {
        'Away Favorites': df[df['home_away_status'] == 'Away Favorite'],
        'Home Favorites': df[df['home_away_status'] == 'Home Favorite'],
        'Home Dogs': df[df['home_away_status'] == 'Home Underdog']
    }
    
    category_rates = {}
    for category, data in categories.items():
        if len(data) > 0:
            rate = data['underdog_covered'].sum() / len(data) * 100
            category_rates[category] = rate
            print(f"{category}: {data['underdog_covered'].sum()}/{len(data)} ({rate:.1f}%)")
    
    # Recent trend (last 3 weeks)
    recent_weeks = df[df['week'].isin(sorted(df['week'].unique())[-3:])]
    recent_rate = recent_weeks['underdog_covered'].sum() / len(recent_weeks) * 100
    print(f"Recent 3 weeks: {recent_weeks['underdog_covered'].sum()}/{len(recent_weeks)} ({recent_rate:.1f}%)")
    
    return {
        'overall_underdog_rate': overall_underdog_rate,
        'overall_favorite_rate': overall_favorite_rate,
        'category_rates': category_rates,
        'recent_rate': recent_rate
    }

def generate_model_c_rules(trends):
    """Generate Model C rules based on current trends"""
    
    print("\n=== Model C Updated Rules ===")
    
    rules = {}
    
    # Away Favorites rule
    away_fav_rate = trends['category_rates'].get('Away Favorites', 50)
    if away_fav_rate < 40:
        rules['away_favorites'] = {
            'action': 'FADE',
            'confidence': 'HIGH',
            'probability': 100 - away_fav_rate,
            'description': f'Away favorites only {away_fav_rate:.1f}% - FADE them'
        }
    elif away_fav_rate > 60:
        rules['away_favorites'] = {
            'action': 'PICK',
            'confidence': 'HIGH',
            'probability': away_fav_rate,
            'description': f'Away favorites {away_fav_rate:.1f}% - STRONG PICK'
        }
    else:
        rules['away_favorites'] = {
            'action': 'NEUTRAL',
            'confidence': 'LOW',
            'probability': 50,
            'description': f'Away favorites {away_fav_rate:.1f}% - NEUTRAL'
        }
    
    # Home Favorites rule
    home_fav_rate = trends['category_rates'].get('Home Favorites', 50)
    if home_fav_rate < 45:
        rules['home_favorites'] = {
            'action': 'FADE',
            'confidence': 'MEDIUM',
            'probability': 100 - home_fav_rate,
            'description': f'Home favorites {home_fav_rate:.1f}% - SLIGHT FADE'
        }
    elif home_fav_rate > 55:
        rules['home_favorites'] = {
            'action': 'PICK',
            'confidence': 'MEDIUM',
            'probability': home_fav_rate,
            'description': f'Home favorites {home_fav_rate:.1f}% - GOOD PICK'
        }
    else:
        rules['home_favorites'] = {
            'action': 'NEUTRAL',
            'confidence': 'LOW',
            'probability': 50,
            'description': f'Home favorites {home_fav_rate:.1f}% - NEUTRAL'
        }
    
    # Home Dogs rule
    home_dog_rate = trends['category_rates'].get('Home Dogs', 50)
    if home_dog_rate < 45:
        rules['home_dogs'] = {
            'action': 'FADE',
            'confidence': 'HIGH',
            'probability': 100 - home_dog_rate,
            'description': f'Home dogs {home_dog_rate:.1f}% - FADE them'
        }
    elif home_dog_rate > 55:
        rules['home_dogs'] = {
            'action': 'PICK',
            'confidence': 'HIGH',
            'probability': home_dog_rate,
            'description': f'Home dogs {home_dog_rate:.1f}% - STRONG PICK'
        }
    else:
        rules['home_dogs'] = {
            'action': 'NEUTRAL',
            'confidence': 'LOW',
            'probability': 50,
            'description': f'Home dogs {home_dog_rate:.1f}% - NEUTRAL'
        }
    
    # Print rules
    for category, rule in rules.items():
        print(f"{category.replace('_', ' ').title()}: {rule['description']}")
        print(f"  Action: {rule['action']} | Confidence: {rule['confidence']} | Probability: {rule['probability']:.1f}%")
    
    return rules

def update_model_c_predictions(week_odds_file, rules):
    """Update Model C predictions based on new rules"""
    
    print(f"\n=== Generating Model C Predictions ===")
    
    try:
        odds_df = pd.read_csv(week_odds_file)
        print(f"Loaded {len(odds_df)} games from {week_odds_file}")
    except FileNotFoundError:
        print(f"❌ Error: {week_odds_file} not found")
        return None
    
    # Team name mapping
    team_mapping = {
        '49ers': 'SF', 'Bears': 'CHI', 'Bengals': 'CIN', 'Bills': 'BUF', 'Broncos': 'DEN',
        'Browns': 'CLE', 'Buccaneers': 'TB', 'Cardinals': 'ARI', 'Chargers': 'LAC', 'Chiefs': 'KC',
        'Colts': 'IND', 'Commanders': 'WAS', 'Cowboys': 'DAL', 'Dolphins': 'MIA', 'Eagles': 'PHI',
        'Falcons': 'ATL', 'Giants': 'NYG', 'Jaguars': 'JAX', 'Jets': 'NYJ', 'Lions': 'DET',
        'Packers': 'GB', 'Panthers': 'CAR', 'Patriots': 'NE', 'Raiders': 'LV', 'Rams': 'LA',
        'Ravens': 'BAL', 'Saints': 'NO', 'Seahawks': 'SEA', 'Steelers': 'PIT', 'Texans': 'HOU',
        'Titans': 'TEN', 'Vikings': 'MIN'
    }
    
    predictions = []
    
    for idx, row in odds_df.iterrows():
        game = f"{row['away_team']} @ {row['home_team']}"
        favorite = row['favorite_team']
        underdog = row['underdog_team']
        spread = row['spread_line']
        
        # Determine category
        if favorite == row['away_team']:
            category = 'away_favorites'
        else:
            category = 'home_favorites'
        
        # Apply rule
        rule = rules[category]
        
        if rule['action'] == 'FADE':
            predicted_cover = True  # Underdog covers
            confidence = rule['confidence']
            probability = rule['probability']
        elif rule['action'] == 'PICK':
            predicted_cover = False  # Favorite covers
            confidence = rule['confidence']
            probability = rule['probability']
        else:  # NEUTRAL
            predicted_cover = True  # Default to underdog
            confidence = 'LOW'
            probability = 50
        
        predictions.append({
            'game': game,
            'favorite': favorite,
            'underdog': underdog,
            'spread': spread,
            'predicted_cover': predicted_cover,
            'confidence': confidence,
            'probability': probability,
            'rule_applied': rule['description']
        })
    
    # Save predictions
    predictions_df = pd.DataFrame(predictions)
    output_file = f"model_c_updated_predictions.csv"
    predictions_df.to_csv(output_file, index=False)
    
    print(f"✅ Predictions saved to {output_file}")
    
    # Summary
    high_confidence = len(predictions_df[predictions_df['confidence'] == 'HIGH'])
    medium_confidence = len(predictions_df[predictions_df['confidence'] == 'MEDIUM'])
    low_confidence = len(predictions_df[predictions_df['confidence'] == 'LOW'])
    
    print(f"\n=== Prediction Summary ===")
    print(f"High Confidence: {high_confidence} games")
    print(f"Medium Confidence: {medium_confidence} games")
    print(f"Low Confidence: {low_confidence} games")
    
    return predictions_df

def main():
    """Main function"""
    print("=== Model C Weekly Updater ===")
    print("Updating Model C with latest ATS trends")
    print("=" * 60)
    
    # Load master data
    df = load_master_ats_data()
    if df is None:
        return
    
    # Calculate trends
    trends = calculate_current_trends(df)
    
    # Generate rules
    rules = generate_model_c_rules(trends)
    
    # Update predictions (example for Week 8)
    week_odds_file = "schedule/week8_2025_odds.csv"
    if os.path.exists(week_odds_file):
        predictions = update_model_c_predictions(week_odds_file, rules)
    else:
        print(f"⚠️ {week_odds_file} not found - skipping prediction generation")
    
    print(f"\n=== Update Complete ===")
    print(f"📊 Model C updated with latest ATS trends")
    print(f"📁 Master data: {len(df)} games from Week {df['week'].min()}-{df['week'].max()}")

if __name__ == "__main__":
    main()
