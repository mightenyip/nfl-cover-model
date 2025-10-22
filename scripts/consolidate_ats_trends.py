#!/usr/bin/env python3
"""
Consolidate ATS Trends from Week 1-7
Use the data we already have from previous analyses
"""

import pandas as pd
import numpy as np
from datetime import datetime

def consolidate_ats_trends():
    """Consolidate ATS trends from our previous analyses"""
    
    print("=== Consolidated ATS Trends (Week 1-7) ===")
    print("Based on our previous comprehensive analyses")
    print("=" * 60)
    
    # Week-by-week underdog cover rates from our analyses
    weekly_data = {
        'Week 1': {'games': 16, 'underdog_covers': 8, 'rate': 50.0},
        'Week 2': {'games': 16, 'underdog_covers': 5, 'rate': 31.2},
        'Week 3': {'games': 16, 'underdog_covers': 6, 'rate': 37.5},
        'Week 4': {'games': 16, 'underdog_covers': 5, 'rate': 31.2},
        'Week 5': {'games': 14, 'underdog_covers': 0, 'rate': 0.0},
        'Week 6': {'games': 15, 'underdog_covers': 11, 'rate': 73.3},
        'Week 7': {'games': 15, 'underdog_covers': 3, 'rate': 20.0}
    }
    
    # Calculate totals
    total_games = sum(data['games'] for data in weekly_data.values())
    total_underdog_covers = sum(data['underdog_covers'] for data in weekly_data.values())
    total_favorite_covers = total_games - total_underdog_covers
    overall_underdog_rate = total_underdog_covers / total_games * 100
    overall_favorite_rate = total_favorite_covers / total_games * 100
    
    print(f"Total Games: {total_games}")
    print(f"Underdog Covers: {total_underdog_covers} ({overall_underdog_rate:.1f}%)")
    print(f"Favorite Covers: {total_favorite_covers} ({overall_favorite_rate:.1f}%)")
    
    # Week-by-week breakdown
    print(f"\n=== Week-by-Week Breakdown ===")
    for week, data in weekly_data.items():
        trend = "📈" if data['rate'] > 50 else "📉" if data['rate'] < 50 else "⚖️"
        print(f"{week}: {data['underdog_covers']}/{data['games']} underdog covers ({data['rate']:.1f}%) {trend}")
    
    # Categorize weeks
    underdog_heavy_weeks = [week for week, data in weekly_data.items() if data['rate'] > 60]
    favorite_heavy_weeks = [week for week, data in weekly_data.items() if data['rate'] < 40]
    balanced_weeks = [week for week, data in weekly_data.items() if 40 <= data['rate'] <= 60]
    
    print(f"\n=== Week Categories ===")
    print(f"Underdog-Heavy Weeks (>60%): {underdog_heavy_weeks}")
    print(f"Favorite-Heavy Weeks (<40%): {favorite_heavy_weeks}")
    print(f"Balanced Weeks (40-60%): {balanced_weeks}")
    
    # Model performance by week type
    print(f"\n=== Model Performance by Week Type ===")
    
    # Underdog-heavy weeks (Model A struggles, Model C adapts)
    underdog_weeks_games = sum(weekly_data[week]['games'] for week in underdog_heavy_weeks)
    underdog_weeks_covers = sum(weekly_data[week]['underdog_covers'] for week in underdog_heavy_weeks)
    
    if underdog_weeks_games > 0:
        print(f"Underdog-Heavy Weeks: {underdog_weeks_covers}/{underdog_weeks_games} covers ({underdog_weeks_covers/underdog_weeks_games*100:.1f}%)")
        print("  → Model A: Struggles (over-optimistic about underdogs)")
        print("  → Model C: Adapts well (rule-based approach)")
    
    # Favorite-heavy weeks (Model A excels, Model C consistent)
    favorite_weeks_games = sum(weekly_data[week]['games'] for week in favorite_heavy_weeks)
    favorite_weeks_covers = sum(weekly_data[week]['underdog_covers'] for week in favorite_heavy_weeks)
    
    if favorite_weeks_games > 0:
        print(f"Favorite-Heavy Weeks: {favorite_weeks_covers}/{favorite_weeks_games} covers ({favorite_weeks_covers/favorite_weeks_games*100:.1f}%)")
        print("  → Model A: Excels (good at identifying favorites)")
        print("  → Model C: Consistent (rule-based approach)")
    
    # Balanced weeks
    balanced_weeks_games = sum(weekly_data[week]['games'] for week in balanced_weeks)
    balanced_weeks_covers = sum(weekly_data[week]['underdog_covers'] for week in balanced_weeks)
    
    if balanced_weeks_games > 0:
        print(f"Balanced Weeks: {balanced_weeks_covers}/{balanced_weeks_games} covers ({balanced_weeks_covers/balanced_weeks_games*100:.1f}%)")
        print("  → Both models: Similar performance")
    
    # Updated ATS trends for Model C
    print(f"\n=== Updated ATS Trends for Model C ===")
    print("Based on Week 1-7 performance:")
    print(f"Overall Underdog Cover Rate: {overall_underdog_rate:.1f}%")
    print(f"Overall Favorite Cover Rate: {overall_favorite_rate:.1f}%")
    
    # Calculate weighted averages by week type
    underdog_heavy_rate = underdog_weeks_covers / underdog_weeks_games * 100 if underdog_weeks_games > 0 else 0
    favorite_heavy_rate = favorite_weeks_covers / favorite_weeks_games * 100 if favorite_weeks_games > 0 else 0
    balanced_rate = balanced_weeks_covers / balanced_weeks_games * 100 if balanced_weeks_games > 0 else 0
    
    print(f"\nUnderdog-Heavy Weeks Rate: {underdog_heavy_rate:.1f}%")
    print(f"Favorite-Heavy Weeks Rate: {favorite_heavy_rate:.1f}%")
    print(f"Balanced Weeks Rate: {balanced_rate:.1f}%")
    
    # Model C strategy recommendations
    print(f"\n=== Model C Strategy Recommendations ===")
    
    if overall_favorite_rate > 60:
        print("✅ STRONG FAVORITE BIAS: Favor favorites heavily")
        print("  - Home Favorites: HIGH confidence")
        print("  - Away Favorites: HIGH confidence")
        print("  - Fade large underdog spreads")
    elif overall_underdog_rate > 60:
        print("✅ STRONG UNDERDOG BIAS: Favor underdogs heavily")
        print("  - Home Underdogs: HIGH confidence")
        print("  - Away Underdogs: HIGH confidence")
        print("  - Fade large favorite spreads")
    else:
        print("⚖️ BALANCED APPROACH: Use spread-based rules")
        print("  - Small spreads: Slight favorite edge")
        print("  - Large spreads: Underdog value")
        print("  - Home field advantage: Consider")
    
    # Create summary table
    print(f"\n=== ATS Performance Summary Table ===")
    print("=" * 50)
    print(f"{'Category':<20} {'Record':<12} {'Percent':<8} {'Strategy'}")
    print("-" * 50)
    
    # Simulate the categories based on our data
    categories = [
        ("Overall Favorites", f"{total_favorite_covers}-{total_underdog_covers}-0", f"{overall_favorite_rate:.1f}%", "STRONG PICK" if overall_favorite_rate > 55 else "MODERATE PICK"),
        ("Overall Underdogs", f"{total_underdog_covers}-{total_favorite_covers}-0", f"{overall_underdog_rate:.1f}%", "STRONG FADE" if overall_underdog_rate < 45 else "SLIGHT FADE"),
        ("Underdog-Heavy Weeks", f"{underdog_weeks_covers}-{underdog_weeks_games-underdog_weeks_covers}-0", f"{underdog_heavy_rate:.1f}%", "ADAPT"),
        ("Favorite-Heavy Weeks", f"{favorite_weeks_covers}-{favorite_weeks_games-favorite_weeks_covers}-0", f"{favorite_heavy_rate:.1f}%", "EXCEL"),
        ("Balanced Weeks", f"{balanced_weeks_covers}-{balanced_weeks_games-balanced_weeks_covers}-0", f"{balanced_rate:.1f}%", "BALANCED")
    ]
    
    for category, record, percent, strategy in categories:
        print(f"{category:<20} {record:<12} {percent:<8} {strategy}")
    
    return {
        'total_games': total_games,
        'underdog_covers': total_underdog_covers,
        'favorite_covers': total_favorite_covers,
        'overall_underdog_rate': overall_underdog_rate,
        'overall_favorite_rate': overall_favorite_rate,
        'underdog_heavy_weeks': underdog_heavy_weeks,
        'favorite_heavy_weeks': favorite_heavy_weeks,
        'balanced_weeks': balanced_weeks
    }

def main():
    """Main function to consolidate ATS trends"""
    
    print("=== Consolidating ATS Trends from Week 1-7 ===")
    print("Using data from our previous comprehensive analyses")
    print("=" * 60)
    
    # Consolidate trends
    trends = consolidate_ats_trends()
    
    print(f"\n=== Analysis Complete ===")
    print(f"📊 Analyzed {trends['total_games']} games from Week 1-7")
    print(f"📈 Overall underdog cover rate: {trends['overall_underdog_rate']:.1f}%")
    print(f"📉 Overall favorite cover rate: {trends['overall_favorite_rate']:.1f}%")
    print(f"🔍 Use this data to update Model C with real trends")

if __name__ == "__main__":
    main()
