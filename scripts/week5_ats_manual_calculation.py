#!/usr/bin/env python3
"""
Manual ATS Calculation for Week 5
Calculate actual ATS performance from game results and odds
"""

import pandas as pd

def calculate_week5_ats():
    """Calculate Week 5 ATS performance manually"""
    
    print("=== Week 5 ATS Performance Calculation ===")
    print("Based on actual game results and odds")
    print("=" * 60)
    
    # Week 5 games with results and odds
    games = [
        {
            'game': '49ers @ Rams',
            'final_score': 'SF 26 - LAR 23',
            'away_score': 26,
            'home_score': 23,
            'favorite': 'Rams',
            'underdog': '49ers',
            'spread': 5.5,
            'favorite_score': 23,
            'underdog_score': 26,
            'margin': -3,  # Rams lost by 3
            'underdog_covered': True  # 49ers +5.5, won by 3, so they covered
        },
        {
            'game': 'Vikings @ Browns',
            'final_score': 'MIN 21 - CLE 17',
            'away_score': 21,
            'home_score': 17,
            'favorite': 'Vikings',
            'underdog': 'Browns',
            'spread': 3.5,
            'favorite_score': 21,
            'underdog_score': 17,
            'margin': 4,  # Vikings won by 4
            'underdog_covered': False  # Browns +3.5, lost by 4, so they didn't cover
        },
        {
            'game': 'Raiders @ Colts',
            'final_score': 'IND 40 - LV 6',
            'away_score': 6,
            'home_score': 40,
            'favorite': 'Colts',
            'underdog': 'Raiders',
            'spread': 6.5,
            'favorite_score': 40,
            'underdog_score': 6,
            'margin': 34,  # Colts won by 34
            'underdog_covered': False  # Raiders +6.5, lost by 34, so they didn't cover
        },
        {
            'game': 'Giants @ Saints',
            'final_score': 'NO 26 - NYG 14',
            'away_score': 14,
            'home_score': 26,
            'favorite': 'Saints',
            'underdog': 'Giants',
            'spread': 1.5,
            'favorite_score': 26,
            'underdog_score': 14,
            'margin': 12,  # Saints won by 12
            'underdog_covered': False  # Giants +1.5, lost by 12, so they didn't cover
        },
        {
            'game': 'Cowboys @ Jets',
            'final_score': 'DAL 37 - NYJ 22',
            'away_score': 37,
            'home_score': 22,
            'favorite': 'Cowboys',
            'underdog': 'Jets',
            'spread': 2.5,
            'favorite_score': 37,
            'underdog_score': 22,
            'margin': 15,  # Cowboys won by 15
            'underdog_covered': False  # Jets +2.5, lost by 15, so they didn't cover
        },
        {
            'game': 'Broncos @ Eagles',
            'final_score': 'DEN 21 - PHI 17',
            'away_score': 21,
            'home_score': 17,
            'favorite': 'Eagles',
            'underdog': 'Broncos',
            'spread': 3.5,
            'favorite_score': 17,
            'underdog_score': 21,
            'margin': -4,  # Eagles lost by 4
            'underdog_covered': True  # Broncos +3.5, won by 4, so they covered
        },
        {
            'game': 'Dolphins @ Panthers',
            'final_score': 'CAR 27 - MIA 24',
            'away_score': 24,
            'home_score': 27,
            'favorite': 'Dolphins',
            'underdog': 'Panthers',
            'spread': 1.5,
            'favorite_score': 24,
            'underdog_score': 27,
            'margin': -3,  # Dolphins lost by 3
            'underdog_covered': True  # Panthers +1.5, won by 3, so they covered
        },
        {
            'game': 'Texans @ Ravens',
            'final_score': 'HOU 44 - BAL 10',
            'away_score': 44,
            'home_score': 10,
            'favorite': 'Texans',
            'underdog': 'Ravens',
            'spread': 2.5,
            'favorite_score': 44,
            'underdog_score': 10,
            'margin': 34,  # Texans won by 34
            'underdog_covered': False  # Ravens +2.5, lost by 34, so they didn't cover
        },
        {
            'game': 'Titans @ Cardinals',
            'final_score': 'TEN 22 - ARI 21',
            'away_score': 22,
            'home_score': 21,
            'favorite': 'Cardinals',
            'underdog': 'Titans',
            'spread': 8.5,
            'favorite_score': 21,
            'underdog_score': 22,
            'margin': -1,  # Cardinals lost by 1
            'underdog_covered': True  # Titans +8.5, won by 1, so they covered
        },
        {
            'game': 'Buccaneers @ Seahawks',
            'final_score': 'TB 38 - SEA 35',
            'away_score': 38,
            'home_score': 35,
            'favorite': 'Seahawks',
            'underdog': 'Buccaneers',
            'spread': 3.5,
            'favorite_score': 35,
            'underdog_score': 38,
            'margin': -3,  # Seahawks lost by 3
            'underdog_covered': True  # Buccaneers +3.5, won by 3, so they covered
        },
        {
            'game': 'Lions @ Bengals',
            'final_score': 'DET 37 - CIN 24',
            'away_score': 37,
            'home_score': 24,
            'favorite': 'Lions',
            'underdog': 'Bengals',
            'spread': 10.5,
            'favorite_score': 37,
            'underdog_score': 24,
            'margin': 13,  # Lions won by 13
            'underdog_covered': False  # Bengals +10.5, lost by 13, so they didn't cover
        },
        {
            'game': 'Commanders @ Chargers',
            'final_score': 'WSH 27 - LAC 10',
            'away_score': 27,
            'home_score': 10,
            'favorite': 'Chargers',
            'underdog': 'Commanders',
            'spread': 2.5,
            'favorite_score': 10,
            'underdog_score': 27,
            'margin': -17,  # Chargers lost by 17
            'underdog_covered': True  # Commanders +2.5, won by 17, so they covered
        },
        {
            'game': 'Patriots @ Bills',
            'final_score': 'NE 23 - BUF 20',
            'away_score': 23,
            'home_score': 20,
            'favorite': 'Bills',
            'underdog': 'Patriots',
            'spread': 8.0,
            'favorite_score': 20,
            'underdog_score': 23,
            'margin': -3,  # Bills lost by 3
            'underdog_covered': True  # Patriots +8, won by 3, so they covered
        },
        {
            'game': 'Chiefs @ Jaguars',
            'final_score': 'JAX 31 - KC 28',
            'away_score': 28,
            'home_score': 31,
            'favorite': 'Chiefs',
            'underdog': 'Jaguars',
            'spread': 3.5,
            'favorite_score': 28,
            'underdog_score': 31,
            'margin': -3,  # Chiefs lost by 3
            'underdog_covered': True  # Jaguars +3.5, won by 3, so they covered
        }
    ]
    
    # Calculate ATS performance
    total_games = len(games)
    underdog_covers = sum(1 for game in games if game['underdog_covered'])
    favorite_covers = total_games - underdog_covers
    
    print(f"Total Games: {total_games}")
    print(f"Underdog Covers: {underdog_covers}/{total_games} ({underdog_covers/total_games*100:.1f}%)")
    print(f"Favorite Covers: {favorite_covers}/{total_games} ({favorite_covers/total_games*100:.1f}%)")
    
    print(f"\n=== All Week 5 Games with ATS Results ===")
    for game in games:
        cover_text = "Yes" if game['underdog_covered'] else "No"
        print(f"  {game['game']}: {game['final_score']} - Underdog covered: {cover_text}")
        print(f"    Spread: {game['favorite']} {game['spread']}, Margin: {game['margin']}")
    
    # Save results
    df = pd.DataFrame(games)
    output_file = "data/ats_results/week5/week5_ats_results.csv"
    df.to_csv(output_file, index=False)
    print(f"\n✅ Week 5 ATS results saved to {output_file}")
    
    return df

def main():
    """Main function"""
    print("=== Week 5 ATS Manual Calculation ===")
    print("Calculating actual ATS performance from game results")
    print("=" * 60)
    
    df = calculate_week5_ats()
    
    print(f"\n=== Analysis Complete ===")
    print(f"📊 Week 5 ATS Performance: {df['underdog_covered'].sum()}/{len(df)} underdog covers")
    print(f"📁 Results saved to data/ats_results/week5/week5_ats_results.csv")

if __name__ == "__main__":
    main()
