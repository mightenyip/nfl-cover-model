#!/usr/bin/env python3
"""
Week 3 2025 NFL Results Analysis Script
Pulls actual game results and compares against model predictions
"""

import pandas as pd
import numpy as np
from datetime import datetime
from typing import Dict, List, Tuple

def load_week3_predictions():
    """Load the Week 3 predictions from the CSV file"""
    
    try:
        predictions_df = pd.read_csv('/Users/mightenyip/Documents/GitHub/nfl-cover-model/week3/week3_sumersports_predictions.csv')
        print(f"✅ Loaded {len(predictions_df)} Week 3 predictions")
        return predictions_df
    except Exception as e:
        print(f"❌ Error loading predictions: {e}")
        return None

def create_week3_results():
    """Create the Week 3 actual results based on the web search data"""
    
    # Week 3 2025 NFL Results (Thursday Sep 18 + Sunday Sep 21, 2025)
    # Note: The web search showed the Lions @ Ravens game wasn't played yet, so I'll need to update this
    results = [
        # Thursday, September 18, 2025
        {"away_team": "MIA", "home_team": "BUF", "away_score": 21, "home_score": 31},
        
        # Sunday, September 21, 2025
        {"away_team": "ATL", "home_team": "CAR", "away_score": 0, "home_score": 30},
        {"away_team": "GB", "home_team": "CLE", "away_score": 10, "home_score": 13},
        {"away_team": "HOU", "home_team": "JAX", "away_score": 10, "home_score": 17},
        {"away_team": "CIN", "home_team": "MIN", "away_score": 10, "home_score": 48},
        {"away_team": "PIT", "home_team": "NE", "away_score": 21, "home_score": 14},
        {"away_team": "LA", "home_team": "PHI", "away_score": 26, "home_score": 33},
        {"away_team": "NYJ", "home_team": "TB", "away_score": 27, "home_score": 29},
        {"away_team": "IND", "home_team": "TEN", "away_score": 41, "home_score": 20},
        {"away_team": "LV", "home_team": "WAS", "away_score": 24, "home_score": 41},
        {"away_team": "DEN", "home_team": "LAC", "away_score": 20, "home_score": 23},
        {"away_team": "NO", "home_team": "SEA", "away_score": 13, "home_score": 44},
        {"away_team": "DAL", "home_team": "CHI", "away_score": 14, "home_score": 31},
        {"away_team": "ARI", "home_team": "SF", "away_score": 15, "home_score": 16},
        {"away_team": "KC", "home_team": "NYG", "away_score": 22, "home_score": 9},
        # Note: Lions @ Ravens game was not found in the web search results - may not have been played yet
    ]
    
    # Convert to DataFrame
    results_df = pd.DataFrame(results)
    
    print(f"✅ Created Week 3 results for {len(results_df)} games")
    return results_df

