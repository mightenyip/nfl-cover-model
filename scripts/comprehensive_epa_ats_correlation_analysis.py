#!/usr/bin/env python3
"""
Comprehensive EPA vs ATS Correlation Analysis (Weeks 1-8)
Analyzes the correlation between EPA metrics and favorites covering the spread
"""

import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
import seaborn as sns
from scipy import stats
import warnings
warnings.filterwarnings('ignore')

def load_historical_data():
    """Load all available historical data from weeks 1-8"""
    print("=== Loading Historical Data (Weeks 1-8) ===")
    print("=" * 50)
    
    # Load EPA data - use detailed_epa_data.csv which has all 32 teams
    epa_df = pd.read_csv('detailed_epa_data.csv')
    print(f"Loaded EPA data for {len(epa_df)} teams")
    
    # Team mapping for consistency
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
    
    # Load data from master ATS trends file (contains weeks 1-7)
    try:
        master_df = pd.read_csv('data/master_ats_trends_final.csv')
        print(f"Loaded master ATS data: {len(master_df)} games")
        
        for _, row in master_df.iterrows():
            week = row['week']
            game = row['game']
            favorite = row['favorite']
            underdog = row['underdog']
            spread = row['spread_line']
            favorite_score = row['favorite_score']
            underdog_score = row['underdog_score']
            underdog_covered = row['underdog_covered']
            
            # Calculate actual margin (favorite - underdog)
            actual_margin = favorite_score - underdog_score
            margin_vs_spread = actual_margin - spread
            
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
                
                # Calculate net EPA difference
                fav_net_epa = fav_epa['net_epa_per_play'].iloc[0]
                dog_net_epa = dog_epa['net_epa_per_play'].iloc[0]
                net_epa_diff = fav_net_epa - dog_net_epa
                
                all_games.append({
                    'week': week,
                    'game': game,
                    'favorite': favorite,
                    'underdog': underdog,
                    'spread': spread,
                    'actual_margin': actual_margin,
                    'margin_vs_spread': margin_vs_spread,
                    'underdog_covered': underdog_covered,
                    'favorite_covered': not underdog_covered,
                    'fav_off_epa': fav_off,
                    'fav_def_epa': fav_def,
                    'dog_off_epa': dog_off,
                    'dog_def_epa': dog_def,
                    'fav_matchup_epa': fav_matchup_epa,
                    'dog_matchup_epa': dog_matchup_epa,
                    'matchup_epa_diff': matchup_epa_diff,
                    'fav_net_epa': fav_net_epa,
                    'dog_net_epa': dog_net_epa,
                    'net_epa_diff': net_epa_diff
                })
        
        print(f"Processed {len([g for g in all_games if g['week'] <= 7])} games from Weeks 1-7")
    except Exception as e:
        print(f"Error loading master ATS data: {e}")
    
    # Load Week 8 data separately
    try:
        week8_df = pd.read_csv('data/week8_ats_results.csv')
        print(f"Loaded Week 8: {len(week8_df)} games")
        
        for _, row in week8_df.iterrows():
            if pd.isna(row['game']) or row['game'] == '':
                continue
                
            game = row['game']
            favorite = row['favorite']
            underdog = row['underdog']
            spread = row['spread']
            favorite_score = row['favorite_score']
            underdog_score = row['underdog_score']
            underdog_covered = row['underdog_covered']
            
            # Calculate actual margin (favorite - underdog)
            actual_margin = favorite_score - underdog_score
            margin_vs_spread = actual_margin - spread
            
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
                
                # Calculate net EPA difference
                fav_net_epa = fav_epa['net_epa_per_play'].iloc[0]
                dog_net_epa = dog_epa['net_epa_per_play'].iloc[0]
                net_epa_diff = fav_net_epa - dog_net_epa
                
                all_games.append({
                    'week': 8,
                    'game': game,
                    'favorite': favorite,
                    'underdog': underdog,
                    'spread': spread,
                    'actual_margin': actual_margin,
                    'margin_vs_spread': margin_vs_spread,
                    'underdog_covered': underdog_covered,
                    'favorite_covered': not underdog_covered,
                    'fav_off_epa': fav_off,
                    'fav_def_epa': fav_def,
                    'dog_off_epa': dog_off,
                    'dog_def_epa': dog_def,
                    'fav_matchup_epa': fav_matchup_epa,
                    'dog_matchup_epa': dog_matchup_epa,
                    'matchup_epa_diff': matchup_epa_diff,
                    'fav_net_epa': fav_net_epa,
                    'dog_net_epa': dog_net_epa,
                    'net_epa_diff': net_epa_diff
                })
        
        print(f"Processed {len([g for g in all_games if g['week'] == 8])} games from Week 8")
    except Exception as e:
        print(f"Error loading Week 8 data: {e}")
    
    print(f"Total games processed: {len(all_games)}")
    return pd.DataFrame(all_games)

