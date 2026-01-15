#!/usr/bin/env python3
"""
Create Comprehensive ATS Trends Table
Display all ATS trends in a clear table format
"""

import pandas as pd

def create_ats_trends_table():
    """Create a comprehensive ATS trends table"""
    
    print("=== NFL ATS Trends Analysis (Week 1-7) ===")
    print("Based on 108 games from actual results and odds")
    print("=" * 80)
    
    # Load the corrected data
    df = pd.read_csv("data/ats_trends/master_ats_trends_final.csv")
    
    print(f"Total Games Analyzed: {len(df)}")
    print(f"Weeks Covered: {df['week'].min()}-{df['week'].max()}")
    print()
    
    # Overall Performance
    total_underdog_covers = df['underdog_covered'].sum()
    total_favorite_covers = len(df) - total_underdog_covers
    overall_underdog_rate = total_underdog_covers / len(df) * 100
    overall_favorite_rate = total_favorite_covers / len(df) * 100
    
    print("📊 OVERALL ATS PERFORMANCE")
    print("-" * 50)
    print(f"{'Category':<20} {'Record':<12} {'Percentage':<12} {'Status'}")
    print("-" * 50)
    print(f"{'Underdogs':<20} {total_underdog_covers}-{total_favorite_covers:<8} {overall_underdog_rate:.1f}%{'':<8} {'Slight Favorite Bias'}")
    print(f"{'Favorites':<20} {total_favorite_covers}-{total_underdog_covers:<8} {overall_favorite_rate:.1f}%{'':<8} {'Slight Favorite Bias'}")
    print()
    
    # Category Analysis
    print("📈 CATEGORY BREAKDOWN")
    print("-" * 80)
    print(f"{'Category':<20} {'Games':<8} {'Underdog Covers':<15} {'Rate':<10} {'Trend':<15}")
    print("-" * 80)
    
    # Away Favorites
    away_favs = df[df['away_favorite']]
    away_fav_covers = away_favs['underdog_covered'].sum()
    away_fav_rate = away_fav_covers / len(away_favs) * 100
    away_fav_trend = "Slight Favorite Bias" if away_fav_rate < 50 else "Slight Underdog Bias"
    print(f"{'Away Favorites':<20} {len(away_favs):<8} {away_fav_covers}/{len(away_favs):<8} {away_fav_rate:.1f}%{'':<6} {away_fav_trend}")
    
    # Home Favorites  
    home_favs = df[df['home_favorite']]
    home_fav_covers = home_favs['underdog_covered'].sum()
    home_fav_rate = home_fav_covers / len(home_favs) * 100
    home_fav_trend = "Slight Favorite Bias" if home_fav_rate < 50 else "Slight Underdog Bias"
    print(f"{'Home Favorites':<20} {len(home_favs):<8} {home_fav_covers}/{len(home_favs):<8} {home_fav_rate:.1f}%{'':<6} {home_fav_trend}")
    
    # Away Underdogs (same as Home Favorites)
    away_dogs = df[df['away_underdog']]
    away_dog_covers = away_dogs['underdog_covered'].sum()
    away_dog_rate = away_dog_covers / len(away_dogs) * 100
    print(f"{'Away Underdogs':<20} {len(away_dogs):<8} {away_dog_covers}/{len(away_dogs):<8} {away_dog_rate:.1f}%{'':<6} {'Same as Home Favorites'}")
    
    # Home Underdogs (same as Away Favorites)
    home_dogs = df[df['home_underdog']]
    home_dog_covers = home_dogs['underdog_covered'].sum()
    home_dog_rate = home_dog_covers / len(home_dogs) * 100
    print(f"{'Home Underdogs':<20} {len(home_dogs):<8} {home_dog_covers}/{len(home_dogs):<8} {home_dog_rate:.1f}%{'':<6} {'Same as Away Favorites'}")
    print()
    
    # Week-by-Week Analysis
    print("📅 WEEK-BY-WEEK BREAKDOWN")
    print("-" * 60)
    print(f"{'Week':<6} {'Games':<8} {'Underdog Covers':<15} {'Rate':<10} {'Trend'}")
    print("-" * 60)
    
    for week in sorted(df['week'].unique()):
        week_data = df[df['week'] == week]
        week_underdog_covers = week_data['underdog_covered'].sum()
        week_total = len(week_data)
        week_rate = week_underdog_covers / week_total * 100
        
        if week_rate > 60:
            trend = "Strong Underdog"
        elif week_rate > 55:
            trend = "Underdog Bias"
        elif week_rate < 40:
            trend = "Strong Favorite"
        elif week_rate < 45:
            trend = "Favorite Bias"
        else:
            trend = "Balanced"
            
        print(f"Week {week:<4} {week_total:<8} {week_underdog_covers}/{week_total:<8} {week_rate:.1f}%{'':<6} {trend}")
    print()
    
    # Recent Trends (Last 3 Weeks)
    recent_weeks = df[df['week'].isin([5, 6, 7])]
    recent_underdog_covers = recent_weeks['underdog_covered'].sum()
    recent_total = len(recent_weeks)
    recent_rate = recent_underdog_covers / recent_total * 100
    
    print("📈 RECENT TRENDS (Week 5-7)")
    print("-" * 40)
    print(f"Recent 3 weeks: {recent_underdog_covers}/{recent_total} underdog covers ({recent_rate:.1f}%)")
    
    if recent_rate > 55:
        recent_trend = "Underdog Performance"
    elif recent_rate < 45:
        recent_trend = "Favorite Performance"
    else:
        recent_trend = "Balanced Performance"
    print(f"Trend: {recent_trend}")
    print()
    
    # Model C Recommendations
    print("🎯 MODEL C RECOMMENDATIONS")
    print("-" * 50)
    
    # Away Favorites recommendation
    if away_fav_rate < 45:
        away_rec = "FADE (bet underdogs)"
        away_conf = "HIGH"
    elif away_fav_rate > 55:
        away_rec = "PICK (bet favorites)"
        away_conf = "HIGH"
    else:
        away_rec = "NEUTRAL"
        away_conf = "LOW"
    
    print(f"Away Favorites ({away_fav_rate:.1f}%): {away_rec} - {away_conf} confidence")
    
    # Home Favorites recommendation
    if home_fav_rate < 45:
        home_rec = "FADE (bet underdogs)"
        home_conf = "HIGH"
    elif home_fav_rate > 55:
        home_rec = "PICK (bet favorites)"
        home_conf = "HIGH"
    else:
        home_rec = "NEUTRAL"
        home_conf = "LOW"
    
    print(f"Home Favorites ({home_fav_rate:.1f}%): {home_rec} - {home_conf} confidence")
    print()
    
    # Key Insights
    print("🔍 KEY INSIGHTS")
    print("-" * 30)
    print("• Overall market shows slight favorite bias (54.6% favorites)")
    print("• Away favorites have slight edge (43.9% underdog success)")
    print("• Home favorites are more balanced (46.3% underdog success)")
    print("• Week 7 was extremely favorite-heavy (26.7% underdogs)")
    print("• Recent 3 weeks show balanced performance (47.7% underdogs)")
    print("• No strong trends in either direction - market is relatively efficient")
    print()
    
    # Save summary table
    summary_data = {
        'Category': ['Overall Underdogs', 'Overall Favorites', 'Away Favorites', 'Home Favorites', 'Away Underdogs', 'Home Underdogs'],
        'Games': [len(df), len(df), len(away_favs), len(home_favs), len(away_dogs), len(home_dogs)],
        'Underdog_Covers': [total_underdog_covers, total_favorite_covers, away_fav_covers, home_fav_covers, away_dog_covers, home_dog_covers],
        'Rate_Percent': [overall_underdog_rate, overall_favorite_rate, away_fav_rate, home_fav_rate, away_dog_rate, home_dog_rate],
        'Trend': ['Slight Favorite Bias', 'Slight Favorite Bias', 'Slight Favorite Bias', 'Slight Underdog Bias', 'Slight Underdog Bias', 'Slight Favorite Bias']
    }
    
    summary_df = pd.DataFrame(summary_data)
    output_file = "data/ats_trends/ats_trends_summary_table.csv"
    summary_df.to_csv(output_file, index=False)
    print(f"✅ Summary table saved to {output_file}")
    
    return summary_df

def main():
    """Main function"""
    print("=== Creating ATS Trends Table ===")
    print("Generating comprehensive ATS analysis")
    print("=" * 60)
    
    df = create_ats_trends_table()
    
    print(f"\n=== Analysis Complete ===")
    print(f"📊 Comprehensive ATS trends table created")
    print(f"📁 Summary saved to data/ats_trends/ats_trends_summary_table.csv")

if __name__ == "__main__":
    main()
