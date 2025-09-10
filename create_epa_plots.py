#!/usr/bin/env python3
"""
Create EPA analysis plots for underdog cover predictions
"""

import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
import seaborn as sns
from scipy.stats import pearsonr

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
            
            if underdog == home_team_full:
                underdog_covered = margin > -spread
                is_home_underdog = True
            else:
                underdog_covered = margin < spread
                is_home_underdog = False
            
            results_with_odds.append({
                'game_id': game['game_id'],
                'home_team': home_team_abbr,
                'away_team': away_team_abbr,
                'favorite': favorite,
                'underdog': underdog,
                'underdog_abbr': underdog_abbr,
                'underdog_covered': underdog_covered,
                'is_home_underdog': is_home_underdog,
                'margin': margin
            })
    
    results_df = pd.DataFrame(results_with_odds)
    
    # Calculate EPA for each team in each game
    team_epa_data = []
    
    for _, result in results_df.iterrows():
        game_id = result['game_id']
        home_team = result['home_team']
        away_team = result['away_team']
        underdog_abbr = result['underdog_abbr']
        
        # Get plays for this game
        game_plays = week1_games[week1_games['game_id'] == game_id].copy()
        
        # Calculate EPA for each team
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
                
                team_epa_data.append({
                    'game_id': game_id,
                    'team': team,
                    'is_underdog': team == underdog_abbr,
                    'underdog_covered': result['underdog_covered'],
                    'is_home_underdog': result['is_home_underdog'],
                    'off_epa': off_epa,
                    'off_epa_per_play': off_epa_per_play,
                    'off_success_rate': success_rate,
                    'def_epa_allowed': def_epa_allowed,
                    'def_epa_per_play_allowed': def_epa_per_play_allowed,
                    'def_success_rate_allowed': def_success_rate_allowed,
                    'net_epa': net_epa
                })
    
    epa_df = pd.DataFrame(team_epa_data)
    
    # Focus on underdogs
    underdog_epa = epa_df[epa_df['is_underdog']].copy()
    
    return underdog_epa

def create_offensive_epa_cover_plot(underdog_epa):
    """Create plot showing offensive EPA vs cover outcome"""
    plt.figure(figsize=(12, 8))
    
    # Create box plot
    plt.subplot(2, 2, 1)
    sns.boxplot(data=underdog_epa, x='underdog_covered', y='off_epa', 
                palette=['lightcoral', 'lightgreen'])
    plt.title('Offensive EPA by Cover Outcome', fontsize=14, fontweight='bold')
    plt.xlabel('Underdog Covered')
    plt.ylabel('Offensive EPA')
    plt.xticks([0, 1], ['No', 'Yes'])
    
    # Add correlation text
    corr, p_val = pearsonr(underdog_epa['underdog_covered'], underdog_epa['off_epa'])
    plt.text(0.5, 0.95, f'r = {corr:.3f}, p = {p_val:.3f}', 
             transform=plt.gca().transAxes, ha='center', va='top',
             bbox=dict(boxstyle='round', facecolor='white', alpha=0.8))
    
    # Scatter plot
    plt.subplot(2, 2, 2)
    colors = ['red' if not x else 'green' for x in underdog_epa['underdog_covered']]
    plt.scatter(underdog_epa['off_epa'], underdog_epa['underdog_covered'], 
                c=colors, alpha=0.7, s=100)
    plt.xlabel('Offensive EPA')
    plt.ylabel('Covered (0=No, 1=Yes)')
    plt.title('Offensive EPA vs Cover Outcome', fontsize=14, fontweight='bold')
    plt.grid(True, alpha=0.3)
    
    # Add trend line
    z = np.polyfit(underdog_epa['off_epa'], underdog_epa['underdog_covered'], 1)
    p = np.poly1d(z)
    plt.plot(underdog_epa['off_epa'], p(underdog_epa['off_epa']), "r--", alpha=0.8)
    
    # Success rate analysis
    plt.subplot(2, 2, 3)
    sns.boxplot(data=underdog_epa, x='underdog_covered', y='off_success_rate', 
                palette=['lightcoral', 'lightgreen'])
    plt.title('Offensive Success Rate by Cover Outcome', fontsize=14, fontweight='bold')
    plt.xlabel('Underdog Covered')
    plt.ylabel('Offensive Success Rate')
    plt.xticks([0, 1], ['No', 'Yes'])
    
    # Net EPA analysis
    plt.subplot(2, 2, 4)
    sns.boxplot(data=underdog_epa, x='underdog_covered', y='net_epa', 
                palette=['lightcoral', 'lightgreen'])
    plt.title('Net EPA by Cover Outcome', fontsize=14, fontweight='bold')
    plt.xlabel('Underdog Covered')
    plt.ylabel('Net EPA')
    plt.xticks([0, 1], ['No', 'Yes'])
    
    plt.tight_layout()
    plt.savefig('images/offensive_epa_cover_analysis.png', dpi=300, bbox_inches='tight')
    plt.show()
    
    return corr, p_val