def analyze_correlations(df):
    """Analyze various EPA correlations with ATS performance"""
    print("\n=== EPA vs ATS Correlation Analysis ===")
    print("=" * 60)
    
    if len(df) < 10:
        print("❌ Insufficient data for correlation analysis")
        return None
    
    # Calculate various correlations
    correlations = {}
    
    # 1. Matchup EPA difference vs margin vs spread
    correlations['matchup_epa_diff'] = df['matchup_epa_diff'].corr(df['margin_vs_spread'])
    
    # 2. Net EPA difference vs margin vs spread
    correlations['net_epa_diff'] = df['net_epa_diff'].corr(df['margin_vs_spread'])
    
    # 3. Favorite offensive EPA vs margin vs spread
    correlations['fav_off_epa'] = df['fav_off_epa'].corr(df['margin_vs_spread'])
    
    # 4. Underdog defensive EPA vs margin vs spread
    correlations['dog_def_epa'] = df['dog_def_epa'].corr(df['margin_vs_spread'])
    
    # 5. Matchup EPA difference vs favorite cover rate
    correlations['matchup_epa_vs_cover'] = df['matchup_epa_diff'].corr(df['favorite_covered'].astype(int))
    
    print("Correlation Results:")
    print("-" * 30)
    for metric, corr in correlations.items():
        print(f"{metric:25s}: {corr:6.3f}")
    
    print()
    
    # Statistical significance tests
    print("Statistical Significance Tests:")
    print("-" * 35)
    
    for metric in ['matchup_epa_diff', 'net_epa_diff', 'fav_off_epa', 'dog_def_epa']:
        if metric in ['matchup_epa_diff', 'net_epa_diff', 'fav_off_epa', 'dog_def_epa']:
            t_stat, p_value = stats.pearsonr(df[metric], df['margin_vs_spread'])
        else:
            t_stat, p_value = stats.pearsonr(df[metric], df['favorite_covered'].astype(int))
        
        significance = "✅ Significant" if p_value < 0.05 else "⚠️  Not Significant"
        print(f"{metric:25s}: p={p_value:.3f} {significance}")
    
    print()
    
    # Interpretation
    print("Interpretation:")
    print("-" * 15)
    
    matchup_corr = correlations['matchup_epa_diff']
    if matchup_corr > 0.3:
        print("✅ STRONG POSITIVE CORRELATION for Matchup EPA")
        print("   Favorites with higher matchup EPA advantages tend to outperform spreads")
    elif matchup_corr > 0.1:
        print("✅ MODERATE POSITIVE CORRELATION for Matchup EPA")
        print("   Some relationship between matchup EPA and spread performance")
    elif matchup_corr > -0.1:
        print("⚠️  WEAK CORRELATION for Matchup EPA")
        print("   Little relationship between matchup EPA and spread performance")
    elif matchup_corr > -0.3:
        print("⚠️  MODERATE NEGATIVE CORRELATION for Matchup EPA")
        print("   Favorites with matchup advantages tend to underperform spreads")
    else:
        print("❌ STRONG NEGATIVE CORRELATION for Matchup EPA")
        print("   Market may be overpricing matchup advantages")
    
    return correlations