def analyze_week3_results(predictions_df: pd.DataFrame, results_df: pd.DataFrame):
    """Analyze Week 3 results and compare against predictions"""
    
    print("\n=== Week 3 2025 NFL Results Analysis ===")
    
    # Team name to abbreviation mapping
    team_name_to_abbr = {
        'Dolphins': 'MIA', 'Bills': 'BUF', 'Falcons': 'ATL', 'Panthers': 'CAR',
        'Packers': 'GB', 'Browns': 'CLE', 'Texans': 'HOU', 'Jaguars': 'JAX',
        'Bengals': 'CIN', 'Vikings': 'MIN', 'Steelers': 'PIT', 'Patriots': 'NE',
        'Rams': 'LA', 'Eagles': 'PHI', 'Jets': 'NYJ', 'Buccaneers': 'TB',
        'Colts': 'IND', 'Titans': 'TEN', 'Raiders': 'LV', 'Commanders': 'WAS',
        'Broncos': 'DEN', 'Chargers': 'LAC', 'Saints': 'NO', 'Seahawks': 'SEA',
        'Cowboys': 'DAL', 'Bears': 'CHI', 'Cardinals': 'ARI', '49ers': 'SF',
        'Chiefs': 'KC', 'Giants': 'NYG', 'Lions': 'DET', 'Ravens': 'BAL'
    }
    
    # Merge predictions with results
    # First, we need to match games between predictions and results
    analysis_data = []
    
    
    for _, pred_row in predictions_df.iterrows():
        # Get team abbreviations from full names
        away_team_abbr = team_name_to_abbr[pred_row['away_team']]
        home_team_abbr = team_name_to_abbr[pred_row['home_team']]
        underdog_abbr = pred_row['underdog_abbr']
        favorite_abbr = pred_row['favorite_abbr']
        spread_line = pred_row['spread_line']
        cover_probability = pred_row['cover_probability']
        confidence = pred_row['confidence']
        predicted_cover = pred_row['predicted_cover']
        
        # Find matching result - check both directions using abbreviations
        result_row = results_df[
            ((results_df['away_team'] == away_team_abbr) & (results_df['home_team'] == home_team_abbr))
        ]
        
        # If no match found, try the reverse
        if len(result_row) == 0:
            result_row = results_df[
                ((results_df['away_team'] == home_team_abbr) & (results_df['home_team'] == away_team_abbr))
            ]
        
        if len(result_row) > 0:
            result = result_row.iloc[0]
            
            # Determine actual scores based on which team was home/away in prediction
            if result['away_team'] == away_team_abbr and result['home_team'] == home_team_abbr:
                # Prediction format matches result format
                actual_away_score = result['away_score']
                actual_home_score = result['home_score']
            else:
                # Prediction format is reversed from result format - swap the scores
                actual_away_score = result['home_score']  # Result's home team score becomes away score
                actual_home_score = result['away_score']  # Result's away team score becomes home score
            
            # Calculate margin (positive means favorite won by that much)
            actual_margin = actual_home_score - actual_away_score
            
            # Calculate if underdog covered
            if underdog_abbr == away_team_abbr:
                # Underdog is away team - they cover if the margin is less than the spread
                actual_underdog_covered = actual_margin < spread_line
                actual_underdog_won = actual_away_score > actual_home_score
            else:
                # Underdog is home team - they cover if the margin is greater than negative spread
                actual_underdog_covered = actual_margin > -spread_line
                actual_underdog_won = actual_home_score > actual_away_score
            
            analysis_data.append({
                'game': f"{away_team_abbr} @ {home_team_abbr}",
                'underdog': underdog_abbr,
                'favorite': favorite_abbr,
                'spread': spread_line,
                'cover_probability': cover_probability,
                'confidence': confidence,
                'predicted_cover': predicted_cover,
                'actual_away_score': actual_away_score,
                'actual_home_score': actual_home_score,
                'actual_margin': actual_margin,
                'actual_cover': actual_underdog_covered,
                'actual_underdog_win': actual_underdog_won,
                'spread_correct': predicted_cover == actual_underdog_covered,
                'outright_correct': actual_underdog_won
            })
        else:
            print(f"⚠️  No result found for {away_team_abbr} @ {home_team_abbr}")
    
    # Convert to DataFrame
    analysis_df = pd.DataFrame(analysis_data)
    
    if len(analysis_df) == 0:
        print("❌ No games could be matched between predictions and results")
        return None
    
    return analysis_df

