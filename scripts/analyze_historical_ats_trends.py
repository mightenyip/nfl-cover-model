#!/usr/bin/env python3
"""
Analyze Historical ATS Trends from Week 1-7
Calculate actual performance of favorites/underdogs and home/away teams
"""

import pandas as pd
import numpy as np
import os
import glob
from datetime import datetime

def load_week_odds(week_num):
    """Load odds data for a specific week"""
    week_file = f"schedule/week{week_num}_2025_odds.csv"
    if os.path.exists(week_file):
        df = pd.read_csv(week_file)
        df['week'] = week_num
        return df
    return None

def load_all_weeks():
    """Load odds data for all weeks 1-7"""
    all_weeks = []
    
    for week in range(1, 8):  # Week 1 through Week 7
        week_data = load_week_odds(week)
        if week_data is not None:
            all_weeks.append(week_data)
            print(f"✅ Loaded Week {week}: {len(week_data)} games")
        else:
            print(f"❌ Week {week} data not found")
    
    if all_weeks:
        combined_df = pd.concat(all_weeks, ignore_index=True)
        print(f"\n📊 Total games loaded: {len(combined_df)}")
        return combined_df
    else:
        print("❌ No week data found")
        return None

def analyze_ats_trends(df):
    """Analyze ATS trends from historical odds data"""
    
    print("\n=== Historical ATS Trends Analysis (Week 1-7) ===")
    print("=" * 60)
    
    # Create analysis columns
    df['favorite_is_home'] = df['favorite_team'] == df['home_team']
    df['favorite_is_away'] = df['favorite_team'] == df['away_team']
    df['underdog_is_home'] = df['underdog_team'] == df['home_team']
    df['underdog_is_away'] = df['underdog_team'] == df['away_team']
    
    # Calculate spread categories
    df['spread_category'] = pd.cut(df['spread_line'].abs(), 
                                  bins=[0, 3.5, 6.5, 10, float('inf')], 
                                  labels=['Small (≤3.5)', 'Medium (3.5-6.5)', 'Large (6.5-10)', 'Very Large (>10)'])
    
    # Analyze by team position
    print("\n=== Team Position Analysis ===")
    
    # Away teams vs Home teams
    away_games = df[df['favorite_is_away'] | df['underdog_is_away']]
    home_games = df[df['favorite_is_home'] | df['underdog_is_home']]
    
    print(f"Away Teams: {len(away_games)} games")
    print(f"Home Teams: {len(home_games)} games")
    
    # Favorites vs Underdogs
    favorite_games = df[df['favorite_is_home'] | df['favorite_is_away']]
    underdog_games = df[df['underdog_is_home'] | df['underdog_is_away']]
    
    print(f"Favorites: {len(favorite_games)} games")
    print(f"Underdogs: {len(underdog_games)} games")
    
    # Specific combinations
    away_favorites = df[df['favorite_is_away']]
    away_underdogs = df[df['underdog_is_away']]
    home_favorites = df[df['favorite_is_home']]
    home_underdogs = df[df['underdog_is_home']]
    
    print(f"\n=== Specific Combinations ===")
    print(f"Away Favorites: {len(away_favorites)} games")
    print(f"Away Underdogs: {len(away_underdogs)} games")
    print(f"Home Favorites: {len(home_favorites)} games")
    print(f"Home Underdogs: {len(home_underdogs)} games")
    
    # Spread analysis
    print(f"\n=== Spread Analysis ===")
    spread_counts = df['spread_category'].value_counts()
    for category, count in spread_counts.items():
        print(f"{category}: {count} games")
    
    # Week-by-week breakdown
    print(f"\n=== Week-by-Week Breakdown ===")
    for week in sorted(df['week'].unique()):
        week_data = df[df['week'] == week]
        print(f"Week {week}: {len(week_data)} games")
        
        # Show sample games
        sample_games = week_data.head(3)
        for _, game in sample_games.iterrows():
            print(f"  {game['away_team']} @ {game['home_team']}: {game['favorite_team']} {game['spread_line']}")
    
    return df

