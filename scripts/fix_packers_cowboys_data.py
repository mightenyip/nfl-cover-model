#!/usr/bin/env python3
"""
Fix Packers @ Cowboys Data Error
Correct the favorite/underdog designation for the Packers @ Cowboys game
"""

import pandas as pd

def fix_packers_cowboys_data():
    """Fix the Packers @ Cowboys data error"""
    
    print("=== Fixing Packers @ Cowboys Data Error ===")
    print("Correcting the favorite/underdog designation")
    print("=" * 60)
    
    # Load the data
    df = pd.read_csv("data/ats_trends/master_ats_trends.csv")
    
    print(f"Total games: {len(df)}")
    
    # Find the Packers @ Cowboys game
    packers_game = df[df['game'] == 'Packers @ Cowboys']
    print(f"\n=== Packers @ Cowboys Game ===")
    print(f"Current data:")
    print(f"  Game: {packers_game['game'].iloc[0]}")
    print(f"  Favorite: {packers_game['favorite'].iloc[0]}")
    print(f"  Underdog: {packers_game['underdog'].iloc[0]}")
    print(f"  Spread: {packers_game['spread_line'].iloc[0]}")
    
    # Correct the data
    df.loc[df['game'] == 'Packers @ Cowboys', 'favorite'] = 'Packers'
    df.loc[df['game'] == 'Packers @ Cowboys', 'underdog'] = 'Cowboys'
    
    # Recalculate the categorization
    df['away_favorite'] = (df['favorite'] == df['away_team'])
    df['home_favorite'] = (df['favorite'] == df['home_team'])
    df['away_underdog'] = (df['underdog'] == df['away_team'])
    df['home_underdog'] = (df['underdog'] == df['home_team'])
    
    # Create corrected categorization
    def get_correct_category(row):
        if row['away_favorite']:
            return 'Away Favorite'
        elif row['home_favorite']:
            return 'Home Favorite'
        else:
            return 'ERROR'
    
    df['corrected_category'] = df.apply(get_correct_category, axis=1)
    
    print(f"\n=== After Correction ===")
    corrected_packers = df[df['game'] == 'Packers @ Cowboys']
    print(f"  Game: {corrected_packers['game'].iloc[0]}")
    print(f"  Favorite: {corrected_packers['favorite'].iloc[0]}")
    print(f"  Underdog: {corrected_packers['underdog'].iloc[0]}")
    print(f"  Category: {corrected_packers['corrected_category'].iloc[0]}")
    
    # Check for any remaining errors
    errors = df[df['corrected_category'] == 'ERROR']
    print(f"\n=== Error Check ===")
    print(f"Games with ERROR: {len(errors)}")
    if len(errors) > 0:
        print("Error games:")
        for _, row in errors.iterrows():
            print(f"  {row['game']}: {row['favorite']} vs {row['underdog']}")
    
    # Calculate corrected totals
    away_favorites = df['away_favorite'].sum()
    home_favorites = df['home_favorite'].sum()
    away_underdogs = df['away_underdog'].sum()
    home_underdogs = df['home_underdog'].sum()
    
    print(f"\n=== Corrected Totals ===")
    print(f"Away Favorites: {away_favorites}")
    print(f"Home Favorites: {home_favorites}")
    print(f"Away Underdogs: {away_underdogs}")
    print(f"Home Underdogs: {home_underdogs}")
    print(f"Total: {away_favorites + home_favorites} (should be {len(df)})")
    
    # Calculate ATS performance
    print(f"\n=== Corrected ATS Performance ===")
    
    away_favs = df[df['away_favorite']]
    away_fav_underdog_covers = away_favs['underdog_covered'].sum()
    away_fav_total = len(away_favs)
    away_fav_rate = away_fav_underdog_covers / away_fav_total * 100
    
    print(f"Away Favorites: {away_fav_underdog_covers}/{away_fav_total} underdog covers ({away_fav_rate:.1f}%)")
    
    home_favs = df[df['home_favorite']]
    home_fav_underdog_covers = home_favs['underdog_covered'].sum()
    home_fav_total = len(home_favs)
    home_fav_rate = home_fav_underdog_covers / home_fav_total * 100
    
    print(f"Home Favorites: {home_fav_underdog_covers}/{home_fav_total} underdog covers ({home_fav_rate:.1f}%)")
    
    # Save corrected data
    output_file = "data/ats_trends/master_ats_trends_final.csv"
    df.to_csv(output_file, index=False)
    print(f"\n✅ Corrected data saved to {output_file}")
    
    return df

def main():
    """Main function"""
    print("=== Fixing Packers @ Cowboys Data Error ===")
    print("Correcting the favorite/underdog designation")
    print("=" * 60)
    
    df = fix_packers_cowboys_data()
    
    print(f"\n=== Fix Complete ===")
    print(f"📊 Data corrected and verified")
    print(f"📁 Saved to data/ats_trends/master_ats_trends_final.csv")

if __name__ == "__main__":
    main()
