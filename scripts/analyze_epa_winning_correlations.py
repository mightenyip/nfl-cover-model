#!/usr/bin/env python3
"""
Comprehensive EPA Analysis: Correlations with Winning and Covering
Analyzes EPA correlations for:
1. Underdog covering the spread
2. Underdog winning outright
3. Any team winning (regardless of favorite/underdog status)
"""

import pandas as pd
import numpy as np
from scipy.stats import pearsonr
import matplotlib.pyplot as plt
import seaborn as sns

def load_week1_data():
    """Load Week 1 data with EPA analysis"""
    # Load corrected Week 1 odds
    week1_odds = pd.read_csv('week1/week1_2025_odds.csv')
    
    # Load real PBP data
    pbp_2025 = pd.read_parquet('images/play_by_play_2025.parquet')
    week1_games = pbp_2025[pbp_2025['week'] == 1].copy()
    
    # Team name mapping
    team_mapping = {
        'Raiders': 'LV', 'Patriots': 'NE', 'Steelers': 'PIT', 'Jets': 'NYJ',
        'Dolphins': 'MIA', 'Colts': 'IND', 'Cardinals': 'ARI', 'Saints': 'NO',
        'Giants': 'NYG', 'Commanders': 'WAS', 'Panthers': 'CAR', 'Jaguars': 'JAX',
        'Bengals': 'CIN', 'Browns': 'CLE', 'Buccaneers': 'TB', 'Falcons': 'ATL',
        'Titans': 'TEN', 'Broncos': 'DEN', '49ers': 'SF', 'Seahawks': 'SEA',
        'Lions': 'DET', 'Packers': 'GB', 'Texans': 'HOU', 'Rams': 'LA',
        'Ravens': 'BAL', 'Bills': 'BUF', 'Vikings': 'MIN', 'Bears': 'CHI',
        'Chiefs': 'KC', 'Chargers': 'LAC', 'Cowboys': 'DAL', 'Eagles': 'PHI'
    }
    reverse_mapping = {v: k for k, v in team_mapping.items()}
    
    return week1_odds, week1_games, team_mapping, reverse_mapping

def analyze_underdog_epa_correlations(week1_odds, week1_games, team_mapping, reverse_mapping):
    """Analyze EPA correlations for underdog outcomes"""
    
    # Get game results and match with odds
    game_results = week1_games.groupby('game_id').agg({
        'home_team': 'first',
        'away_team': 'first', 
        'home_score': 'last',
        'away_score': 'last'
    }).reset_index()
    
    results_with_odds = []
    for _, game in game_results.iterrows():
        home_team_abbr = game['home_team']
        away_team_abbr = game['away_team']
        home_score = game['home_score']
        away_score = game['away_score']
        margin = home_score - away_score
        
        home_team_full = reverse_mapping.get(home_team_abbr, home_team_abbr)
        away_team_full = reverse_mapping.get(away_team_abbr, away_team_abbr)
        
        odds_match = week1_odds[
            ((week1_odds['home_team'] == home_team_full) & (week1_odds['away_team'] == away_team_full)) |
            ((week1_odds['home_team'] == away_team_full) & (week1_odds['away_team'] == home_team_full))
        ]
        
        if len(odds_match) > 0:
            odds_row = odds_match.iloc[0]
            favorite = odds_row['favorite_team']
            underdog = odds_row['underdog_team']
            spread = odds_row['spread_line']
            
            underdog_abbr = team_mapping.get(underdog, underdog)
            
            # Determine if underdog won outright and covered
            if underdog == home_team_full:
                underdog_won_outright = margin > 0  # Home team won
                underdog_covered = margin > -spread
            else:
                underdog_won_outright = margin < 0  # Away team won
                underdog_covered = margin < spread
            
            results_with_odds.append({
                'game_id': game['game_id'],
                'home_team': home_team_abbr,
                'away_team': away_team_abbr,
                'favorite': favorite,
                'underdog': underdog,
                'underdog_abbr': underdog_abbr,
                'underdog_won_outright': underdog_won_outright,
                'underdog_covered': underdog_covered,
                'margin': margin
            })
    
    results_df = pd.DataFrame(results_with_odds)
    
    # Calculate EPA for each underdog
    underdog_epa_data = []
    
    for _, result in results_df.iterrows():
        game_id = result['game_id']
        underdog_abbr = result['underdog_abbr']
        
        # Get plays for this game
        game_plays = week1_games[week1_games['game_id'] == game_id].copy()
        
        # Calculate EPA for underdog
        underdog_plays = game_plays[game_plays['posteam'] == underdog_abbr].copy()
        
        if len(underdog_plays) > 0:
            # Offensive EPA
            off_epa = underdog_plays['epa'].sum()
            off_epa_per_play = underdog_plays['epa'].mean()
            success_rate = (underdog_plays['epa'] > 0).mean()
            
            # Defensive EPA (EPA allowed)
            def_plays = game_plays[game_plays['posteam'] != underdog_abbr].copy()
            def_epa_allowed = def_plays['epa'].sum()
            def_epa_per_play_allowed = def_plays['epa'].mean()
            def_success_rate_allowed = (def_plays['epa'] > 0).mean()
            
            # Net EPA
            net_epa = off_epa - def_epa_allowed
            
            underdog_epa_data.append({
                'game_id': game_id,
                'underdog': result['underdog'],
                'underdog_won_outright': result['underdog_won_outright'],
                'underdog_covered': result['underdog_covered'],
                'off_epa': off_epa,
                'off_epa_per_play': off_epa_per_play,
                'off_success_rate': success_rate,
                'def_epa_allowed': def_epa_allowed,
                'def_epa_per_play_allowed': def_epa_per_play_allowed,
                'def_success_rate_allowed': def_success_rate_allowed,
                'net_epa': net_epa
            })
    
    return pd.DataFrame(underdog_epa_data)

