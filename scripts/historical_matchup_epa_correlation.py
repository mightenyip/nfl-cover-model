#!/usr/bin/env python3
"""
Analyze correlation between matchup EPA differences and spread performance
using historical data from Weeks 3-7
"""

import pandas as pd
import numpy as np
from scipy import stats

def load_historical_data():
    """Load historical game data from Weeks 3-7"""
    print("=== Loading Historical Data (Weeks 3-7) ===")
    print("=" * 50)
    
    # Load EPA data
    epa_df = pd.read_csv('detailed_epa_data.csv')
    print(f"Loaded EPA data for {len(epa_df)} teams")
    
    # Team mapping
    team_mapping = {
        '49ers': 'SF', 'Bears': 'CHI', 'Bengals': 'CIN', 'Bills': 'BUF', 'Broncos': 'DEN',
        'Browns': 'CLE', 'Buccaneers': 'TB', 'Cardinals': 'ARI', 'Chargers': 'LAC', 'Chiefs': 'KC',
        'Colts': 'IND', 'Commanders': 'WAS', 'Cowboys': 'DAL', 'Dolphins': 'MIA', 'Eagles': 'PHI',
        'Falcons': 'ATL', 'Giants': 'NYG', 'Jaguars': 'JAX', 'Jets': 'NYJ', 'Lions': 'DET',
        'Packers': 'GB', 'Panthers': 'CAR', 'Patriots': 'NE', 'Raiders': 'LV', 'Rams': 'LA',
        'Ravens': 'BAL', 'Saints': 'NO', 'Seahawks': 'SEA', 'Steelers': 'PIT', 'Texans': 'HOU',
        'Titans': 'TEN', 'Vikings': 'MIN'
    }
    
    # Load historical results from all weeks
    historical_games = []
    
    # Process all weeks 1-7
    for week in range(1, 8):
        try:
            # Try to load results data
            if week == 1:
                results_file = 'week1/week1_2025_results_analysis.md'
                # Parse markdown file for Week 1
                print(f"Loading Week {week} data...")
                continue  # Skip Week 1 for now, need to parse markdown
            elif week == 2:
                results_file = 'week2/week2_all_models_predictions_vs_reality.csv'
            elif week == 3:
                results_file = 'week3/week3_all_models_predictions_vs_reality.csv'
            elif week == 4:
                results_file = 'week4/week4_all_models_predictions_vs_reality.csv'
            elif week == 5:
                results_file = 'week5/week5_all_models_predictions_vs_reality.csv'
            elif week == 6:
                results_file = 'week6/week6_all_models_predictions_vs_reality.csv'
            elif week == 7:
                results_file = 'week7/week7_all_models_predictions_vs_reality.csv'
            
            # Load results
            try:
                week_results = pd.read_csv(results_file)
                print(f"Loaded Week {week}: {len(week_results)} games")
            except FileNotFoundError:
                print(f"Week {week} results file not found, skipping...")
                continue
            
            # Process each game
            for idx, row in week_results.iterrows():
                game = row['Game']
                favorite = row['Favorite']
                underdog = row['Underdog']
                spread = row['Spread']
                final_score = row['Final_Score']
                actual_cover = row['Actual_Cover']
                
                # Parse final score to get actual margin
                if ' - ' in final_score:
                    home_score, away_score = final_score.split(' - ')
                    home_score = int(home_score.split()[-1])
                    away_score = int(away_score.split()[-1])
                    
                    # Determine which team is home/away from game string
                    if ' @ ' in game:
                        away_team, home_team = game.split(' @ ')
                    else:
                        continue
                        
                    # Calculate actual margin (favorite - underdog)
                    if favorite == home_team:
                        actual_margin = home_score - away_score
                    else:
                        actual_margin = away_score - home_score
                else:
                    continue
                
                # Get EPA data for both teams
                fav_abbr = team_mapping.get(favorite, favorite)
                dog_abbr = team_mapping.get(underdog, underdog)
                
                fav_epa = epa_df[epa_df['team'] == fav_abbr]
                dog_epa = epa_df[epa_df['team'] == dog_abbr]
                
                if not fav_epa.empty and not dog_epa.empty:
                    fav_off = fav_epa['epa_off_per_play'].iloc[0]
                    fav_def = fav_epa['epa_def_allowed_per_play'].iloc[0]
                    dog_off = dog_epa['epa_off_per_play'].iloc[0]
                    dog_def = dog_epa['epa_def_allowed_per_play'].iloc[0]
                    
                    # Calculate matchup EPA differences
                    # Favorite matchup EPA vs Underdog defense
                    fav_matchup_epa = fav_off + dog_def
                    # Underdog matchup EPA vs Favorite defense  
                    dog_matchup_epa = dog_off + fav_def
                    
                    matchup_epa_diff = fav_matchup_epa - dog_matchup_epa
                    margin_vs_spread = actual_margin - spread
                    
                    historical_games.append({
                        'week': week,
                        'game': game,
                        'favorite': favorite,
                        'underdog': underdog,
                        'spread': spread,
                        'actual_margin': actual_margin,
                        'margin_vs_spread': margin_vs_spread,
                        'actual_cover': actual_cover,
                        'fav_matchup_epa': fav_matchup_epa,
                        'dog_matchup_epa': dog_matchup_epa,
                        'matchup_epa_diff': matchup_epa_diff
                    })
            
            print(f"Processed {len([g for g in historical_games if g['week'] == week])} games from Week {week}")
            
        except Exception as e:
            print(f"Error processing Week {week}: {e}")
            continue
    
    print(f"Total games processed: {len(historical_games)}")
    
    return pd.DataFrame(historical_games)

