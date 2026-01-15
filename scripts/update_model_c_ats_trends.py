#!/usr/bin/env python3
"""
Update Model C ATS Trends
Automatically calculate and update ATS trends for Model C based on master data
"""

import pandas as pd
import numpy as np

def calculate_ats_trends():
    """Calculate comprehensive ATS trends from master data"""
    
    print("=== Model C ATS Trends Calculator ===")
    print("Updating trends based on master ATS data")
    print("=" * 60)
    
    # Load master ATS data
    df = pd.read_csv("data/ats_trends/master_ats_trends.csv")
    
    print(f"Total Games: {len(df)}")
    print(f"Weeks Covered: {df['week'].min()} - {df['week'].max()}")
    
    # Calculate overall trends
    total_games = len(df)
    underdog_covers = df['underdog_covered'].sum()
    favorite_covers = total_games - underdog_covers
    
    print(f"\n=== Overall ATS Performance ===")
    print(f"Underdog Covers: {underdog_covers}/{total_games} ({underdog_covers/total_games*100:.1f}%)")
    print(f"Favorite Covers: {favorite_covers}/{total_games} ({favorite_covers/total_games*100:.1f}%)")
    
    # Calculate trends by category
    print(f"\n=== ATS Trends by Category ===")
    
    # Away vs Home
    away_games = df[df['home_away_status'].str.contains('Away')]
    home_games = df[df['home_away_status'].str.contains('Home')]
    
    away_underdog_covers = away_games['underdog_covered'].sum()
    away_total = len(away_games)
    home_underdog_covers = home_games['underdog_covered'].sum()
    home_total = len(home_games)
    
    print(f"Away Teams: {away_underdog_covers}/{away_total} underdog covers ({away_underdog_covers/away_total*100:.1f}%)")
    print(f"Home Teams: {home_underdog_covers}/{home_total} underdog covers ({home_underdog_covers/home_total*100:.1f}%)")
    
    # Favorites vs Dogs
    favorite_games = df[df['home_away_status'].str.contains('Favorite')]
    dog_games = df[df['home_away_status'].str.contains('Underdog')]
    
    favorite_underdog_covers = favorite_games['underdog_covered'].sum()
    favorite_total = len(favorite_games)
    dog_underdog_covers = dog_games['underdog_covered'].sum()
    dog_total = len(dog_games)
    
    print(f"Favorites: {favorite_underdog_covers}/{favorite_total} underdog covers ({favorite_underdog_covers/favorite_total*100:.1f}%)")
    print(f"Dogs: {dog_underdog_covers}/{dog_total} underdog covers ({dog_underdog_covers/dog_total*100:.1f}%)")
    
    # Specific categories
    categories = {
        'Away Favorites': df[df['home_away_status'] == 'Away Favorite'],
        'Away Dogs': df[df['home_away_status'] == 'Away Underdog'],
        'Home Favorites': df[df['home_away_status'] == 'Home Favorite'],
        'Home Dogs': df[df['home_away_status'] == 'Home Underdog']
    }
    
    print(f"\n=== Detailed Category Analysis ===")
    category_results = {}
    
    for category, data in categories.items():
        if len(data) > 0:
            underdog_covers = data['underdog_covered'].sum()
            total = len(data)
            rate = underdog_covers / total * 100 if total > 0 else 0
            
            category_results[category] = {
                'underdog_covers': underdog_covers,
                'total': total,
                'rate': rate
            }
            
            print(f"{category}: {underdog_covers}/{total} underdog covers ({rate:.1f}%)")
        else:
            print(f"{category}: No data available")
    
    # Week-by-week analysis
    print(f"\n=== Week-by-Week Analysis ===")
    week_analysis = {}
    
    for week in sorted(df['week'].unique()):
        week_data = df[df['week'] == week]
        week_underdog_covers = week_data['underdog_covered'].sum()
        week_total = len(week_data)
        week_rate = week_underdog_covers / week_total * 100
        
        week_analysis[week] = {
            'underdog_covers': week_underdog_covers,
            'total': week_total,
            'rate': week_rate
        }
        
        print(f"Week {week}: {week_underdog_covers}/{week_total} underdog covers ({week_rate:.1f}%)")
    
    # Recent trend analysis (last 3 weeks)
    recent_weeks = df[df['week'].isin(sorted(df['week'].unique())[-3:])]
    recent_underdog_covers = recent_weeks['underdog_covered'].sum()
    recent_total = len(recent_weeks)
    recent_rate = recent_underdog_covers / recent_total * 100
    
    print(f"\n=== Recent Trend Analysis (Last 3 Weeks) ===")
    print(f"Recent: {recent_underdog_covers}/{recent_total} underdog covers ({recent_rate:.1f}%)")
    
    # Model C recommendations
    print(f"\n=== Model C Recommendations ===")
    
    # Find strongest and weakest trends
    if category_results:
        strongest_category = max(category_results.items(), key=lambda x: x[1]['rate'])
        weakest_category = min(category_results.items(), key=lambda x: x[1]['rate'])
        
        print(f"🔥 STRONGEST TREND: {strongest_category[0]} ({strongest_category[1]['rate']:.1f}%)")
        print(f"❄️ WEAKEST TREND: {weakest_category[0]} ({weakest_category[1]['rate']:.1f}%)")
        
        # Generate Model C rules
        print(f"\n=== Model C Updated Rules ===")
        
        for category, data in category_results.items():
            if data['total'] >= 5:  # Only include categories with sufficient data
                rate = data['rate']
                if rate > 60:
                    confidence = "HIGH"
                    recommendation = "STRONG PICK"
                elif rate > 55:
                    confidence = "MEDIUM"
                    recommendation = "GOOD PICK"
                elif rate < 40:
                    confidence = "HIGH"
                    recommendation = "FADE (opposite side)"
                elif rate < 45:
                    confidence = "MEDIUM"
                    recommendation = "SLIGHT FADE"
                else:
                    confidence = "LOW"
                    recommendation = "NEUTRAL"
                
                print(f"{category}: {rate:.1f}% → {confidence} confidence, {recommendation}")
    
    # Save updated trends
    trends_summary = {
        'overall_underdog_rate': underdog_covers / total_games * 100,
        'overall_favorite_rate': favorite_covers / total_games * 100,
        'recent_rate': recent_rate,
        'category_results': category_results,
        'week_analysis': week_analysis
    }
    
    # Save to file
    output_file = "data/trends/model_c_updated_trends.csv"
    trends_df = pd.DataFrame([
        {
            'category': 'Overall Underdogs',
            'record': f"{underdog_covers}-{favorite_covers}",
            'percentage': f"{underdog_covers/total_games*100:.1f}%",
            'confidence': 'MEDIUM' if 45 <= underdog_covers/total_games*100 <= 55 else 'HIGH'
        },
        {
            'category': 'Overall Favorites',
            'record': f"{favorite_covers}-{underdog_covers}",
            'percentage': f"{favorite_covers/total_games*100:.1f}%",
            'confidence': 'MEDIUM' if 45 <= favorite_covers/total_games*100 <= 55 else 'HIGH'
        }
    ])
    
    for category, data in category_results.items():
        if data['total'] >= 5:
            trends_df = pd.concat([trends_df, pd.DataFrame([{
                'category': category,
                'record': f"{data['underdog_covers']}-{data['total'] - data['underdog_covers']}",
                'percentage': f"{data['rate']:.1f}%",
                'confidence': 'HIGH' if data['rate'] > 60 or data['rate'] < 40 else 'MEDIUM' if data['rate'] > 55 or data['rate'] < 45 else 'LOW'
            }])], ignore_index=True)
    
    trends_df.to_csv(output_file, index=False)
    print(f"\n✅ Updated trends saved to {output_file}")
    
    return trends_summary

def main():
    """Main function"""
    print("=== Model C ATS Trends Updater ===")
    print("Calculating updated trends for Model C")
    print("=" * 60)
    
    trends = calculate_ats_trends()
    
    print(f"\n=== Update Complete ===")
    print(f"📊 Overall: {trends['overall_underdog_rate']:.1f}% underdogs, {trends['overall_favorite_rate']:.1f}% favorites")
    print(f"📈 Recent: {trends['recent_rate']:.1f}% underdogs")
    print(f"📁 Trends saved to data/trends/model_c_updated_trends.csv")

if __name__ == "__main__":
    main()
