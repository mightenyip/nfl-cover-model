#!/usr/bin/env python3
"""
Manual ATS Calculation for Week 3
Calculate actual ATS performance from game results and odds
"""

import pandas as pd

def calculate_week3_ats():
    """Calculate Week 3 ATS performance manually"""
    
    print("=== Week 3 ATS Performance Calculation ===")
    print("Based on actual game results and odds")
    print("=" * 60)
    
    # Week 3 games with results and odds
    games = [
        {
            'game': 'Dolphins @ Bills',
            'final_score': 'BUF 31 - MIA 21',
            'away_score': 21,
            'home_score': 31,
            'favorite': 'Bills',
            'underdog': 'Dolphins',
            'spread': 12.5,
            'favorite_score': 31,
            'underdog_score': 21,
            'margin': 10,  # Bills won by 10
            'underdog_covered': True  # Dolphins +12.5, lost by 10, so they covered
        },
        {
            'game': 'Packers @ Browns',
            'final_score': 'CLE 13 - GB 10',
            'away_score': 10,
            'home_score': 13,
            'favorite': 'Packers',
            'underdog': 'Browns',
            'spread': 8.5,
            'favorite_score': 10,
            'underdog_score': 13,
            'margin': -3,  # Packers lost by 3
            'underdog_covered': True  # Browns +8.5, won by 3, so they covered
        },
        {
            'game': 'Colts @ Titans',
            'final_score': 'IND 41 - TEN 20',
            'away_score': 41,
            'home_score': 20,
            'favorite': 'Colts',
            'underdog': 'Titans',
            'spread': 3.5,
            'favorite_score': 41,
            'underdog_score': 20,
            'margin': 21,  # Colts won by 21
            'underdog_covered': False  # Titans +3.5, lost by 21, so they didn't cover
        },
        {
            'game': 'Bengals @ Vikings',
            'final_score': 'MIN 48 - CIN 10',
            'away_score': 10,
            'home_score': 48,
            'favorite': 'Vikings',
            'underdog': 'Bengals',
            'spread': 3.0,
            'favorite_score': 48,
            'underdog_score': 10,
            'margin': 38,  # Vikings won by 38
            'underdog_covered': False  # Bengals +3, lost by 38, so they didn't cover
        },
        {
            'game': 'Steelers @ Patriots',
            'final_score': 'PIT 21 - NE 14',
            'away_score': 21,
            'home_score': 14,
            'favorite': 'Steelers',
            'underdog': 'Patriots',
            'spread': 1.5,
            'favorite_score': 21,
            'underdog_score': 14,
            'margin': 7,  # Steelers won by 7
            'underdog_covered': False  # Patriots +1.5, lost by 7, so they didn't cover
        },
        {
            'game': 'Rams @ Eagles',
            'final_score': 'PHI 33 - LAR 26',
            'away_score': 26,
            'home_score': 33,
            'favorite': 'Eagles',
            'underdog': 'Rams',
            'spread': 3.5,
            'favorite_score': 33,
            'underdog_score': 26,
            'margin': 7,  # Eagles won by 7
            'underdog_covered': False  # Rams +3.5, lost by 7, so they didn't cover
        },
        {
            'game': 'Jets @ Buccaneers',
            'final_score': 'TB 29 - NYJ 27',
            'away_score': 27,
            'home_score': 29,
            'favorite': 'Buccaneers',
            'underdog': 'Jets',
            'spread': 7.0,
            'favorite_score': 29,
            'underdog_score': 27,
            'margin': 2,  # Buccaneers won by 2
            'underdog_covered': True  # Jets +7, lost by 2, so they covered
        },
        {
            'game': 'Raiders @ Commanders',
            'final_score': 'WSH 41 - LV 24',
            'away_score': 24,
            'home_score': 41,
            'favorite': 'Commanders',
            'underdog': 'Raiders',
            'spread': 3.5,
            'favorite_score': 41,
            'underdog_score': 24,
            'margin': 17,  # Commanders won by 17
            'underdog_covered': False  # Raiders +3.5, lost by 17, so they didn't cover
        },
        {
            'game': 'Falcons @ Panthers',
            'final_score': 'CAR 30 - ATL 0',
            'away_score': 0,
            'home_score': 30,
            'favorite': 'Falcons',
            'underdog': 'Panthers',
            'spread': 5.5,
            'favorite_score': 0,
            'underdog_score': 30,
            'margin': -30,  # Falcons lost by 30
            'underdog_covered': True  # Panthers +5.5, won by 30, so they covered
        },
        {
            'game': 'Texans @ Jaguars',
            'final_score': 'JAX 17 - HOU 10',
            'away_score': 10,
            'home_score': 17,
            'favorite': 'Jaguars',
            'underdog': 'Texans',
            'spread': 1.5,
            'favorite_score': 17,
            'underdog_score': 10,
            'margin': 7,  # Jaguars won by 7
            'underdog_covered': False  # Texans +1.5, lost by 7, so they didn't cover
        },
        {
            'game': 'Broncos @ Chargers',
            'final_score': 'LAC 23 - DEN 20',
            'away_score': 20,
            'home_score': 23,
            'favorite': 'Chargers',
            'underdog': 'Broncos',
            'spread': 2.5,
            'favorite_score': 23,
            'underdog_score': 20,
            'margin': 3,  # Chargers won by 3
            'underdog_covered': False  # Broncos +2.5, lost by 3, so they didn't cover
        },
        {
            'game': 'Saints @ Seahawks',
            'final_score': 'SEA 44 - NO 13',
            'away_score': 13,
            'home_score': 44,
            'favorite': 'Seahawks',
            'underdog': 'Saints',
            'spread': 7.5,
            'favorite_score': 44,
            'underdog_score': 13,
            'margin': 31,  # Seahawks won by 31
            'underdog_covered': False  # Saints +7.5, lost by 31, so they didn't cover
        },
        {
            'game': 'Cowboys @ Bears',
            'final_score': 'CHI 31 - DAL 14',
            'away_score': 14,
            'home_score': 31,
            'favorite': 'Bears',
            'underdog': 'Cowboys',
            'spread': 1.5,
            'favorite_score': 31,
            'underdog_score': 14,
            'margin': 17,  # Bears won by 17
            'underdog_covered': False  # Cowboys +1.5, lost by 17, so they didn't cover
        },
        {
            'game': 'Cardinals @ 49ers',
            'final_score': 'SF 16 - ARI 15',
            'away_score': 15,
            'home_score': 16,
            'favorite': '49ers',
            'underdog': 'Cardinals',
            'spread': 1.5,
            'favorite_score': 16,
            'underdog_score': 15,
            'margin': 1,  # 49ers won by 1
            'underdog_covered': True  # Cardinals +1.5, lost by 1, so they covered
        },
        {
            'game': 'Chiefs @ Giants',
            'final_score': 'KC 22 - NYG 9',
            'away_score': 22,
            'home_score': 9,
            'favorite': 'Chiefs',
            'underdog': 'Giants',
            'spread': 6.5,
            'favorite_score': 22,
            'underdog_score': 9,
            'margin': 13,  # Chiefs won by 13
            'underdog_covered': False  # Giants +6.5, lost by 13, so they didn't cover
        },
        {
            'game': 'Lions @ Ravens',
            'final_score': 'DET 38 - BAL 30',
            'away_score': 38,
            'home_score': 30,
            'favorite': 'Ravens',
            'underdog': 'Lions',
            'spread': 5.5,
            'favorite_score': 30,
            'underdog_score': 38,
            'margin': -8,  # Ravens lost by 8
            'underdog_covered': True  # Lions +5.5, won by 8, so they covered
        }
    ]
    
    # Calculate ATS performance
    total_games = len(games)
    underdog_covers = sum(1 for game in games if game['underdog_covered'])
    favorite_covers = total_games - underdog_covers
    
    print(f"Total Games: {total_games}")
    print(f"Underdog Covers: {underdog_covers}/{total_games} ({underdog_covers/total_games*100:.1f}%)")
    print(f"Favorite Covers: {favorite_covers}/{total_games} ({favorite_covers/total_games*100:.1f}%)")
    
    print(f"\n=== All Week 3 Games with ATS Results ===")
    for game in games:
        cover_text = "Yes" if game['underdog_covered'] else "No"
        print(f"  {game['game']}: {game['final_score']} - Underdog covered: {cover_text}")
        print(f"    Spread: {game['favorite']} {game['spread']}, Margin: {game['margin']}")
    
    # Save results
    df = pd.DataFrame(games)
    output_file = "data/week3_ats_results.csv"
    df.to_csv(output_file, index=False)
    print(f"\n✅ Week 3 ATS results saved to {output_file}")
    
    return df

def main():
    """Main function"""
    print("=== Week 3 ATS Manual Calculation ===")
    print("Calculating actual ATS performance from game results")
    print("=" * 60)
    
    df = calculate_week3_ats()
    
    print(f"\n=== Analysis Complete ===")
    print(f"📊 Week 3 ATS Performance: {df['underdog_covered'].sum()}/{len(df)} underdog covers")
    print(f"📁 Results saved to data/week3_ats_results.csv")

if __name__ == "__main__":
    main()