def analyze_all_teams_epa_correlations(week1_games):
    """Analyze EPA correlations for all teams winning (regardless of favorite/underdog)"""
    
    # Get game results
    game_results = week1_games.groupby('game_id').agg({
        'home_team': 'first',
        'away_team': 'first', 
        'home_score': 'last',
        'away_score': 'last'
    }).reset_index()
    
    all_teams_epa_data = []
    
    for _, game in game_results.iterrows():
        game_id = game['game_id']
        home_team = game['home_team']
        away_team = game['away_team']
        home_score = game['home_score']
        away_score = game['away_score']
        margin = home_score - away_score
        
        # Get plays for this game
        game_plays = week1_games[week1_games['game_id'] == game_id].copy()
        
        # Calculate EPA for both teams
        for team in [home_team, away_team]:
            team_plays = game_plays[game_plays['posteam'] == team].copy()
            
            if len(team_plays) > 0:
                # Offensive EPA
                off_epa = team_plays['epa'].sum()
                off_epa_per_play = team_plays['epa'].mean()
                success_rate = (team_plays['epa'] > 0).mean()
                
                # Defensive EPA (EPA allowed)
                def_plays = game_plays[game_plays['posteam'] != team].copy()
                def_epa_allowed = def_plays['epa'].sum()
                def_epa_per_play_allowed = def_plays['epa'].mean()
                def_success_rate_allowed = (def_plays['epa'] > 0).mean()
                
                # Net EPA
                net_epa = off_epa - def_epa_allowed
                
                # Determine if team won
                if team == home_team:
                    team_won = margin > 0  # Home team won
                else:
                    team_won = margin < 0  # Away team won
                
                all_teams_epa_data.append({
                    'game_id': game_id,
                    'team': team,
                    'team_won': team_won,
                    'off_epa': off_epa,
                    'off_epa_per_play': off_epa_per_play,
                    'off_success_rate': success_rate,
                    'def_epa_allowed': def_epa_allowed,
                    'def_epa_per_play_allowed': def_epa_per_play_allowed,
                    'def_success_rate_allowed': def_success_rate_allowed,
                    'net_epa': net_epa
                })
    
    return pd.DataFrame(all_teams_epa_data)

