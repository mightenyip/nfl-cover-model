#!/usr/bin/env python3
"""
Manual ATS Calculation for Week 7
Calculate actual ATS performance from game results and odds
"""

import pandas as pd

def calculate_week7_ats():
    """Calculate Week 7 ATS performance manually"""
    
    print("=== Week 7 ATS Performance Calculation ===")
    print("Based on actual game results and odds")
    print("=" * 60)
    
    # Week 7 games with results and odds
    games = [
        {
            'game': 'Steelers @ Bengals',
            'final_score': 'CIN 33 - PIT 31',
            'away_score': 31,
            'home_score': 33,
            'favorite': 'Bengals',
            'underdog': 'Steelers',
            'spread': 3.5,
            'favorite_score': 33,
            'underdog_score': 31,
            'margin': 2,  # Bengals won by 2
            'underdog_covered': True  # Steelers +3.5, lost by 2, so they covered
        },
        {
            'game': 'Rams @ Jaguars',
            'final_score': 'LAR 35 - JAX 7',
            'away_score': 35,
            'home_score': 7,
            'favorite': 'Rams',
            'underdog': 'Jaguars',
            'spread': 3.5,
            'favorite_score': 35,
            'underdog_score': 7,
            'margin': 28,  # Rams won by 28
            'underdog_covered': False  # Jaguars +3.5, lost by 28, so they didn't cover
        },
        {
            'game': 'Saints @ Bears',
            'final_score': 'CHI 26 - NO 14',
            'away_score': 14,
            'home_score': 26,
            'favorite': 'Bears',
            'underdog': 'Saints',
            'spread': 3.5,
            'favorite_score': 26,
            'underdog_score': 14,
            'margin': 12,  # Bears won by 12
            'underdog_covered': False  # Saints +3.5, lost by 12, so they didn't cover
        },
        {
            'game': 'Dolphins @ Browns',
            'final_score': 'CLE 31 - MIA 6',
            'away_score': 6,
            'home_score': 31,
            'favorite': 'Browns',
            'underdog': 'Dolphins',
            'spread': 3.5,
            'favorite_score': 31,
            'underdog_score': 6,
            'margin': 25,  # Browns won by 25
            'underdog_covered': False  # Dolphins +3.5, lost by 25, so they didn't cover
        },
        {
            'game': 'Patriots @ Titans',
            'final_score': 'NE 31 - TEN 13',
            'away_score': 31,
            'home_score': 13,
            'favorite': 'Patriots',
            'underdog': 'Titans',
            'spread': 3.5,
            'favorite_score': 31,
            'underdog_score': 13,
            'margin': 18,  # Patriots won by 18
            'underdog_covered': False  # Titans +3.5, lost by 18, so they didn't cover
        },
        {
            'game': 'Raiders @ Chiefs',
            'final_score': 'KC 31 - LV 0',
            'away_score': 0,
            'home_score': 31,
            'favorite': 'Chiefs',
            'underdog': 'Raiders',
            'spread': 7.5,
            'favorite_score': 31,
            'underdog_score': 0,
            'margin': 31,  # Chiefs won by 31
            'underdog_covered': False  # Raiders +7.5, lost by 31, so they didn't cover
        },
        {
            'game': 'Eagles @ Vikings',
            'final_score': 'PHI 28 - MIN 22',
            'away_score': 28,
            'home_score': 22,
            'favorite': 'Eagles',
            'underdog': 'Vikings',
            'spread': 3.5,
            'favorite_score': 28,
            'underdog_score': 22,
            'margin': 6,  # Eagles won by 6
            'underdog_covered': False  # Vikings +3.5, lost by 6, so they didn't cover
        },
        {
            'game': 'Panthers @ Jets',
            'final_score': 'CAR 13 - NYJ 6',
            'away_score': 13,
            'home_score': 6,
            'favorite': 'Jets',
            'underdog': 'Panthers',
            'spread': 3.5,
            'favorite_score': 6,
            'underdog_score': 13,
            'margin': -7,  # Jets lost by 7
            'underdog_covered': True  # Panthers +3.5, won by 7, so they covered
        },
        {
            'game': 'Giants @ Broncos',
            'final_score': 'DEN 33 - NYG 32',
            'away_score': 32,
            'home_score': 33,
            'favorite': 'Broncos',
            'underdog': 'Giants',
            'spread': 3.5,
            'favorite_score': 33,
            'underdog_score': 32,
            'margin': 1,  # Broncos won by 1
            'underdog_covered': True  # Giants +3.5, lost by 1, so they covered
        },
        {
            'game': 'Colts @ Chargers',
            'final_score': 'IND 38 - LAC 24',
            'away_score': 38,
            'home_score': 24,
            'favorite': 'Colts',
            'underdog': 'Chargers',
            'spread': 3.5,
            'favorite_score': 38,
            'underdog_score': 24,
            'margin': 14,  # Colts won by 14
            'underdog_covered': False  # Chargers +3.5, lost by 14, so they didn't cover
        },
        {
            'game': 'Commanders @ Cowboys',
            'final_score': 'DAL 44 - WSH 22',
            'away_score': 22,
            'home_score': 44,
            'favorite': 'Cowboys',
            'underdog': 'Commanders',
            'spread': 7.5,
            'favorite_score': 44,
            'underdog_score': 22,
            'margin': 22,  # Cowboys won by 22
            'underdog_covered': False  # Commanders +7.5, lost by 22, so they didn't cover
        },
        {
            'game': 'Packers @ Cardinals',
            'final_score': 'GB 27 - ARI 23',
            'away_score': 27,
            'home_score': 23,
            'favorite': 'Packers',
            'underdog': 'Cardinals',
            'spread': 3.5,
            'favorite_score': 27,
            'underdog_score': 23,
            'margin': 4,  # Packers won by 4
            'underdog_covered': True  # Cardinals +3.5, lost by 4, so they covered
        },
        {
            'game': 'Falcons @ 49ers',
            'final_score': 'SF 20 - ATL 10',
            'away_score': 10,
            'home_score': 20,
            'favorite': '49ers',
            'underdog': 'Falcons',
            'spread': 7.5,
            'favorite_score': 20,
            'underdog_score': 10,
            'margin': 10,  # 49ers won by 10
            'underdog_covered': False  # Falcons +7.5, lost by 10, so they didn't cover
        },
        {
            'game': 'Buccaneers @ Lions',
            'final_score': 'DET 24 - TB 9',
            'away_score': 9,
            'home_score': 24,
            'favorite': 'Lions',
            'underdog': 'Buccaneers',
            'spread': 7.5,
            'favorite_score': 24,
            'underdog_score': 9,
            'margin': 15,  # Lions won by 15
            'underdog_covered': False  # Buccaneers +7.5, lost by 15, so they didn't cover
        },
        {
            'game': 'Texans @ Seahawks',
            'final_score': 'SEA 27 - HOU 19',
            'away_score': 19,
            'home_score': 27,
            'favorite': 'Seahawks',
            'underdog': 'Texans',
            'spread': 3.5,
            'favorite_score': 27,
            'underdog_score': 19,
            'margin': 8,  # Seahawks won by 8
            'underdog_covered': False  # Texans +3.5, lost by 8, so they didn't cover
        }
    ]
    
    # Calculate ATS performance
    total_games = len(games)
    underdog_covers = sum(1 for game in games if game['underdog_covered'])
    favorite_covers = total_games - underdog_covers
    
    print(f"Total Games: {total_games}")
    print(f"Underdog Covers: {underdog_covers}/{total_games} ({underdog_covers/total_games*100:.1f}%)")
    print(f"Favorite Covers: {favorite_covers}/{total_games} ({favorite_covers/total_games*100:.1f}%)")
    
    print(f"\n=== All Week 7 Games with ATS Results ===")
    for game in games:
        cover_text = "Yes" if game['underdog_covered'] else "No"
        print(f"  {game['game']}: {game['final_score']} - Underdog covered: {cover_text}")
        print(f"    Spread: {game['favorite']} {game['spread']}, Margin: {game['margin']}")
    
    # Save results
    df = pd.DataFrame(games)
    output_file = "data/week7_ats_results.csv"
    df.to_csv(output_file, index=False)
    print(f"\n✅ Week 7 ATS results saved to {output_file}")
    
    return df

def main():
    """Main function"""
    print("=== Week 7 ATS Manual Calculation ===")
    print("Calculating actual ATS performance from game results")
    print("=" * 60)
    
    df = calculate_week7_ats()
    
    print(f"\n=== Analysis Complete ===")
    print(f"📊 Week 7 ATS Performance: {df['underdog_covered'].sum()}/{len(df)} underdog covers")
    print(f"📁 Results saved to data/week7_ats_results.csv")

if __name__ == "__main__":
    main()