def calculate_ats_performance(df):
    """Calculate ATS performance metrics"""
    
    print(f"\n=== ATS Performance Calculation ===")
    print("Note: This analysis shows the structure of games, not actual results")
    print("To get actual ATS performance, we would need the game results")
    
    # Show distribution of spreads
    print(f"\n=== Spread Distribution ===")
    spread_stats = df['spread_line'].describe()
    print(spread_stats)
    
    # Show favorite/underdog distribution
    print(f"\n=== Favorite/Underdog Distribution ===")
    fav_home = len(df[df['favorite_is_home']])
    fav_away = len(df[df['favorite_is_away']])
    dog_home = len(df[df['underdog_is_home']])
    dog_away = len(df[df['underdog_is_away']])
    
    print(f"Home Favorites: {fav_home} games ({fav_home/len(df)*100:.1f}%)")
    print(f"Away Favorites: {fav_away} games ({fav_away/len(df)*100:.1f}%)")
    print(f"Home Underdogs: {dog_home} games ({dog_home/len(df)*100:.1f}%)")
    print(f"Away Underdogs: {dog_away} games ({dog_away/len(df)*100:.1f}%)")
    
    # Show spread ranges
    print(f"\n=== Spread Range Analysis ===")
    small_spreads = df[df['spread_line'].abs() <= 3.5]
    medium_spreads = df[(df['spread_line'].abs() > 3.5) & (df['spread_line'].abs() <= 6.5)]
    large_spreads = df[df['spread_line'].abs() > 6.5]
    
    print(f"Small Spreads (≤3.5): {len(small_spreads)} games ({len(small_spreads)/len(df)*100:.1f}%)")
    print(f"Medium Spreads (3.5-6.5): {len(medium_spreads)} games ({len(medium_spreads)/len(df)*100:.1f}%)")
    print(f"Large Spreads (>6.5): {len(large_spreads)} games ({len(large_spreads)/len(df)*100:.1f}%)")
    
    return {
        'total_games': len(df),
        'home_favorites': fav_home,
        'away_favorites': fav_away,
        'home_underdogs': dog_home,
        'away_underdogs': dog_away,
        'small_spreads': len(small_spreads),
        'medium_spreads': len(medium_spreads),
        'large_spreads': len(large_spreads)
    }

def create_ats_summary(df):
    """Create a summary of ATS trends for Model C"""
    
    print(f"\n=== ATS Summary for Model C ===")
    
    # Calculate percentages
    total_games = len(df)
    home_fav_pct = len(df[df['favorite_is_home']]) / total_games * 100
    away_fav_pct = len(df[df['favorite_is_away']]) / total_games * 100
    home_dog_pct = len(df[df['underdog_is_home']]) / total_games * 100
    away_dog_pct = len(df[df['underdog_is_away']]) / total_games * 100
    
    print(f"Total Games Analyzed: {total_games}")
    print(f"Home Favorites: {home_fav_pct:.1f}%")
    print(f"Away Favorites: {away_fav_pct:.1f}%")
    print(f"Home Underdogs: {home_dog_pct:.1f}%")
    print(f"Away Underdogs: {away_dog_pct:.1f}%")
    
    # Show most common spreads
    print(f"\n=== Most Common Spreads ===")
    spread_counts = df['spread_line'].value_counts().head(10)
    for spread, count in spread_counts.items():
        print(f"{spread}: {count} games")
    
    # Show teams as favorites most often
    print(f"\n=== Teams as Favorites Most Often ===")
    fav_counts = df['favorite_team'].value_counts().head(10)
    for team, count in fav_counts.items():
        print(f"{team}: {count} times")
    
    # Show teams as underdogs most often
    print(f"\n=== Teams as Underdogs Most Often ===")
    dog_counts = df['underdog_team'].value_counts().head(10)
    for team, count in dog_counts.items():
        print(f"{team}: {count} times")
    
    return {
        'total_games': total_games,
        'home_favorites_pct': home_fav_pct,
        'away_favorites_pct': away_fav_pct,
        'home_underdogs_pct': home_dog_pct,
        'away_underdogs_pct': away_dog_pct
    }

def main():
    """Main function to analyze historical ATS trends"""
    
    print("=== Historical ATS Trends Analysis ===")
    print("Analyzing Week 1-7 odds data to understand game structure")
    print("=" * 60)
    
    # Load all weeks
    df = load_all_weeks()
    
    if df is not None:
        # Analyze trends
        df = analyze_ats_trends(df)
        
        # Calculate performance metrics
        performance = calculate_ats_performance(df)
        
        # Create summary
        summary = create_ats_summary(df)
        
        # Save analysis
        output_file = "historical_ats_analysis.csv"
        df.to_csv(output_file, index=False)
        print(f"\n✅ Analysis saved to {output_file}")
        
        print(f"\n=== Analysis Complete ===")
        print(f"📊 Analyzed {len(df)} games from Week 1-7")
        print(f"📁 Data saved to {output_file}")
        print(f"🔍 Use this data to update Model C with actual game structure")
        
    else:
        print("❌ Failed to load week data")

if __name__ == "__main__":
    main()
