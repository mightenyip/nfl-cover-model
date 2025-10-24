#!/usr/bin/env python3
"""
Model X: Matchup-Specific Analysis Model
Compares each team's offense vs opponent's defense and vice versa
to find matchup advantages that could affect spread outcomes.
"""

import pandas as pd
import numpy as np
import os

def run_model_x_matchup_analysis():
    """Run Model X using matchup-specific EPA analysis"""
    print("=== Model X: Matchup-Specific Analysis ===")
    print("Analyzing offense vs defense matchups for spread correlation")
    print("=" * 60)
    
    # Load EPA data
    epa_df = pd.read_csv('detailed_epa_data.csv')
    print(f"Loaded EPA data for {len(epa_df)} teams")
    
    # Load Week 8 odds
    odds_df = pd.read_csv('schedule/week8_2025_odds.csv')
    print(f"Loaded {len(odds_df)} games from Week 8 odds")
    
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
    
    predictions = []
    
    for idx, row in odds_df.iterrows():
        away_team = row['away_team']
        home_team = row['home_team']
        favorite = row['favorite_team']
        underdog = row['underdog_team']
        spread = row['spread_line']
        
        # Get team abbreviations
        away_abbr = team_mapping.get(away_team, away_team)
        home_abbr = team_mapping.get(home_team, home_team)
        fav_abbr = team_mapping.get(favorite, favorite)
        dog_abbr = team_mapping.get(underdog, underdog)
        
        # Get EPA data for both teams
        away_epa = epa_df[epa_df['team'] == away_abbr]
        home_epa = epa_df[epa_df['team'] == home_abbr]
        
        if away_epa.empty or home_epa.empty:
            print(f"Warning: Missing EPA data for {away_team} or {home_team}")
            continue
            
        # Extract EPA values
        away_off = away_epa['epa_off_per_play'].iloc[0]
        away_def = away_epa['epa_def_allowed_per_play'].iloc[0]
        home_off = home_epa['epa_off_per_play'].iloc[0]
        home_def = home_epa['epa_def_allowed_per_play'].iloc[0]
        
        # Calculate matchup advantages using improved formula
        # MatchupEPA = OffEPA + DefEPA (where DefEPA is negative for good defense)
        
        # Away offense vs Home defense matchup
        away_off_vs_home_def = away_off + home_def
        
        # Home offense vs Away defense matchup  
        home_off_vs_away_def = home_off + away_def
        
        # Net matchup advantage (positive = home advantage)
        net_matchup_advantage = home_off_vs_away_def - away_off_vs_home_def
        
        # Calculate net EPA (overall team strength difference)
        away_net_epa = away_off - away_def
        home_net_epa = home_off - home_def
        net_epa_difference = home_net_epa - away_net_epa
        
        prediction_data = {
            'game': f'{away_team} @ {home_team}',
            'favorite': favorite,
            'underdog': underdog,
            'spread': spread,
            'away_off_epa': away_off,
            'home_off_epa': home_off,
            'away_def_epa': away_def,
            'home_def_epa': home_def,
            'away_matchup_epa': away_off_vs_home_def,
            'home_matchup_epa': home_off_vs_away_def,
            'net_matchup_advantage': net_matchup_advantage,
            'away_net_epa': away_net_epa,
            'home_net_epa': home_net_epa,
            'net_epa_difference': net_epa_difference
        }
        
        predictions.append(prediction_data)
        
        # Print analysis for this game
        print(f"\n{away_team} @ {home_team}:")
        print(f"  Spread: {favorite} {spread}")
        print(f"  Away Matchup EPA: Off({away_off:.3f}) + Def({home_def:.3f}) = {away_off_vs_home_def:.3f}")
        print(f"  Home Matchup EPA: Off({home_off:.3f}) + Def({away_def:.3f}) = {home_off_vs_away_def:.3f}")
        print(f"  Net Matchup Advantage: {net_matchup_advantage:.3f}")
        print(f"  Away Net EPA: {away_net_epa:.3f}")
        print(f"  Home Net EPA: {home_net_epa:.3f}")
        print(f"  Net EPA Difference: {net_epa_difference:.3f}")
    
    # Create predictions DataFrame
    predictions_df = pd.DataFrame(predictions)
    
    # Summary
    print(f"\n=== Model X Week 8 Analysis Summary ===")
    print(f"Total games: {len(predictions_df)}")
    print(f"Average Net Matchup Advantage: {predictions_df['net_matchup_advantage'].mean():.3f}")
    print(f"Average Net EPA Difference: {predictions_df['net_epa_difference'].mean():.3f}")
    
    # Find games with largest matchup advantages
    print(f"\nGames with Largest Matchup Advantages:")
    top_matchups = predictions_df.nlargest(3, 'net_matchup_advantage')
    for _, row in top_matchups.iterrows():
        print(f"  {row['game']}: {row['net_matchup_advantage']:.3f}")
    
    print(f"\nGames with Largest Matchup Disadvantages:")
    bottom_matchups = predictions_df.nsmallest(3, 'net_matchup_advantage')
    for _, row in bottom_matchups.iterrows():
        print(f"  {row['game']}: {row['net_matchup_advantage']:.3f}")
    
    # Save predictions
    output_path = 'models/model_x/model_x_week8_predictions.csv'
    os.makedirs('models/model_x', exist_ok=True)
    predictions_df.to_csv(output_path, index=False)
    print(f"\n✅ Model X predictions saved to: {output_path}")
    
    return predictions_df

if __name__ == "__main__":
    run_model_x_matchup_analysis()
