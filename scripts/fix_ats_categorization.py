#!/usr/bin/env python3
"""
Fix ATS Categorization Bug
Correct the home_away_status categorization to properly identify all categories
"""

import pandas as pd

def fix_categorization():
    """Fix the categorization bug in master ATS data"""
    
    print("=== Fixing ATS Categorization Bug ===")
    print("Correcting home_away_status to properly identify all categories")
    print("=" * 60)
    
    # Load the data
    df = pd.read_csv("data/master_ats_trends.csv")
    
    print(f"Total games: {len(df)}")
    
    # Check current categorization
    print(f"\n=== Current Categorization ===")
    current_counts = df['home_away_status'].value_counts()
    print(current_counts)
    
    # Fix the categorization logic
    print(f"\n=== Fixing Categorization Logic ===")
    
    # Create proper categories
    df['away_favorite'] = (df['favorite'] == df['away_team'])
    df['home_favorite'] = (df['favorite'] == df['home_team'])
    df['away_underdog'] = (df['underdog'] == df['away_team'])
    df['home_underdog'] = (df['underdog'] == df['home_team'])
    
    # Verify the logic
    print(f"Away Favorites: {df['away_favorite'].sum()}")
    print(f"Home Favorites: {df['home_favorite'].sum()}")
    print(f"Away Underdogs: {df['away_underdog'].sum()}")
    print(f"Home Underdogs: {df['home_underdog'].sum()}")
    
    # Check for consistency
    total_favorites = df['away_favorite'].sum() + df['home_favorite'].sum()
    total_underdogs = df['away_underdog'].sum() + df['home_underdog'].sum()
    
    print(f"\n=== Consistency Check ===")
    print(f"Total Favorites: {total_favorites}")
    print(f"Total Underdogs: {total_underdogs}")
    print(f"Total Games: {len(df)}")
    print(f"Consistent: {total_favorites == total_underdogs == len(df)}")
    
    # Create corrected categorization
    def get_correct_category(row):
        if row['away_favorite']:
            return 'Away Favorite'
        elif row['home_favorite']:
            return 'Home Favorite'
        else:
            return 'ERROR'
    
    df['corrected_category'] = df.apply(get_correct_category, axis=1)
    
    # Also create the underdog perspective
    def get_underdog_category(row):
        if row['away_underdog']:
            return 'Away Underdog'
        elif row['home_underdog']:
            return 'Home Underdog'
        else:
            return 'ERROR'
    
    df['underdog_category'] = df.apply(get_underdog_category, axis=1)
    
    print(f"\n=== Corrected Categorization ===")
    print(f"From Favorite Perspective:")
    print(df['corrected_category'].value_counts())
    print(f"\nFrom Underdog Perspective:")
    print(df['underdog_category'].value_counts())
    
    # Calculate ATS performance by corrected categories
    print(f"\n=== ATS Performance by Corrected Categories ===")
    
    # Away Favorites (should be same as Home Underdogs)
    away_favs = df[df['away_favorite']]
    away_fav_underdog_covers = away_favs['underdog_covered'].sum()
    away_fav_total = len(away_favs)
    away_fav_rate = away_fav_underdog_covers / away_fav_total * 100
    
    print(f"Away Favorites: {away_fav_underdog_covers}/{away_fav_total} underdog covers ({away_fav_rate:.1f}%)")
    
    # Home Favorites (should be same as Away Underdogs)
    home_favs = df[df['home_favorite']]
    home_fav_underdog_covers = home_favs['underdog_covered'].sum()
    home_fav_total = len(home_favs)
    home_fav_rate = home_fav_underdog_covers / home_fav_total * 100
    
    print(f"Home Favorites: {home_fav_underdog_covers}/{home_fav_total} underdog covers ({home_fav_rate:.1f}%)")
    
    # From underdog perspective
    home_underdogs = df[df['home_underdog']]
    home_dog_covers = home_underdogs['underdog_covered'].sum()
    home_dog_total = len(home_underdogs)
    home_dog_rate = home_dog_covers / home_dog_total * 100
    
    print(f"Home Underdogs: {home_dog_covers}/{home_dog_total} underdog covers ({home_dog_rate:.1f}%)")
    
    away_underdogs = df[df['away_underdog']]
    away_dog_covers = away_underdogs['underdog_covered'].sum()
    away_dog_total = len(away_underdogs)
    away_dog_rate = away_dog_covers / away_dog_total * 100
    
    print(f"Away Underdogs: {away_dog_covers}/{away_dog_total} underdog covers ({away_dog_rate:.1f}%)")
    
    # Verify they match
    print(f"\n=== Verification ===")
    print(f"Away Favorites rate: {away_fav_rate:.1f}%")
    print(f"Home Underdogs rate: {home_dog_rate:.1f}%")
    print(f"Match: {abs(away_fav_rate - home_dog_rate) < 0.1}")
    
    print(f"Home Favorites rate: {home_fav_rate:.1f}%")
    print(f"Away Underdogs rate: {away_dog_rate:.1f}%")
    print(f"Match: {abs(home_fav_rate - away_dog_rate) < 0.1}")
    
    # Save corrected data
    output_file = "data/master_ats_trends_corrected.csv"
    df.to_csv(output_file, index=False)
    print(f"\n✅ Corrected data saved to {output_file}")
    
    return df

def main():
    """Main function"""
    print("=== Fixing ATS Categorization Bug ===")
    print("Correcting the categorization logic")
    print("=" * 60)
    
    df = fix_categorization()
    
    print(f"\n=== Fix Complete ===")
    print(f"📊 Data corrected and verified")
    print(f"📁 Saved to data/master_ats_trends_corrected.csv")

if __name__ == "__main__":
    main()
