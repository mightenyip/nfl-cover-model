#!/usr/bin/env python3
"""
Comprehensive Matchup EPA Analysis - ALL WEEKS 1-7
Processes every single game from all available weeks
"""

import pandas as pd
import numpy as np
import os
from scipy import stats

# Load EPA data
epa_df = pd.read_csv('detailed_epa_data.csv')
print(f"Loaded EPA data for {len(epa_df)} teams")

def process_week_data(week_num):
    """Process data for a specific week"""
    print(f"\n=== PROCESSING WEEK {week_num} ===")
    
    # Use the correct data sources - all weeks should use data/week#_ats_results.csv
    possible_files = [
        f'data/ats_results/week{week_num}/week{week_num}_ats_results.csv'
    ]
    
    week_data = None
    used_file = None
    
    for file_path in possible_files:
        if os.path.exists(file_path):
            try:
                week_data = pd.read_csv(file_path)
                used_file = file_path
                print(f"✅ Loaded Week {week_num} from: {file_path}")
                print(f"   Columns: {list(week_data.columns)}")
                print(f"   Games: {len(week_data)}")
                break
            except Exception as e:
                print(f"❌ Failed to load {file_path}: {e}")
                continue
    
    if week_data is None:
        print(f"❌ No data found for Week {week_num}")
        return []
    
    games_processed = []
    
    # Process each game in the week
    for idx, row in week_data.iterrows():
        try:
            # Extract game information - try different column names
            game = None
            if 'game' in row:
                game = row['game']
            elif 'Game' in row:
                game = row['Game']
            elif 'matchup' in row:
                game = row['matchup']
            
            if not game:
                print(f"  Skipping row {idx}: No game identifier found")
                continue
            
            # Extract team information - use standard column names from ats_results files
            favorite = row['favorite']
            underdog = row['underdog']
            spread = row['spread']
            
            if not all([favorite, underdog, spread]):
                print(f"  Skipping {game}: Missing favorite/underdog/spread data")
                continue
            
            # Convert spread to float
            try:
                spread = float(spread)
            except (ValueError, TypeError):
                print(f"  Skipping {game}: Invalid spread value: {spread}")
                continue
            
            # Extract actual scores - use standard column names from ats_results files
            actual_home_score = row['home_score']
            actual_away_score = row['away_score']
            
            if actual_home_score is None or actual_away_score is None:
                print(f"  Skipping {game}: Missing score data")
                continue
            
            # Parse home/away teams from game string
            if ' @ ' in game:
                away_team_full, home_team_full = game.split(' @ ')
            else:
                print(f"  Skipping {game}: Cannot parse home/away teams")
                continue
            
            # Calculate actual margin (favorite - underdog)
            if favorite == home_team_full:
                actual_margin = actual_home_score - actual_away_score
            elif favorite == away_team_full:
                actual_margin = actual_away_score - actual_home_score
            else:
                print(f"  Skipping {game}: Favorite team doesn't match home/away")
                continue
            
            # Get EPA data for both teams
            fav_epa = epa_df[epa_df['team_name'] == favorite]
            dog_epa = epa_df[epa_df['team_name'] == underdog]
            
            if fav_epa.empty or dog_epa.empty:
                print(f"  Skipping {game}: EPA data not found for {favorite} or {underdog}")
                continue
            
            fav_off = fav_epa['epa_off_per_play'].iloc[0]
            fav_def = fav_epa['epa_def_allowed_per_play'].iloc[0]
            dog_off = dog_epa['epa_off_per_play'].iloc[0]
            dog_def = dog_epa['epa_def_allowed_per_play'].iloc[0]
            
            # Calculate matchup EPA for favorite and underdog
            fav_matchup_epa = fav_off + dog_def
            dog_matchup_epa = dog_off + fav_def
            
            matchup_epa_diff = fav_matchup_epa - dog_matchup_epa
            margin_vs_spread = actual_margin - spread
            
            game_data = {
                'week': week_num,
                'game': game,
                'favorite': favorite,
                'underdog': underdog,
                'spread': spread,
                'actual_margin': actual_margin,
                'margin_vs_spread': margin_vs_spread,
                'fav_matchup_epa': fav_matchup_epa,
                'dog_matchup_epa': dog_matchup_epa,
                'matchup_epa_diff': matchup_epa_diff,
                'fav_off_epa': fav_off,
                'fav_def_epa': fav_def,
                'dog_off_epa': dog_off,
                'dog_def_epa': dog_def
            }
            
            games_processed.append(game_data)
            print(f"  ✅ Processed: {game} - EPA Diff: {matchup_epa_diff:.3f}, Margin vs Spread: {margin_vs_spread:.1f}")
            
        except Exception as e:
            print(f"  ❌ Error processing row {idx}: {e}")
            continue
    
    print(f"  📊 Week {week_num} Summary: {len(games_processed)} games processed")
    return games_processed

