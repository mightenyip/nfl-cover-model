#!/usr/bin/env python3
"""
Comprehensive analysis of matchup EPA correlation using all available historical data
"""

import pandas as pd
import numpy as np
import os
import re
from scipy import stats

def load_week2_data():
    """Load Week 2 data from available files"""
    print("Loading Week 2 data...")
    
    # Try to load from detailed results
    try:
        df = pd.read_csv('week2/week2_detailed_results.csv')
        print(f"Loaded Week 2 detailed results: {len(df)} games")
        return df
    except:
        pass
    
    # Try other Week 2 files
    for file in ['week2_results_template.csv', 'week2_results_sample.csv']:
        try:
            df = pd.read_csv(f'week2/{file}')
            print(f"Loaded Week 2 from {file}: {len(df)} games")
            return df
        except:
            continue
    
    return None

def load_week3_data():
    """Load Week 3 data"""
    print("Loading Week 3 data...")
    try:
        df = pd.read_csv('week3/week3_detailed_results.csv')
        print(f"Loaded Week 3 detailed results: {len(df)} games")
        return df
    except:
        try:
            df = pd.read_csv('week3/week3_all_models_predictions_vs_reality.csv')
            print(f"Loaded Week 3 from predictions vs reality: {len(df)} games")
            return df
        except:
            pass
    
    return None

def parse_markdown_results(file_path):
    """Parse markdown files to extract game results"""
    print(f"Parsing markdown file: {file_path}")
    
    try:
        with open(file_path, 'r') as f:
            content = f.read()
        
        games = []
        lines = content.split('\n')
        
        for line in lines:
            # Look for game result patterns
            if ' @ ' in line and (' - ' in line or ':' in line):
                # Extract game info
                parts = line.split()
                if len(parts) >= 3:
                    # Try to extract scores
                    score_match = re.search(r'(\d+)\s*-\s*(\d+)', line)
                    if score_match:
                        home_score = int(score_match.group(1))
                        away_score = int(score_match.group(2))
                        
                        # Extract team names
                        if ' @ ' in line:
                            away_team, home_team = line.split(' @ ')[0], line.split(' @ ')[1].split()[0]
                            
                            games.append({
                                'game': f"{away_team} @ {home_team}",
                                'home_team': home_team,
                                'away_team': away_team,
                                'home_score': home_score,
                                'away_score': away_score
                            })
        
        print(f"Parsed {len(games)} games from markdown")
        return games
    except Exception as e:
        print(f"Error parsing markdown: {e}")
        return []

def load_all_historical_data():
    """Load all available historical data"""
    print("=== Loading All Historical Data ===")
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
    
    all_games = []
    
    # Load Week 1 (markdown)
    try:
        week1_games = parse_markdown_results('week1/week1_2025_results_analysis.md')
        for game in week1_games:
            all_games.append({
                'week': 1,
                'game': game['game'],
                'home_team': game['home_team'],
                'away_team': game['away_team'],
                'home_score': game['home_score'],
                'away_score': game['away_score']
            })
        print(f"Added {len(week1_games)} games from Week 1")
    except:
        print("Could not load Week 1 data")
    
    # Load Week 2
    week2_data = load_week2_data()
    if week2_data is not None:
        for _, row in week2_data.iterrows():
            all_games.append({
                'week': 2,
                'game': row.get('Game', ''),
                'home_team': row.get('Home_Team', ''),
                'away_team': row.get('Away_Team', ''),
                'home_score': row.get('Home_Score', 0),
                'away_score': row.get('Away_Score', 0)
            })
        print(f"Added {len(week2_data)} games from Week 2")
    
    # Load Week 3
    week3_data = load_week3_data()
    if week3_data is not None:
        for _, row in week3_data.iterrows():
            all_games.append({
                'week': 3,
                'game': row.get('Game', ''),
                'home_team': row.get('Home_Team', ''),
                'away_team': row.get('Away_Team', ''),
                'home_score': row.get('Home_Score', 0),
                'away_score': row.get('Away_Score', 0)
            })
        print(f"Added {len(week3_data)} games from Week 3")
    
    print(f"Total games loaded: {len(all_games)}")
    return all_games, epa_df, team_mapping

