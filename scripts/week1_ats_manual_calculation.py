#!/usr/bin/env python3
"""
Manual ATS Calculation for Week 1
Calculate actual ATS performance from game results and odds
"""

import pandas as pd

def calculate_week1_ats():
    """Calculate Week 1 ATS performance manually"""
    
    print("=== Week 1 ATS Performance Calculation ===")
    print("Based on actual game results and odds")
    print("=" * 60)
    
    # Week 1 games with results and odds
    games = [
        {
            'game': 'Cowboys @ Eagles',
            'final_score': 'PHI 24 - DAL 20',
            'away_score': 20,
            'home_score': 24,
            'favorite': 'Eagles',
            'underdog': 'Cowboys',
            'spread': 8.5,
            'favorite_score': 24,
            'underdog_score': 20,
            'margin': 4,  # Eagles won by 4
            'underdog_covered': True  # Cowboys +8.5, lost by 4, so they covered
        },
        {
            'game': 'Chiefs @ Chargers',
            'final_score': 'LAC 27 - KC 21',
            'away_score': 21,
            'home_score': 27,
            'favorite': 'Chiefs',
            'underdog': 'Chargers',
            'spread': 3.0,
            'favorite_score': 21,
            'underdog_score': 27,
            'margin': -6,  # Chiefs lost by 6
            'underdog_covered': True  # Chargers +3, won by 6, so they covered
        },
        {
            'game': 'Buccaneers @ Falcons',
            'final_score': 'TB 23 - ATL 20',
            'away_score': 23,
            'home_score': 20,
            'favorite': 'Buccaneers',
            'underdog': 'Falcons',
            'spread': 1.5,
            'favorite_score': 23,
            'underdog_score': 20,
            'margin': 3,  # Buccaneers won by 3
            'underdog_covered': False  # Falcons +1.5, lost by 3, so they didn't cover
        },
        {
            'game': 'Bengals @ Browns',
            'final_score': 'CIN 17 - CLE 16',
            'away_score': 17,
            'home_score': 16,
            'favorite': 'Bengals',
            'underdog': 'Browns',
            'spread': 5.5,
            'favorite_score': 17,
            'underdog_score': 16,
            'margin': 1,  # Bengals won by 1
            'underdog_covered': True  # Browns +5.5, lost by 1, so they covered
        },
        {
            'game': 'Dolphins @ Colts',
            'final_score': 'IND 33 - MIA 8',
            'away_score': 8,
            'home_score': 33,
            'favorite': 'Colts',
            'underdog': 'Dolphins',
            'spread': 1.5,
            'favorite_score': 33,
            'underdog_score': 8,
            'margin': 25,  # Colts won by 25
            'underdog_covered': False  # Dolphins +1.5, lost by 25, so they didn't cover
        },
        {
            'game': 'Raiders @ Patriots',
            'final_score': 'LV 20 - NE 13',
            'away_score': 20,
            'home_score': 13,
            'favorite': 'Patriots',
            'underdog': 'Raiders',
            'spread': 2.5,
            'favorite_score': 13,
            'underdog_score': 20,
            'margin': -7,  # Patriots lost by 7
            'underdog_covered': True  # Raiders +2.5, won by 7, so they covered
        },
        {
            'game': 'Cardinals @ Saints',
            'final_score': 'ARI 20 - NO 13',
            'away_score': 20,
            'home_score': 13,
            'favorite': 'Cardinals',
            'underdog': 'Saints',
            'spread': 6.5,
            'favorite_score': 20,
            'underdog_score': 13,
            'margin': 7,  # Cardinals won by 7
            'underdog_covered': False  # Saints +6.5, lost by 7, so they didn't cover
        },
        {
            'game': 'Steelers @ Jets',
            'final_score': 'PIT 34 - NYJ 32',
            'away_score': 34,
            'home_score': 32,
            'favorite': 'Steelers',
            'underdog': 'Jets',
            'spread': 3.0,
            'favorite_score': 34,
            'underdog_score': 32,
            'margin': 2,  # Steelers won by 2
            'underdog_covered': True  # Jets +3, lost by 2, so they covered
        },
        {
            'game': 'Giants @ Commanders',
            'final_score': 'WSH 21 - NYG 6',
            'away_score': 6,
            'home_score': 21,
            'favorite': 'Commanders',
            'underdog': 'Giants',
            'spread': 6.5,
            'favorite_score': 21,
            'underdog_score': 6,
            'margin': 15,  # Commanders won by 15
            'underdog_covered': False  # Giants +6.5, lost by 15, so they didn't cover
        },
        {
            'game': 'Panthers @ Jaguars',
            'final_score': 'JAX 26 - CAR 10',
            'away_score': 10,
            'home_score': 26,
            'favorite': 'Jaguars',
            'underdog': 'Panthers',
            'spread': 4.5,
            'favorite_score': 26,
            'underdog_score': 10,
            'margin': 16,  # Jaguars won by 16
            'underdog_covered': False  # Panthers +4.5, lost by 16, so they didn't cover
        },
        {
            'game': 'Titans @ Broncos',
            'final_score': 'DEN 20 - TEN 12',
            'away_score': 12,
            'home_score': 20,
            'favorite': 'Broncos',
            'underdog': 'Titans',
            'spread': 8.5,
            'favorite_score': 20,
            'underdog_score': 12,
            'margin': 8,  # Broncos won by 8
            'underdog_covered': True  # Titans +8.5, lost by 8, so they covered
        },
        {
            'game': '49ers @ Seahawks',
            'final_score': 'SF 17 - SEA 13',
            'away_score': 17,
            'home_score': 13,
            'favorite': '49ers',
            'underdog': 'Seahawks',
            'spread': 1.5,
            'favorite_score': 17,
            'underdog_score': 13,
            'margin': 4,  # 49ers won by 4
            'underdog_covered': False  # Seahawks +1.5, lost by 4, so they didn't cover
        },
        {
            'game': 'Lions @ Packers',
            'final_score': 'GB 27 - DET 13',
            'away_score': 13,
            'home_score': 27,
            'favorite': 'Packers',
            'underdog': 'Lions',
            'spread': 1.5,
            'favorite_score': 27,
            'underdog_score': 13,
            'margin': 14,  # Packers won by 14
            'underdog_covered': False  # Lions +1.5, lost by 14, so they didn't cover
        },
        {
            'game': 'Texans @ Rams',
            'final_score': 'LAR 14 - HOU 9',
            'away_score': 9,
            'home_score': 14,
            'favorite': 'Rams',
            'underdog': 'Texans',
            'spread': 3.0,
            'favorite_score': 14,
            'underdog_score': 9,
            'margin': 5,  # Rams won by 5
            'underdog_covered': False  # Texans +3, lost by 5, so they didn't cover
        },
        {
            'game': 'Ravens @ Bills',
            'final_score': 'BUF 41 - BAL 40',
            'away_score': 40,
            'home_score': 41,
            'favorite': 'Bills',
            'underdog': 'Ravens',
            'spread': 1.5,
            'favorite_score': 41,
            'underdog_score': 40,
            'margin': 1,  # Bills won by 1
            'underdog_covered': True  # Ravens +1.5, lost by 1, so they covered
        },
        {
            'game': 'Vikings @ Bears',
            'final_score': 'MIN 27 - CHI 24',
            'away_score': 27,
            'home_score': 24,
            'favorite': 'Bears',
            'underdog': 'Vikings',
            'spread': 1.5,
            'favorite_score': 24,
            'underdog_score': 27,
            'margin': -3,  # Bears lost by 3
            'underdog_covered': True  # Vikings +1.5, won by 3, so they covered
        }
    ]
    
    # Calculate ATS performance
    total_games = len(games)
    underdog_covers = sum(1 for game in games if game['underdog_covered'])
    favorite_covers = total_games - underdog_covers
    
    print(f"Total Games: {total_games}")
    print(f"Underdog Covers: {underdog_covers}/{total_games} ({underdog_covers/total_games*100:.1f}%)")
    print(f"Favorite Covers: {favorite_covers}/{total_games} ({favorite_covers/total_games*100:.1f}%)")
    
    print(f"\n=== All Week 1 Games with ATS Results ===")
    for game in games:
        cover_text = "Yes" if game['underdog_covered'] else "No"
        print(f"  {game['game']}: {game['final_score']} - Underdog covered: {cover_text}")
        print(f"    Spread: {game['favorite']} {game['spread']}, Margin: {game['margin']}")
    
    # Save results
    df = pd.DataFrame(games)
    output_file = "data/ats_results/week1/week1_ats_results.csv"
    df.to_csv(output_file, index=False)
    print(f"\n✅ Week 1 ATS results saved to {output_file}")
    
    return df

def main():
    """Main function"""
    print("=== Week 1 ATS Manual Calculation ===")
    print("Calculating actual ATS performance from game results")
    print("=" * 60)
    
    df = calculate_week1_ats()
    
    print(f"\n=== Analysis Complete ===")
    print(f"📊 Week 1 ATS Performance: {df['underdog_covered'].sum()}/{len(df)} underdog covers")
    print(f"📁 Results saved to data/ats_results/week1/week1_ats_results.csv")

if __name__ == "__main__":
    main()
