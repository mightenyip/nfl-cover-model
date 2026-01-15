#!/usr/bin/env python3
"""
Weighted Run/Pass Matchup EPA Analysis
Incorporates team run/pass ratios to weight the importance of run vs pass EPA
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
    
    # Load EPA data with run/pass breakdown
    epa_df = pd.read_csv('data/epa/source/comprehensive_epa_data_week8.csv')
    print(f"Loaded EPA data for {len(epa_df)} teams")
    
    # Load run/pass ratio data (source: https://www.fftoday.com/stats/25_run_pass_ratios.html)
    ratio_df = pd.read_csv('data/team_metrics/team_run_pass_ratios_2025.csv')
    print(f"Loaded run/pass ratios for {len(ratio_df)} teams")
    print("Note: Run/pass ratio data sourced from https://www.fftoday.com/stats/25_run_pass_ratios.html")
    
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
        master_df = pd.read_csv('data/ats_trends/master_ats_trends_final.csv')
        print(f"Loaded master ATS data: {len(master_df)} games")
        
        processed_count = 0
        skipped_count = 0
        
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
            
            # Get run/pass ratio data
            fav_ratio = ratio_df[ratio_df['team_abbr'] == fav_abbr]
            dog_ratio = ratio_df[ratio_df['team_abbr'] == dog_abbr]
            
            if not fav_epa.empty and not dog_epa.empty and not fav_ratio.empty and not dog_ratio.empty:
                # Overall EPA metrics
                fav_off = fav_epa['epa_off_per_play'].iloc[0]
                fav_def = fav_epa['epa_def_allowed_per_play'].iloc[0]
                dog_off = dog_epa['epa_off_per_play'].iloc[0]
                dog_def = dog_epa['epa_def_allowed_per_play'].iloc[0]
                
                # Run and Pass specific EPA metrics
                fav_off_pass = fav_epa['epa_off_per_pass'].iloc[0]
                fav_off_rush = fav_epa['epa_off_per_rush'].iloc[0]
                fav_def_pass = fav_epa['epa_def_allowed_per_pass'].iloc[0]
                fav_def_rush = fav_epa['epa_def_allowed_per_rush'].iloc[0]
                
                dog_off_pass = dog_epa['epa_off_per_pass'].iloc[0]
                dog_off_rush = dog_epa['epa_off_per_rush'].iloc[0]
                dog_def_pass = dog_epa['epa_def_allowed_per_pass'].iloc[0]
                dog_def_rush = dog_epa['epa_def_allowed_per_rush'].iloc[0]
                
                # Get run/pass ratios
                fav_run_pct = fav_ratio['run_pct'].iloc[0] / 100  # Convert percentage to decimal
                fav_pass_pct = fav_ratio['pass_pct'].iloc[0] / 100
                dog_run_pct = dog_ratio['run_pct'].iloc[0] / 100
                dog_pass_pct = dog_ratio['pass_pct'].iloc[0] / 100
                
                # Calculate matchup EPA differences
                # Overall matchup EPA
                fav_matchup_epa = fav_off + dog_def
                dog_matchup_epa = dog_off + fav_def
                matchup_epa_diff = fav_matchup_epa - dog_matchup_epa
                
                # Pass matchup EPA
                fav_matchup_pass_epa = fav_off_pass + dog_def_pass
                dog_matchup_pass_epa = dog_off_pass + fav_def_pass
                matchup_pass_epa_diff = fav_matchup_pass_epa - dog_matchup_pass_epa
                
                # Rush matchup EPA
                fav_matchup_rush_epa = fav_off_rush + dog_def_rush
                dog_matchup_rush_epa = dog_off_rush + fav_def_rush
                matchup_rush_epa_diff = fav_matchup_rush_epa - dog_matchup_rush_epa
                
                # Combined Run-Pass Matchup EPA (simple average)
                matchup_rp_epa_diff = (matchup_pass_epa_diff + matchup_rush_epa_diff) / 2
                
                # WEIGHTED Run-Pass Matchup EPA (weighted by actual usage)
                # Weight by the average run/pass ratio of both teams
                avg_run_pct = (fav_run_pct + dog_run_pct) / 2
                avg_pass_pct = (fav_pass_pct + dog_pass_pct) / 2
                
                matchup_weighted_rp_epa_diff = (matchup_pass_epa_diff * avg_pass_pct + 
                                               matchup_rush_epa_diff * avg_run_pct)
                
                # FAVORITE-SPECIFIC Weighted EPA (weight by favorite's tendencies)
                matchup_fav_weighted_epa_diff = (matchup_pass_epa_diff * fav_pass_pct + 
                                                matchup_rush_epa_diff * fav_run_pct)
                
                # UNDERDOG-SPECIFIC Weighted EPA (weight by underdog's tendencies)
                matchup_dog_weighted_epa_diff = (matchup_pass_epa_diff * dog_pass_pct + 
                                                matchup_rush_epa_diff * dog_run_pct)
                
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
                    
                    # Overall EPA
                    'fav_off_epa': fav_off,
                    'fav_def_epa': fav_def,
                    'dog_off_epa': dog_off,
                    'dog_def_epa': dog_def,
                    'matchup_epa_diff': matchup_epa_diff,
                    'net_epa_diff': net_epa_diff,
                    
                    # Pass-specific EPA
                    'fav_off_pass_epa': fav_off_pass,
                    'fav_def_pass_epa': fav_def_pass,
                    'dog_off_pass_epa': dog_off_pass,
                    'dog_def_pass_epa': dog_def_pass,
                    'matchup_pass_epa_diff': matchup_pass_epa_diff,
                    
                    # Rush-specific EPA
                    'fav_off_rush_epa': fav_off_rush,
                    'fav_def_rush_epa': fav_def_rush,
                    'dog_off_rush_epa': dog_off_rush,
                    'dog_def_rush_epa': dog_def_rush,
                    'matchup_rush_epa_diff': matchup_rush_epa_diff,
                    
                    # Combined Run-Pass EPA
                    'matchup_rp_epa_diff': matchup_rp_epa_diff,
                    
                    # NEW: Weighted Run-Pass EPA
                    'matchup_weighted_rp_epa_diff': matchup_weighted_rp_epa_diff,
                    'matchup_fav_weighted_epa_diff': matchup_fav_weighted_epa_diff,
                    'matchup_dog_weighted_epa_diff': matchup_dog_weighted_epa_diff,
                    
                    # Run/Pass ratios
                    'fav_run_pct': fav_run_pct,
                    'fav_pass_pct': fav_pass_pct,
                    'dog_run_pct': dog_run_pct,
                    'dog_pass_pct': dog_pass_pct,
                    'avg_run_pct': avg_run_pct,
                    'avg_pass_pct': avg_pass_pct
                })
                processed_count += 1
            else:
                skipped_count += 1
                missing_data = []
                if fav_epa.empty:
                    missing_data.append(f"EPA for {favorite}")
                if dog_epa.empty:
                    missing_data.append(f"EPA for {underdog}")
                if fav_ratio.empty:
                    missing_data.append(f"Ratios for {favorite}")
                if dog_ratio.empty:
                    missing_data.append(f"Ratios for {underdog}")
                print(f"Missing data: {', '.join(missing_data)}")
        
        print(f"Processed {processed_count} games from Weeks 1-7")
        print(f"Skipped {skipped_count} games due to missing data")
    except Exception as e:
        print(f"Error loading master ATS data: {e}")
    
    # Load Week 8 data separately
    try:
        week8_df = pd.read_csv('data/ats_results/week8/week8_ats_results.csv')
        print(f"Loaded Week 8: {len(week8_df)} games")
        
        processed_count = 0
        skipped_count = 0
        
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
            
            # Get run/pass ratio data
            fav_ratio = ratio_df[ratio_df['team_abbr'] == fav_abbr]
            dog_ratio = ratio_df[ratio_df['team_abbr'] == dog_abbr]
            
            if not fav_epa.empty and not dog_epa.empty and not fav_ratio.empty and not dog_ratio.empty:
                # Overall EPA metrics
                fav_off = fav_epa['epa_off_per_play'].iloc[0]
                fav_def = fav_epa['epa_def_allowed_per_play'].iloc[0]
                dog_off = dog_epa['epa_off_per_play'].iloc[0]
                dog_def = dog_epa['epa_def_allowed_per_play'].iloc[0]
                
                # Run and Pass specific EPA metrics
                fav_off_pass = fav_epa['epa_off_per_pass'].iloc[0]
                fav_off_rush = fav_epa['epa_off_per_rush'].iloc[0]
                fav_def_pass = fav_epa['epa_def_allowed_per_pass'].iloc[0]
                fav_def_rush = fav_epa['epa_def_allowed_per_rush'].iloc[0]
                
                dog_off_pass = dog_epa['epa_off_per_pass'].iloc[0]
                dog_off_rush = dog_epa['epa_off_per_rush'].iloc[0]
                dog_def_pass = dog_epa['epa_def_allowed_per_pass'].iloc[0]
                dog_def_rush = dog_epa['epa_def_allowed_per_rush'].iloc[0]
                
                # Get run/pass ratios
                fav_run_pct = fav_ratio['run_pct'].iloc[0] / 100  # Convert percentage to decimal
                fav_pass_pct = fav_ratio['pass_pct'].iloc[0] / 100
                dog_run_pct = dog_ratio['run_pct'].iloc[0] / 100
                dog_pass_pct = dog_ratio['pass_pct'].iloc[0] / 100
                
                # Calculate matchup EPA differences
                # Overall matchup EPA
                fav_matchup_epa = fav_off + dog_def
                dog_matchup_epa = dog_off + fav_def
                matchup_epa_diff = fav_matchup_epa - dog_matchup_epa
                
                # Pass matchup EPA
                fav_matchup_pass_epa = fav_off_pass + dog_def_pass
                dog_matchup_pass_epa = dog_off_pass + fav_def_pass
                matchup_pass_epa_diff = fav_matchup_pass_epa - dog_matchup_pass_epa
                
                # Rush matchup EPA
                fav_matchup_rush_epa = fav_off_rush + dog_def_rush
                dog_matchup_rush_epa = dog_off_rush + fav_def_rush
                matchup_rush_epa_diff = fav_matchup_rush_epa - dog_matchup_rush_epa
                
                # Combined Run-Pass Matchup EPA (simple average)
                matchup_rp_epa_diff = (matchup_pass_epa_diff + matchup_rush_epa_diff) / 2
                
                # WEIGHTED Run-Pass Matchup EPA (weighted by actual usage)
                # Weight by the average run/pass ratio of both teams
                avg_run_pct = (fav_run_pct + dog_run_pct) / 2
                avg_pass_pct = (fav_pass_pct + dog_pass_pct) / 2
                
                matchup_weighted_rp_epa_diff = (matchup_pass_epa_diff * avg_pass_pct + 
                                               matchup_rush_epa_diff * avg_run_pct)
                
                # FAVORITE-SPECIFIC Weighted EPA (weight by favorite's tendencies)
                matchup_fav_weighted_epa_diff = (matchup_pass_epa_diff * fav_pass_pct + 
                                                matchup_rush_epa_diff * fav_run_pct)
                
                # UNDERDOG-SPECIFIC Weighted EPA (weight by underdog's tendencies)
                matchup_dog_weighted_epa_diff = (matchup_pass_epa_diff * dog_pass_pct + 
                                                matchup_rush_epa_diff * dog_run_pct)
                
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
                    
                    # Overall EPA
                    'fav_off_epa': fav_off,
                    'fav_def_epa': fav_def,
                    'dog_off_epa': dog_off,
                    'dog_def_epa': dog_def,
                    'matchup_epa_diff': matchup_epa_diff,
                    'net_epa_diff': net_epa_diff,
                    
                    # Pass-specific EPA
                    'fav_off_pass_epa': fav_off_pass,
                    'fav_def_pass_epa': fav_def_pass,
                    'dog_off_pass_epa': dog_off_pass,
                    'dog_def_pass_epa': dog_def_pass,
                    'matchup_pass_epa_diff': matchup_pass_epa_diff,
                    
                    # Rush-specific EPA
                    'fav_off_rush_epa': fav_off_rush,
                    'fav_def_rush_epa': fav_def_rush,
                    'dog_off_rush_epa': dog_off_rush,
                    'dog_def_rush_epa': dog_def_rush,
                    'matchup_rush_epa_diff': matchup_rush_epa_diff,
                    
                    # Combined Run-Pass EPA
                    'matchup_rp_epa_diff': matchup_rp_epa_diff,
                    
                    # NEW: Weighted Run-Pass EPA
                    'matchup_weighted_rp_epa_diff': matchup_weighted_rp_epa_diff,
                    'matchup_fav_weighted_epa_diff': matchup_fav_weighted_epa_diff,
                    'matchup_dog_weighted_epa_diff': matchup_dog_weighted_epa_diff,
                    
                    # Run/Pass ratios
                    'fav_run_pct': fav_run_pct,
                    'fav_pass_pct': fav_pass_pct,
                    'dog_run_pct': dog_run_pct,
                    'dog_pass_pct': dog_pass_pct,
                    'avg_run_pct': avg_run_pct,
                    'avg_pass_pct': avg_pass_pct
                })
                processed_count += 1
            else:
                skipped_count += 1
                missing_data = []
                if fav_epa.empty:
                    missing_data.append(f"EPA for {favorite}")
                if dog_epa.empty:
                    missing_data.append(f"EPA for {underdog}")
                if fav_ratio.empty:
                    missing_data.append(f"Ratios for {favorite}")
                if dog_ratio.empty:
                    missing_data.append(f"Ratios for {underdog}")
                print(f"Missing data: {', '.join(missing_data)}")
        
        print(f"Processed {processed_count} games from Week 8")
        print(f"Skipped {skipped_count} games due to missing data")
    except Exception as e:
        print(f"Error loading Week 8 data: {e}")
    
    print(f"Total games processed: {len(all_games)}")
    return pd.DataFrame(all_games)

def analyze_correlations(df):
    """Analyze various EPA correlations with ATS performance"""
    print("\n=== Weighted Run/Pass Matchup EPA vs ATS Correlation Analysis ===")
    print("=" * 80)
    
    if len(df) < 10:
        print("❌ Insufficient data for correlation analysis")
        return None
    
    # Calculate various correlations
    correlations = {}
    
    # Overall EPA correlations
    correlations['matchup_epa_diff'] = df['matchup_epa_diff'].corr(df['margin_vs_spread'])
    correlations['net_epa_diff'] = df['net_epa_diff'].corr(df['margin_vs_spread'])
    
    # Pass-specific correlations
    correlations['matchup_pass_epa_diff'] = df['matchup_pass_epa_diff'].corr(df['margin_vs_spread'])
    correlations['fav_off_pass_epa'] = df['fav_off_pass_epa'].corr(df['margin_vs_spread'])
    correlations['dog_def_pass_epa'] = df['dog_def_pass_epa'].corr(df['margin_vs_spread'])
    
    # Rush-specific correlations
    correlations['matchup_rush_epa_diff'] = df['matchup_rush_epa_diff'].corr(df['margin_vs_spread'])
    correlations['fav_off_rush_epa'] = df['fav_off_rush_epa'].corr(df['margin_vs_spread'])
    correlations['dog_def_rush_epa'] = df['dog_def_rush_epa'].corr(df['margin_vs_spread'])
    
    # Combined Run-Pass EPA
    correlations['matchup_rp_epa_diff'] = df['matchup_rp_epa_diff'].corr(df['margin_vs_spread'])
    
    # NEW: Weighted Run-Pass EPA
    correlations['matchup_weighted_rp_epa_diff'] = df['matchup_weighted_rp_epa_diff'].corr(df['margin_vs_spread'])
    correlations['matchup_fav_weighted_epa_diff'] = df['matchup_fav_weighted_epa_diff'].corr(df['margin_vs_spread'])
    correlations['matchup_dog_weighted_epa_diff'] = df['matchup_dog_weighted_epa_diff'].corr(df['margin_vs_spread'])
    
    # Cover rate correlations
    correlations['matchup_epa_vs_cover'] = df['matchup_epa_diff'].corr(df['favorite_covered'].astype(int))
    correlations['matchup_weighted_rp_epa_vs_cover'] = df['matchup_weighted_rp_epa_diff'].corr(df['favorite_covered'].astype(int))
    
    print("Correlation Results:")
    print("-" * 60)
    print("OVERALL EPA:")
    print(f"  Matchup EPA Diff:                    {correlations['matchup_epa_diff']:6.3f}")
    print(f"  Net EPA Diff:                        {correlations['net_epa_diff']:6.3f}")
    print()
    print("PASS-SPECIFIC EPA:")
    print(f"  Matchup Pass EPA Diff:               {correlations['matchup_pass_epa_diff']:6.3f}")
    print(f"  Fav Off Pass EPA:                    {correlations['fav_off_pass_epa']:6.3f}")
    print(f"  Dog Def Pass EPA:                    {correlations['dog_def_pass_epa']:6.3f}")
    print()
    print("RUSH-SPECIFIC EPA:")
    print(f"  Matchup Rush EPA Diff:               {correlations['matchup_rush_epa_diff']:6.3f}")
    print(f"  Fav Off Rush EPA:                    {correlations['fav_off_rush_epa']:6.3f}")
    print(f"  Dog Def Rush EPA:                    {correlations['dog_def_rush_epa']:6.3f}")
    print()
    print("COMBINED RUN-PASS EPA:")
    print(f"  Simple Average RP EPA:               {correlations['matchup_rp_epa_diff']:6.3f}")
    print()
    print("WEIGHTED RUN-PASS EPA (NEW):")
    print(f"  Average Weighted RP EPA:             {correlations['matchup_weighted_rp_epa_diff']:6.3f}")
    print(f"  Favorite-Weighted RP EPA:            {correlations['matchup_fav_weighted_epa_diff']:6.3f}")
    print(f"  Underdog-Weighted RP EPA:            {correlations['matchup_dog_weighted_epa_diff']:6.3f}")
    print()
    print("COVER RATE CORRELATIONS:")
    print(f"  Matchup EPA vs Cover:                {correlations['matchup_epa_vs_cover']:6.3f}")
    print(f"  Weighted RP EPA vs Cover:            {correlations['matchup_weighted_rp_epa_vs_cover']:6.3f}")
    
    print()
    
    # Statistical significance tests
    print("Statistical Significance Tests:")
    print("-" * 50)
    
    significance_tests = [
        ('matchup_epa_diff', 'margin_vs_spread'),
        ('matchup_pass_epa_diff', 'margin_vs_spread'),
        ('matchup_rush_epa_diff', 'margin_vs_spread'),
        ('matchup_rp_epa_diff', 'margin_vs_spread'),
        ('matchup_weighted_rp_epa_diff', 'margin_vs_spread'),
        ('matchup_fav_weighted_epa_diff', 'margin_vs_spread'),
        ('matchup_dog_weighted_epa_diff', 'margin_vs_spread')
    ]
    
    for metric, target in significance_tests:
        t_stat, p_value = stats.pearsonr(df[metric], df[target])
        significance = "✅ Significant" if p_value < 0.05 else "⚠️  Not Significant"
        print(f"{metric:35s}: p={p_value:.3f} {significance}")
    
    print()
    
    # Interpretation
    print("Interpretation:")
    print("-" * 15)
    
    # Find the best performing metric
    margin_correlations = {
        'Overall Matchup EPA': correlations['matchup_epa_diff'],
        'Pass Matchup EPA': correlations['matchup_pass_epa_diff'],
        'Rush Matchup EPA': correlations['matchup_rush_epa_diff'],
        'Simple Average RP EPA': correlations['matchup_rp_epa_diff'],
        'Average Weighted RP EPA': correlations['matchup_weighted_rp_epa_diff'],
        'Favorite-Weighted RP EPA': correlations['matchup_fav_weighted_epa_diff'],
        'Underdog-Weighted RP EPA': correlations['matchup_dog_weighted_epa_diff']
    }
    
    best_metric = max(margin_correlations, key=margin_correlations.get)
    best_correlation = margin_correlations[best_metric]
    
    print(f"Best performing metric: {best_metric} (r = {best_correlation:.3f})")
    print()
    
    if best_correlation > 0.3:
        print("✅ STRONG POSITIVE CORRELATION")
        print("   The best EPA metric shows strong predictive power for spread performance")
    elif best_correlation > 0.1:
        print("✅ MODERATE POSITIVE CORRELATION")
        print("   The best EPA metric shows moderate predictive power")
    else:
        print("⚠️  WEAK CORRELATION")
        print("   EPA metrics show limited predictive power")
    
    return correlations

def create_visualizations(df, correlations):
    """Create visualizations for the weighted run/pass EPA analysis"""
    print("\n=== Creating Weighted Run/Pass EPA Visualizations ===")
    print("=" * 55)
    
    # Set up the plotting style
    plt.style.use('default')
    sns.set_palette("husl")
    
    # Create figure with subplots
    fig, axes = plt.subplots(2, 3, figsize=(18, 12))
    fig.suptitle('Weighted Run/Pass Matchup EPA vs ATS Performance Analysis', fontsize=16, fontweight='bold')
    
    # 1. Overall Matchup EPA vs Margin vs Spread
    ax1 = axes[0, 0]
    ax1.scatter(df['matchup_epa_diff'], df['margin_vs_spread'], alpha=0.7, s=60, color='blue')
    ax1.axhline(y=0, color='red', linestyle='--', alpha=0.5)
    ax1.axvline(x=0, color='red', linestyle='--', alpha=0.5)
    ax1.set_xlabel('Overall Matchup EPA Difference')
    ax1.set_ylabel('Margin vs Spread')
    ax1.set_title(f'Overall Matchup EPA\n(r = {correlations["matchup_epa_diff"]:.3f})')
    
    # Add trend line
    z = np.polyfit(df['matchup_epa_diff'], df['margin_vs_spread'], 1)
    p = np.poly1d(z)
    ax1.plot(df['matchup_epa_diff'], p(df['matchup_epa_diff']), "r--", alpha=0.8)
    
    # 2. Weighted RP EPA vs Margin vs Spread
    ax2 = axes[0, 1]
    ax2.scatter(df['matchup_weighted_rp_epa_diff'], df['margin_vs_spread'], alpha=0.7, s=60, color='purple')
    ax2.axhline(y=0, color='red', linestyle='--', alpha=0.5)
    ax2.axvline(x=0, color='red', linestyle='--', alpha=0.5)
    ax2.set_xlabel('Weighted RP EPA Difference')
    ax2.set_ylabel('Margin vs Spread')
    ax2.set_title(f'Weighted RP EPA\n(r = {correlations["matchup_weighted_rp_epa_diff"]:.3f})')
    
    # Add trend line
    z = np.polyfit(df['matchup_weighted_rp_epa_diff'], df['margin_vs_spread'], 1)
    p = np.poly1d(z)
    ax2.plot(df['matchup_weighted_rp_epa_diff'], p(df['matchup_weighted_rp_epa_diff']), "r--", alpha=0.8)
    
    # 3. Favorite-Weighted RP EPA vs Margin vs Spread
    ax3 = axes[0, 2]
    ax3.scatter(df['matchup_fav_weighted_epa_diff'], df['margin_vs_spread'], alpha=0.7, s=60, color='green')
    ax3.axhline(y=0, color='red', linestyle='--', alpha=0.5)
    ax3.axvline(x=0, color='red', linestyle='--', alpha=0.5)
    ax3.set_xlabel('Favorite-Weighted RP EPA Difference')
    ax3.set_ylabel('Margin vs Spread')
    ax3.set_title(f'Favorite-Weighted RP EPA\n(r = {correlations["matchup_fav_weighted_epa_diff"]:.3f})')
    
    # Add trend line
    z = np.polyfit(df['matchup_fav_weighted_epa_diff'], df['margin_vs_spread'], 1)
    p = np.poly1d(z)
    ax3.plot(df['matchup_fav_weighted_epa_diff'], p(df['matchup_fav_weighted_epa_diff']), "r--", alpha=0.8)
    
    # 4. Correlation comparison bar chart
    ax4 = axes[1, 0]
    metrics = ['Overall', 'Pass', 'Rush', 'Simple RP', 'Weighted RP', 'Fav-Weighted', 'Dog-Weighted']
    corr_values = [
        correlations['matchup_epa_diff'],
        correlations['matchup_pass_epa_diff'],
        correlations['matchup_rush_epa_diff'],
        correlations['matchup_rp_epa_diff'],
        correlations['matchup_weighted_rp_epa_diff'],
        correlations['matchup_fav_weighted_epa_diff'],
        correlations['matchup_dog_weighted_epa_diff']
    ]
    colors = ['blue', 'green', 'orange', 'purple', 'red', 'brown', 'pink']
    
    bars = ax4.bar(metrics, corr_values, color=colors, alpha=0.7)
    ax4.set_ylabel('Correlation with Margin vs Spread')
    ax4.set_title('EPA Metric Comparison')
    ax4.axhline(y=0, color='red', linestyle='--', alpha=0.5)
    ax4.tick_params(axis='x', rotation=45)
    
    # Add value labels on bars
    for bar, value in zip(bars, corr_values):
        height = bar.get_height()
        ax4.text(bar.get_x() + bar.get_width()/2., height + 0.01 if height >= 0 else height - 0.01,
                f'{value:.3f}', ha='center', va='bottom' if height >= 0 else 'top', fontsize=8)
    
    # 5. Run/Pass ratio distribution
    ax5 = axes[1, 1]
    ax5.hist(df['avg_pass_pct'], bins=15, alpha=0.7, color='purple', label='Pass %')
    ax5.hist(df['avg_run_pct'], bins=15, alpha=0.7, color='orange', label='Run %')
    ax5.set_xlabel('Percentage')
    ax5.set_ylabel('Frequency')
    ax5.set_title('Distribution of Run/Pass Ratios')
    ax5.legend()
    
    # 6. Weighted vs Simple RP EPA comparison
    ax6 = axes[1, 2]
    ax6.scatter(df['matchup_rp_epa_diff'], df['matchup_weighted_rp_epa_diff'], alpha=0.7, s=60, color='purple')
    ax6.plot([df['matchup_rp_epa_diff'].min(), df['matchup_rp_epa_diff'].max()], 
             [df['matchup_rp_epa_diff'].min(), df['matchup_rp_epa_diff'].max()], 
             'r--', alpha=0.5, label='y=x')
    ax6.set_xlabel('Simple Average RP EPA')
    ax6.set_ylabel('Weighted RP EPA')
    ax6.set_title('Weighted vs Simple RP EPA')
    ax6.legend()
    
    plt.tight_layout()
    
    # Save the plot
    output_path = 'images/weighted_matchup_rp_epa_analysis.png'
    plt.savefig(output_path, dpi=300, bbox_inches='tight')
    print(f"✅ Visualization saved to: {output_path}")
    
    plt.show()

def generate_summary_report(df, correlations):
    """Generate a comprehensive summary report"""
    print("\n=== WEIGHTED RUN/PASS MATCHUP EPA ANALYSIS REPORT ===")
    print("=" * 70)
    
    total_games = len(df)
    favorite_cover_rate = df['favorite_covered'].mean()
    
    print(f"Analysis Period: Weeks 1-8")
    print(f"Total Games Analyzed: {total_games}")
    print(f"Overall Favorite Cover Rate: {favorite_cover_rate:.1%}")
    print()
    
    print("CORRELATION FINDINGS:")
    print("-" * 30)
    print(f"Overall Matchup EPA:           {correlations['matchup_epa_diff']:.3f}")
    print(f"Pass Matchup EPA:              {correlations['matchup_pass_epa_diff']:.3f}")
    print(f"Rush Matchup EPA:              {correlations['matchup_rush_epa_diff']:.3f}")
    print(f"Simple Average RP EPA:         {correlations['matchup_rp_epa_diff']:.3f}")
    print(f"Average Weighted RP EPA:       {correlations['matchup_weighted_rp_epa_diff']:.3f}")
    print(f"Favorite-Weighted RP EPA:      {correlations['matchup_fav_weighted_epa_diff']:.3f}")
    print(f"Underdog-Weighted RP EPA:      {correlations['matchup_dog_weighted_epa_diff']:.3f}")
    print()
    
    # Find best performing metrics
    margin_correlations = {
        'Overall Matchup EPA': correlations['matchup_epa_diff'],
        'Pass Matchup EPA': correlations['matchup_pass_epa_diff'],
        'Rush Matchup EPA': correlations['matchup_rush_epa_diff'],
        'Simple Average RP EPA': correlations['matchup_rp_epa_diff'],
        'Average Weighted RP EPA': correlations['matchup_weighted_rp_epa_diff'],
        'Favorite-Weighted RP EPA': correlations['matchup_fav_weighted_epa_diff'],
        'Underdog-Weighted RP EPA': correlations['matchup_dog_weighted_epa_diff']
    }
    
    sorted_metrics = sorted(margin_correlations.items(), key=lambda x: x[1], reverse=True)
    
    print("RANKING BY CORRELATION STRENGTH:")
    print("-" * 40)
    for i, (metric, corr) in enumerate(sorted_metrics, 1):
        print(f"{i}. {metric:25s}: {corr:.3f}")
    
    print()
    
    # Top games by weighted RP EPA
    print("TOP 5 GAMES BY WEIGHTED RP EPA ADVANTAGE:")
    print("-" * 50)
    top_games = df.nlargest(5, 'matchup_weighted_rp_epa_diff')
    for _, row in top_games.iterrows():
        print(f"{row['game']}: Weighted RP EPA = {row['matchup_weighted_rp_epa_diff']:.3f}, "
              f"Margin vs Spread = {row['margin_vs_spread']:+.1f}, "
              f"Covered = {row['favorite_covered']}")
    
    print()
    
    # Run/Pass ratio analysis
    print("RUN/PASS RATIO ANALYSIS:")
    print("-" * 25)
    print(f"Average Pass %: {df['avg_pass_pct'].mean():.1%}")
    print(f"Average Run %:  {df['avg_run_pct'].mean():.1%}")
    print(f"Most Pass-Heavy Teams: {df.groupby('favorite')['avg_pass_pct'].mean().nlargest(3).to_dict()}")
    print(f"Most Run-Heavy Teams: {df.groupby('favorite')['avg_run_pct'].mean().nlargest(3).to_dict()}")
    
    print()
    
    # Conclusions
    print("CONCLUSIONS:")
    print("-" * 12)
    
    best_metric, best_correlation = sorted_metrics[0]
    
    print(f"1. Best performing metric: {best_metric} (r = {best_correlation:.3f})")
    
    if best_correlation > 0.3:
        print("2. Strong predictive power for spread performance")
        print("3. Weighted run/pass analysis provides valuable insights")
    elif best_correlation > 0.1:
        print("2. Moderate predictive power for spread performance")
        print("3. Some value in weighted run/pass analysis")
    else:
        print("2. Limited predictive power for spread performance")
        print("3. Weighted approach may not add significant value")
    
    print(f"4. Overall favorite cover rate: {favorite_cover_rate:.1%}")
    print(f"5. Analysis based on {total_games} games across 8 weeks")
    print(f"6. Weighted approach considers actual team run/pass tendencies")

def main():
    """Main analysis function"""
    print("=== Weighted Run/Pass Matchup EPA Analysis ===")
    print("Incorporating team run/pass ratios into matchup EPA calculations")
    print("=" * 80)
    
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
    
    # Create visualizations
    create_visualizations(df, correlations)
    
    # Generate summary report
    generate_summary_report(df, correlations)
    
    # Save detailed results
    output_path = 'data/epa/analysis/weighted_matchup_rp_epa_analysis.csv'
    df.to_csv(output_path, index=False)
    print(f"\n✅ Detailed analysis saved to: {output_path}")

if __name__ == "__main__":
    main()