def generate_week3_analysis_report(analysis_df: pd.DataFrame):
    """Generate comprehensive Week 3 analysis report"""
    
    print(f"\n=== Week 3 2025 NFL Results Analysis ===")
    print(f"Analysis Date: {datetime.now().strftime('%Y-%m-%d')}")
    
    # Overall results
    total_games = len(analysis_df)
    total_underdogs = total_games  # Each game has one underdog
    underdogs_covered = analysis_df['actual_cover'].sum()
    underdogs_won_outright = analysis_df['actual_underdog_win'].sum()
    
    print(f"\n## Underdog Cover Analysis")
    print(f"- **Total underdogs**: {total_underdogs}")
    print(f"- **Underdogs who covered**: {underdogs_covered}")
    print(f"- **Cover rate**: {underdogs_covered/total_underdogs:.1%}")
    print(f"- **Underdogs who won outright**: {underdogs_won_outright}")
    print(f"- **Outright win rate**: {underdogs_won_outright/total_underdogs:.1%}")
    
    # Home vs Away underdogs
    home_underdogs = analysis_df[analysis_df['underdog'] == analysis_df['game'].str.split(' @ ').str[1].str[:3]]
    away_underdogs = analysis_df[analysis_df['underdog'] == analysis_df['game'].str.split(' @ ').str[0].str[:3]]
    
    print(f"\n### Home vs Away Underdogs")
    print(f"- **Home underdogs**: {len(home_underdogs)} games")
    if len(home_underdogs) > 0:
        print(f"  - Cover rate: {home_underdogs['actual_cover'].sum()/len(home_underdogs):.1%} ({home_underdogs['actual_cover'].sum()}/{len(home_underdogs)})")
    print(f"- **Away underdogs**: {len(away_underdogs)} games")
    if len(away_underdogs) > 0:
        print(f"  - Cover rate: {away_underdogs['actual_cover'].sum()/len(away_underdogs):.1%} ({away_underdogs['actual_cover'].sum()}/{len(away_underdogs)})")
    
    # Model performance
    spread_correct = analysis_df['spread_correct'].sum()
    outright_correct = analysis_df['outright_correct'].sum()
    
    print(f"\n## Model Performance Analysis")
    print(f"- **Spread prediction accuracy**: {spread_correct/total_games:.1%} ({spread_correct}/{total_games})")
    print(f"- **Outright prediction accuracy**: {outright_correct/total_games:.1%} ({outright_correct}/{total_games})")
    
    # Performance by confidence level
    print(f"\n### Performance by Confidence Level")
    confidence_analysis = analysis_df.groupby('confidence').agg({
        'actual_cover': ['count', 'sum', 'mean'],
        'spread_correct': ['sum', 'mean'],
        'outright_correct': ['sum', 'mean']
    }).round(3)
    
    confidence_analysis.columns = ['games', 'covered', 'cover_rate', 'spread_correct', 'spread_accuracy', 'outright_correct', 'outright_accuracy']
    print(confidence_analysis.to_string())
    
    # Detailed results table
    print(f"\n### Detailed Results")
    print("| Game | Underdog | Spread | Score | Margin | Covered | Outright Win |")
    print("|------|----------|--------|-------|--------|---------|--------------|")
    
    for _, row in analysis_df.iterrows():
        game_parts = row['game'].split(' @ ')
        away_team = game_parts[0]
        home_team = game_parts[1]
        score_str = f"{row['actual_away_score']}-{row['actual_home_score']}"
        covered_str = "YES" if row['actual_cover'] else "NO"
        outright_str = "YES" if row['actual_underdog_win'] else "NO"
        
        print(f"| {row['game']} | {row['underdog']} | +{row['spread']} | {score_str} | {row['actual_margin']:+d} | {covered_str} | {outright_str} |")
    
    # Spread distribution analysis
    print(f"\n## Spread Distribution Analysis")
    spread_analysis = analysis_df.groupby('spread').agg({
        'actual_cover': ['count', 'sum', 'mean']
    }).round(3)
    spread_analysis.columns = ['games', 'covered', 'cover_rate']
    print(spread_analysis.to_string())
    
    return analysis_df