def analyze_by_week(df):
    """Analyze correlations by individual week"""
    print("\n=== Week-by-Week Analysis ===")
    print("=" * 30)
    
    week_correlations = []
    
    for week in sorted(df['week'].unique()):
        week_data = df[df['week'] == week]
        if len(week_data) < 3:
            continue
            
        correlation = week_data['matchup_epa_diff'].corr(week_data['margin_vs_spread'])
        favorite_cover_rate = week_data['favorite_covered'].mean()
        
        week_correlations.append({
            'week': week,
            'games': len(week_data),
            'correlation': correlation,
            'favorite_cover_rate': favorite_cover_rate
        })
        
        print(f"Week {week:2d}: {len(week_data):2d} games, "
              f"Correlation: {correlation:6.3f}, "
              f"Favorite Cover Rate: {favorite_cover_rate:.1%}")
    
    print()
    print("Week-by-Week Summary:")
    print("-" * 20)
    
    strong_weeks = [w for w in week_correlations if abs(w['correlation']) > 0.3]
    moderate_weeks = [w for w in week_correlations if 0.1 < abs(w['correlation']) <= 0.3]
    weak_weeks = [w for w in week_correlations if abs(w['correlation']) <= 0.1]
    
    print(f"Strong correlation weeks (|r| > 0.3): {len(strong_weeks)}")
    print(f"Moderate correlation weeks (0.1 < |r| <= 0.3): {len(moderate_weeks)}")
    print(f"Weak correlation weeks (|r| <= 0.1): {len(weak_weeks)}")
    
    return week_correlations

