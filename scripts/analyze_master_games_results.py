#!/usr/bin/env python3
"""
Analyze Master Games Results CSV
Calculate actual ATS performance from game results
"""

import pandas as pd
import numpy as np
import os

def load_week_odds(week_num):
    """Load odds data for a specific week"""
    week_file = f"schedule/week{week_num}_2025_odds.csv"
    if os.path.exists(week_file):
        df = pd.read_csv(week_file)
        df['week'] = week_num
        return df
    return None

def calculate_ats_performance(games_df, odds_df):
    """Calculate ATS performance by matching games with odds"""
    
    print("=== ATS Performance Calculation ===")
    print("Matching game results with odds data")
    
    # Merge games with odds
    merged_df = pd.merge(games_df, odds_df, 
                        left_on=['away_team', 'home_team'], 
                        right_on=['away_team', 'home_team'], 
                        how='inner')
    
    print(f"Successfully matched {len(merged_df)} games with odds")
    
    # Calculate ATS results
    ats_results = []
    
    for _, row in merged_df.iterrows():
        away_score = row['away_score']
        home_score = row['home_score']
        spread = row['spread_line']
        favorite = row['favorite_team']
        underdog = row['underdog_team']
        
        # Determine who won
        if away_score > home_score:
            winner = row['away_team']
        elif home_score > away_score:
            winner = row['home_team']
        else:
            winner = 'Tie'
        
        # Calculate ATS result
        if favorite == row['away_team']:
            # Away team is favorite
            favorite_score = away_score
            underdog_score = home_score
            margin = away_score - home_score
        else:
            # Home team is favorite
            favorite_score = home_score
            underdog_score = away_score
            margin = home_score - away_score
        
        # Check if underdog covered
        if margin > abs(spread):
            # Favorite won by more than spread
            underdog_covered = False
        elif margin < -abs(spread):
            # Underdog won outright or by more than spread
            underdog_covered = True
        else:
            # Push (exact spread)
            underdog_covered = None
        
        ats_results.append({
            'week': row['week_x'],
            'game': f"{row['away_team']} @ {row['home_team']}",
            'final_score': f"{row['away_team']} {away_score} - {row['home_team']} {home_score}",
            'favorite': favorite,
            'underdog': underdog,
            'spread': spread,
            'margin': margin,
            'underdog_covered': underdog_covered,
            'winner': winner
        })
    
    return pd.DataFrame(ats_results)

def analyze_ats_results(ats_df):
    """Analyze ATS results"""
    
    print(f"\n=== ATS Results Analysis ===")
    print(f"Total games: {len(ats_df)}")
    
    # Remove pushes (None values)
    valid_games = ats_df[ats_df['underdog_covered'].notna()]
    print(f"Valid games (excluding pushes): {len(valid_games)}")
    
    if len(valid_games) == 0:
        print("No valid games to analyze")
        return
    
    # Calculate overall performance
    underdog_covers = valid_games['underdog_covered'].sum()
    favorite_covers = len(valid_games) - underdog_covers
    
    print(f"\nOverall ATS Performance:")
    print(f"  Underdog Covers: {underdog_covers}/{len(valid_games)} ({underdog_covers/len(valid_games)*100:.1f}%)")
    print(f"  Favorite Covers: {favorite_covers}/{len(valid_games)} ({favorite_covers/len(valid_games)*100:.1f}%)")
    
    # Week-by-week breakdown
    print(f"\nWeek-by-week breakdown:")
    for week in sorted(valid_games['week'].unique()):
        week_data = valid_games[valid_games['week'] == week]
        week_underdog_covers = week_data['underdog_covered'].sum()
        week_total = len(week_data)
        week_rate = week_underdog_covers / week_total * 100
        
        print(f"  Week {week}: {week_underdog_covers}/{week_total} underdog covers ({week_rate:.1f}%)")
        
        # Show sample games
        print(f"    Sample games:")
        for _, game in week_data.head(3).iterrows():
            print(f"      {game['game']}: {game['final_score']} - Underdog covered: {game['underdog_covered']}")
    
    # Show all games
    print(f"\nAll Games with ATS Results:")
    for _, game in valid_games.iterrows():
        cover_text = "Yes" if game['underdog_covered'] else "No"
        print(f"  {game['game']}: {game['final_score']} - Underdog covered: {cover_text}")
    
    return valid_games

def main():
    """Main function to analyze master games results"""
    
    print("=== Analyzing Master Games Results ===")
    print("Calculating ATS performance from actual game results")
    print("=" * 60)
    
    # Load master games results
    games_file = "data/master_games_results.csv"
    if not os.path.exists(games_file):
        print(f"❌ {games_file} not found")
        return
    
    games_df = pd.read_csv(games_file)
    print(f"✅ Loaded {len(games_df)} games from master results")
    
    # Load Week 1 odds
    odds_df = load_week_odds(1)
    if odds_df is None:
        print("❌ Week 1 odds not found")
        return
    
    print(f"✅ Loaded {len(odds_df)} games from Week 1 odds")
    
    # Calculate ATS performance
    ats_df = calculate_ats_performance(games_df, odds_df)
    
    # Analyze results
    valid_games = analyze_ats_results(ats_df)
    
    # Save results
    if valid_games is not None:
        output_file = "data/week1_ats_analysis.csv"
        valid_games.to_csv(output_file, index=False)
        print(f"\n✅ ATS analysis saved to {output_file}")
    
    print(f"\n=== Analysis Complete ===")
    print(f"📊 Analyzed {len(games_df)} games from master results")
    print(f"📁 Data sources: {games_file} and schedule/week1_2025_odds.csv")

if __name__ == "__main__":
    main()
