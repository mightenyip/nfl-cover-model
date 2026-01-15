#!/usr/bin/env python3
"""
Combined Week 1-6 ATS Analysis
Calculate overall performance from all six weeks
"""

import pandas as pd

def combine_week1_week6_ats():
    """Combine Week 1, 2, 3, 4, 5, and 6 ATS results"""
    
    print("=== Combined Week 1-6 ATS Analysis ===")
    print("Based on actual game results and odds")
    print("=" * 60)
    
    # Load all weeks
    week1_df = pd.read_csv("data/ats_results/week1/week1_ats_results.csv")
    week1_df['week'] = 1
    
    week2_df = pd.read_csv("data/ats_results/week2/week2_ats_results.csv")
    week2_df['week'] = 2
    
    week3_df = pd.read_csv("data/ats_results/week3/week3_ats_results.csv")
    week3_df['week'] = 3
    
    week4_df = pd.read_csv("data/ats_results/week4/week4_ats_results.csv")
    week4_df['week'] = 4
    
    week5_df = pd.read_csv("data/ats_results/week5/week5_ats_results.csv")
    week5_df['week'] = 5
    
    week6_df = pd.read_csv("data/ats_results/week6/week6_ats_results.csv")
    week6_df['week'] = 6
    
    # Combine results
    combined_df = pd.concat([week1_df, week2_df, week3_df, week4_df, week5_df, week6_df], ignore_index=True)
    
    print(f"Total Games: {len(combined_df)}")
    print(f"Week 1: {len(week1_df)} games")
    print(f"Week 2: {len(week2_df)} games")
    print(f"Week 3: {len(week3_df)} games")
    print(f"Week 4: {len(week4_df)} games")
    print(f"Week 5: {len(week5_df)} games")
    print(f"Week 6: {len(week6_df)} games")
    
    # Calculate overall performance
    total_underdog_covers = combined_df['underdog_covered'].sum()
    total_favorite_covers = len(combined_df) - total_underdog_covers
    
    print(f"\n=== Overall ATS Performance (Week 1-6) ===")
    print(f"Underdog Covers: {total_underdog_covers}/{len(combined_df)} ({total_underdog_covers/len(combined_df)*100:.1f}%)")
    print(f"Favorite Covers: {total_favorite_covers}/{len(combined_df)} ({total_favorite_covers/len(combined_df)*100:.1f}%)")
    
    # Week-by-week breakdown
    print(f"\n=== Week-by-Week Breakdown ===")
    for week in [1, 2, 3, 4, 5, 6]:
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
    week4_rate = (week4_df['underdog_covered'].sum() / len(week4_df)) * 100
    week5_rate = (week5_df['underdog_covered'].sum() / len(week5_df)) * 100
    week6_rate = (week6_df['underdog_covered'].sum() / len(week6_df)) * 100
    
    print(f"Week 1: {week1_rate:.1f}% underdog covers")
    print(f"Week 2: {week2_rate:.1f}% underdog covers")
    print(f"Week 3: {week3_rate:.1f}% underdog covers")
    print(f"Week 4: {week4_rate:.1f}% underdog covers")
    print(f"Week 5: {week5_rate:.1f}% underdog covers")
    print(f"Week 6: {week6_rate:.1f}% underdog covers")
    
    # Calculate trend
    rates = [week1_rate, week2_rate, week3_rate, week4_rate, week5_rate, week6_rate]
    if all(rates[i] >= rates[i+1] for i in range(len(rates)-1)):
        print("📉 TREND: Consistently decreasing underdog success rate")
    elif all(rates[i] <= rates[i+1] for i in range(len(rates)-1)):
        print("📈 TREND: Consistently increasing underdog success rate")
    else:
        print("📊 TREND: Mixed underdog success rate")
    
    # Model C implications
    print(f"\n=== Model C Implications ===")
    overall_favorite_rate = (total_favorite_covers / len(combined_df)) * 100
    overall_underdog_rate = (total_underdog_covers / len(combined_df)) * 100
    
    if overall_favorite_rate > 55:
        print(f"✅ STRONG FAVORITE BIAS: {overall_favorite_rate:.1f}% favorite success rate")
        print("  - Model C should heavily favor favorites")
        print("  - Use HIGH confidence for favorite picks")
        print("  - Fade large underdog spreads")
    elif overall_underdog_rate > 55:
        print(f"✅ STRONG UNDERDOG BIAS: {overall_underdog_rate:.1f}% underdog success rate")
        print("  - Model C should favor underdogs")
        print("  - Use HIGH confidence for underdog picks")
        print("  - Fade large favorite spreads")
    else:
        print(f"⚖️ BALANCED APPROACH: {overall_favorite_rate:.1f}% favorites vs {overall_underdog_rate:.1f}% underdogs")
        print("  - Model C should use spread-based rules")
        print("  - Consider home field advantage")
        print("  - Fade large spreads regardless of direction")
    
    # Recent trend analysis (last 3 weeks)
    print(f"\n=== Recent Trend Analysis (Week 4-6) ===")
    recent_weeks = combined_df[combined_df['week'].isin([4, 5, 6])]
    recent_underdog_covers = recent_weeks['underdog_covered'].sum()
    recent_total = len(recent_weeks)
    recent_rate = recent_underdog_covers / recent_total * 100
    
    print(f"Recent 3 weeks: {recent_underdog_covers}/{recent_total} underdog covers ({recent_rate:.1f}%)")
    
    if recent_rate > 55:
        print("📈 RECENT TREND: Strong underdog performance recently")
    elif recent_rate < 45:
        print("📉 RECENT TREND: Strong favorite performance recently")
    else:
        print("⚖️ RECENT TREND: Balanced performance recently")
    
    # Save combined results
    output_file = "data/ats_trends/combined/combined_week1_week6_ats.csv"
    combined_df.to_csv(output_file, index=False)
    print(f"\n✅ Combined results saved to {output_file}")
    
    return combined_df

def main():
    """Main function"""
    print("=== Combined Week 1-6 ATS Analysis ===")
    print("Calculating overall performance from all six weeks")
    print("=" * 60)
    
    df = combine_week1_week6_ats()
    
    print(f"\n=== Analysis Complete ===")
    print(f"📊 Combined ATS Performance: {df['underdog_covered'].sum()}/{len(df)} underdog covers")
    print(f"📁 Results saved to data/ats_trends/combined/combined_week1_week6_ats.csv")

if __name__ == "__main__":
    main()
