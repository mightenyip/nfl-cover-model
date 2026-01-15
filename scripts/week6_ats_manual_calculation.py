#!/usr/bin/env python3
"""
Manual ATS Calculation for Week 6
Calculate actual ATS performance from game results and odds
"""

import pandas as pd

def calculate_week6_ats():
    """Calculate Week 6 ATS performance manually"""
    
    print("=== Week 6 ATS Performance Calculation ===")
    print("Based on actual game results and odds")
    print("=" * 60)
    
    # Week 6 games with results and odds
    games = [
        {
            'game': 'Eagles @ Giants',
            'final_score': 'NYG 34 - PHI 17',
            'away_score': 17,
            'home_score': 34,
            'favorite': 'Eagles',
            'underdog': 'Giants',
            'spread': 7.5,
            'favorite_score': 17,
            'underdog_score': 34,
            'margin': -17,  # Eagles lost by 17
            'underdog_covered': True  # Giants +7.5, won by 17, so they covered
        },
        {
            'game': 'Broncos @ Jets',
            'final_score': 'DEN 13 - NYJ 11',
            'away_score': 13,
            'home_score': 11,
            'favorite': 'Broncos',
            'underdog': 'Jets',
            'spread': 7.5,
            'favorite_score': 13,
            'underdog_score': 11,
            'margin': 2,  # Broncos won by 2
            'underdog_covered': True  # Jets +7.5, lost by 2, so they covered
        },
        {
            'game': 'Cardinals @ Colts',
            'final_score': 'IND 31 - ARI 27',
            'away_score': 27,
            'home_score': 31,
            'favorite': 'Colts',
            'underdog': 'Cardinals',
            'spread': 6.5,
            'favorite_score': 31,
            'underdog_score': 27,
            'margin': 4,  # Colts won by 4
            'underdog_covered': True  # Cardinals +6.5, lost by 4, so they covered
        },
        {
            'game': 'Chargers @ Dolphins',
            'final_score': 'LAC 29 - MIA 27',
            'away_score': 29,
            'home_score': 27,
            'favorite': 'Chargers',
            'underdog': 'Dolphins',
            'spread': 4.5,
            'favorite_score': 29,
            'underdog_score': 27,
            'margin': 2,  # Chargers won by 2
            'underdog_covered': True  # Dolphins +4.5, lost by 2, so they covered
        },
        {
            'game': 'Patriots @ Saints',
            'final_score': 'NE 25 - NO 19',
            'away_score': 25,
            'home_score': 19,
            'favorite': 'Patriots',
            'underdog': 'Saints',
            'spread': 3.5,
            'favorite_score': 25,
            'underdog_score': 19,
            'margin': 6,  # Patriots won by 6
            'underdog_covered': False  # Saints +3.5, lost by 6, so they didn't cover
        },
        {
            'game': 'Browns @ Steelers',
            'final_score': 'PIT 23 - CLE 9',
            'away_score': 9,
            'home_score': 23,
            'favorite': 'Steelers',
            'underdog': 'Browns',
            'spread': 5.0,
            'favorite_score': 23,
            'underdog_score': 9,
            'margin': 14,  # Steelers won by 14
            'underdog_covered': False  # Browns +5, lost by 14, so they didn't cover
        },
        {
            'game': 'Cowboys @ Panthers',
            'final_score': 'CAR 30 - DAL 27',
            'away_score': 27,
            'home_score': 30,
            'favorite': 'Cowboys',
            'underdog': 'Panthers',
            'spread': 3.5,
            'favorite_score': 27,
            'underdog_score': 30,
            'margin': -3,  # Cowboys lost by 3
            'underdog_covered': True  # Panthers +3.5, won by 3, so they covered
        },
        {
            'game': 'Seahawks @ Jaguars',
            'final_score': 'SEA 20 - JAX 12',
            'away_score': 20,
            'home_score': 12,
            'favorite': 'Seahawks',
            'underdog': 'Jaguars',
            'spread': 1.5,
            'favorite_score': 20,
            'underdog_score': 12,
            'margin': 8,  # Seahawks won by 8
            'underdog_covered': False  # Jaguars +1.5, lost by 8, so they didn't cover
        },
        {
            'game': 'Rams @ Ravens',
            'final_score': 'LAR 17 - BAL 3',
            'away_score': 17,
            'home_score': 3,
            'favorite': 'Rams',
            'underdog': 'Ravens',
            'spread': 7.5,
            'favorite_score': 17,
            'underdog_score': 3,
            'margin': 14,  # Rams won by 14
            'underdog_covered': False  # Ravens +7.5, lost by 14, so they didn't cover
        },
        {
            'game': 'Titans @ Raiders',
            'final_score': 'LV 20 - TEN 10',
            'away_score': 10,
            'home_score': 20,
            'favorite': 'Raiders',
            'underdog': 'Titans',
            'spread': 4.5,
            'favorite_score': 20,
            'underdog_score': 10,
            'margin': 10,  # Raiders won by 10
            'underdog_covered': False  # Titans +4.5, lost by 10, so they didn't cover
        },
        {
            'game': 'Bengals @ Packers',
            'final_score': 'GB 27 - CIN 18',
            'away_score': 18,
            'home_score': 27,
            'favorite': 'Packers',
            'underdog': 'Bengals',
            'spread': 14.5,
            'favorite_score': 27,
            'underdog_score': 18,
            'margin': 9,  # Packers won by 9
            'underdog_covered': True  # Bengals +14.5, lost by 9, so they covered
        },
        {
            'game': '49ers @ Buccaneers',
            'final_score': 'TB 30 - SF 19',
            'away_score': 19,
            'home_score': 30,
            'favorite': '49ers',
            'underdog': 'Buccaneers',
            'spread': 3.0,
            'favorite_score': 19,
            'underdog_score': 30,
            'margin': -11,  # 49ers lost by 11
            'underdog_covered': True  # Buccaneers +3, won by 11, so they covered
        },
        {
            'game': 'Lions @ Chiefs',
            'final_score': 'KC 30 - DET 17',
            'away_score': 17,
            'home_score': 30,
            'favorite': 'Chiefs',
            'underdog': 'Lions',
            'spread': 2.5,
            'favorite_score': 30,
            'underdog_score': 17,
            'margin': 13,  # Chiefs won by 13
            'underdog_covered': False  # Lions +2.5, lost by 13, so they didn't cover
        },
        {
            'game': 'Bills @ Falcons',
            'final_score': 'ATL 24 - BUF 14',
            'away_score': 14,
            'home_score': 24,
            'favorite': 'Bills',
            'underdog': 'Falcons',
            'spread': 4.5,
            'favorite_score': 14,
            'underdog_score': 24,
            'margin': -10,  # Bills lost by 10
            'underdog_covered': True  # Falcons +4.5, won by 10, so they covered
        },
        {
            'game': 'Bears @ Commanders',
            'final_score': 'CHI 25 - WSH 24',
            'away_score': 25,
            'home_score': 24,
            'favorite': 'Commanders',
            'underdog': 'Bears',
            'spread': 4.5,
            'favorite_score': 24,
            'underdog_score': 25,
            'margin': -1,  # Commanders lost by 1
            'underdog_covered': True  # Bears +4.5, won by 1, so they covered
        }
    ]
    
    # Calculate ATS performance
    total_games = len(games)
    underdog_covers = sum(1 for game in games if game['underdog_covered'])
    favorite_covers = total_games - underdog_covers
    
    print(f"Total Games: {total_games}")
    print(f"Underdog Covers: {underdog_covers}/{total_games} ({underdog_covers/total_games*100:.1f}%)")
    print(f"Favorite Covers: {favorite_covers}/{total_games} ({favorite_covers/total_games*100:.1f}%)")
    
    print(f"\n=== All Week 6 Games with ATS Results ===")
    for game in games:
        cover_text = "Yes" if game['underdog_covered'] else "No"
        print(f"  {game['game']}: {game['final_score']} - Underdog covered: {cover_text}")
        print(f"    Spread: {game['favorite']} {game['spread']}, Margin: {game['margin']}")
    
    # Save results
    df = pd.DataFrame(games)
    output_file = "data/ats_results/week6/week6_ats_results.csv"
    df.to_csv(output_file, index=False)
    print(f"\n✅ Week 6 ATS results saved to {output_file}")
    
    return df

def main():
    """Main function"""
    print("=== Week 6 ATS Manual Calculation ===")
    print("Calculating actual ATS performance from game results")
    print("=" * 60)
    
    df = calculate_week6_ats()
    
    print(f"\n=== Analysis Complete ===")
    print(f"📊 Week 6 ATS Performance: {df['underdog_covered'].sum()}/{len(df)} underdog covers")
    print(f"📁 Results saved to data/ats_results/week6/week6_ats_results.csv")

if __name__ == "__main__":
    main()