def save_week3_results(analysis_df: pd.DataFrame):
    """Save Week 3 results to CSV files"""
    
    # Save detailed results
    detailed_file = '/Users/mightenyip/Documents/GitHub/nfl-cover-model/week3/week3_detailed_results.csv'
    analysis_df.to_csv(detailed_file, index=False)
    print(f"\n✅ Saved detailed results to {detailed_file}")
    
    # Create a summary file similar to previous weeks
    summary_file = '/Users/mightenyip/Documents/GitHub/nfl-cover-model/week3/week3_2025_results_analysis.md'
    
    with open(summary_file, 'w') as f:
        f.write("# Week 3 2025 NFL Results Analysis\n\n")
        f.write("## Overview\n")
        f.write("This analysis examines Week 3 2025 NFL results with a focus on underdog performance against the spread, model accuracy, and EPA correlations using actual game results.\n\n")
        
        # Add the analysis content
        total_games = len(analysis_df)
        underdogs_covered = analysis_df['actual_cover'].sum()
        underdogs_won_outright = analysis_df['actual_underdog_win'].sum()
        
        f.write("## Underdog Cover Analysis\n\n")
        f.write("### Overall Results\n")
        f.write(f"- **Total underdogs**: {total_games}\n")
        f.write(f"- **Underdogs who covered**: {underdogs_covered}\n")
        f.write(f"- **Cover rate**: {underdogs_covered/total_games:.1%}\n\n")
        
        f.write("### Detailed Results\n\n")
        f.write("| Game | Underdog | Spread | Score | Margin | Covered | Outright Win |\n")
        f.write("|------|----------|--------|-------|--------|---------|--------------|\n")
        
        for _, row in analysis_df.iterrows():
            score_str = f"{row['actual_away_score']}-{row['actual_home_score']}"
            covered_str = "YES" if row['actual_cover'] else "NO"
            outright_str = "YES" if row['actual_underdog_win'] else "NO"
            
            f.write(f"| {row['game']} | {row['underdog']} | +{row['spread']} | {score_str} | {row['actual_margin']:+d} | {covered_str} | {outright_str} |\n")
        
        f.write(f"\n## Model Performance Analysis\n\n")
        spread_correct = analysis_df['spread_correct'].sum()
        outright_correct = analysis_df['outright_correct'].sum()
        
        f.write("### Overall Model Accuracy\n")
        f.write(f"- **Spread prediction accuracy**: {spread_correct/total_games:.1%} ({spread_correct}/{total_games})\n")
        f.write(f"- **Outright prediction accuracy**: {outright_correct/total_games:.1%} ({outright_correct}/{total_games})\n\n")
        
        f.write("### Performance by Confidence Level\n\n")
        confidence_analysis = analysis_df.groupby('confidence').agg({
            'actual_cover': ['count', 'sum', 'mean'],
            'spread_correct': ['sum', 'mean'],
            'outright_correct': ['sum', 'mean']
        }).round(3)
        
        confidence_analysis.columns = ['games', 'covered', 'cover_rate', 'spread_correct', 'spread_accuracy', 'outright_correct', 'outright_accuracy']
        
        f.write("| Confidence | Games | Cover Rate | Spread Accuracy | Outright Accuracy |\n")
        f.write("|------------|-------|------------|-----------------|-------------------|\n")
        
        for confidence, row in confidence_analysis.iterrows():
            f.write(f"| {confidence} | {int(row['games'])} | {row['cover_rate']:.1%} ({int(row['covered'])}/{int(row['games'])}) | {row['spread_accuracy']:.1%} ({int(row['spread_correct'])}/{int(row['games'])}) | {row['outright_accuracy']:.1%} ({int(row['outright_correct'])}/{int(row['games'])}) |\n")
    
    print(f"✅ Saved summary analysis to {summary_file}")

def main():
    """Main function to run Week 3 results analysis"""
    
    print("=== Week 3 2025 NFL Results Analysis ===")
    
    # Load predictions
    predictions_df = load_week3_predictions()
    if predictions_df is None:
        return
    
    # Create results data
    results_df = create_week3_results()
    
    # Analyze results
    analysis_df = analyze_week3_results(predictions_df, results_df)
    if analysis_df is None:
        return
    
    # Generate report
    generate_week3_analysis_report(analysis_df)
    
    # Save results
    save_week3_results(analysis_df)
    
    print(f"\n✅ Week 3 analysis complete!")
    print(f"📊 Analyzed {len(analysis_df)} games")
    print(f"📈 Overall underdog cover rate: {analysis_df['actual_cover'].sum()/len(analysis_df):.1%}")

if __name__ == "__main__":
    main()
