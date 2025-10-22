#!/usr/bin/env python3
"""
Calculate Actual ATS Performance from Week 1-7
Combine odds data with actual results to get real ATS trends
"""

import pandas as pd
import numpy as np
import os
from datetime import datetime

def load_week_results(week_num):
    """Load actual results for a specific week"""
    result_files = [
        f"week{week_num}/week{week_num}_all_models_predictions_vs_reality.csv",
        f"week{week_num}/week{week_num}_model_predictions_vs_reality.csv",
        f"week{week_num}/week{week_num}_all_models_comparison.csv"
    ]
    
    for file_path in result_files:
        if os.path.exists(file_path):
            df = pd.read_csv(file_path)
            if 'Actual_Cover' in df.columns:
                df['week'] = week_num
                return df
    return None

def load_all_results():
    """Load actual results for all weeks 1-7"""
    all_results = []
    
    for week in range(1, 8):  # Week 1 through Week 7
        week_data = load_week_results(week)
        if week_data is not None:
            all_results.append(week_data)
            print(f"✅ Loaded Week {week} results: {len(week_data)} games")
        else:
            print(f"❌ Week {week} results not found")
    
    if all_results:
        combined_df = pd.concat(all_results, ignore_index=True)
        print(f"\n📊 Total games with results: {len(combined_df)}")
        return combined_df
    else:
        print("❌ No result data found")
        return None

def analyze_actual_ats_performance(df):
    """Analyze actual ATS performance from results data"""
    
    print("\n=== Actual ATS Performance Analysis (Week 1-7) ===")
    print("=" * 60)
    
    # Create analysis columns
    df['favorite_is_home'] = df['Favorite'] == df['home_team']
    df['favorite_is_away'] = df['Favorite'] == df['away_team']
    df['underdog_is_home'] = df['Underdog'] == df['home_team']
    df['underdog_is_away'] = df['Underdog'] == df['away_team']
    
    # Calculate actual ATS performance
    total_games = len(df)
    underdog_covers = df['Actual_Cover'].sum()
    favorite_covers = total_games - underdog_covers
    
    print(f"Total Games: {total_games}")
    print(f"Underdog Covers: {underdog_covers} ({underdog_covers/total_games*100:.1f}%)")
    print(f"Favorite Covers: {favorite_covers} ({favorite_covers/total_games*100:.1f}%)")
    
    # Analyze by team position
    print(f"\n=== Team Position ATS Performance ===")
    
    # Away teams performance
    away_games = df[df['favorite_is_away'] | df['underdog_is_away']]
    away_underdog_covers = away_games[away_games['underdog_is_away']]['Actual_Cover'].sum()
    away_favorite_covers = away_games[away_games['favorite_is_away']]['Actual_Cover'].sum()
    away_total = len(away_games)
    
    print(f"Away Teams: {away_total} games")
    print(f"  Away Underdogs: {away_underdog_covers}/{len(away_games[away_games['underdog_is_away']])} covers ({away_underdog_covers/len(away_games[away_games['underdog_is_away']])*100:.1f}%)")
    print(f"  Away Favorites: {away_favorite_covers}/{len(away_games[away_games['favorite_is_away']])} covers ({away_favorite_covers/len(away_games[away_games['favorite_is_away']])*100:.1f}%)")
    
    # Home teams performance
    home_games = df[df['favorite_is_home'] | df['underdog_is_home']]
    home_underdog_covers = home_games[home_games['underdog_is_home']]['Actual_Cover'].sum()
    home_favorite_covers = home_games[home_games['favorite_is_home']]['Actual_Cover'].sum()
    home_total = len(home_games)
    
    print(f"Home Teams: {home_total} games")
    print(f"  Home Underdogs: {home_underdog_covers}/{len(home_games[home_games['underdog_is_home']])} covers ({home_underdog_covers/len(home_games[home_games['underdog_is_home']])*100:.1f}%)")
    print(f"  Home Favorites: {home_favorite_covers}/{len(home_games[home_games['favorite_is_home']])} covers ({home_favorite_covers/len(home_games[home_games['favorite_is_home']])*100:.1f}%)")
    
    # Specific combinations
    print(f"\n=== Specific Combinations ATS Performance ===")
    
    # Away Favorites
    away_fav_games = df[df['favorite_is_away']]
    away_fav_covers = away_fav_games['Actual_Cover'].sum()
    away_fav_total = len(away_fav_games)
    away_fav_pct = away_fav_covers / away_fav_total * 100 if away_fav_total > 0 else 0
    
    print(f"Away Favorites: {away_fav_covers}/{away_fav_total} covers ({away_fav_pct:.1f}%)")
    
    # Away Underdogs
    away_dog_games = df[df['underdog_is_away']]
    away_dog_covers = away_dog_games['Actual_Cover'].sum()
    away_dog_total = len(away_dog_games)
    away_dog_pct = away_dog_covers / away_dog_total * 100 if away_dog_total > 0 else 0
    
    print(f"Away Underdogs: {away_dog_covers}/{away_dog_total} covers ({away_dog_pct:.1f}%)")
    
    # Home Favorites
    home_fav_games = df[df['favorite_is_home']]
    home_fav_covers = home_fav_games['Actual_Cover'].sum()
    home_fav_total = len(home_fav_games)
    home_fav_pct = home_fav_covers / home_fav_total * 100 if home_fav_total > 0 else 0
    
    print(f"Home Favorites: {home_fav_covers}/{home_fav_total} covers ({home_fav_pct:.1f}%)")
    
    # Home Underdogs
    home_dog_games = df[df['underdog_is_home']]
    home_dog_covers = home_dog_games['Actual_Cover'].sum()
    home_dog_total = len(home_dog_games)
    home_dog_pct = home_dog_covers / home_dog_total * 100 if home_dog_total > 0 else 0
    
    print(f"Home Underdogs: {home_dog_covers}/{home_dog_total} covers ({home_dog_pct:.1f}%)")
    
    # Spread analysis
    print(f"\n=== Spread Range ATS Performance ===")
    
    small_spreads = df[df['Spread'].abs() <= 3.5]
    medium_spreads = df[(df['Spread'].abs() > 3.5) & (df['Spread'].abs() <= 6.5)]
    large_spreads = df[df['Spread'].abs() > 6.5]
    
    for name, data in [("Small (≤3.5)", small_spreads), ("Medium (3.5-6.5)", medium_spreads), ("Large (>6.5)", large_spreads)]:
        if len(data) > 0:
            covers = data['Actual_Cover'].sum()
            total = len(data)
            pct = covers / total * 100
            print(f"{name}: {covers}/{total} underdog covers ({pct:.1f}%)")
    
    return {
        'total_games': total_games,
        'underdog_covers': underdog_covers,
        'favorite_covers': favorite_covers,
        'away_favorites': {'covers': away_fav_covers, 'total': away_fav_total, 'pct': away_fav_pct},
        'away_underdogs': {'covers': away_dog_covers, 'total': away_dog_total, 'pct': away_dog_pct},
        'home_favorites': {'covers': home_fav_covers, 'total': home_fav_total, 'pct': home_fav_pct},
        'home_underdogs': {'covers': home_dog_covers, 'total': home_dog_total, 'pct': home_dog_pct}
    }