def create_visualizations(df, correlations):
    """Create visualizations for the analysis"""
    print("\n=== Creating Visualizations ===")
    print("=" * 30)
    
    # Set up the plotting style
    plt.style.use('default')
    sns.set_palette("husl")
    
    # Create figure with subplots
    fig, axes = plt.subplots(2, 2, figsize=(15, 12))
    fig.suptitle('EPA vs ATS Performance Analysis (Weeks 1-8)', fontsize=16, fontweight='bold')
    
    # 1. Matchup EPA Difference vs Margin vs Spread
    ax1 = axes[0, 0]
    ax1.scatter(df['matchup_epa_diff'], df['margin_vs_spread'], alpha=0.7, s=60)
    ax1.axhline(y=0, color='red', linestyle='--', alpha=0.5)
    ax1.axvline(x=0, color='red', linestyle='--', alpha=0.5)
    ax1.set_xlabel('Matchup EPA Difference (Favorite - Underdog)')
    ax1.set_ylabel('Margin vs Spread')
    ax1.set_title(f'Matchup EPA vs Margin vs Spread\n(r = {correlations["matchup_epa_diff"]:.3f})')
    
    # Add trend line
    z = np.polyfit(df['matchup_epa_diff'], df['margin_vs_spread'], 1)
    p = np.poly1d(z)
    ax1.plot(df['matchup_epa_diff'], p(df['matchup_epa_diff']), "r--", alpha=0.8)
    
    # 2. Net EPA Difference vs Margin vs Spread
    ax2 = axes[0, 1]
    ax2.scatter(df['net_epa_diff'], df['margin_vs_spread'], alpha=0.7, s=60, color='orange')
    ax2.axhline(y=0, color='red', linestyle='--', alpha=0.5)
    ax2.axvline(x=0, color='red', linestyle='--', alpha=0.5)
    ax2.set_xlabel('Net EPA Difference (Favorite - Underdog)')
    ax2.set_ylabel('Margin vs Spread')
    ax2.set_title(f'Net EPA vs Margin vs Spread\n(r = {correlations["net_epa_diff"]:.3f})')
    
    # Add trend line
    z = np.polyfit(df['net_epa_diff'], df['margin_vs_spread'], 1)
    p = np.poly1d(z)
    ax2.plot(df['net_epa_diff'], p(df['net_epa_diff']), "r--", alpha=0.8)
    
    # 3. Week-by-week correlation
    ax3 = axes[1, 0]
    weeks = sorted(df['week'].unique())
    week_corrs = []
    for week in weeks:
        week_data = df[df['week'] == week]
        if len(week_data) >= 3:
            corr = week_data['matchup_epa_diff'].corr(week_data['margin_vs_spread'])
            week_corrs.append(corr)
        else:
            week_corrs.append(np.nan)
    
    ax3.bar(weeks, week_corrs, alpha=0.7, color='green')
    ax3.axhline(y=0, color='red', linestyle='--', alpha=0.5)
    ax3.set_xlabel('Week')
    ax3.set_ylabel('Correlation (Matchup EPA vs Margin vs Spread)')
    ax3.set_title('Week-by-Week Correlation')
    ax3.set_xticks(weeks)
    
    # 4. Favorite cover rate by matchup EPA advantage
    ax4 = axes[1, 1]
    
    # Create bins for matchup EPA difference
    df['epa_bin'] = pd.cut(df['matchup_epa_diff'], bins=5, labels=['Very Low', 'Low', 'Medium', 'High', 'Very High'])
    cover_rates = df.groupby('epa_bin')['favorite_covered'].mean()
    
    ax4.bar(range(len(cover_rates)), cover_rates.values, alpha=0.7, color='purple')
    ax4.set_xlabel('Matchup EPA Advantage Level')
    ax4.set_ylabel('Favorite Cover Rate')
    ax4.set_title('Favorite Cover Rate by EPA Advantage')
    ax4.set_xticks(range(len(cover_rates)))
    ax4.set_xticklabels(cover_rates.index, rotation=45)
    ax4.axhline(y=0.5, color='red', linestyle='--', alpha=0.5, label='50% Baseline')
    ax4.legend()
    
    plt.tight_layout()
    
    # Save the plot
    output_path = 'images/comprehensive_epa_ats_analysis.png'
    plt.savefig(output_path, dpi=300, bbox_inches='tight')
    print(f"✅ Visualization saved to: {output_path}")
    
    plt.show()