def analyze_comprehensive_correlation(all_games_df):
    """Analyze correlation across all weeks"""
    print(f"\n{'='*60}")
    print(f"COMPREHENSIVE MATCHUP EPA CORRELATION ANALYSIS")
    print(f"{'='*60}")
    
    if all_games_df.empty:
        print("❌ No games processed for correlation analysis")
        return
    
    print(f"📊 Total Games Analyzed: {len(all_games_df)}")
    print(f"📅 Weeks Covered: {sorted(all_games_df['week'].unique())}")
    
    # Overall correlation
    correlation = all_games_df['matchup_epa_diff'].corr(all_games_df['margin_vs_spread'])
    print(f"\n🎯 OVERALL CORRELATION: {correlation:.3f}")
    
    # Statistical significance
    if len(all_games_df) > 2:
        t_statistic = correlation * np.sqrt((len(all_games_df) - 2) / (1 - correlation**2))
        p_value = 2 * (1 - stats.t.cdf(abs(t_statistic), len(all_games_df) - 2))
        print(f"📈 t-statistic: {t_statistic:.3f}")
        print(f"📈 p-value: {p_value:.3f}")
        
        if p_value < 0.05:
            print("✅ Statistically significant (p < 0.05)")
        elif p_value < 0.10:
            print("⚠️ Marginally statistically significant (p < 0.10)")
        else:
            print("❌ Not statistically significant (p >= 0.10)")
    
    # Week-by-week analysis
    print(f"\n📅 WEEK-BY-WEEK CORRELATIONS:")
    for week in sorted(all_games_df['week'].unique()):
        week_data = all_games_df[all_games_df['week'] == week]
        if len(week_data) > 1:
            week_corr = week_data['matchup_epa_diff'].corr(week_data['margin_vs_spread'])
            print(f"  Week {week}: {week_corr:.3f} ({len(week_data)} games)")
    
    # Summary statistics
    print(f"\n📊 SUMMARY STATISTICS:")
    print(f"  Average Matchup EPA Diff: {all_games_df['matchup_epa_diff'].mean():.3f}")
    print(f"  Average Margin vs Spread: {all_games_df['margin_vs_spread'].mean():.3f}")
    print(f"  Std Dev EPA Diff: {all_games_df['matchup_epa_diff'].std():.3f}")
    print(f"  Std Dev Margin vs Spread: {all_games_df['margin_vs_spread'].std():.3f}")
    
    # Top and bottom games
    print(f"\n🏆 TOP 5 GAMES BY MATCHUP EPA DIFFERENCE:")
    top_games = all_games_df.nlargest(5, 'matchup_epa_diff')
    for _, row in top_games.iterrows():
        print(f"  {row['game']}: EPA Diff {row['matchup_epa_diff']:.3f}, Margin vs Spread {row['margin_vs_spread']:.1f}")
    
    print(f"\n📉 BOTTOM 5 GAMES BY MATCHUP EPA DIFFERENCE:")
    bottom_games = all_games_df.nsmallest(5, 'matchup_epa_diff')
    for _, row in bottom_games.iterrows():
        print(f"  {row['game']}: EPA Diff {row['matchup_epa_diff']:.3f}, Margin vs Spread {row['margin_vs_spread']:.1f}")
    
    # Save comprehensive analysis
    output_path = 'data/epa/analysis/comprehensive_matchup_epa_analysis.csv'
    os.makedirs('data', exist_ok=True)
    all_games_df.to_csv(output_path, index=False)
    print(f"\n💾 Comprehensive analysis saved to: {output_path}")
    
    return correlation

def main():
    print("🚀 COMPREHENSIVE MATCHUP EPA ANALYSIS")
    print("Processing ALL games from ALL weeks (1-7)")
    print("="*60)
    
    all_games = []
    
    # Process all weeks 1-7
    for week in range(1, 8):
        week_games = process_week_data(week)
        all_games.extend(week_games)
    
    print(f"\n🎯 TOTAL GAMES PROCESSED: {len(all_games)}")
    
    if all_games:
        all_games_df = pd.DataFrame(all_games)
        correlation = analyze_comprehensive_correlation(all_games_df)
        
        print(f"\n🏁 FINAL CONCLUSION:")
        if correlation > 0.2:
            print(f"✅ STRONG POSITIVE CORRELATION: {correlation:.3f}")
            print("   Model X shows strong predictive power!")
        elif correlation < -0.2:
            print(f"⚠️ STRONG NEGATIVE CORRELATION: {correlation:.3f}")
            print("   Model X identifies overpriced favorites!")
        else:
            print(f"↔️ WEAK CORRELATION: {correlation:.3f}")
            print("   Model X shows limited predictive power")
    else:
        print("❌ No games were successfully processed")

if __name__ == "__main__":
    main()