def create_ats_summary_table(performance):
    """Create a summary table of ATS performance"""
    
    print(f"\n=== ATS Performance Summary Table ===")
    print("=" * 50)
    
    categories = [
        ("Away Favorites", performance['away_favorites']),
        ("Away Underdogs", performance['away_underdogs']),
        ("Home Favorites", performance['home_favorites']),
        ("Home Underdogs", performance['home_underdogs'])
    ]
    
    print(f"{'Category':<15} {'Record':<12} {'Percent':<8} {'Strategy'}")
    print("-" * 50)
    
    for category, data in categories:
        covers = data['covers']
        total = data['total']
        pct = data['pct']
        
        if pct > 55:
            strategy = "STRONG PICK"
        elif pct > 52:
            strategy = "MODERATE PICK"
        elif pct > 48:
            strategy = "SLIGHT EDGE"
        elif pct > 45:
            strategy = "SLIGHT FADE"
        else:
            strategy = "STRONG FADE"
        
        print(f"{category:<15} {covers}-{total-covers}-0 {pct:<8.1f}% {strategy}")
    
    # Overall trends
    print(f"\n=== Overall Trends ===")
    print(f"Favorites: {performance['favorite_covers']}/{performance['total_games']} ({performance['favorite_covers']/performance['total_games']*100:.1f}%)")
    print(f"Underdogs: {performance['underdog_covers']}/{performance['total_games']} ({performance['underdog_covers']/performance['total_games']*100:.1f}%)")
    
    return performance

def main():
    """Main function to calculate actual ATS performance"""
    
    print("=== Actual ATS Performance Analysis ===")
    print("Calculating real ATS trends from Week 1-7 results")
    print("=" * 60)
    
    # Load all results
    df = load_all_results()
    
    if df is not None:
        # Analyze actual ATS performance
        performance = analyze_actual_ats_performance(df)
        
        # Create summary table
        create_ats_summary_table(performance)
        
        # Save analysis
        output_file = "actual_ats_performance.csv"
        df.to_csv(output_file, index=False)
        print(f"\n✅ Analysis saved to {output_file}")
        
        print(f"\n=== Analysis Complete ===")
        print(f"📊 Analyzed {len(df)} games with actual results")
        print(f"📁 Data saved to {output_file}")
        print(f"🔍 Use this data to update Model C with real ATS trends")
        
    else:
        print("❌ Failed to load result data")

if __name__ == "__main__":
    main()
