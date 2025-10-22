#!/usr/bin/env python3
"""
Verify Actual ATS Data from Real CSV Files
Show the actual game results with odds to prove the numbers
"""

import pandas as pd
import numpy as np
import os
import glob

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
                print(f"✅ Found Week {week_num} data in: {file_path}")
                return df
    return None

def analyze_actual_ats_data():
    """Analyze actual ATS data from real CSV files"""
    
    print("=== VERIFYING ACTUAL ATS DATA FROM REAL CSV FILES ===")
    print("Reading actual game results with odds from CSV files")
    print("=" * 70)
    
    all_weeks_data = []
    
    # Load data for each week
    for week in range(1, 8):  # Week 1 through Week 7
        week_data = load_week_results(week)
        if week_data is not None:
            all_weeks_data.append(week_data)
            print(f"Week {week}: {len(week_data)} games loaded")
        else:
            print(f"Week {week}: No data found")
    
    if not all_weeks_data:
        print("❌ No data found for any week")
        return
    
    # Combine all weeks
    combined_df = pd.concat(all_weeks_data, ignore_index=True)
    print(f"\n📊 Total games with actual results: {len(combined_df)}")
    
    # Show sample data
    print(f"\n=== SAMPLE DATA FROM CSV FILES ===")
    print("Showing first 5 games with actual results:")
    sample_cols = ['Game', 'Favorite', 'Underdog', 'Spread', 'Final_Score', 'Actual_Cover']
    if all(col in combined_df.columns for col in sample_cols):
        print(combined_df[sample_cols].head().to_string(index=False))
    else:
        print("Available columns:", list(combined_df.columns))
        print(combined_df.head())
    
    # Calculate actual ATS performance
    print(f"\n=== ACTUAL ATS PERFORMANCE CALCULATION ===")
    
    total_games = len(combined_df)
    underdog_covers = combined_df['Actual_Cover'].sum()
    favorite_covers = total_games - underdog_covers
    
    print(f"Total Games: {total_games}")
    print(f"Underdog Covers: {underdog_covers} ({underdog_covers/total_games*100:.1f}%)")
    print(f"Favorite Covers: {favorite_covers} ({favorite_covers/total_games*100:.1f}%)")
    
    # Week-by-week breakdown
    print(f"\n=== WEEK-BY-WEEK ACTUAL RESULTS ===")
    for week in sorted(combined_df['week'].unique()):
        week_data = combined_df[combined_df['week'] == week]
        week_underdog_covers = week_data['Actual_Cover'].sum()
        week_total = len(week_data)
        week_rate = week_underdog_covers / week_total * 100
        
        print(f"Week {week}: {week_underdog_covers}/{week_total} underdog covers ({week_rate:.1f}%)")
        
        # Show sample games from this week
        print(f"  Sample games:")
        for _, game in week_data.head(3).iterrows():
            game_name = game.get('Game', 'Unknown')
            final_score = game.get('Final_Score', 'Unknown')
            actual_cover = game.get('Actual_Cover', 'Unknown')
            spread = game.get('Spread', 'Unknown')
            print(f"    {game_name}: {final_score} - {actual_cover} (Spread: {spread})")
    
    # Show the actual data source
    print(f"\n=== DATA SOURCE VERIFICATION ===")
    print("These numbers come from the following CSV files:")
    
    for week in range(1, 8):
        week_data = load_week_results(week)
        if week_data is not None:
            print(f"Week {week}: {len(week_data)} games")
            # Show file path
            result_files = [
                f"week{week}/week{week}_all_models_predictions_vs_reality.csv",
                f"week{week}/week{week}_model_predictions_vs_reality.csv",
                f"week{week}/week{week}_all_models_comparison.csv"
            ]
            
            for file_path in result_files:
                if os.path.exists(file_path):
                    print(f"  Source: {file_path}")
                    break
    
    # Save the combined data for verification
    output_file = "verified_ats_data.csv"
    combined_df.to_csv(output_file, index=False)
    print(f"\n✅ All data saved to {output_file} for verification")
    
    return combined_df

def show_specific_game_examples():
    """Show specific game examples with actual results"""
    
    print(f"\n=== SPECIFIC GAME EXAMPLES ===")
    print("Showing actual game results with odds:")
    
    # Week 3 examples
    week3_file = "week3/week3_all_models_predictions_vs_reality.csv"
    if os.path.exists(week3_file):
        df = pd.read_csv(week3_file)
        print(f"\nWeek 3 Examples (from {week3_file}):")
        for _, game in df.head(5).iterrows():
            print(f"  {game['Game']}: {game['Final_Score']}")
            print(f"    Spread: {game['Favorite']} {game['Spread']}")
            print(f"    Underdog: {game['Underdog']}")
            print(f"    Actual Cover: {game['Actual_Cover']}")
            print(f"    Winner: {game['Actual_Winner']}")
            print()
    
    # Week 4 examples
    week4_file = "week4/week4_model_predictions_vs_reality.csv"
    if os.path.exists(week4_file):
        df = pd.read_csv(week4_file)
        print(f"Week 4 Examples (from {week4_file}):")
        for _, game in df.head(5).iterrows():
            print(f"  {game['Game']}: {game['Final_Score']}")
            print(f"    Spread: {game['Favorite']} {game['Spread']}")
            print(f"    Underdog: {game['Underdog']}")
            print(f"    Actual Cover: {game['Actual_Cover']}")
            print(f"    Winner: {game['Actual_Winner']}")
            print()

def main():
    """Main function to verify actual ATS data"""
    
    print("=== VERIFYING ACTUAL ATS DATA ===")
    print("Reading real CSV files with game results and odds")
    print("=" * 60)
    
    # Analyze actual data
    df = analyze_actual_ats_data()
    
    # Show specific examples
    show_specific_game_examples()
    
    print(f"\n=== VERIFICATION COMPLETE ===")
    print(f"📊 All numbers are from actual CSV files with game results")
    print(f"📁 Data sources: week*/week*_*_predictions_vs_reality.csv")
    print(f"🔍 You can verify by opening these CSV files")

if __name__ == "__main__":
    main()