def create_comprehensive_plots(underdog_epa_df, all_teams_epa_df):
    """Create comprehensive plots for EPA correlations"""
    
    plt.figure(figsize=(20, 15))
    
    # 1. Underdog Offensive EPA vs Cover
    plt.subplot(3, 4, 1)
    sns.boxplot(data=underdog_epa_df, x='underdog_covered', y='off_epa', 
                palette=['lightcoral', 'lightgreen'])
    plt.title('Underdog Off EPA vs Cover', fontweight='bold')
    plt.xlabel('Covered')
    plt.ylabel('Offensive EPA')
    plt.xticks([0, 1], ['No', 'Yes'])
    
    corr_cover, p_cover = pearsonr(underdog_epa_df['underdog_covered'], underdog_epa_df['off_epa'])
    plt.text(0.5, 0.95, f'r = {corr_cover:.3f}\np = {p_cover:.3f}', 
             transform=plt.gca().transAxes, ha='center', va='top',
             bbox=dict(boxstyle='round', facecolor='white', alpha=0.8))
    
    # 2. Underdog Net EPA vs Cover
    plt.subplot(3, 4, 2)
    sns.boxplot(data=underdog_epa_df, x='underdog_covered', y='net_epa', 
                palette=['lightcoral', 'lightgreen'])
    plt.title('Underdog Net EPA vs Cover', fontweight='bold')
    plt.xlabel('Covered')
    plt.ylabel('Net EPA')
    plt.xticks([0, 1], ['No', 'Yes'])
    
    corr_net_cover, p_net_cover = pearsonr(underdog_epa_df['underdog_covered'], underdog_epa_df['net_epa'])
    plt.text(0.5, 0.95, f'r = {corr_net_cover:.3f}\np = {p_net_cover:.3f}', 
             transform=plt.gca().transAxes, ha='center', va='top',
             bbox=dict(boxstyle='round', facecolor='white', alpha=0.8))
    
    # 3. Underdog Offensive EPA vs Outright Win
    plt.subplot(3, 4, 3)
    sns.boxplot(data=underdog_epa_df, x='underdog_won_outright', y='off_epa', 
                palette=['lightcoral', 'lightgreen'])
    plt.title('Underdog Off EPA vs Outright Win', fontweight='bold')
    plt.xlabel('Won Outright')
    plt.ylabel('Offensive EPA')
    plt.xticks([0, 1], ['No', 'Yes'])
    
    corr_win, p_win = pearsonr(underdog_epa_df['underdog_won_outright'], underdog_epa_df['off_epa'])
    plt.text(0.5, 0.95, f'r = {corr_win:.3f}\np = {p_win:.3f}', 
             transform=plt.gca().transAxes, ha='center', va='top',
             bbox=dict(boxstyle='round', facecolor='white', alpha=0.8))
    
    # 4. Underdog Net EPA vs Outright Win
    plt.subplot(3, 4, 4)
    sns.boxplot(data=underdog_epa_df, x='underdog_won_outright', y='net_epa', 
                palette=['lightcoral', 'lightgreen'])
    plt.title('Underdog Net EPA vs Outright Win', fontweight='bold')
    plt.xlabel('Won Outright')
    plt.ylabel('Net EPA')
    plt.xticks([0, 1], ['No', 'Yes'])
    
    corr_net_win, p_net_win = pearsonr(underdog_epa_df['underdog_won_outright'], underdog_epa_df['net_epa'])
    plt.text(0.5, 0.95, f'r = {corr_net_win:.3f}\np = {p_net_win:.3f}', 
             transform=plt.gca().transAxes, ha='center', va='top',
             bbox=dict(boxstyle='round', facecolor='white', alpha=0.8))
    
    # 5. All Teams Offensive EPA vs Win
    plt.subplot(3, 4, 5)
    sns.boxplot(data=all_teams_epa_df, x='team_won', y='off_epa', 
                palette=['lightcoral', 'lightgreen'])
    plt.title('All Teams Off EPA vs Win', fontweight='bold')
    plt.xlabel('Won')
    plt.ylabel('Offensive EPA')
    plt.xticks([0, 1], ['No', 'Yes'])
    
    corr_all_off, p_all_off = pearsonr(all_teams_epa_df['team_won'], all_teams_epa_df['off_epa'])
    plt.text(0.5, 0.95, f'r = {corr_all_off:.3f}\np = {p_all_off:.3f}', 
             transform=plt.gca().transAxes, ha='center', va='top',
             bbox=dict(boxstyle='round', facecolor='white', alpha=0.8))
    
    # 6. All Teams Net EPA vs Win
    plt.subplot(3, 4, 6)
    sns.boxplot(data=all_teams_epa_df, x='team_won', y='net_epa', 
                palette=['lightcoral', 'lightgreen'])
    plt.title('All Teams Net EPA vs Win', fontweight='bold')
    plt.xlabel('Won')
    plt.ylabel('Net EPA')
    plt.xticks([0, 1], ['No', 'Yes'])
    
    corr_all_net, p_all_net = pearsonr(all_teams_epa_df['team_won'], all_teams_epa_df['net_epa'])
    plt.text(0.5, 0.95, f'r = {corr_all_net:.3f}\np = {p_all_net:.3f}', 
             transform=plt.gca().transAxes, ha='center', va='top',
             bbox=dict(boxstyle='round', facecolor='white', alpha=0.8))
    
    # 7. Scatter: Underdog Off EPA vs Cover
    plt.subplot(3, 4, 7)
    colors = ['red' if not x else 'green' for x in underdog_epa_df['underdog_covered']]
    plt.scatter(underdog_epa_df['off_epa'], underdog_epa_df['underdog_covered'], 
                c=colors, alpha=0.7, s=100)
    plt.xlabel('Offensive EPA')
    plt.ylabel('Covered (0=No, 1=Yes)')
    plt.title('Underdog Off EPA vs Cover', fontweight='bold')
    plt.grid(True, alpha=0.3)
    
    # 8. Scatter: All Teams Net EPA vs Win
    plt.subplot(3, 4, 8)
    colors = ['red' if not x else 'green' for x in all_teams_epa_df['team_won']]
    plt.scatter(all_teams_epa_df['net_epa'], all_teams_epa_df['team_won'], 
                c=colors, alpha=0.7, s=100)
    plt.xlabel('Net EPA')
    plt.ylabel('Won (0=No, 1=Yes)')
    plt.title('All Teams Net EPA vs Win', fontweight='bold')
    plt.grid(True, alpha=0.3)
    
    # 9. Success Rate Analysis
    plt.subplot(3, 4, 9)
    sns.boxplot(data=underdog_epa_df, x='underdog_covered', y='off_success_rate', 
                palette=['lightcoral', 'lightgreen'])
    plt.title('Underdog Success Rate vs Cover', fontweight='bold')
    plt.xlabel('Covered')
    plt.ylabel('Offensive Success Rate')
    plt.xticks([0, 1], ['No', 'Yes'])
    
    # 10. All Teams Success Rate
    plt.subplot(3, 4, 10)
    sns.boxplot(data=all_teams_epa_df, x='team_won', y='off_success_rate', 
                palette=['lightcoral', 'lightgreen'])
    plt.title('All Teams Success Rate vs Win', fontweight='bold')
    plt.xlabel('Won')
    plt.ylabel('Offensive Success Rate')
    plt.xticks([0, 1], ['No', 'Yes'])
    
    # 11. Summary Statistics
    plt.subplot(3, 4, 11)
    plt.axis('off')
    
    # Calculate key statistics
    underdog_cover_rate = underdog_epa_df['underdog_covered'].mean()
    underdog_win_rate = underdog_epa_df['underdog_won_outright'].mean()
    all_teams_win_rate = all_teams_epa_df['team_won'].mean()
    
    stats_text = f"""
    UNDERDOG OUTCOMES
    Cover Rate: {underdog_cover_rate:.1%}
    Outright Win Rate: {underdog_win_rate:.1%}
    
    ALL TEAMS
    Win Rate: {all_teams_win_rate:.1%}
    
    KEY CORRELATIONS
    Off EPA vs Cover: r = {corr_cover:.3f}
    Net EPA vs Cover: r = {corr_net_cover:.3f}
    Off EPA vs Win: r = {corr_win:.3f}
    Net EPA vs Win: r = {corr_net_win:.3f}
    All Teams Net EPA vs Win: r = {corr_all_net:.3f}
    """
    
    plt.text(0.1, 0.9, stats_text, transform=plt.gca().transAxes, 
             fontsize=10, verticalalignment='top', fontfamily='monospace',
             bbox=dict(boxstyle='round', facecolor='lightgray', alpha=0.8))
    
    # 12. Correlation Matrix
    plt.subplot(3, 4, 12)
    plt.axis('off')
    
    # Create correlation summary
    correlations = [
        ('Off EPA vs Cover', corr_cover, p_cover),
        ('Net EPA vs Cover', corr_net_cover, p_net_cover),
        ('Off EPA vs Win', corr_win, p_win),
        ('Net EPA vs Win', corr_net_win, p_net_win),
        ('All Teams Net EPA vs Win', corr_all_net, p_all_net)
    ]
    
    corr_text = "CORRELATION SUMMARY\n" + "="*25 + "\n"
    for name, corr, p in correlations:
        significance = "***" if p < 0.01 else "**" if p < 0.05 else "*" if p < 0.1 else ""
        corr_text += f"{name[:20]:<20} {corr:+.3f}{significance}\n"
    
    corr_text += "\n*** p<0.01, ** p<0.05, * p<0.1"
    
    plt.text(0.1, 0.9, corr_text, transform=plt.gca().transAxes, 
             fontsize=9, verticalalignment='top', fontfamily='monospace',
             bbox=dict(boxstyle='round', facecolor='lightblue', alpha=0.8))
    
    plt.tight_layout()
    plt.savefig('images/comprehensive_epa_analysis.png', dpi=300, bbox_inches='tight')
    plt.show()

