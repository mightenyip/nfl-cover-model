#!/usr/bin/env python3
"""
Manual ATS Calculation for Week 2
Calculate actual ATS performance from game results and odds
"""

import pandas as pd

def calculate_week2_ats():
    """Calculate Week 2 ATS performance manually"""
    
    print("=== Week 2 ATS Performance Calculation ===")
    print("Based on actual game results and odds")
    print("=" * 60)
    
    # Week 2 games with results and odds
    games = [
        {
            'game': 'Commanders @ Packers',
            'final_score': 'GB 27 - WSH 18',
            'away_score': 18,
            'home_score': 27,
            'favorite': 'Packers',
            'underdog': 'Commanders',
            'spread': 3.5,
            'favorite_score': 27,
            'underdog_score': 18,
            'margin': 9,  # Packers won by 9
            'underdog_covered': False  # Commanders +3.5, lost by 9, so they didn't cover
        },
        {
            'game': 'Jaguars @ Bengals',
            'final_score': 'CIN 31 - JAX 27',
            'away_score': 27,
            'home_score': 31,
            'favorite': 'Bengals',
            'underdog': 'Jaguars',
            'spread': 3.5,
            'favorite_score': 31,
            'underdog_score': 27,
            'margin': 4,  # Bengals won by 4
            'underdog_covered': False  # Jaguars +3.5, lost by 4, so they didn't cover
        },
        {
            'game': 'Giants @ Cowboys',
            'final_score': 'DAL 40 - NYG 37',
            'away_score': 37,
            'home_score': 40,
            'favorite': 'Cowboys',
            'underdog': 'Giants',
            'spread': 6.5,
            'favorite_score': 40,
            'underdog_score': 37,
            'margin': 3,  # Cowboys won by 3
            'underdog_covered': True  # Giants +6.5, lost by 3, so they covered
        },
        {
            'game': 'Bears @ Lions',
            'final_score': 'DET 52 - CHI 21',
            'away_score': 21,
            'home_score': 52,
            'favorite': 'Lions',
            'underdog': 'Bears',
            'spread': 5.5,
            'favorite_score': 52,
            'underdog_score': 21,
            'margin': 31,  # Lions won by 31
            'underdog_covered': False  # Bears +5.5, lost by 31, so they didn't cover
        },
        {
            'game': 'Rams @ Titans',
            'final_score': 'LAR 33 - TEN 19',
            'away_score': 33,
            'home_score': 19,
            'favorite': 'Rams',
            'underdog': 'Titans',
            'spread': 3.0,
            'favorite_score': 33,
            'underdog_score': 19,
            'margin': 14,  # Rams won by 14
            'underdog_covered': False  # Titans +3, lost by 14, so they didn't cover
        },
        {
            'game': 'Patriots @ Dolphins',
            'final_score': 'NE 33 - MIA 27',
            'away_score': 33,
            'home_score': 27,
            'favorite': 'Dolphins',
            'underdog': 'Patriots',
            'spread': 1.5,
            'favorite_score': 27,
            'underdog_score': 33,
            'margin': -6,  # Dolphins lost by 6
            'underdog_covered': True  # Patriots +1.5, won by 6, so they covered
        },
        {
            'game': '49ers @ Saints',
            'final_score': 'SF 26 - NO 21',
            'away_score': 26,
            'home_score': 21,
            'favorite': '49ers',
            'underdog': 'Saints',
            'spread': 1.5,
            'favorite_score': 26,
            'underdog_score': 21,
            'margin': 5,  # 49ers won by 5
            'underdog_covered': False  # Saints +1.5, lost by 5, so they didn't cover
        },
        {
            'game': 'Bills @ Jets',
            'final_score': 'BUF 30 - NYJ 10',
            'away_score': 30,
            'home_score': 10,
            'favorite': 'Bills',
            'underdog': 'Jets',
            'spread': 1.5,
            'favorite_score': 30,
            'underdog_score': 10,
            'margin': 20,  # Bills won by 20
            'underdog_covered': False  # Jets +1.5, lost by 20, so they didn't cover
        },
        {
            'game': 'Seahawks @ Steelers',
            'final_score': 'SEA 31 - PIT 17',
            'away_score': 31,
            'home_score': 17,
            'favorite': 'Steelers',
            'underdog': 'Seahawks',
            'spread': 3.0,
            'favorite_score': 17,
            'underdog_score': 31,
            'margin': -14,  # Steelers lost by 14
            'underdog_covered': True  # Seahawks +3, won by 14, so they covered
        },
        {
            'game': 'Browns @ Ravens',
            'final_score': 'BAL 41 - CLE 17',
            'away_score': 17,
            'home_score': 41,
            'favorite': 'Ravens',
            'underdog': 'Browns',
            'spread': 11.5,
            'favorite_score': 41,
            'underdog_score': 17,
            'margin': 24,  # Ravens won by 24
            'underdog_covered': False  # Browns +11.5, lost by 24, so they didn't cover
        },
        {
            'game': 'Broncos @ Colts',
            'final_score': 'IND 29 - DEN 28',
            'away_score': 28,
            'home_score': 29,
            'favorite': 'Colts',
            'underdog': 'Broncos',
            'spread': 3.5,
            'favorite_score': 29,
            'underdog_score': 28,
            'margin': 1,  # Colts won by 1
            'underdog_covered': True  # Broncos +3.5, lost by 1, so they covered
        },
        {
            'game': 'Panthers @ Cardinals',
            'final_score': 'ARI 27 - CAR 22',
            'away_score': 22,
            'home_score': 27,
            'favorite': 'Cardinals',
            'underdog': 'Panthers',
            'spread': 3.5,
            'favorite_score': 27,
            'underdog_score': 22,
            'margin': 5,  # Cardinals won by 5
            'underdog_covered': False  # Panthers +3.5, lost by 5, so they didn't cover
        },
        {
            'game': 'Eagles @ Chiefs',
            'final_score': 'PHI 20 - KC 17',
            'away_score': 20,
            'home_score': 17,
            'favorite': 'Eagles',
            'underdog': 'Chiefs',
            'spread': 7.5,
            'favorite_score': 20,
            'underdog_score': 17,
            'margin': 3,  # Eagles won by 3
            'underdog_covered': True  # Chiefs +7.5, lost by 3, so they covered
        },
        {
            'game': 'Falcons @ Vikings',
            'final_score': 'ATL 22 - MIN 6',
            'away_score': 22,
            'home_score': 6,
            'favorite': 'Vikings',
            'underdog': 'Falcons',
            'spread': 1.5,
            'favorite_score': 6,
            'underdog_score': 22,
            'margin': -16,  # Vikings lost by 16
            'underdog_covered': True  # Falcons +1.5, won by 16, so they covered
        },
        {
            'game': 'Buccaneers @ Texans',
            'final_score': 'TB 20 - HOU 19',
            'away_score': 20,
            'home_score': 19,
            'favorite': 'Buccaneers',
            'underdog': 'Texans',
            'spread': 1.5,
            'favorite_score': 20,
            'underdog_score': 19,
            'margin': 1,  # Buccaneers won by 1
            'underdog_covered': True  # Texans +1.5, lost by 1, so they covered
        },
        {
            'game': 'Chargers @ Raiders',
            'final_score': 'LAC 20 - LV 9',
            'away_score': 20,
            'home_score': 9,
            'favorite': 'Chargers',
            'underdog': 'Raiders',
            'spread': 3.0,
            'favorite_score': 20,
            'underdog_score': 9,
            'margin': 11,  # Chargers won by 11
            'underdog_covered': False  # Raiders +3, lost by 11, so they didn't cover
        }
    ]
    
    # Calculate ATS performance
    total_games = len(games)
    underdog_covers = sum(1 for game in games if game['underdog_covered'])
    favorite_covers = total_games - underdog_covers
    
    print(f"Total Games: {total_games}")
    print(f"Underdog Covers: {underdog_covers}/{total_games} ({underdog_covers/total_games*100:.1f}%)")
    print(f"Favorite Covers: {favorite_covers}/{total_games} ({favorite_covers/total_games*100:.1f}%)")
    
    print(f"\n=== All Week 2 Games with ATS Results ===")
    for game in games:
        cover_text = "Yes" if game['underdog_covered'] else "No"
        print(f"  {game['game']}: {game['final_score']} - Underdog covered: {cover_text}")
        print(f"    Spread: {game['favorite']} {game['spread']}, Margin: {game['margin']}")
    
    # Save results
    df = pd.DataFrame(games)
    output_file = "data/ats_results/week2/week2_ats_results.csv"
    df.to_csv(output_file, index=False)
    print(f"\n✅ Week 2 ATS results saved to {output_file}")
    
    return df

def main():
    """Main function"""
    print("=== Week 2 ATS Manual Calculation ===")
    print("Calculating actual ATS performance from game results")
    print("=" * 60)
    
    df = calculate_week2_ats()
    
    print(f"\n=== Analysis Complete ===")
    print(f"📊 Week 2 ATS Performance: {df['underdog_covered'].sum()}/{len(df)} underdog covers")
    print(f"📁 Results saved to data/ats_results/week2/week2_ats_results.csv")

if __name__ == "__main__":
    main()