def analyze_correlation(df):
    """Analyze correlation between matchup EPA differences and spread performance"""
    print("\n=== Matchup EPA Correlation Analysis ===")
    print("=" * 50)
    
    if len(df) < 3:
        print("❌ Insufficient data for correlation analysis")
        return None
    
    # Calculate correlation
    correlation = df['matchup_epa_diff'].corr(df['margin_vs_spread'])
    
    print(f"Correlation between Matchup EPA Diff and Margin vs Spread: {correlation:.3f}")
    print(f"Sample size: {len(df)} games")
    print()
    
    # Statistical significance
    t_stat, p_value = stats.pearsonr(df['matchup_epa_diff'], df['margin_vs_spread'])
    print(f"Statistical Significance:")
    print(f"  t-statistic: {t_stat:.3f}")
    print(f"  p-value: {p_value:.3f}")
    
    if p_value < 0.05:
        print("  ✅ Statistically significant (p < 0.05)")
    elif p_value < 0.10:
        print("  ⚠️  Marginally significant (p < 0.10)")
    else:
        print("  ❌ Not statistically significant (p >= 0.10)")
    
    print()
    
    # Interpretation
    if correlation > 0.3:
        print("✅ STRONG POSITIVE CORRELATION")
        print("   Favorites with higher matchup EPA differences tend to outperform their spreads")
        print("   Model X can predict which favorites will cover")
    elif correlation > 0.1:
        print("✅ MODERATE POSITIVE CORRELATION")
        print("   Some relationship between matchup EPA and spread performance")
    elif correlation > -0.1:
        print("⚠️  WEAK CORRELATION")
        print("   Little relationship between matchup EPA and spread performance")
    elif correlation > -0.3:
        print("⚠️  MODERATE NEGATIVE CORRELATION")
        print("   Favorites with higher matchup EPA differences tend to underperform spreads")
        print("   Market might be overpricing matchup advantages")
    else:
        print("❌ STRONG NEGATIVE CORRELATION")
        print("   Strong favorites with matchup advantages tend to underperform")
        print("   Market is significantly overpricing matchup advantages")
    
    print()
    
    # Summary statistics
    print("Summary Statistics:")
    print(f"  Average Matchup EPA Diff: {df['matchup_epa_diff'].mean():.3f}")
    print(f"  Average Margin vs Spread: {df['margin_vs_spread'].mean():.3f}")
    print(f"  Standard Deviation EPA Diff: {df['matchup_epa_diff'].std():.3f}")
    print(f"  Standard Deviation Margin vs Spread: {df['margin_vs_spread'].std():.3f}")
    
    print()
    
    # Show individual games
    print("Individual Game Analysis:")
    print("-" * 30)
    for _, row in df.iterrows():
        print(f"{row['game']}:")
        print(f"  Matchup EPA Diff: {row['matchup_epa_diff']:.3f}")
        print(f"  Margin vs Spread: {row['margin_vs_spread']:.1f}")
        print(f"  Actual Cover: {row['actual_cover']}")
        print()
    
    return correlation

def main():
    """Main analysis function"""
    print("=== Historical Matchup EPA Correlation Analysis ===")
    print("Testing Model X effectiveness with Weeks 3-7 data")
    print("=" * 70)
    
    # Load historical data
    df = load_historical_data()
    
    if df.empty:
        print("❌ No historical data available")
        return
    
    # Analyze correlation
    correlation = analyze_correlation(df)
    
    if correlation is not None:
        print(f"\n=== CONCLUSION ===")
        print(f"Model X Correlation: {correlation:.3f}")
        
        if abs(correlation) > 0.3:
            print("✅ Model X shows strong predictive power for spread performance")
        elif abs(correlation) > 0.1:
            print("⚠️  Model X shows moderate predictive power")
        else:
            print("❌ Model X shows weak predictive power for spread performance")
    
    # Save results
    output_path = 'data/historical_matchup_epa_analysis.csv'
    df.to_csv(output_path, index=False)
    print(f"\n✅ Historical analysis saved to: {output_path}")

if __name__ == "__main__":
    main()
