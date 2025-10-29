#!/usr/bin/env python3
"""
Simple matchup EPA correlation analysis using actual data structure
"""

import pandas as pd
import numpy as np
from scipy import stats

def load_historical_data():
    """Load all available historical data"""
    print("=== Loading Historical Data ===")
    print("=" * 40)
    
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
    
    all_games = []
    
    # Load Week 2 data
    try:
        week2_df = pd.read_csv('week2/week2_detailed_results.csv')
        print(f"Loaded Week 2: {len(week2_df)} games")
        
        for _, row in week2_df.iterrows():
            game = row['game']
            favorite = row['favorite']
            underdog = row['underdog']
            spread = row['spread']
            home_score = row['actual_home_score']
            away_score = row['actual_away_score']
            actual_cover = row['actual_cover']
            
            # Determine home/away teams
            if ' at ' in game:
                away_team, home_team = game.split(' at ')
            elif ' @ ' in game:
                away_team, home_team = game.split(' @ ')
            else:
                continue
            
            # Calculate actual margin (favorite - underdog)
            if favorite == home_team:
                actual_margin = home_score - away_score
            else:
                actual_margin = away_score - home_score
            
            # Get EPA data
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
                fav_matchup_epa = fav_off + dog_def
                dog_matchup_epa = dog_off + fav_def
                matchup_epa_diff = fav_matchup_epa - dog_matchup_epa
                margin_vs_spread = actual_margin - spread
                
                all_games.append({
                    'week': 2,
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
        
        print(f"Processed {len([g for g in all_games if g['week'] == 2])} games from Week 2")
    except Exception as e:
        print(f"Error loading Week 2: {e}")
    
    # Load Week 3 data
    try:
        week3_df = pd.read_csv('week3/week3_detailed_results.csv')
        print(f"Loaded Week 3: {len(week3_df)} games")
        
        for _, row in week3_df.iterrows():
            game = row['game']
            favorite = row['favorite']
            underdog = row['underdog']
            spread = row['spread']
            home_score = row['actual_home_score']
            away_score = row['actual_away_score']
            actual_cover = row['actual_cover']
            
            # Determine home/away teams
            if ' @ ' in game:
                away_team, home_team = game.split(' @ ')
            else:
                continue
            
            # Calculate actual margin (favorite - underdog)
            if favorite == home_team:
                actual_margin = home_score - away_score
            else:
                actual_margin = away_score - home_score
            
            # Get EPA data
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
                fav_matchup_epa = fav_off + dog_def
                dog_matchup_epa = dog_off + fav_def
                matchup_epa_diff = fav_matchup_epa - dog_matchup_epa
                margin_vs_spread = actual_margin - spread
                
                all_games.append({
                    'week': 3,
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
        
        print(f"Processed {len([g for g in all_games if g['week'] == 3])} games from Week 3")
    except Exception as e:
        print(f"Error loading Week 3: {e}")
    
    print(f"Total games processed: {len(all_games)}")
    return pd.DataFrame(all_games)

def analyze_correlation(df):
    """Analyze correlation between matchup EPA differences and spread performance"""
    print("\n=== Matchup EPA Correlation Analysis ===")
    print("=" * 50)
    
    if len(df) < 3:
        print("❌ Insufficient data for correlation analysis")
        return None
    
    # Calculate correlation between matchup EPA diff and margin vs spread
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
    print("=== Simple Matchup EPA Correlation Analysis ===")
    print("Analyzing historical data from Weeks 2-3")
    print("=" * 60)
    
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
    output_path = 'data/simple_matchup_epa_analysis.csv'
    df.to_csv(output_path, index=False)
    print(f"\n✅ Analysis saved to: {output_path}")

if __name__ == "__main__":
    main()
