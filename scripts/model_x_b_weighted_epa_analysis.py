#!/usr/bin/env python3
"""
Model X_b: Inverse Weighted Run/Pass Matchup EPA Analysis
Uses inverse weighting approach:
- Fav Run EPA × Fav Pass % (weight run by pass tendency)
- Fav Pass EPA × Fav Run % (weight pass by run tendency)
- Dog Run EPA × Dog Pass % (weight run by pass tendency)  
- Dog Pass EPA × Dog Run % (weight pass by run tendency)
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
                # Overall matchup EPA (original Model X)
                fav_matchup_epa = fav_off + dog_def
                dog_matchup_epa = dog_off + fav_def
                matchup_epa_diff = fav_matchup_epa - dog_matchup_epa
                
                # Pass matchup EPA (original)
                fav_matchup_pass_epa = fav_off_pass + dog_def_pass
                dog_matchup_pass_epa = dog_off_pass + fav_def_pass
                matchup_pass_epa_diff = fav_matchup_pass_epa - dog_matchup_pass_epa
                
                # Rush matchup EPA (original)
                fav_matchup_rush_epa = fav_off_rush + dog_def_rush
                dog_matchup_rush_epa = dog_off_rush + fav_def_rush
                matchup_rush_epa_diff = fav_matchup_rush_epa - dog_matchup_rush_epa
                
                # Combined Run-Pass Matchup EPA (simple average)
                matchup_rp_epa_diff = (matchup_pass_epa_diff + matchup_rush_epa_diff) / 2
                
                # MODEL X_b: INVERSE WEIGHTED Run-Pass Matchup EPA
                # Weight by OPPOSITE tendencies (run EPA × pass %, pass EPA × run %)
                
                # Favorite's inverse weighted components
                fav_inverse_pass_epa = fav_off_pass * fav_run_pct  # Pass EPA weighted by run %
                fav_inverse_rush_epa = fav_off_rush * fav_pass_pct  # Rush EPA weighted by pass %
                fav_inverse_def_pass_epa = dog_def_pass * fav_run_pct  # Dog def pass weighted by fav run %
                fav_inverse_def_rush_epa = dog_def_rush * fav_pass_pct  # Dog def rush weighted by fav pass %
                
                # Underdog's inverse weighted components
                dog_inverse_pass_epa = dog_off_pass * dog_run_pct  # Pass EPA weighted by run %
                dog_inverse_rush_epa = dog_off_rush * dog_pass_pct  # Rush EPA weighted by pass %
                dog_inverse_def_pass_epa = fav_def_pass * dog_run_pct  # Fav def pass weighted by dog run %
                dog_inverse_def_rush_epa = fav_def_rush * dog_pass_pct  # Fav def rush weighted by dog pass %
                
                # Model X_b Matchup EPA calculations
                # Favorite's inverse weighted matchup EPA
                fav_inverse_matchup_pass_epa = fav_inverse_pass_epa + fav_inverse_def_pass_epa
                fav_inverse_matchup_rush_epa = fav_inverse_rush_epa + fav_inverse_def_rush_epa
                fav_inverse_matchup_rp_epa = fav_inverse_matchup_pass_epa + fav_inverse_matchup_rush_epa
                
                # Underdog's inverse weighted matchup EPA
                dog_inverse_matchup_pass_epa = dog_inverse_pass_epa + dog_inverse_def_pass_epa
                dog_inverse_matchup_rush_epa = dog_inverse_rush_epa + dog_inverse_def_rush_epa
                dog_inverse_matchup_rp_epa = dog_inverse_matchup_pass_epa + dog_inverse_matchup_rush_epa
                
                # Model X_b final matchup EPA difference
                model_x_b_matchup_epa_diff = fav_inverse_matchup_rp_epa - dog_inverse_matchup_rp_epa
                
                # Alternative Model X_b: Weight by overall defensive EPA instead of specific pass/rush
                # This is what you mentioned: "fav_run epa x fav pass % - defense overall EPA"
                fav_inverse_rush_vs_def_overall = (fav_off_rush * fav_pass_pct) - dog_def
                fav_inverse_pass_vs_def_overall = (fav_off_pass * fav_run_pct) - dog_def
                dog_inverse_rush_vs_def_overall = (dog_off_rush * dog_pass_pct) - fav_def
                dog_inverse_pass_vs_def_overall = (dog_off_pass * dog_run_pct) - fav_def
                
                # Combined alternative approach
                model_x_b_alt_matchup_epa_diff = (fav_inverse_rush_vs_def_overall + fav_inverse_pass_vs_def_overall) - (dog_inverse_rush_vs_def_overall + dog_inverse_pass_vs_def_overall)
                
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
                    
                    # MODEL X_b: Inverse Weighted Run-Pass EPA
                    'model_x_b_matchup_epa_diff': model_x_b_matchup_epa_diff,
                    'model_x_b_alt_matchup_epa_diff': model_x_b_alt_matchup_epa_diff,
                    
                    # Individual inverse weighted components
                    'fav_inverse_pass_epa': fav_inverse_pass_epa,
                    'fav_inverse_rush_epa': fav_inverse_rush_epa,
                    'dog_inverse_pass_epa': dog_inverse_pass_epa,
                    'dog_inverse_rush_epa': dog_inverse_rush_epa,
                    
                    # Alternative approach components
                    'fav_inverse_rush_vs_def_overall': fav_inverse_rush_vs_def_overall,
                    'fav_inverse_pass_vs_def_overall': fav_inverse_pass_vs_def_overall,
                    'dog_inverse_rush_vs_def_overall': dog_inverse_rush_vs_def_overall,
                    'dog_inverse_pass_vs_def_overall': dog_inverse_pass_vs_def_overall,
                    
                    # Run/Pass ratios
                    'fav_run_pct': fav_run_pct,
                    'fav_pass_pct': fav_pass_pct,
                    'dog_run_pct': dog_run_pct,
                    'dog_pass_pct': dog_pass_pct
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
                # Overall matchup EPA (original Model X)
                fav_matchup_epa = fav_off + dog_def
                dog_matchup_epa = dog_off + fav_def
                matchup_epa_diff = fav_matchup_epa - dog_matchup_epa
                
                # Pass matchup EPA (original)
                fav_matchup_pass_epa = fav_off_pass + dog_def_pass
                dog_matchup_pass_epa = dog_off_pass + fav_def_pass
                matchup_pass_epa_diff = fav_matchup_pass_epa - dog_matchup_pass_epa
                
                # Rush matchup EPA (original)
                fav_matchup_rush_epa = fav_off_rush + dog_def_rush
                dog_matchup_rush_epa = dog_off_rush + fav_def_rush
                matchup_rush_epa_diff = fav_matchup_rush_epa - dog_matchup_rush_epa
                
                # Combined Run-Pass Matchup EPA (simple average)
                matchup_rp_epa_diff = (matchup_pass_epa_diff + matchup_rush_epa_diff) / 2
                
                # MODEL X_b: INVERSE WEIGHTED Run-Pass Matchup EPA
                # Weight by OPPOSITE tendencies (run EPA × pass %, pass EPA × run %)
                
                # Favorite's inverse weighted components
                fav_inverse_pass_epa = fav_off_pass * fav_run_pct  # Pass EPA weighted by run %
                fav_inverse_rush_epa = fav_off_rush * fav_pass_pct  # Rush EPA weighted by pass %
                fav_inverse_def_pass_epa = dog_def_pass * fav_run_pct  # Dog def pass weighted by fav run %
                fav_inverse_def_rush_epa = dog_def_rush * fav_pass_pct  # Dog def rush weighted by fav pass %
                
                # Underdog's inverse weighted components
                dog_inverse_pass_epa = dog_off_pass * dog_run_pct  # Pass EPA weighted by run %
                dog_inverse_rush_epa = dog_off_rush * dog_pass_pct  # Rush EPA weighted by pass %
                dog_inverse_def_pass_epa = fav_def_pass * dog_run_pct  # Fav def pass weighted by dog run %
                dog_inverse_def_rush_epa = fav_def_rush * dog_pass_pct  # Fav def rush weighted by dog pass %
                
                # Model X_b Matchup EPA calculations
                # Favorite's inverse weighted matchup EPA
                fav_inverse_matchup_pass_epa = fav_inverse_pass_epa + fav_inverse_def_pass_epa
                fav_inverse_matchup_rush_epa = fav_inverse_rush_epa + fav_inverse_def_rush_epa
                fav_inverse_matchup_rp_epa = fav_inverse_matchup_pass_epa + fav_inverse_matchup_rush_epa
                
                # Underdog's inverse weighted matchup EPA
                dog_inverse_matchup_pass_epa = dog_inverse_pass_epa + dog_inverse_def_pass_epa
                dog_inverse_matchup_rush_epa = dog_inverse_rush_epa + dog_inverse_def_rush_epa
                dog_inverse_matchup_rp_epa = dog_inverse_matchup_pass_epa + dog_inverse_matchup_rush_epa
                
                # Model X_b final matchup EPA difference
                model_x_b_matchup_epa_diff = fav_inverse_matchup_rp_epa - dog_inverse_matchup_rp_epa
                
                # Alternative Model X_b: Weight by overall defensive EPA instead of specific pass/rush
                # This is what you mentioned: "fav_run epa x fav pass % - defense overall EPA"
                fav_inverse_rush_vs_def_overall = (fav_off_rush * fav_pass_pct) - dog_def
                fav_inverse_pass_vs_def_overall = (fav_off_pass * fav_run_pct) - fav_def
                dog_inverse_rush_vs_def_overall = (dog_off_rush * dog_pass_pct) - fav_def
                dog_inverse_pass_vs_def_overall = (dog_off_pass * dog_run_pct) - dog_def
                
                # Combined alternative approach
                model_x_b_alt_matchup_epa_diff = (fav_inverse_rush_vs_def_overall + fav_inverse_pass_vs_def_overall) - (dog_inverse_rush_vs_def_overall + dog_inverse_pass_vs_def_overall)
                
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
                    
                    # MODEL X_b: Inverse Weighted Run-Pass EPA
                    'model_x_b_matchup_epa_diff': model_x_b_matchup_epa_diff,
                    'model_x_b_alt_matchup_epa_diff': model_x_b_alt_matchup_epa_diff,
                    
                    # Individual inverse weighted components
                    'fav_inverse_pass_epa': fav_inverse_pass_epa,
                    'fav_inverse_rush_epa': fav_inverse_rush_epa,
                    'dog_inverse_pass_epa': dog_inverse_pass_epa,
                    'dog_inverse_rush_epa': dog_inverse_rush_epa,
                    
                    # Alternative approach components
                    'fav_inverse_rush_vs_def_overall': fav_inverse_rush_vs_def_overall,
                    'fav_inverse_pass_vs_def_overall': fav_inverse_pass_vs_def_overall,
                    'dog_inverse_rush_vs_def_overall': dog_inverse_rush_vs_def_overall,
                    'dog_inverse_pass_vs_def_overall': dog_inverse_pass_vs_def_overall,
                    
                    # Run/Pass ratios
                    'fav_run_pct': fav_run_pct,
                    'fav_pass_pct': fav_pass_pct,
                    'dog_run_pct': dog_run_pct,
                    'dog_pass_pct': dog_pass_pct
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
    print("\n=== Model X_b: Inverse Weighted Run/Pass Matchup EPA vs ATS Correlation Analysis ===")
    print("=" * 100)
    
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
    
    # MODEL X_b: Inverse Weighted Run-Pass EPA
    correlations['model_x_b_matchup_epa_diff'] = df['model_x_b_matchup_epa_diff'].corr(df['margin_vs_spread'])
    correlations['model_x_b_alt_matchup_epa_diff'] = df['model_x_b_alt_matchup_epa_diff'].corr(df['margin_vs_spread'])
    
    # Individual inverse weighted components
    correlations['fav_inverse_pass_epa'] = df['fav_inverse_pass_epa'].corr(df['margin_vs_spread'])
    correlations['fav_inverse_rush_epa'] = df['fav_inverse_rush_epa'].corr(df['margin_vs_spread'])
    correlations['dog_inverse_pass_epa'] = df['dog_inverse_pass_epa'].corr(df['margin_vs_spread'])
    correlations['dog_inverse_rush_epa'] = df['dog_inverse_rush_epa'].corr(df['margin_vs_spread'])
    
    # Alternative approach components
    correlations['fav_inverse_rush_vs_def_overall'] = df['fav_inverse_rush_vs_def_overall'].corr(df['margin_vs_spread'])
    correlations['fav_inverse_pass_vs_def_overall'] = df['fav_inverse_pass_vs_def_overall'].corr(df['margin_vs_spread'])
    correlations['dog_inverse_rush_vs_def_overall'] = df['dog_inverse_rush_vs_def_overall'].corr(df['margin_vs_spread'])
    correlations['dog_inverse_pass_vs_def_overall'] = df['dog_inverse_pass_vs_def_overall'].corr(df['margin_vs_spread'])
    
    # Cover rate correlations
    correlations['matchup_epa_vs_cover'] = df['matchup_epa_diff'].corr(df['favorite_covered'].astype(int))
    correlations['model_x_b_vs_cover'] = df['model_x_b_matchup_epa_diff'].corr(df['favorite_covered'].astype(int))
    correlations['model_x_b_alt_vs_cover'] = df['model_x_b_alt_matchup_epa_diff'].corr(df['favorite_covered'].astype(int))
    
    print("Correlation Results:")
    print("-" * 80)
    print("OVERALL EPA:")
    print(f"  Matchup EPA Diff:                           {correlations['matchup_epa_diff']:6.3f}")
    print(f"  Net EPA Diff:                               {correlations['net_epa_diff']:6.3f}")
    print()
    print("PASS-SPECIFIC EPA:")
    print(f"  Matchup Pass EPA Diff:                      {correlations['matchup_pass_epa_diff']:6.3f}")
    print(f"  Fav Off Pass EPA:                           {correlations['fav_off_pass_epa']:6.3f}")
    print(f"  Dog Def Pass EPA:                           {correlations['dog_def_pass_epa']:6.3f}")
    print()
    print("RUSH-SPECIFIC EPA:")
    print(f"  Matchup Rush EPA Diff:                      {correlations['matchup_rush_epa_diff']:6.3f}")
    print(f"  Fav Off Rush EPA:                           {correlations['fav_off_rush_epa']:6.3f}")
    print(f"  Dog Def Rush EPA:                           {correlations['dog_def_rush_epa']:6.3f}")
    print()
    print("COMBINED RUN-PASS EPA:")
    print(f"  Simple Average RP EPA:                      {correlations['matchup_rp_epa_diff']:6.3f}")
    print()
    print("MODEL X_b: INVERSE WEIGHTED RUN-PASS EPA:")
    print(f"  Model X_b Matchup EPA Diff:                 {correlations['model_x_b_matchup_epa_diff']:6.3f}")
    print(f"  Model X_b Alt Matchup EPA Diff:             {correlations['model_x_b_alt_matchup_epa_diff']:6.3f}")
    print()
    print("INDIVIDUAL INVERSE WEIGHTED COMPONENTS:")
    print(f"  Fav Inverse Pass EPA (pass × run %):        {correlations['fav_inverse_pass_epa']:6.3f}")
    print(f"  Fav Inverse Rush EPA (rush × pass %):       {correlations['fav_inverse_rush_epa']:6.3f}")
    print(f"  Dog Inverse Pass EPA (pass × run %):        {correlations['dog_inverse_pass_epa']:6.3f}")
    print(f"  Dog Inverse Rush EPA (rush × pass %):       {correlations['dog_inverse_rush_epa']:6.3f}")
    print()
    print("ALTERNATIVE APPROACH COMPONENTS:")
    print(f"  Fav Rush × Pass % vs Def Overall:           {correlations['fav_inverse_rush_vs_def_overall']:6.3f}")
    print(f"  Fav Pass × Run % vs Def Overall:            {correlations['fav_inverse_pass_vs_def_overall']:6.3f}")
    print(f"  Dog Rush × Pass % vs Def Overall:           {correlations['dog_inverse_rush_vs_def_overall']:6.3f}")
    print(f"  Dog Pass × Run % vs Def Overall:            {correlations['dog_inverse_pass_vs_def_overall']:6.3f}")
    print()
    print("COVER RATE CORRELATIONS:")
    print(f"  Matchup EPA vs Cover:                       {correlations['matchup_epa_vs_cover']:6.3f}")
    print(f"  Model X_b vs Cover:                         {correlations['model_x_b_vs_cover']:6.3f}")
    print(f"  Model X_b Alt vs Cover:                     {correlations['model_x_b_alt_vs_cover']:6.3f}")
    
    print()
    
    # Statistical significance tests
    print("Statistical Significance Tests:")
    print("-" * 70)
    
    significance_tests = [
        ('matchup_epa_diff', 'margin_vs_spread'),
        ('matchup_pass_epa_diff', 'margin_vs_spread'),
        ('matchup_rush_epa_diff', 'margin_vs_spread'),
        ('matchup_rp_epa_diff', 'margin_vs_spread'),
        ('model_x_b_matchup_epa_diff', 'margin_vs_spread'),
        ('model_x_b_alt_matchup_epa_diff', 'margin_vs_spread'),
        ('fav_inverse_pass_epa', 'margin_vs_spread'),
        ('fav_inverse_rush_epa', 'margin_vs_spread'),
        ('dog_inverse_pass_epa', 'margin_vs_spread'),
        ('dog_inverse_rush_epa', 'margin_vs_spread'),
        ('fav_inverse_rush_vs_def_overall', 'margin_vs_spread'),
        ('fav_inverse_pass_vs_def_overall', 'margin_vs_spread'),
        ('dog_inverse_rush_vs_def_overall', 'margin_vs_spread'),
        ('dog_inverse_pass_vs_def_overall', 'margin_vs_spread')
    ]
    
    for metric, target in significance_tests:
        t_stat, p_value = stats.pearsonr(df[metric], df[target])
        significance = "✅ Significant" if p_value < 0.05 else "⚠️  Not Significant"
        print(f"{metric:45s}: p={p_value:.3f} {significance}")
    
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
        'Model X_b Matchup EPA': correlations['model_x_b_matchup_epa_diff'],
        'Model X_b Alt Matchup EPA': correlations['model_x_b_alt_matchup_epa_diff']
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
    """Create visualizations for the Model X_b analysis"""
    print("\n=== Creating Model X_b Visualizations ===")
    print("=" * 40)
    
    # Set up the plotting style
    plt.style.use('default')
    sns.set_palette("husl")
    
    # Create figure with subplots
    fig, axes = plt.subplots(2, 3, figsize=(18, 12))
    fig.suptitle('Model X_b: Inverse Weighted Run/Pass Matchup EPA vs ATS Performance Analysis', fontsize=16, fontweight='bold')
    
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
    
    # 2. Model X_b vs Margin vs Spread
    ax2 = axes[0, 1]
    ax2.scatter(df['model_x_b_matchup_epa_diff'], df['margin_vs_spread'], alpha=0.7, s=60, color='purple')
    ax2.axhline(y=0, color='red', linestyle='--', alpha=0.5)
    ax2.axvline(x=0, color='red', linestyle='--', alpha=0.5)
    ax2.set_xlabel('Model X_b Matchup EPA Difference')
    ax2.set_ylabel('Margin vs Spread')
    ax2.set_title(f'Model X_b Matchup EPA\n(r = {correlations["model_x_b_matchup_epa_diff"]:.3f})')
    
    # Add trend line
    z = np.polyfit(df['model_x_b_matchup_epa_diff'], df['margin_vs_spread'], 1)
    p = np.poly1d(z)
    ax2.plot(df['model_x_b_matchup_epa_diff'], p(df['model_x_b_matchup_epa_diff']), "r--", alpha=0.8)
    
    # 3. Model X_b Alt vs Margin vs Spread
    ax3 = axes[0, 2]
    ax3.scatter(df['model_x_b_alt_matchup_epa_diff'], df['margin_vs_spread'], alpha=0.7, s=60, color='green')
    ax3.axhline(y=0, color='red', linestyle='--', alpha=0.5)
    ax3.axvline(x=0, color='red', linestyle='--', alpha=0.5)
    ax3.set_xlabel('Model X_b Alt Matchup EPA Difference')
    ax3.set_ylabel('Margin vs Spread')
    ax3.set_title(f'Model X_b Alt Matchup EPA\n(r = {correlations["model_x_b_alt_matchup_epa_diff"]:.3f})')
    
    # Add trend line
    z = np.polyfit(df['model_x_b_alt_matchup_epa_diff'], df['margin_vs_spread'], 1)
    p = np.poly1d(z)
    ax3.plot(df['model_x_b_alt_matchup_epa_diff'], p(df['model_x_b_alt_matchup_epa_diff']), "r--", alpha=0.8)
    
    # 4. Correlation comparison bar chart
    ax4 = axes[1, 0]
    metrics = ['Overall', 'Pass', 'Rush', 'Simple RP', 'Model X_b', 'Model X_b Alt']
    corr_values = [
        correlations['matchup_epa_diff'],
        correlations['matchup_pass_epa_diff'],
        correlations['matchup_rush_epa_diff'],
        correlations['matchup_rp_epa_diff'],
        correlations['model_x_b_matchup_epa_diff'],
        correlations['model_x_b_alt_matchup_epa_diff']
    ]
    colors = ['blue', 'green', 'orange', 'purple', 'red', 'brown']
    
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
    
    # 5. Individual inverse weighted components
    ax5 = axes[1, 1]
    components = ['Fav Pass×Run%', 'Fav Rush×Pass%', 'Dog Pass×Run%', 'Dog Rush×Pass%']
    comp_values = [
        correlations['fav_inverse_pass_epa'],
        correlations['fav_inverse_rush_epa'],
        correlations['dog_inverse_pass_epa'],
        correlations['dog_inverse_rush_epa']
    ]
    colors = ['lightblue', 'lightgreen', 'lightcoral', 'lightyellow']
    
    bars = ax5.bar(components, comp_values, color=colors, alpha=0.7)
    ax5.set_ylabel('Correlation with Margin vs Spread')
    ax5.set_title('Individual Inverse Weighted Components')
    ax5.axhline(y=0, color='red', linestyle='--', alpha=0.5)
    ax5.tick_params(axis='x', rotation=45)
    
    # Add value labels on bars
    for bar, value in zip(bars, comp_values):
        height = bar.get_height()
        ax5.text(bar.get_x() + bar.get_width()/2., height + 0.01 if height >= 0 else height - 0.01,
                f'{value:.3f}', ha='center', va='bottom' if height >= 0 else 'top', fontsize=8)
    
    # 6. Model X_b vs Overall Matchup EPA comparison
    ax6 = axes[1, 2]
    ax6.scatter(df['matchup_epa_diff'], df['model_x_b_matchup_epa_diff'], alpha=0.7, s=60, color='purple')
    ax6.plot([df['matchup_epa_diff'].min(), df['matchup_epa_diff'].max()], 
             [df['matchup_epa_diff'].min(), df['matchup_epa_diff'].max()], 
             'r--', alpha=0.5, label='y=x')
    ax6.set_xlabel('Overall Matchup EPA')
    ax6.set_ylabel('Model X_b Matchup EPA')
    ax6.set_title('Model X_b vs Overall Matchup EPA')
    ax6.legend()
    
    plt.tight_layout()
    
    # Save the plot
    output_path = 'images/model_x_b_weighted_epa_analysis.png'
    plt.savefig(output_path, dpi=300, bbox_inches='tight')
    print(f"✅ Visualization saved to: {output_path}")
    
    plt.show()

def generate_summary_report(df, correlations):
    """Generate a comprehensive summary report"""
    print("\n=== MODEL X_b: INVERSE WEIGHTED RUN/PASS MATCHUP EPA ANALYSIS REPORT ===")
    print("=" * 90)
    
    total_games = len(df)
    favorite_cover_rate = df['favorite_covered'].mean()
    
    print(f"Analysis Period: Weeks 1-8")
    print(f"Total Games Analyzed: {total_games}")
    print(f"Overall Favorite Cover Rate: {favorite_cover_rate:.1%}")
    print()
    
    print("CORRELATION FINDINGS:")
    print("-" * 40)
    print(f"Overall Matchup EPA:              {correlations['matchup_epa_diff']:.3f}")
    print(f"Pass Matchup EPA:                 {correlations['matchup_pass_epa_diff']:.3f}")
    print(f"Rush Matchup EPA:                 {correlations['matchup_rush_epa_diff']:.3f}")
    print(f"Simple Average RP EPA:            {correlations['matchup_rp_epa_diff']:.3f}")
    print(f"Model X_b Matchup EPA:            {correlations['model_x_b_matchup_epa_diff']:.3f}")
    print(f"Model X_b Alt Matchup EPA:        {correlations['model_x_b_alt_matchup_epa_diff']:.3f}")
    print()
    
    # Find best performing metrics
    margin_correlations = {
        'Overall Matchup EPA': correlations['matchup_epa_diff'],
        'Pass Matchup EPA': correlations['matchup_pass_epa_diff'],
        'Rush Matchup EPA': correlations['matchup_rush_epa_diff'],
        'Simple Average RP EPA': correlations['matchup_rp_epa_diff'],
        'Model X_b Matchup EPA': correlations['model_x_b_matchup_epa_diff'],
        'Model X_b Alt Matchup EPA': correlations['model_x_b_alt_matchup_epa_diff']
    }
    
    sorted_metrics = sorted(margin_correlations.items(), key=lambda x: x[1], reverse=True)
    
    print("RANKING BY CORRELATION STRENGTH:")
    print("-" * 50)
    for i, (metric, corr) in enumerate(sorted_metrics, 1):
        print(f"{i}. {metric:30s}: {corr:.3f}")
    
    print()
    
    # Top games by Model X_b
    print("TOP 5 GAMES BY MODEL X_b MATCHUP EPA ADVANTAGE:")
    print("-" * 60)
    top_games = df.nlargest(5, 'model_x_b_matchup_epa_diff')
    for _, row in top_games.iterrows():
        print(f"{row['game']}: Model X_b EPA = {row['model_x_b_matchup_epa_diff']:.3f}, "
              f"Margin vs Spread = {row['margin_vs_spread']:+.1f}, "
              f"Covered = {row['favorite_covered']}")
    
    print()
    
    # Conclusions
    print("CONCLUSIONS:")
    print("-" * 12)
    
    best_metric, best_correlation = sorted_metrics[0]
    
    print(f"1. Best performing metric: {best_metric} (r = {best_correlation:.3f})")
    
    if best_correlation > 0.3:
        print("2. Strong predictive power for spread performance")
        print("3. Model X_b inverse weighted analysis provides valuable insights")
    elif best_correlation > 0.1:
        print("2. Moderate predictive power for spread performance")
        print("3. Some value in Model X_b inverse weighted analysis")
    else:
        print("2. Limited predictive power for spread performance")
        print("3. Model X_b inverse weighted approach may not add significant value")
    
    print(f"4. Overall favorite cover rate: {favorite_cover_rate:.1%}")
    print(f"5. Analysis based on {total_games} games across 8 weeks")
    print("6. Model X_b uses inverse weighting: run EPA × pass %, pass EPA × run %")

def main():
    """Main analysis function"""
    print("=== Model X_b: Inverse Weighted Run/Pass Matchup EPA Analysis ===")
    print("Weighting by opposite tendencies: run EPA × pass %, pass EPA × run %")
    print("=" * 90)
    
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
    output_path = 'data/epa/analysis/model_x_b_weighted_epa_analysis.csv'
    df.to_csv(output_path, index=False)
    print(f"\n✅ Detailed analysis saved to: {output_path}")

if __name__ == "__main__":
    main()