def generate_summary_report(df, correlations, week_correlations):
    """Generate a comprehensive summary report"""
    print("\n=== COMPREHENSIVE EPA vs ATS ANALYSIS REPORT ===")
    print("=" * 60)
    
    total_games = len(df)
    favorite_cover_rate = df['favorite_covered'].mean()
    
    print(f"Analysis Period: Weeks 1-8")
    print(f"Total Games Analyzed: {total_games}")
    print(f"Overall Favorite Cover Rate: {favorite_cover_rate:.1%}")
    print()
    
    print("KEY CORRELATION FINDINGS:")
    print("-" * 25)
    print(f"Matchup EPA Difference vs Margin vs Spread: {correlations['matchup_epa_diff']:.3f}")
    print(f"Net EPA Difference vs Margin vs Spread: {correlations['net_epa_diff']:.3f}")
    print(f"Favorite Offensive EPA vs Margin vs Spread: {correlations['fav_off_epa']:.3f}")
    print(f"Underdog Defensive EPA vs Margin vs Spread: {correlations['dog_def_epa']:.3f}")
    print()
    
    # Week-by-week summary
    strong_weeks = [w for w in week_correlations if abs(w['correlation']) > 0.3]
    moderate_weeks = [w for w in week_correlations if 0.1 < abs(w['correlation']) <= 0.3]
    weak_weeks = [w for w in week_correlations if abs(w['correlation']) <= 0.1]
    
    print("WEEK-BY-WEEK PERFORMANCE:")
    print("-" * 25)
    print(f"Strong correlation weeks (|r| > 0.3): {len(strong_weeks)}")
    for week in strong_weeks:
        print(f"  Week {week['week']}: r = {week['correlation']:.3f} ({week['games']} games)")
    
    print(f"Moderate correlation weeks (0.1 < |r| <= 0.3): {len(moderate_weeks)}")
    for week in moderate_weeks:
        print(f"  Week {week['week']}: r = {week['correlation']:.3f} ({week['games']} games)")
    
    print(f"Weak correlation weeks (|r| <= 0.1): {len(weak_weeks)}")
    for week in weak_weeks:
        print(f"  Week {week['week']}: r = {week['correlation']:.3f} ({week['games']} games)")
    
    print()
    
    # Top and bottom games
    print("TOP 5 GAMES BY MATCHUP EPA ADVANTAGE:")
    print("-" * 40)
    top_games = df.nlargest(5, 'matchup_epa_diff')
    for _, row in top_games.iterrows():
        print(f"{row['game']}: EPA Diff = {row['matchup_epa_diff']:.3f}, "
              f"Margin vs Spread = {row['margin_vs_spread']:+.1f}, "
              f"Covered = {row['favorite_covered']}")
    
    print()
    print("BOTTOM 5 GAMES BY MATCHUP EPA ADVANTAGE:")
    print("-" * 42)
    bottom_games = df.nsmallest(5, 'matchup_epa_diff')
    for _, row in bottom_games.iterrows():
        print(f"{row['game']}: EPA Diff = {row['matchup_epa_diff']:.3f}, "
              f"Margin vs Spread = {row['margin_vs_spread']:+.1f}, "
              f"Covered = {row['favorite_covered']}")
    
    print()
    
    # Conclusions
    print("CONCLUSIONS:")
    print("-" * 12)
    
    matchup_corr = correlations['matchup_epa_diff']
    if abs(matchup_corr) > 0.3:
        strength = "STRONG"
    elif abs(matchup_corr) > 0.1:
        strength = "MODERATE"
    else:
        strength = "WEAK"
    
    direction = "POSITIVE" if matchup_corr > 0 else "NEGATIVE"
    
    print(f"1. EPA shows {strength} {direction} correlation with spread performance")
    
    if matchup_corr > 0.2:
        print("2. Favorites with EPA advantages tend to outperform their spreads")
        print("3. EPA-based models can be effective for spread prediction")
    elif matchup_corr < -0.2:
        print("2. Favorites with EPA advantages tend to underperform their spreads")
        print("3. Market may be overpricing EPA-based advantages")
    else:
        print("2. EPA shows limited predictive power for spread performance")
        print("3. Other factors may be more important than EPA alone")
    
    print(f"4. Overall favorite cover rate: {favorite_cover_rate:.1%}")
    print(f"5. Analysis based on {total_games} games across 8 weeks")

def main():
    """Main analysis function"""
    print("=== Comprehensive EPA vs ATS Correlation Analysis ===")
    print("Analyzing Weeks 1-8 data")
    print("=" * 60)
    
    # Load historical data
    df = load_historical_data()
    
    if df.empty:
        print("❌ No historical data available")
        return
    
    # Analyze correlations
    correlations = analyze_correlations(df)
    
    if correlations is None:
        print("❌ Insufficient data for correlation analysis")
        return
    
    # Analyze by week
    week_correlations = analyze_by_week(df)
    
    # Create visualizations
    create_visualizations(df, correlations)
    
    # Generate summary report
    generate_summary_report(df, correlations, week_correlations)
    
    # Save detailed results
    output_path = 'data/comprehensive_epa_ats_analysis.csv'
    df.to_csv(output_path, index=False)
    print(f"\n✅ Detailed analysis saved to: {output_path}")

if __name__ == "__main__":
    main()