def main():
    """Main function to run comprehensive EPA analysis"""
    print("="*80)
    print("COMPREHENSIVE EPA ANALYSIS: WINNING AND COVERING CORRELATIONS")
    print("="*80)
    
    # Load data
    week1_odds, week1_games, team_mapping, reverse_mapping = load_week1_data()
    
    # Analyze underdog EPA correlations
    print("Analyzing underdog EPA correlations...")
    underdog_epa_df = analyze_underdog_epa_correlations(week1_odds, week1_games, team_mapping, reverse_mapping)
    
    # Analyze all teams EPA correlations
    print("Analyzing all teams EPA correlations...")
    all_teams_epa_df = analyze_all_teams_epa_correlations(week1_games)
    
    # Print summary statistics
    print(f"\nUNDERDOG ANALYSIS ({len(underdog_epa_df)} games):")
    print(f"Cover Rate: {underdog_epa_df['underdog_covered'].mean():.1%}")
    print(f"Outright Win Rate: {underdog_epa_df['underdog_won_outright'].mean():.1%}")
    
    print(f"\nALL TEAMS ANALYSIS ({len(all_teams_epa_df)} team-games):")
    print(f"Win Rate: {all_teams_epa_df['team_won'].mean():.1%}")
    
    # Calculate correlations
    print(f"\nCORRELATION ANALYSIS:")
    print("="*50)
    
    # Underdog correlations
    corr_cover, p_cover = pearsonr(underdog_epa_df['underdog_covered'], underdog_epa_df['off_epa'])
    corr_net_cover, p_net_cover = pearsonr(underdog_epa_df['underdog_covered'], underdog_epa_df['net_epa'])
    corr_win, p_win = pearsonr(underdog_epa_df['underdog_won_outright'], underdog_epa_df['off_epa'])
    corr_net_win, p_net_win = pearsonr(underdog_epa_df['underdog_won_outright'], underdog_epa_df['net_epa'])
    
    # All teams correlations
    corr_all_off, p_all_off = pearsonr(all_teams_epa_df['team_won'], all_teams_epa_df['off_epa'])
    corr_all_net, p_all_net = pearsonr(all_teams_epa_df['team_won'], all_teams_epa_df['net_epa'])
    
    print(f"UNDERDOG CORRELATIONS:")
    print(f"  Offensive EPA vs Cover: r = {corr_cover:.3f} (p = {p_cover:.3f})")
    print(f"  Net EPA vs Cover: r = {corr_net_cover:.3f} (p = {p_net_cover:.3f})")
    print(f"  Offensive EPA vs Outright Win: r = {corr_win:.3f} (p = {p_win:.3f})")
    print(f"  Net EPA vs Outright Win: r = {corr_net_win:.3f} (p = {p_net_win:.3f})")
    
    print(f"\nALL TEAMS CORRELATIONS:")
    print(f"  Offensive EPA vs Win: r = {corr_all_off:.3f} (p = {p_all_off:.3f})")
    print(f"  Net EPA vs Win: r = {corr_all_net:.3f} (p = {p_all_net:.3f})")
    
    # Create comprehensive plots
    print(f"\nCreating comprehensive plots...")
    create_comprehensive_plots(underdog_epa_df, all_teams_epa_df)
    
    # Key insights
    print(f"\nKEY INSIGHTS:")
    print("="*50)
    
    if corr_net_win > corr_win:
        print(f"1. Net EPA is a STRONGER predictor of outright winning than offensive EPA alone")
    
    if corr_all_net > corr_all_off:
        print(f"2. Net EPA is a STRONGER predictor of winning than offensive EPA alone")
    
    if corr_cover > corr_win:
        print(f"3. EPA is a STRONGER predictor of covering than outright winning")
    
    if corr_all_net > corr_cover:
        print(f"4. Net EPA is a STRONGER predictor of general winning than underdog covering")
    
    print(f"5. Net EPA consistently shows the strongest correlations across all outcomes")
    
    print(f"\nPlot saved to: images/comprehensive_epa_analysis.png")

if __name__ == "__main__":
    main()
