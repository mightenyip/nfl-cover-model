#!/usr/bin/env python3
"""
Week 3 Corrected Analysis
Recalculates Week 3 results with correct spread logic
"""

import pandas as pd
import numpy as np

def recalculate_week3_results():
    """Recalculate Week 3 results with correct spread logic"""
    
    print("=== Week 3 Corrected Analysis ===")
    print("Recalculating Week 3 results with correct spread logic")
    print("=" * 60)
    
    # Week 3 games with correct calculations
    week3_games = [
        {
            'game': 'Dolphins @ Bills',
            'favorite': 'Bills',
            'underdog': 'Dolphins',
            'spread': 12.5,
            'final_score': 'BUF 48 - MIA 20',
            'favorite_score': 48,
            'underdog_score': 20,
            'margin': 28,
            'underdog_covered': False,  # 28 > 12.5
            'winner': 'Bills'
        },
        {
            'game': 'Falcons @ Panthers',
            'favorite': 'Falcons',
            'underdog': 'Panthers',
            'spread': 5.5,
            'final_score': 'ATL 37 - CAR 34',
            'favorite_score': 37,
            'underdog_score': 34,
            'margin': 3,
            'underdog_covered': True,  # 3 < 5.5
            'winner': 'Panthers'
        },
        {
            'game': 'Packers @ Browns',
            'favorite': 'Packers',
            'underdog': 'Browns',
            'spread': 8.5,
            'final_score': 'GB 31 - CLE 17',
            'favorite_score': 31,
            'underdog_score': 17,
            'margin': 14,
            'underdog_covered': False,  # 14 > 8.5
            'winner': 'Packers'
        },
        {
            'game': 'Texans @ Jaguars',
            'favorite': 'Jaguars',
            'underdog': 'Texans',
            'spread': 1.5,
            'final_score': 'JAX 37 - HOU 17',
            'favorite_score': 37,
            'underdog_score': 17,
            'margin': 20,
            'underdog_covered': False,  # 20 > 1.5
            'winner': 'Jaguars'
        },
        {
            'game': 'Bengals @ Vikings',
            'favorite': 'Vikings',
            'underdog': 'Bengals',
            'spread': 3.0,
            'final_score': 'MIN 24 - CIN 21',
            'favorite_score': 24,
            'underdog_score': 21,
            'margin': 3,
            'underdog_covered': True,  # 3 = 3.0 (tie, so underdog covers)
            'winner': 'Vikings'
        },
        {
            'game': 'Steelers @ Patriots',
            'favorite': 'Steelers',
            'underdog': 'Patriots',
            'spread': 1.5,
            'final_score': 'NE 17 - PIT 14',
            'favorite_score': 14,
            'underdog_score': 17,
            'margin': -3,  # Underdog won outright
            'underdog_covered': True,  # Underdog won
            'winner': 'Patriots'
        },
        {
            'game': 'Rams @ Eagles',
            'favorite': 'Eagles',
            'underdog': 'Rams',
            'spread': 3.5,
            'final_score': 'PHI 37 - LA 31',
            'favorite_score': 37,
            'underdog_score': 31,
            'margin': 6,
            'underdog_covered': False,  # 6 > 3.5
            'winner': 'Eagles'
        },
        {
            'game': 'Jets @ Buccaneers',
            'favorite': 'Buccaneers',
            'underdog': 'Jets',
            'spread': 7.0,
            'final_score': 'TB 13 - NYJ 12',
            'favorite_score': 13,
            'underdog_score': 12,
            'margin': 1,
            'underdog_covered': True,  # 1 < 7.0
            'winner': 'Buccaneers'
        },
        {
            'game': 'Colts @ Titans',
            'favorite': 'Colts',
            'underdog': 'Titans',
            'spread': 3.5,
            'final_score': 'IND 23 - TEN 16',
            'favorite_score': 23,
            'underdog_score': 16,
            'margin': 7,
            'underdog_covered': False,  # 7 > 3.5
            'winner': 'Colts'
        },
        {
            'game': 'Raiders @ Commanders',
            'favorite': 'Commanders',
            'underdog': 'Raiders',
            'spread': 3.5,
            'final_score': 'WAS 30 - LV 24',
            'favorite_score': 30,
            'underdog_score': 24,
            'margin': 6,
            'underdog_covered': False,  # 6 > 3.5
            'winner': 'Commanders'
        },
        {
            'game': 'Broncos @ Chargers',
            'favorite': 'Chargers',
            'underdog': 'Broncos',
            'spread': 2.5,
            'final_score': 'LAC 24 - DEN 17',
            'favorite_score': 24,
            'underdog_score': 17,
            'margin': 7,
            'underdog_covered': False,  # 7 > 2.5
            'winner': 'Chargers'
        },
        {
            'game': 'Saints @ Seahawks',
            'favorite': 'Seahawks',
            'underdog': 'Saints',
            'spread': 7.5,
            'final_score': 'SEA 37 - NO 31',
            'favorite_score': 37,
            'underdog_score': 31,
            'margin': 6,
            'underdog_covered': True,  # 6 < 7.5
            'winner': 'Saints'
        },
        {
            'game': 'Cowboys @ Bears',
            'favorite': 'Bears',
            'underdog': 'Cowboys',
            'spread': 1.5,
            'final_score': 'CHI 28 - DAL 13',
            'favorite_score': 28,
            'underdog_score': 13,
            'margin': 15,
            'underdog_covered': False,  # 15 > 1.5
            'winner': 'Bears'
        },
        {
            'game': 'Cardinals @ 49ers',
            'favorite': '49ers',
            'underdog': 'Cardinals',
            'spread': 1.5,
            'final_score': 'SF 35 - ARI 16',
            'favorite_score': 35,
            'underdog_score': 16,
            'margin': 19,
            'underdog_covered': False,  # 19 > 1.5
            'winner': '49ers'
        },
        {
            'game': 'Chiefs @ Giants',
            'favorite': 'Chiefs',
            'underdog': 'Giants',
            'spread': 6.5,
            'final_score': 'KC 34 - NYG 12',
            'favorite_score': 34,
            'underdog_score': 12,
            'margin': 22,
            'underdog_covered': False,  # 22 > 6.5
            'winner': 'Chiefs'
        },
        {
            'game': 'Lions @ Ravens',
            'favorite': 'Ravens',
            'underdog': 'Lions',
            'spread': 5.5,
            'final_score': 'DET 38 - BAL 30',
            'favorite_score': 30,
            'underdog_score': 38,
            'margin': -8,  # Underdog won outright
            'underdog_covered': True,  # Underdog won
            'winner': 'Lions'
        }
    ]
    
    # Model A predictions (from the original data)
    model_a_predictions = {
        'Dolphins @ Bills': 'Cover',
        'Falcons @ Panthers': 'No Cover',
        'Packers @ Browns': 'Cover',
        'Texans @ Jaguars': 'Cover',
        'Bengals @ Vikings': 'Cover',
        'Steelers @ Patriots': 'Cover',
        'Rams @ Eagles': 'Cover',
        'Jets @ Buccaneers': 'Cover',
        'Colts @ Titans': 'Cover',
        'Raiders @ Commanders': 'Cover',
        'Broncos @ Chargers': 'Cover',
        'Saints @ Seahawks': 'Cover',
        'Cowboys @ Bears': 'Cover',
        'Cardinals @ 49ers': 'Cover',
        'Chiefs @ Giants': 'Cover',
        'Lions @ Ravens': 'Cover'
    }
    
    # Calculate Model A performance with corrected results
    print(f"\n=== CORRECTED Week 3 Results ===")
    print(f"{'Game':<25} {'Underdog':<10} {'Spread':<8} {'Score':<15} {'Margin':<8} {'Cover':<6} {'Model A':<10} {'Correct':<8}")
    print("-" * 100)
    
    correct_predictions = 0
    total_games = len(week3_games)
    underdog_covers = 0
    
    for game in week3_games:
        game_name = game['game']
        underdog = game['underdog']
        spread = game['spread']
        score = game['final_score']
        margin = game['margin']
        covered = game['underdog_covered']
        model_pred = model_a_predictions[game_name]
        
        # Check if Model A was correct
        model_correct = (model_pred == 'Cover' and covered) or (model_pred == 'No Cover' and not covered)
        if model_correct:
            correct_predictions += 1
        
        if covered:
            underdog_covers += 1
        
        cover_text = "Yes" if covered else "No"
        correct_text = "✅" if model_correct else "❌"
        
        print(f"{game_name:<25} {underdog:<10} +{spread:<7} {score:<15} {margin:<8} {cover_text:<6} {model_pred:<10} {correct_text:<8}")
    
    # Calculate statistics
    accuracy = correct_predictions / total_games
    underdog_cover_rate = underdog_covers / total_games
    
    print(f"\n=== CORRECTED Week 3 Summary ===")
    print(f"Total Games: {total_games}")
    print(f"Underdog Covers: {underdog_covers}/{total_games} ({underdog_cover_rate:.1%})")
    print(f"Model A Accuracy: {correct_predictions}/{total_games} ({accuracy:.1%})")
    
    # Compare with original incorrect data
    print(f"\n=== Comparison with Original (Incorrect) Data ===")
    print(f"Original showed: 6/16 underdog covers (37.5%)")
    print(f"Corrected shows: {underdog_covers}/{total_games} underdog covers ({underdog_cover_rate:.1%})")
    print(f"Original showed: Model A 5/16 correct (31.2%)")
    print(f"Corrected shows: Model A {correct_predictions}/{total_games} correct ({accuracy:.1%})")
    
    # Analyze Model A's prediction pattern
    cover_predictions = sum(1 for pred in model_a_predictions.values() if pred == 'Cover')
    no_cover_predictions = sum(1 for pred in model_a_predictions.values() if pred == 'No Cover')
    
    cover_correct = sum(1 for game in week3_games 
                       if model_a_predictions[game['game']] == 'Cover' and game['underdog_covered'])
    no_cover_correct = sum(1 for game in week3_games 
                          if model_a_predictions[game['game']] == 'No Cover' and not game['underdog_covered'])
    
    print(f"\n=== Model A Prediction Breakdown ===")
    print(f"'Cover' Predictions: {cover_correct}/{cover_predictions} correct ({cover_correct/cover_predictions:.1%})")
    print(f"'No Cover' Predictions: {no_cover_correct}/{no_cover_predictions} correct ({no_cover_correct/no_cover_predictions:.1%})")
    
    return {
        'total_games': total_games,
        'underdog_covers': underdog_covers,
        'underdog_cover_rate': underdog_cover_rate,
        'model_a_correct': correct_predictions,
        'model_a_accuracy': accuracy,
        'cover_predictions': cover_predictions,
        'cover_correct': cover_correct,
        'no_cover_predictions': no_cover_predictions,
        'no_cover_correct': no_cover_correct
    }

if __name__ == "__main__":
    recalculate_week3_results()
