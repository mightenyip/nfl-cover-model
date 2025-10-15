#!/usr/bin/env python3
"""
Analyze Model A v2 patterns: why it was correct vs wrong
Focus on defense EPA numbers and probability adjustments
"""

import pandas as pd
import numpy as np

def analyze_model_a_v2_patterns():
    """Analyze why Model A v2 was correct vs wrong in Week 6"""
    
    print("=== Model A v2 Pattern Analysis ===")
    print("Analyzing why correct picks vs wrong picks")
    print("=" * 60)
    
    # Model A v2 predictions with defense data
    model_predictions = {
        'Eagles @ Giants': {
            'prediction': 'Cover', 'probability': 61.9, 'confidence': 'HIGH',
            'opponent_def_epa': -0.01, 'defense_quality': 'AVERAGE',
            'net_epa_diff': 0.036, 'spread': 7.5,
            'actual_result': 'Giants 34-17', 'underdog_covered': True, 'correct': True
        },
        'Broncos @ Jets': {
            'prediction': 'Cover', 'probability': 52.5, 'confidence': 'MEDIUM',
            'opponent_def_epa': -0.14, 'defense_quality': 'ELITE',
            'net_epa_diff': -0.268, 'spread': 7.5,
            'actual_result': 'Broncos 13-11', 'underdog_covered': True, 'correct': True
        },
        'Cardinals @ Colts': {
            'prediction': 'No Cover', 'probability': 14.6, 'confidence': 'VERY_LOW',
            'opponent_def_epa': -0.05, 'defense_quality': 'AVERAGE',
            'net_epa_diff': -0.546, 'spread': 6.5,
            'actual_result': 'Colts 31-27', 'underdog_covered': True, 'correct': False
        },
        'Chargers @ Dolphins': {
            'prediction': 'Cover', 'probability': 66.1, 'confidence': 'HIGH',
            'opponent_def_epa': -0.02, 'defense_quality': 'AVERAGE',
            'net_epa_diff': 0.118, 'spread': 4.5,
            'actual_result': 'Chargers 29-27', 'underdog_covered': True, 'correct': True
        },
        'Patriots @ Saints': {
            'prediction': 'Cover', 'probability': 64.4, 'confidence': 'HIGH',
            'opponent_def_epa': 0.04, 'defense_quality': 'AVERAGE',
            'net_epa_diff': 0.108, 'spread': 3.5,
            'actual_result': 'Patriots 28-17', 'underdog_covered': True, 'correct': True
        },
        'Browns @ Steelers': {
            'prediction': 'Cover', 'probability': 64.7, 'confidence': 'HIGH',
            'opponent_def_epa': -0.01, 'defense_quality': 'AVERAGE',
            'net_epa_diff': 0.096, 'spread': 5.0,
            'actual_result': 'Steelers 23-9', 'underdog_covered': False, 'correct': False
        },
        'Cowboys @ Panthers': {
            'prediction': 'No Cover', 'probability': 40.0, 'confidence': 'LOW',
            'opponent_def_epa': 0.18, 'defense_quality': 'POOR',
            'net_epa_diff': 0.028, 'spread': 3.5,
            'actual_result': 'Panthers 30-27', 'underdog_covered': True, 'correct': False
        },
        'Seahawks @ Jaguars': {
            'prediction': 'No Cover', 'probability': 48.3, 'confidence': 'MEDIUM',
            'opponent_def_epa': -0.07, 'defense_quality': 'STRONG',
            'net_epa_diff': -0.187, 'spread': 1.5,
            'actual_result': 'Seahawks 20-12', 'underdog_covered': True, 'correct': False
        },
        'Rams @ Ravens': {
            'prediction': 'No Cover', 'probability': 27.8, 'confidence': 'VERY_LOW',
            'opponent_def_epa': -0.08, 'defense_quality': 'STRONG',
            'net_epa_diff': -0.502, 'spread': 7.5,
            'actual_result': 'Rams 17-3', 'underdog_covered': False, 'correct': True
        },
        'Titans @ Raiders': {
            'prediction': 'Cover', 'probability': 69.8, 'confidence': 'HIGH',
            'opponent_def_epa': 0.00, 'defense_quality': 'AVERAGE',
            'net_epa_diff': 0.165, 'spread': 4.5,
            'actual_result': 'Raiders 20-10', 'underdog_covered': False, 'correct': False
        },
        'Bengals @ Packers': {
            'prediction': 'No Cover', 'probability': 31.8, 'confidence': 'LOW',
            'opponent_def_epa': 0.02, 'defense_quality': 'AVERAGE',
            'net_epa_diff': -0.410, 'spread': 14.5,
            'actual_result': 'Packers 27-18', 'underdog_covered': True, 'correct': False
        },
        '49ers @ Buccaneers': {
            'prediction': 'No Cover', 'probability': 45.7, 'confidence': 'MEDIUM',
            'opponent_def_epa': 0.01, 'defense_quality': 'AVERAGE',
            'net_epa_diff': -0.121, 'spread': 3.0,
            'actual_result': 'Buccaneers 30-19', 'underdog_covered': True, 'correct': False
        },
        'Lions @ Chiefs': {
            'prediction': 'Cover', 'probability': 85.2, 'confidence': 'VERY_HIGH',
            'opponent_def_epa': 0.01, 'defense_quality': 'AVERAGE',
            'net_epa_diff': 0.377, 'spread': 2.5,
            'actual_result': 'Chiefs 30-17', 'underdog_covered': False, 'correct': False
        },
        'Bills @ Falcons': {
            'prediction': 'Cover', 'probability': 61.0, 'confidence': 'HIGH',
            'opponent_def_epa': 0.03, 'defense_quality': 'AVERAGE',
            'net_epa_diff': 0.055, 'spread': 4.5,
            'actual_result': 'Falcons 24-14', 'underdog_covered': True, 'correct': True
        },
        'Bears @ Commanders': {
            'prediction': 'Cover', 'probability': 69.0, 'confidence': 'HIGH',
            'opponent_def_epa': 0.03, 'defense_quality': 'AVERAGE',
            'net_epa_diff': 0.155, 'spread': 4.5,
            'actual_result': 'Bears 25-24', 'underdog_covered': True, 'correct': True
        }
    }
    
    # Analyze patterns
    correct_picks = {k: v for k, v in model_predictions.items() if v['correct']}
    wrong_picks = {k: v for k, v in model_predictions.items() if not v['correct']}
    
    print(f"\n=== CORRECT PICKS ANALYSIS ({len(correct_picks)} games) ===")
    print("Defense Quality Distribution:")
    correct_defense_quality = [v['defense_quality'] for v in correct_picks.values()]
    for quality in ['ELITE', 'STRONG', 'AVERAGE', 'WEAK', 'POOR']:
        count = correct_defense_quality.count(quality)
        print(f"  {quality}: {count} games")
    
    print(f"\nAverage Opponent Defense EPA: {np.mean([v['opponent_def_epa'] for v in correct_picks.values()]):.3f}")
    print(f"Average Net EPA Diff: {np.mean([v['net_epa_diff'] for v in correct_picks.values()]):.3f}")
    print(f"Average Spread: {np.mean([v['spread'] for v in correct_picks.values()]):.1f}")
    
    print(f"\n=== WRONG PICKS ANALYSIS ({len(wrong_picks)} games) ===")
    print("Defense Quality Distribution:")
    wrong_defense_quality = [v['defense_quality'] for v in wrong_picks.values()]
    for quality in ['ELITE', 'STRONG', 'AVERAGE', 'WEAK', 'POOR']:
        count = wrong_defense_quality.count(quality)
        print(f"  {quality}: {count} games")
    
    print(f"\nAverage Opponent Defense EPA: {np.mean([v['opponent_def_epa'] for v in wrong_picks.values()]):.3f}")
    print(f"Average Net EPA Diff: {np.mean([v['net_epa_diff'] for v in wrong_picks.values()]):.3f}")
    print(f"Average Spread: {np.mean([v['spread'] for v in wrong_picks.values()]):.1f}")
    
    # Analyze by defense quality
    print(f"\n=== DEFENSE QUALITY PERFORMANCE ===")
    defense_performance = {}
    for game, data in model_predictions.items():
        quality = data['defense_quality']
        if quality not in defense_performance:
            defense_performance[quality] = {'correct': 0, 'total': 0}
        defense_performance[quality]['total'] += 1
        if data['correct']:
            defense_performance[quality]['correct'] += 1
    
    for quality in ['ELITE', 'STRONG', 'AVERAGE', 'WEAK', 'POOR']:
        if quality in defense_performance:
            stats = defense_performance[quality]
            accuracy = (stats['correct'] / stats['total']) * 100
            print(f"{quality}: {stats['correct']}/{stats['total']} ({accuracy:.1f}%)")
    
    # Analyze specific patterns
    print(f"\n=== KEY PATTERNS ===")
    
    # Pattern 1: ELITE defenses
    elite_games = {k: v for k, v in model_predictions.items() if v['defense_quality'] == 'ELITE'}
    print(f"\n1. ELITE Defense Games ({len(elite_games)}):")
    for game, data in elite_games.items():
        print(f"   {game}: {data['prediction']} ({data['probability']:.1f}%) - {'✅' if data['correct'] else '❌'}")
    
    # Pattern 2: STRONG defenses
    strong_games = {k: v for k, v in model_predictions.items() if v['defense_quality'] == 'STRONG'}
    print(f"\n2. STRONG Defense Games ({len(strong_games)}):")
    for game, data in strong_games.items():
        print(f"   {game}: {data['prediction']} ({data['probability']:.1f}%) - {'✅' if data['correct'] else '❌'}")
    
    # Pattern 3: POOR defenses
    poor_games = {k: v for k, v in model_predictions.items() if v['defense_quality'] == 'POOR'}
    print(f"\n3. POOR Defense Games ({len(poor_games)}):")
    for game, data in poor_games.items():
        print(f"   {game}: {data['prediction']} ({data['probability']:.1f}%) - {'✅' if data['correct'] else '❌'}")
    
    # Pattern 4: Large spreads
    large_spread_games = {k: v for k, v in model_predictions.items() if abs(v['spread']) >= 7.0}
    print(f"\n4. Large Spread Games (≥7 points) ({len(large_spread_games)}):")
    for game, data in large_spread_games.items():
        print(f"   {game}: {data['prediction']} ({data['probability']:.1f}%) - {'✅' if data['correct'] else '❌'}")
    
    # Recommendations
    print(f"\n=== RECOMMENDATIONS ===")
    print("Based on the analysis:")
    
    # Check if ELITE defense adjustment is too high
    elite_accuracy = defense_performance.get('ELITE', {'correct': 0, 'total': 0})
    if elite_accuracy['total'] > 0:
        elite_acc = (elite_accuracy['correct'] / elite_accuracy['total']) * 100
        print(f"1. ELITE Defense: {elite_acc:.1f}% accuracy - Current +18% adjustment may be too high")
    
    # Check if STRONG defense adjustment is appropriate
    strong_accuracy = defense_performance.get('STRONG', {'correct': 0, 'total': 0})
    if strong_accuracy['total'] > 0:
        strong_acc = (strong_accuracy['correct'] / strong_accuracy['total']) * 100
        print(f"2. STRONG Defense: {strong_acc:.1f}% accuracy - Current +12% adjustment may need tuning")
    
    # Check if POOR defense adjustment is appropriate
    poor_accuracy = defense_performance.get('POOR', {'correct': 0, 'total': 0})
    if poor_accuracy['total'] > 0:
        poor_acc = (poor_accuracy['correct'] / poor_accuracy['total']) * 100
        print(f"3. POOR Defense: {poor_acc:.1f}% accuracy - Current -15% adjustment may be too aggressive")
    
    print(f"\n4. Consider adjusting defense quality thresholds based on actual performance")
    print(f"5. Net EPA differential multiplier (0.8) may need adjustment")
    print(f"6. Spread adjustment (0.008) may need fine-tuning")

if __name__ == "__main__":
    analyze_model_a_v2_patterns()
