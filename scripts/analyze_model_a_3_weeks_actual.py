#!/usr/bin/env python3
"""
Analyze Model A performance over past 3 weeks (Weeks 4, 5, 6) using actual data
Look at underdog cover rates and accuracy patterns across multiple weeks
"""

import pandas as pd
import numpy as np

def analyze_model_a_3_weeks_actual():
    """Analyze Model A performance across Weeks 4, 5, and 6 using actual data"""
    
    print("=== Model A Performance Analysis - 3 Weeks (Actual Data) ===")
    print("Analyzing underdog cover rates and accuracy across Weeks 4, 5, 6")
    print("=" * 70)
    
    # Week 4 data (from actual results)
    week4_data = {
        'Seahawks @ Cardinals': {'prediction': 'Cover', 'underdog_covered': False, 'correct': False, 'spread': 1.5},
        'Vikings @ Steelers': {'prediction': 'Cover', 'underdog_covered': True, 'correct': True, 'spread': 2.5},
        'Commanders @ Falcons': {'prediction': 'Cover', 'underdog_covered': True, 'correct': True, 'spread': 1.5},
        'Saints @ Bills': {'prediction': 'No Cover', 'underdog_covered': False, 'correct': True, 'spread': 16.5},
        'Browns @ Lions': {'prediction': 'No Cover', 'underdog_covered': False, 'correct': True, 'spread': 8.5},
        'Titans @ Texans': {'prediction': 'No Cover', 'underdog_covered': False, 'correct': True, 'spread': 7.0},
        'Panthers @ Patriots': {'prediction': 'No Cover', 'underdog_covered': False, 'correct': True, 'spread': 5.5},
        'Chargers @ Giants': {'prediction': 'No Cover', 'underdog_covered': True, 'correct': False, 'spread': 6.5},
        'Eagles @ Buccaneers': {'prediction': 'Cover', 'underdog_covered': False, 'correct': False, 'spread': 3.5},
        'Colts @ Rams': {'prediction': 'Cover', 'underdog_covered': False, 'correct': False, 'spread': 3.5},
        'Jaguars @ 49ers': {'prediction': 'Cover', 'underdog_covered': True, 'correct': True, 'spread': 3.0},
        'Ravens @ Chiefs': {'prediction': 'No Cover', 'underdog_covered': False, 'correct': True, 'spread': 2.5},
        'Bears @ Raiders': {'prediction': 'No Cover', 'underdog_covered': True, 'correct': False, 'spread': 1.5},
        'Packers @ Cowboys': {'prediction': 'No Cover', 'underdog_covered': False, 'correct': True, 'spread': 7.0},
        'Jets @ Dolphins': {'prediction': 'Cover', 'underdog_covered': False, 'correct': False, 'spread': 2.5},
        'Bengals @ Broncos': {'prediction': 'Cover', 'underdog_covered': False, 'correct': False, 'spread': 7.0}
    }
    
    # Week 5 data (from actual results)
    week5_data = {
        '49ers @ Rams': {'prediction': 'Cover', 'underdog_covered': False, 'correct': False, 'spread': 5.5},
        'Vikings @ Browns': {'prediction': 'Cover', 'underdog_covered': False, 'correct': False, 'spread': 3.5},
        'Texans @ Ravens': {'prediction': 'Cover', 'underdog_covered': False, 'correct': False, 'spread': 2.5},
        'Dolphins @ Panthers': {'prediction': 'No Cover', 'underdog_covered': False, 'correct': True, 'spread': 1.5},
        'Raiders @ Colts': {'prediction': 'No Cover', 'underdog_covered': False, 'correct': True, 'spread': 6.5},
        'Giants @ Saints': {'prediction': 'No Cover', 'underdog_covered': False, 'correct': True, 'spread': 1.5},
        'Cowboys @ Jets': {'prediction': 'No Cover', 'underdog_covered': False, 'correct': True, 'spread': 2.5},
        'Broncos @ Eagles': {'prediction': 'Cover', 'underdog_covered': False, 'correct': False, 'spread': 3.5},
        'Titans @ Cardinals': {'prediction': 'No Cover', 'underdog_covered': False, 'correct': True, 'spread': 8.5},
        'Buccaneers @ Seahawks': {'prediction': 'Cover', 'underdog_covered': False, 'correct': False, 'spread': 3.5},
        'Lions @ Bengals': {'prediction': 'No Cover', 'underdog_covered': False, 'correct': True, 'spread': 10.5},
        'Commanders @ Chargers': {'prediction': 'Cover', 'underdog_covered': False, 'correct': False, 'spread': 2.5},
        'Patriots @ Bills': {'prediction': 'No Cover', 'underdog_covered': False, 'correct': True, 'spread': 8.0},
        'Chiefs @ Jaguars': {'prediction': 'Cover', 'underdog_covered': False, 'correct': False, 'spread': 3.5}
    }
    
    # Week 6 data (actual results from our analysis)
    week6_data = {
        'Eagles @ Giants': {'prediction': 'Cover', 'underdog_covered': True, 'correct': True, 'spread': 7.5},
        'Broncos @ Jets': {'prediction': 'Cover', 'underdog_covered': True, 'correct': True, 'spread': 7.5},
        'Cardinals @ Colts': {'prediction': 'No Cover', 'underdog_covered': True, 'correct': False, 'spread': 6.5},
        'Chargers @ Dolphins': {'prediction': 'Cover', 'underdog_covered': True, 'correct': True, 'spread': 4.5},
        'Patriots @ Saints': {'prediction': 'Cover', 'underdog_covered': True, 'correct': True, 'spread': 3.5},
        'Browns @ Steelers': {'prediction': 'Cover', 'underdog_covered': False, 'correct': False, 'spread': 5.0},
        'Cowboys @ Panthers': {'prediction': 'No Cover', 'underdog_covered': True, 'correct': False, 'spread': 3.5},
        'Seahawks @ Jaguars': {'prediction': 'No Cover', 'underdog_covered': True, 'correct': False, 'spread': 1.5},
        'Rams @ Ravens': {'prediction': 'No Cover', 'underdog_covered': False, 'correct': True, 'spread': 7.5},
        'Titans @ Raiders': {'prediction': 'Cover', 'underdog_covered': False, 'correct': False, 'spread': 4.5},
        'Bengals @ Packers': {'prediction': 'No Cover', 'underdog_covered': True, 'correct': False, 'spread': 14.5},
        '49ers @ Buccaneers': {'prediction': 'No Cover', 'underdog_covered': True, 'correct': False, 'spread': 3.0},
        'Lions @ Chiefs': {'prediction': 'Cover', 'underdog_covered': False, 'correct': False, 'spread': 2.5},
        'Bills @ Falcons': {'prediction': 'Cover', 'underdog_covered': True, 'correct': True, 'spread': 4.5},
        'Bears @ Commanders': {'prediction': 'Cover', 'underdog_covered': True, 'correct': True, 'spread': 4.5}
    }
    
    # Combine all weeks
    all_weeks = {
        'Week 4': week4_data,
        'Week 5': week5_data, 
        'Week 6': week6_data
    }
    
    # Analyze each week
    weekly_stats = {}
    
    for week, data in all_weeks.items():
        total_games = len(data)
        correct_picks = sum(1 for v in data.values() if v['correct'])
        underdog_covers = sum(1 for v in data.values() if v['underdog_covered'])
        
        # Separate by prediction type
        cover_predictions = {k: v for k, v in data.items() if v['prediction'] == 'Cover'}
        no_cover_predictions = {k: v for k, v in data.items() if v['prediction'] == 'No Cover'}
        
        cover_correct = sum(1 for v in cover_predictions.values() if v['correct'])
        no_cover_correct = sum(1 for v in no_cover_predictions.values() if v['correct'])
        
        cover_underdog_covers = sum(1 for v in cover_predictions.values() if v['underdog_covered'])
        no_cover_underdog_covers = sum(1 for v in no_cover_predictions.values() if v['underdog_covered'])
        
        weekly_stats[week] = {
            'total_games': total_games,
            'correct_picks': correct_picks,
            'accuracy': (correct_picks / total_games) * 100,
            'underdog_covers': underdog_covers,
            'underdog_cover_rate': (underdog_covers / total_games) * 100,
            'cover_predictions': len(cover_predictions),
            'cover_correct': cover_correct,
            'cover_accuracy': (cover_correct / len(cover_predictions)) * 100 if cover_predictions else 0,
            'cover_underdog_covers': cover_underdog_covers,
            'cover_underdog_rate': (cover_underdog_covers / len(cover_predictions)) * 100 if cover_predictions else 0,
            'no_cover_predictions': len(no_cover_predictions),
            'no_cover_correct': no_cover_correct,
            'no_cover_accuracy': (no_cover_correct / len(no_cover_predictions)) * 100 if no_cover_predictions else 0,
            'no_cover_underdog_covers': no_cover_underdog_covers,
            'no_cover_underdog_rate': (no_cover_underdog_covers / len(no_cover_predictions)) * 100 if no_cover_predictions else 0
        }
    
    # Print weekly analysis
    for week, stats in weekly_stats.items():
        print(f"\n=== {week.upper()} ANALYSIS ===")
        print(f"Total Games: {stats['total_games']}")
        print(f"Model Accuracy: {stats['correct_picks']}/{stats['total_games']} ({stats['accuracy']:.1f}%)")
        print(f"Underdog Cover Rate: {stats['underdog_covers']}/{stats['total_games']} ({stats['underdog_cover_rate']:.1f}%)")
        print(f"'Cover' Predictions: {stats['cover_correct']}/{stats['cover_predictions']} ({stats['cover_accuracy']:.1f}%)")
        print(f"  - Underdogs Actually Covered: {stats['cover_underdog_covers']}/{stats['cover_predictions']} ({stats['cover_underdog_rate']:.1f}%)")
        print(f"'No Cover' Predictions: {stats['no_cover_correct']}/{stats['no_cover_predictions']} ({stats['no_cover_accuracy']:.1f}%)")
        print(f"  - Underdogs Actually Covered: {stats['no_cover_underdog_covers']}/{stats['no_cover_predictions']} ({stats['no_cover_underdog_rate']:.1f}%)")
    
    # Overall 3-week analysis
    print(f"\n=== OVERALL 3-WEEK ANALYSIS ===")
    
    total_games = sum(stats['total_games'] for stats in weekly_stats.values())
    total_correct = sum(stats['correct_picks'] for stats in weekly_stats.values())
    total_underdog_covers = sum(stats['underdog_covers'] for stats in weekly_stats.values())
    
    total_cover_predictions = sum(stats['cover_predictions'] for stats in weekly_stats.values())
    total_cover_correct = sum(stats['cover_correct'] for stats in weekly_stats.values())
    total_cover_underdog_covers = sum(stats['cover_underdog_covers'] for stats in weekly_stats.values())
    
    total_no_cover_predictions = sum(stats['no_cover_predictions'] for stats in weekly_stats.values())
    total_no_cover_correct = sum(stats['no_cover_correct'] for stats in weekly_stats.values())
    total_no_cover_underdog_covers = sum(stats['no_cover_underdog_covers'] for stats in weekly_stats.values())
    
    overall_accuracy = (total_correct / total_games) * 100
    overall_underdog_rate = (total_underdog_covers / total_games) * 100
    cover_accuracy = (total_cover_correct / total_cover_predictions) * 100 if total_cover_predictions > 0 else 0
    no_cover_accuracy = (total_no_cover_correct / total_no_cover_predictions) * 100 if total_no_cover_predictions > 0 else 0
    
    print(f"Total Games: {total_games}")
    print(f"Overall Model Accuracy: {total_correct}/{total_games} ({overall_accuracy:.1f}%)")
    print(f"Overall Underdog Cover Rate: {total_underdog_covers}/{total_games} ({overall_underdog_rate:.1f}%)")
    print(f"'Cover' Predictions Accuracy: {total_cover_correct}/{total_cover_predictions} ({cover_accuracy:.1f}%)")
    print(f"'No Cover' Predictions Accuracy: {total_no_cover_correct}/{total_no_cover_predictions} ({no_cover_accuracy:.1f}%)")
    
    # Pattern analysis
    print(f"\n=== PATTERN ANALYSIS (3 Weeks) ===")
    
    if cover_accuracy > no_cover_accuracy:
        print("✅ Model is better at identifying underdog covers than favorite covers")
        print("   - Suggests good underdog identification")
        print("   - But struggles with favorite identification")
    elif no_cover_accuracy > cover_accuracy:
        print("✅ Model is better at identifying favorite covers than underdog covers")
        print("   - Suggests good favorite identification")
        print("   - But struggles with underdog identification")
    else:
        print("⚖️ Model accuracy is similar for both prediction types")
        print("   - Suggests balanced approach")
        print("   - But may need overall improvement")
    
    # Week-by-week trends
    print(f"\n=== WEEK-BY-WEEK TRENDS ===")
    for week, stats in weekly_stats.items():
        trend = "📈" if stats['underdog_cover_rate'] > 50 else "📉" if stats['underdog_cover_rate'] < 50 else "⚖️"
        print(f"{week}: {stats['underdog_cover_rate']:.1f}% underdog cover rate {trend}")
        print(f"  Model Accuracy: {stats['accuracy']:.1f}%")
        print(f"  'Cover' Accuracy: {stats['cover_accuracy']:.1f}%")
        print(f"  'No Cover' Accuracy: {stats['no_cover_accuracy']:.1f}%")
    
    # Key insights
    print(f"\n=== KEY INSIGHTS (3 Weeks) ===")
    print(f"1. Overall Model Accuracy: {overall_accuracy:.1f}%")
    print(f"2. Overall Underdog Cover Rate: {overall_underdog_rate:.1f}%")
    print(f"3. 'Cover' Predictions Accuracy: {cover_accuracy:.1f}%")
    print(f"4. 'No Cover' Predictions Accuracy: {no_cover_accuracy:.1f}%")
    
    if overall_underdog_rate > 50:
        print(f"\n📈 Underdog-heavy period: {overall_underdog_rate:.1f}% of underdogs covered")
        if cover_accuracy > no_cover_accuracy:
            print("✅ Model adapted well to underdog-heavy period")
        else:
            print("❌ Model struggled in underdog-heavy period")
    else:
        print(f"\n📉 Favorite-heavy period: {100-overall_underdog_rate:.1f}% of favorites covered")
        if no_cover_accuracy > cover_accuracy:
            print("✅ Model adapted well to favorite-heavy period")
        else:
            print("❌ Model struggled in favorite-heavy period")
    
    return weekly_stats

if __name__ == "__main__":
    analyze_model_a_3_weeks_actual()
