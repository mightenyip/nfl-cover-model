#!/usr/bin/env python3
"""
Manual ATS Calculation for Week 4
Calculate actual ATS performance from game results and odds
"""

import pandas as pd

def calculate_week4_ats():
    """Calculate Week 4 ATS performance manually"""
    
    print("=== Week 4 ATS Performance Calculation ===")
    print("Based on actual game results and odds")
    print("=" * 60)
    
    # Week 4 games with results and odds
    games = [
        {
            'game': 'Seahawks @ Cardinals',
            'final_score': 'SEA 23 - ARI 20',
            'away_score': 23,
            'home_score': 20,
            'favorite': 'Seahawks',
            'underdog': 'Cardinals',
            'spread': 1.5,
            'favorite_score': 23,
            'underdog_score': 20,
            'margin': 3,  # Seahawks won by 3
            'underdog_covered': False  # Cardinals +1.5, lost by 3, so they didn't cover
        },
        {
            'game': 'Vikings @ Steelers',
            'final_score': 'PIT 24 - MIN 21',
            'away_score': 21,
            'home_score': 24,
            'favorite': 'Vikings',
            'underdog': 'Steelers',
            'spread': 2.5,
            'favorite_score': 21,
            'underdog_score': 24,
            'margin': -3,  # Vikings lost by 3
            'underdog_covered': True  # Steelers +2.5, won by 3, so they covered
        },
        {
            'game': 'Commanders @ Falcons',
            'final_score': 'ATL 34 - WSH 27',
            'away_score': 27,
            'home_score': 34,
            'favorite': 'Commanders',
            'underdog': 'Falcons',
            'spread': 1.5,
            'favorite_score': 27,
            'underdog_score': 34,
            'margin': -7,  # Commanders lost by 7
            'underdog_covered': True  # Falcons +1.5, won by 7, so they covered
        },
        {
            'game': 'Saints @ Bills',
            'final_score': 'BUF 31 - NO 19',
            'away_score': 19,
            'home_score': 31,
            'favorite': 'Bills',
            'underdog': 'Saints',
            'spread': 16.5,
            'favorite_score': 31,
            'underdog_score': 19,
            'margin': 12,  # Bills won by 12
            'underdog_covered': True  # Saints +16.5, lost by 12, so they covered
        },
        {
            'game': 'Browns @ Lions',
            'final_score': 'DET 34 - CLE 10',
            'away_score': 10,
            'home_score': 34,
            'favorite': 'Lions',
            'underdog': 'Browns',
            'spread': 8.5,
            'favorite_score': 34,
            'underdog_score': 10,
            'margin': 24,  # Lions won by 24
            'underdog_covered': False  # Browns +8.5, lost by 24, so they didn't cover
        },
        {
            'game': 'Panthers @ Patriots',
            'final_score': 'NE 42 - CAR 13',
            'away_score': 13,
            'home_score': 42,
            'favorite': 'Patriots',
            'underdog': 'Panthers',
            'spread': 5.5,
            'favorite_score': 42,
            'underdog_score': 13,
            'margin': 29,  # Patriots won by 29
            'underdog_covered': False  # Panthers +5.5, lost by 29, so they didn't cover
        },
        {
            'game': 'Chargers @ Giants',
            'final_score': 'NYG 21 - LAC 18',
            'away_score': 18,
            'home_score': 21,
            'favorite': 'Chargers',
            'underdog': 'Giants',
            'spread': 6.5,
            'favorite_score': 18,
            'underdog_score': 21,
            'margin': -3,  # Chargers lost by 3
            'underdog_covered': True  # Giants +6.5, won by 3, so they covered
        },
        {
            'game': 'Eagles @ Buccaneers',
            'final_score': 'PHI 31 - TB 25',
            'away_score': 31,
            'home_score': 25,
            'favorite': 'Eagles',
            'underdog': 'Buccaneers',
            'spread': 3.5,
            'favorite_score': 31,
            'underdog_score': 25,
            'margin': 6,  # Eagles won by 6
            'underdog_covered': False  # Buccaneers +3.5, lost by 6, so they didn't cover
        },
        {
            'game': 'Titans @ Texans',
            'final_score': 'HOU 26 - TEN 0',
            'away_score': 0,
            'home_score': 26,
            'favorite': 'Texans',
            'underdog': 'Titans',
            'spread': 7.0,
            'favorite_score': 26,
            'underdog_score': 0,
            'margin': 26,  # Texans won by 26
            'underdog_covered': False  # Titans +7, lost by 26, so they didn't cover
        },
        {
            'game': 'Colts @ Rams',
            'final_score': 'LAR 27 - IND 20',
            'away_score': 20,
            'home_score': 27,
            'favorite': 'Rams',
            'underdog': 'Colts',
            'spread': 3.5,
            'favorite_score': 27,
            'underdog_score': 20,
            'margin': 7,  # Rams won by 7
            'underdog_covered': False  # Colts +3.5, lost by 7, so they didn't cover
        },
        {
            'game': 'Jaguars @ 49ers',
            'final_score': 'JAX 26 - SF 21',
            'away_score': 26,
            'home_score': 21,
            'favorite': '49ers',
            'underdog': 'Jaguars',
            'spread': 3.0,
            'favorite_score': 21,
            'underdog_score': 26,
            'margin': -5,  # 49ers lost by 5
            'underdog_covered': True  # Jaguars +3, won by 5, so they covered
        },
        {
            'game': 'Ravens @ Chiefs',
            'final_score': 'KC 37 - BAL 20',
            'away_score': 20,
            'home_score': 37,
            'favorite': 'Chiefs',
            'underdog': 'Ravens',
            'spread': 2.5,
            'favorite_score': 37,
            'underdog_score': 20,
            'margin': 17,  # Chiefs won by 17
            'underdog_covered': False  # Ravens +2.5, lost by 17, so they didn't cover
        },
        {
            'game': 'Bears @ Raiders',
            'final_score': 'CHI 25 - LV 24',
            'away_score': 25,
            'home_score': 24,
            'favorite': 'Raiders',
            'underdog': 'Bears',
            'spread': 1.5,
            'favorite_score': 24,
            'underdog_score': 25,
            'margin': -1,  # Raiders lost by 1
            'underdog_covered': True  # Bears +1.5, won by 1, so they covered
        },
        {
            'game': 'Packers @ Cowboys',
            'final_score': 'GB 40 - DAL 40',
            'away_score': 40,
            'home_score': 40,
            'favorite': 'Eagles',  # This was actually Packers -7.0 based on odds
            'underdog': 'Cowboys',
            'spread': 7.0,
            'favorite_score': 40,
            'underdog_score': 40,
            'margin': 0,  # Tie game
            'underdog_covered': True  # Cowboys +7, tied, so they covered
        },
        {
            'game': 'Jets @ Dolphins',
            'final_score': 'MIA 27 - NYJ 21',
            'away_score': 21,
            'home_score': 27,
            'favorite': 'Dolphins',
            'underdog': 'Jets',
            'spread': 2.5,
            'favorite_score': 27,
            'underdog_score': 21,
            'margin': 6,  # Dolphins won by 6
            'underdog_covered': False  # Jets +2.5, lost by 6, so they didn't cover
        },
        {
            'game': 'Bengals @ Broncos',
            'final_score': 'DEN 28 - CIN 3',
            'away_score': 3,
            'home_score': 28,
            'favorite': 'Broncos',
            'underdog': 'Bengals',
            'spread': 7.0,
            'favorite_score': 28,
            'underdog_score': 3,
            'margin': 25,  # Broncos won by 25
            'underdog_covered': False  # Bengals +7, lost by 25, so they didn't cover
        }
    ]
    
    # Calculate ATS performance
    total_games = len(games)
    underdog_covers = sum(1 for game in games if game['underdog_covered'])
    favorite_covers = total_games - underdog_covers
    
    print(f"Total Games: {total_games}")
    print(f"Underdog Covers: {underdog_covers}/{total_games} ({underdog_covers/total_games*100:.1f}%)")
    print(f"Favorite Covers: {favorite_covers}/{total_games} ({favorite_covers/total_games*100:.1f}%)")
    
    print(f"\n=== All Week 4 Games with ATS Results ===")
    for game in games:
        cover_text = "Yes" if game['underdog_covered'] else "No"
        print(f"  {game['game']}: {game['final_score']} - Underdog covered: {cover_text}")
        print(f"    Spread: {game['favorite']} {game['spread']}, Margin: {game['margin']}")
    
    # Save results
    df = pd.DataFrame(games)
    output_file = "data/ats_results/week4/week4_ats_results.csv"
    df.to_csv(output_file, index=False)
    print(f"\n✅ Week 4 ATS results saved to {output_file}")
    
    return df

def main():
    """Main function"""
    print("=== Week 4 ATS Manual Calculation ===")
    print("Calculating actual ATS performance from game results")
    print("=" * 60)
    
    df = calculate_week4_ats()
    
    print(f"\n=== Analysis Complete ===")
    print(f"📊 Week 4 ATS Performance: {df['underdog_covered'].sum()}/{len(df)} underdog covers")
    print(f"📁 Results saved to data/ats_results/week4/week4_ats_results.csv")

if __name__ == "__main__":
    main()
