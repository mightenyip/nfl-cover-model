#!/usr/bin/env python3
"""
Show Real ATS Data from CSV Files
Display actual game results with odds to prove the numbers
"""

import pandas as pd
import numpy as np
import os

def show_week3_data():
    """Show Week 3 actual data"""
    print("=== WEEK 3 ACTUAL DATA ===")
    print("Source: week3/week3_all_models_predictions_vs_reality.csv")
    
    df = pd.read_csv("week3/week3_all_models_predictions_vs_reality.csv")
    
    print(f"Total games: {len(df)}")
    print(f"Columns: {list(df.columns)}")
    
    print(f"\nAll Week 3 games with actual results:")
    for _, game in df.iterrows():
        print(f"  {game['Game']}: {game['Final_Score']}")
        print(f"    Spread: {game['Favorite']} {game['Spread']}")
        print(f"    Underdog: {game['Underdog']}")
        print(f"    Actual Cover: {game['Actual_Cover']}")
        print(f"    Winner: {game['Actual_Winner']}")
        print()
    
    # Count actual covers
    underdog_covers = (df['Actual_Cover'] == 'Yes').sum()
    favorite_covers = (df['Actual_Cover'] == 'No').sum()
    
    print(f"Week 3 Summary:")
    print(f"  Underdog Covers: {underdog_covers}/{len(df)} ({underdog_covers/len(df)*100:.1f}%)")
    print(f"  Favorite Covers: {favorite_covers}/{len(df)} ({favorite_covers/len(df)*100:.1f}%)")
    
    return df

def show_week4_data():
    """Show Week 4 actual data"""
    print("=== WEEK 4 ACTUAL DATA ===")
    print("Source: week4/week4_model_predictions_vs_reality.csv")
    
    df = pd.read_csv("week4/week4_model_predictions_vs_reality.csv")
    
    print(f"Total games: {len(df)}")
    
    print(f"\nAll Week 4 games with actual results:")
    for _, game in df.iterrows():
        print(f"  {game['Game']}: {game['Final_Score']}")
        print(f"    Spread: {game['Favorite']} {game['Spread']}")
        print(f"    Underdog: {game['Underdog']}")
        print(f"    Actual Cover: {game['Actual_Cover']}")
        print(f"    Winner: {game['Actual_Winner']}")
        print()
    
    # Count actual covers
    underdog_covers = (df['Actual_Cover'] == 'Yes').sum()
    favorite_covers = (df['Actual_Cover'] == 'No').sum()
    
    print(f"Week 4 Summary:")
    print(f"  Underdog Covers: {underdog_covers}/{len(df)} ({underdog_covers/len(df)*100:.1f}%)")
    print(f"  Favorite Covers: {favorite_covers}/{len(df)} ({favorite_covers/len(df)*100:.1f}%)")
    
    return df

def show_week5_data():
    """Show Week 5 actual data"""
    print("=== WEEK 5 ACTUAL DATA ===")
    print("Source: week5/week5_model_predictions_vs_reality.csv")
    
    df = pd.read_csv("week5/week5_model_predictions_vs_reality.csv")
    
    print(f"Total games: {len(df)}")
    
    print(f"\nAll Week 5 games with actual results:")
    for _, game in df.iterrows():
        print(f"  {game['Game']}: {game['Final_Score']}")
        print(f"    Spread: {game['Favorite']} {game['Spread']}")
        print(f"    Underdog: {game['Underdog']}")
        print(f"    Actual Cover: {game['Actual_Cover']}")
        print(f"    Winner: {game['Actual_Winner']}")
        print()
    
    # Count actual covers
    underdog_covers = (df['Actual_Cover'] == 'Yes').sum()
    favorite_covers = (df['Actual_Cover'] == 'No').sum()
    
    print(f"Week 5 Summary:")
    print(f"  Underdog Covers: {underdog_covers}/{len(df)} ({underdog_covers/len(df)*100:.1f}%)")
    print(f"  Favorite Covers: {favorite_covers}/{len(df)} ({favorite_covers/len(df)*100:.1f}%)")
    
    return df

def calculate_total_ats_performance():
    """Calculate total ATS performance from all available weeks"""
    
    print("=== TOTAL ATS PERFORMANCE CALCULATION ===")
    print("Based on actual CSV files with game results")
    
    all_weeks = []
    
    # Week 3
    if os.path.exists("week3/week3_all_models_predictions_vs_reality.csv"):
        df3 = pd.read_csv("week3/week3_all_models_predictions_vs_reality.csv")
        df3['week'] = 3
        all_weeks.append(df3)
        print(f"Week 3: {len(df3)} games")
    
    # Week 4
    if os.path.exists("week4/week4_model_predictions_vs_reality.csv"):
        df4 = pd.read_csv("week4/week4_model_predictions_vs_reality.csv")
        df4['week'] = 4
        all_weeks.append(df4)
        print(f"Week 4: {len(df4)} games")
    
    # Week 5
    if os.path.exists("week5/week5_model_predictions_vs_reality.csv"):
        df5 = pd.read_csv("week5/week5_model_predictions_vs_reality.csv")
        df5['week'] = 5
        all_weeks.append(df5)
        print(f"Week 5: {len(df5)} games")
    
    if not all_weeks:
        print("❌ No data found")
        return
    
    # Combine all weeks
    combined_df = pd.concat(all_weeks, ignore_index=True)
    
    print(f"\nTotal games with actual results: {len(combined_df)}")
    
    # Calculate actual ATS performance
    underdog_covers = (combined_df['Actual_Cover'] == 'Yes').sum()
    favorite_covers = (combined_df['Actual_Cover'] == 'No').sum()
    
    print(f"\nACTUAL ATS PERFORMANCE:")
    print(f"  Underdog Covers: {underdog_covers}/{len(combined_df)} ({underdog_covers/len(combined_df)*100:.1f}%)")
    print(f"  Favorite Covers: {favorite_covers}/{len(combined_df)} ({favorite_covers/len(combined_df)*100:.1f}%)")
    
    # Week-by-week breakdown
    print(f"\nWeek-by-week breakdown:")
    for week in sorted(combined_df['week'].unique()):
        week_data = combined_df[combined_df['week'] == week]
        week_underdog_covers = (week_data['Actual_Cover'] == 'Yes').sum()
        week_total = len(week_data)
        week_rate = week_underdog_covers / week_total * 100
        
        print(f"  Week {week}: {week_underdog_covers}/{week_total} underdog covers ({week_rate:.1f}%)")
    
    return combined_df

def main():
    """Main function to show real ATS data"""
    
    print("=== SHOWING REAL ATS DATA FROM CSV FILES ===")
    print("These are the actual game results with odds from CSV files")
    print("=" * 70)
    
    # Show individual weeks
    if os.path.exists("week3/week3_all_models_predictions_vs_reality.csv"):
        show_week3_data()
    
    if os.path.exists("week4/week4_model_predictions_vs_reality.csv"):
        show_week4_data()
    
    if os.path.exists("week5/week5_model_predictions_vs_reality.csv"):
        show_week5_data()
    
    # Calculate total performance
    calculate_total_ats_performance()
    
    print(f"\n=== VERIFICATION COMPLETE ===")
    print(f"📊 All numbers come from actual CSV files")
    print(f"📁 You can verify by opening these files:")
    print(f"   - week3/week3_all_models_predictions_vs_reality.csv")
    print(f"   - week4/week4_model_predictions_vs_reality.csv")
    print(f"   - week5/week5_model_predictions_vs_reality.csv")

if __name__ == "__main__":
    main()