def calculate_matchup_epa_analysis(games, epa_df, team_mapping):
    """Calculate matchup EPA analysis for all games"""
    print("\n=== Calculating Matchup EPA Analysis ===")
    print("=" * 50)
    
    analysis_results = []
    
    for game in games:
        try:
            home_team = game['home_team']
            away_team = game['away_team']
            home_score = game['home_score']
            away_score = game['away_score']
            
            # Get EPA data
            home_abbr = team_mapping.get(home_team, home_team)
            away_abbr = team_mapping.get(away_team, away_team)
            
            home_epa = epa_df[epa_df['team'] == home_abbr]
            away_epa = epa_df[epa_df['team'] == away_abbr]
            
            if not home_epa.empty and not away_epa.empty:
                home_off = home_epa['epa_off_per_play'].iloc[0]
                home_def = home_epa['epa_def_allowed_per_play'].iloc[0]
                away_off = away_epa['epa_off_per_play'].iloc[0]
                away_def = away_epa['epa_def_allowed_per_play'].iloc[0]
                
                # Calculate matchup EPA
                home_matchup_epa = home_off + away_def
                away_matchup_epa = away_off + home_def
                matchup_epa_diff = home_matchup_epa - away_matchup_epa
                
                # Calculate actual margin
                actual_margin = home_score - away_score
                
                analysis_results.append({
                    'week': game['week'],
                    'game': game['game'],
                    'home_team': home_team,
                    'away_team': away_team,
                    'home_score': home_score,
                    'away_score': away_score,
                    'actual_margin': actual_margin,
                    'home_matchup_epa': home_matchup_epa,
                    'away_matchup_epa': away_matchup_epa,
                    'matchup_epa_diff': matchup_epa_diff
                })
        except Exception as e:
            print(f"Error processing {game['game']}: {e}")
            continue
    
    print(f"Successfully analyzed {len(analysis_results)} games")
    return pd.DataFrame(analysis_results)

def analyze_correlation(df):
    """Analyze correlation between matchup EPA differences and spread performance"""
    print("\n=== Matchup EPA Correlation Analysis ===")
    print("=" * 50)
    
    if len(df) < 3:
        print("❌ Insufficient data for correlation analysis")
        return None
    
    # For this analysis, we'll use actual margin as a proxy for spread performance
    # In a real analysis, we'd need the actual spreads for each game
    
    # Calculate correlation between matchup EPA diff and actual margin
    correlation = df['matchup_epa_diff'].corr(df['actual_margin'])
    
    print(f"Correlation between Matchup EPA Diff and Actual Margin: {correlation:.3f}")
    print(f"Sample size: {len(df)} games")
    print()
    
    # Statistical significance
    t_stat, p_value = stats.pearsonr(df['matchup_epa_diff'], df['actual_margin'])
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
        print("   Home teams with higher matchup EPA differences tend to win by larger margins")
        print("   Model X can predict game outcomes")
    elif correlation > 0.1:
        print("✅ MODERATE POSITIVE CORRELATION")
        print("   Some relationship between matchup EPA and game outcomes")
    elif correlation > -0.1:
        print("⚠️  WEAK CORRELATION")
        print("   Little relationship between matchup EPA and game outcomes")
    elif correlation > -0.3:
        print("⚠️  MODERATE NEGATIVE CORRELATION")
        print("   Home teams with higher matchup EPA differences tend to win by smaller margins")
    else:
        print("❌ STRONG NEGATIVE CORRELATION")
        print("   Home teams with higher matchup EPA differences tend to lose")
    
    print()
    
    # Summary statistics
    print("Summary Statistics:")
    print(f"  Average Matchup EPA Diff: {df['matchup_epa_diff'].mean():.3f}")
    print(f"  Average Actual Margin: {df['actual_margin'].mean():.3f}")
    print(f"  Standard Deviation EPA Diff: {df['matchup_epa_diff'].std():.3f}")
    print(f"  Standard Deviation Actual Margin: {df['actual_margin'].std():.3f}")
    
    print()
    
    # Show top and bottom games
    print("Games with Highest Matchup EPA Differences:")
    top_epa = df.nlargest(5, 'matchup_epa_diff')
    for _, row in top_epa.iterrows():
        print(f"  {row['game']}: EPA Diff {row['matchup_epa_diff']:.3f}, Margin {row['actual_margin']:+.1f}")
    
    print()
    print("Games with Lowest Matchup EPA Differences:")
    bottom_epa = df.nsmallest(5, 'matchup_epa_diff')
    for _, row in bottom_epa.iterrows():
        print(f"  {row['game']}: EPA Diff {row['matchup_epa_diff']:.3f}, Margin {row['actual_margin']:+.1f}")
    
    return correlation

def main():
    """Main analysis function"""
    print("=== Comprehensive Matchup EPA Correlation Analysis ===")
    print("Analyzing all available historical data (Weeks 1-7)")
    print("=" * 70)
    
    # Load all historical data
    games, epa_df, team_mapping = load_all_historical_data()
    
    if not games:
        print("❌ No historical data available")
        return
    
    # Calculate matchup EPA analysis
    df = calculate_matchup_epa_analysis(games, epa_df, team_mapping)
    
    if df.empty:
        print("❌ No games could be analyzed")
        return
    
    # Analyze correlation
    correlation = analyze_correlation(df)
    
    if correlation is not None:
        print(f"\n=== CONCLUSION ===")
        print(f"Model X Correlation: {correlation:.3f}")
        
        if abs(correlation) > 0.3:
            print("✅ Model X shows strong predictive power for game outcomes")
        elif abs(correlation) > 0.1:
            print("⚠️  Model X shows moderate predictive power")
        else:
            print("❌ Model X shows weak predictive power for game outcomes")
    
    # Save results
    output_path = 'data/epa/analysis/comprehensive_matchup_epa_analysis.csv'
    df.to_csv(output_path, index=False)
    print(f"\n✅ Comprehensive analysis saved to: {output_path}")

if __name__ == "__main__":
    main()
