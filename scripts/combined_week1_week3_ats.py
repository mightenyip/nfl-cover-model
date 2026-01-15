#!/usr/bin/env python3
"""
Combined Week 1-3 ATS Analysis
Calculate overall performance from all three weeks
"""

import pandas as pd

def combine_week1_week3_ats():
    """Combine Week 1, 2, and 3 ATS results"""
    
    print("=== Combined Week 1-3 ATS Analysis ===")
    print("Based on actual game results and odds")
    print("=" * 60)
    
    # Load all weeks
    week1_df = pd.read_csv("data/ats_results/week1/week1_ats_results.csv")
    week1_df['week'] = 1
    
    week2_df = pd.read_csv("data/ats_results/week2/week2_ats_results.csv")
    week2_df['week'] = 2
    
    week3_df = pd.read_csv("data/ats_results/week3/week3_ats_results.csv")
    week3_df['week'] = 3
    
    # Combine results
    combined_df = pd.concat([week1_df, week2_df, week3_df], ignore_index=True)
    
    print(f"Total Games: {len(combined_df)}")
    print(f"Week 1: {len(week1_df)} games")
    print(f"Week 2: {len(week2_df)} games")
    print(f"Week 3: {len(week3_df)} games")
    
    # Calculate overall performance
    total_underdog_covers = combined_df['underdog_covered'].sum()
    total_favorite_covers = len(combined_df) - total_underdog_covers
    
    print(f"\n=== Overall ATS Performance (Week 1-3) ===")
    print(f"Underdog Covers: {total_underdog_covers}/{len(combined_df)} ({total_underdog_covers/len(combined_df)*100:.1f}%)")
    print(f"Favorite Covers: {total_favorite_covers}/{len(combined_df)} ({total_favorite_covers/len(combined_df)*100:.1f}%)")
    
    # Week-by-week breakdown
    print(f"\n=== Week-by-Week Breakdown ===")
    for week in [1, 2, 3]:
        week_data = combined_df[combined_df['week'] == week]
        week_underdog_covers = week_data['underdog_covered'].sum()
        week_total = len(week_data)
        week_rate = week_underdog_covers / week_total * 100
        
        print(f"Week {week}: {week_underdog_covers}/{week_total} underdog covers ({week_rate:.1f}%)")
    
    # Trend analysis
    print(f"\n=== Trend Analysis ===")
    week1_rate = (week1_df['underdog_covered'].sum() / len(week1_df)) * 100
    week2_rate = (week2_df['underdog_covered'].sum() / len(week2_df)) * 100
    week3_rate = (week3_df['underdog_covered'].sum() / len(week3_df)) * 100
    
    print(f"Week 1: {week1_rate:.1f}% underdog covers")
    print(f"Week 2: {week2_rate:.1f}% underdog covers")
    print(f"Week 3: {week3_rate:.1f}% underdog covers")
    
    if week3_rate < week2_rate < week1_rate:
        print("📉 TREND: Decreasing underdog success rate")
    elif week3_rate > week2_rate > week1_rate:
        print("📈 TREND: Increasing underdog success rate")
    else:
        print("📊 TREND: Mixed underdog success rate")
    
    # Save combined results
    output_file = "data/ats_trends/combined/combined_week1_week3_ats.csv"
    combined_df.to_csv(output_file, index=False)
    print(f"\n✅ Combined results saved to {output_file}")
    
    return combined_df

def main():
    """Main function"""
    print("=== Combined Week 1-3 ATS Analysis ===")
    print("Calculating overall performance from all three weeks")
    print("=" * 60)
    
    df = combine_week1_week3_ats()
    
    print(f"\n=== Analysis Complete ===")
    print(f"📊 Combined ATS Performance: {df['underdog_covered'].sum()}/{len(df)} underdog covers")
    print(f"📁 Results saved to data/ats_trends/combined/combined_week1_week3_ats.csv")

if __name__ == "__main__":
    main()