def create_home_away_epa_analysis(underdog_epa):
    """Create plot showing home vs away underdog EPA analysis"""
    plt.figure(figsize=(15, 10))
    
    # Home vs Away cover rates
    plt.subplot(2, 3, 1)
    home_away_cover = underdog_epa.groupby('is_home_underdog')['underdog_covered'].agg(['count', 'sum', 'mean'])
    home_away_cover.columns = ['Total', 'Covers', 'Cover_Rate']
    
    bars = plt.bar(['Away Underdogs', 'Home Underdogs'], 
                   [home_away_cover.loc[False, 'Cover_Rate'], 
                    home_away_cover.loc[True, 'Cover_Rate']],
                   color=['lightblue', 'lightgreen'])
    plt.title('Cover Rate: Home vs Away Underdogs', fontsize=14, fontweight='bold')
    plt.ylabel('Cover Rate')
    plt.ylim(0, 1)
    
    # Add percentage labels on bars
    for i, bar in enumerate(bars):
        height = bar.get_height()
        plt.text(bar.get_x() + bar.get_width()/2., height + 0.02,
                f'{height:.1%}', ha='center', va='bottom', fontweight='bold')
    
    # Add count labels
    for i, bar in enumerate(bars):
        height = bar.get_height()
        count = home_away_cover.iloc[i]['Total']
        plt.text(bar.get_x() + bar.get_width()/2., height/2,
                f'n={count}', ha='center', va='center', fontweight='bold', color='white')
    
    # Offensive EPA by home/away
    plt.subplot(2, 3, 2)
    sns.boxplot(data=underdog_epa, x='is_home_underdog', y='off_epa', 
                palette=['lightblue', 'lightgreen'])
    plt.title('Offensive EPA: Home vs Away Underdogs', fontsize=14, fontweight='bold')
    plt.xlabel('Home Underdog')
    plt.ylabel('Offensive EPA')
    plt.xticks([0, 1], ['Away', 'Home'])
    
    # Net EPA by home/away
    plt.subplot(2, 3, 3)
    sns.boxplot(data=underdog_epa, x='is_home_underdog', y='net_epa', 
                palette=['lightblue', 'lightgreen'])
    plt.title('Net EPA: Home vs Away Underdogs', fontsize=14, fontweight='bold')
    plt.xlabel('Home Underdog')
    plt.ylabel('Net EPA')
    plt.xticks([0, 1], ['Away', 'Home'])
    
    # Home underdogs: EPA vs Cover
    plt.subplot(2, 3, 4)
    home_underdogs = underdog_epa[underdog_epa['is_home_underdog']]
    colors = ['red' if not x else 'green' for x in home_underdogs['underdog_covered']]
    plt.scatter(home_underdogs['off_epa'], home_underdogs['underdog_covered'], 
                c=colors, alpha=0.7, s=100)
    plt.xlabel('Offensive EPA')
    plt.ylabel('Covered (0=No, 1=Yes)')
    plt.title('Home Underdogs: EPA vs Cover', fontsize=14, fontweight='bold')
    plt.grid(True, alpha=0.3)
    
    # Away underdogs: EPA vs Cover
    plt.subplot(2, 3, 5)
    away_underdogs = underdog_epa[~underdog_epa['is_home_underdog']]
    colors = ['red' if not x else 'green' for x in away_underdogs['underdog_covered']]
    plt.scatter(away_underdogs['off_epa'], away_underdogs['underdog_covered'], 
                c=colors, alpha=0.7, s=100)
    plt.xlabel('Offensive EPA')
    plt.ylabel('Covered (0=No, 1=Yes)')
    plt.title('Away Underdogs: EPA vs Cover', fontsize=14, fontweight='bold')
    plt.grid(True, alpha=0.3)
    
    # Summary statistics
    plt.subplot(2, 3, 6)
    plt.axis('off')
    
    # Calculate statistics
    home_cover_rate = home_underdogs['underdog_covered'].mean()
    away_cover_rate = away_underdogs['underdog_covered'].mean()
    home_avg_epa = home_underdogs['off_epa'].mean()
    away_avg_epa = away_underdogs['off_epa'].mean()
    
    stats_text = f"""
    HOME UNDERDOGS (n={len(home_underdogs)})
    Cover Rate: {home_cover_rate:.1%}
    Avg Off EPA: {home_avg_epa:+.1f}
    
    AWAY UNDERDOGS (n={len(away_underdogs)})
    Cover Rate: {away_cover_rate:.1%}
    Avg Off EPA: {away_avg_epa:+.1f}
    
    DIFFERENCE
    Cover Rate: {home_cover_rate - away_cover_rate:+.1%}
    Off EPA: {home_avg_epa - away_avg_epa:+.1f}
    """
    
    plt.text(0.1, 0.9, stats_text, transform=plt.gca().transAxes, 
             fontsize=12, verticalalignment='top', fontfamily='monospace',
             bbox=dict(boxstyle='round', facecolor='lightgray', alpha=0.8))
    
    plt.tight_layout()
    plt.savefig('images/home_away_epa_analysis.png', dpi=300, bbox_inches='tight')
    plt.show()
    
    return home_cover_rate, away_cover_rate

def main():
    """Main function to create EPA analysis plots"""
    print("Creating EPA analysis plots...")
    
    # Load data
    underdog_epa = load_week1_data()
    print(f"Loaded {len(underdog_epa)} underdog observations")
    
    # Create plots
    print("Creating offensive EPA vs cover analysis...")
    corr, p_val = create_offensive_epa_cover_plot(underdog_epa)
    
    print("Creating home vs away EPA analysis...")
    home_rate, away_rate = create_home_away_epa_analysis(underdog_epa)
    
    # Print summary
    print("\n" + "="*60)
    print("EPA ANALYSIS SUMMARY")
    print("="*60)
    print(f"Offensive EPA vs Cover Correlation: r = {corr:.3f} (p = {p_val:.3f})")
    print(f"Home Underdog Cover Rate: {home_rate:.1%}")
    print(f"Away Underdog Cover Rate: {away_rate:.1%}")
    print(f"Home Field Advantage: {home_rate - away_rate:+.1%}")
    
    print(f"\nPlots saved to:")
    print(f"- images/offensive_epa_cover_analysis.png")
    print(f"- images/home_away_epa_analysis.png")

if __name__ == "__main__":
    main()
