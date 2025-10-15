#!/usr/bin/env python3
"""
Analyze underdog cover rates for Model A v2's correct vs wrong picks
"""

def analyze_underdog_cover_rates():
    """Analyze underdog cover rates for correct vs wrong picks"""
    
    print("=== Model A v2 Underdog Cover Rate Analysis ===")
    print("Analyzing underdog cover rates for correct vs wrong picks")
    print("=" * 60)
    
    # Model A v2 predictions with actual results
    model_data = {
        'Eagles @ Giants': {
            'prediction': 'Cover', 'probability': 61.9, 'confidence': 'HIGH',
            'underdog_covered': True, 'correct': True, 'spread': 7.5
        },
        'Broncos @ Jets': {
            'prediction': 'Cover', 'probability': 52.5, 'confidence': 'MEDIUM',
            'underdog_covered': True, 'correct': True, 'spread': 7.5
        },
        'Cardinals @ Colts': {
            'prediction': 'No Cover', 'probability': 14.6, 'confidence': 'VERY_LOW',
            'underdog_covered': True, 'correct': False, 'spread': 6.5
        },
        'Chargers @ Dolphins': {
            'prediction': 'Cover', 'probability': 66.1, 'confidence': 'HIGH',
            'underdog_covered': True, 'correct': True, 'spread': 4.5
        },
        'Patriots @ Saints': {
            'prediction': 'Cover', 'probability': 64.4, 'confidence': 'HIGH',
            'underdog_covered': True, 'correct': True, 'spread': 3.5
        },
        'Browns @ Steelers': {
            'prediction': 'Cover', 'probability': 64.7, 'confidence': 'HIGH',
            'underdog_covered': False, 'correct': False, 'spread': 5.0
        },
        'Cowboys @ Panthers': {
            'prediction': 'No Cover', 'probability': 40.0, 'confidence': 'LOW',
            'underdog_covered': True, 'correct': False, 'spread': 3.5
        },
        'Seahawks @ Jaguars': {
            'prediction': 'No Cover', 'probability': 48.3, 'confidence': 'MEDIUM',
            'underdog_covered': True, 'correct': False, 'spread': 1.5
        },
        'Rams @ Ravens': {
            'prediction': 'No Cover', 'probability': 27.8, 'confidence': 'VERY_LOW',
            'underdog_covered': False, 'correct': True, 'spread': 7.5
        },
        'Titans @ Raiders': {
            'prediction': 'Cover', 'probability': 69.8, 'confidence': 'HIGH',
            'underdog_covered': False, 'correct': False, 'spread': 4.5
        },
        'Bengals @ Packers': {
            'prediction': 'No Cover', 'probability': 31.8, 'confidence': 'LOW',
            'underdog_covered': True, 'correct': False, 'spread': 14.5
        },
        '49ers @ Buccaneers': {
            'prediction': 'No Cover', 'probability': 45.7, 'confidence': 'MEDIUM',
            'underdog_covered': True, 'correct': False, 'spread': 3.0
        },
        'Lions @ Chiefs': {
            'prediction': 'Cover', 'probability': 85.2, 'confidence': 'VERY_HIGH',
            'underdog_covered': False, 'correct': False, 'spread': 2.5
        },
        'Bills @ Falcons': {
            'prediction': 'Cover', 'probability': 61.0, 'confidence': 'HIGH',
            'underdog_covered': True, 'correct': True, 'spread': 4.5
        },
        'Bears @ Commanders': {
            'prediction': 'Cover', 'probability': 69.0, 'confidence': 'HIGH',
            'underdog_covered': True, 'correct': True, 'spread': 4.5
        }
    }
    
    # Separate correct and wrong picks
    correct_picks = {k: v for k, v in model_data.items() if v['correct']}
    wrong_picks = {k: v for k, v in model_data.items() if not v['correct']}
    
    print(f"\n=== CORRECT PICKS ANALYSIS ({len(correct_picks)} games) ===")
    print("Underdog Cover Rate for Correct Picks:")
    
    correct_underdog_covers = sum(1 for v in correct_picks.values() if v['underdog_covered'])
    correct_total = len(correct_picks)
    correct_cover_rate = (correct_underdog_covers / correct_total) * 100
    
    print(f"Underdogs Covered: {correct_underdog_covers}/{correct_total} ({correct_cover_rate:.1f}%)")
    
    print(f"\nCorrect Picks Details:")
    for game, data in correct_picks.items():
        cover_status = "✅ COVERED" if data['underdog_covered'] else "❌ NO COVER"
        print(f"  {game}: {cover_status} (Spread: {data['spread']})")
    
    print(f"\n=== WRONG PICKS ANALYSIS ({len(wrong_picks)} games) ===")
    print("Underdog Cover Rate for Wrong Picks:")
    
    wrong_underdog_covers = sum(1 for v in wrong_picks.values() if v['underdog_covered'])
    wrong_total = len(wrong_picks)
    wrong_cover_rate = (wrong_underdog_covers / wrong_total) * 100
    
    print(f"Underdogs Covered: {wrong_underdog_covers}/{wrong_total} ({wrong_cover_rate:.1f}%)")
    
    print(f"\nWrong Picks Details:")
    for game, data in wrong_picks.items():
        cover_status = "✅ COVERED" if data['underdog_covered'] else "❌ NO COVER"
        prediction = data['prediction']
        print(f"  {game}: {cover_status} (Predicted: {prediction}, Spread: {data['spread']})")
    
    # Analyze by prediction type
    print(f"\n=== ANALYSIS BY PREDICTION TYPE ===")
    
    # Games where model predicted "Cover"
    cover_predictions = {k: v for k, v in model_data.items() if v['prediction'] == 'Cover'}
    cover_correct = sum(1 for v in cover_predictions.values() if v['correct'])
    cover_total = len(cover_predictions)
    cover_accuracy = (cover_correct / cover_total) * 100 if cover_total > 0 else 0
    
    print(f"\n'Cover' Predictions ({cover_total} games):")
    print(f"  Correct: {cover_correct}/{cover_total} ({cover_accuracy:.1f}%)")
    
    cover_underdog_covers = sum(1 for v in cover_predictions.values() if v['underdog_covered'])
    cover_cover_rate = (cover_underdog_covers / cover_total) * 100 if cover_total > 0 else 0
    print(f"  Underdogs Actually Covered: {cover_underdog_covers}/{cover_total} ({cover_cover_rate:.1f}%)")
    
    # Games where model predicted "No Cover"
    no_cover_predictions = {k: v for k, v in model_data.items() if v['prediction'] == 'No Cover'}
    no_cover_correct = sum(1 for v in no_cover_predictions.values() if v['correct'])
    no_cover_total = len(no_cover_predictions)
    no_cover_accuracy = (no_cover_correct / no_cover_total) * 100 if no_cover_total > 0 else 0
    
    print(f"\n'No Cover' Predictions ({no_cover_total} games):")
    print(f"  Correct: {no_cover_correct}/{no_cover_total} ({no_cover_accuracy:.1f}%)")
    
    no_cover_underdog_covers = sum(1 for v in no_cover_predictions.values() if v['underdog_covered'])
    no_cover_cover_rate = (no_cover_underdog_covers / no_cover_total) * 100 if no_cover_total > 0 else 0
    print(f"  Underdogs Actually Covered: {no_cover_underdog_covers}/{no_cover_total} ({no_cover_cover_rate:.1f}%)")
    
    # Overall Week 6 underdog cover rate
    total_underdog_covers = sum(1 for v in model_data.values() if v['underdog_covered'])
    total_games = len(model_data)
    overall_cover_rate = (total_underdog_covers / total_games) * 100
    
    print(f"\n=== OVERALL WEEK 6 UNDERDOG COVER RATE ===")
    print(f"Total Underdogs Covered: {total_underdog_covers}/{total_games} ({overall_cover_rate:.1f}%)")
    
    # Key insights
    print(f"\n=== KEY INSIGHTS ===")
    print(f"1. Correct Picks Underdog Cover Rate: {correct_cover_rate:.1f}%")
    print(f"2. Wrong Picks Underdog Cover Rate: {wrong_cover_rate:.1f}%")
    print(f"3. Overall Week 6 Underdog Cover Rate: {overall_cover_rate:.1f}%")
    print(f"4. 'Cover' Predictions Accuracy: {cover_accuracy:.1f}%")
    print(f"5. 'No Cover' Predictions Accuracy: {no_cover_accuracy:.1f}%")
    
    if correct_cover_rate > wrong_cover_rate:
        print(f"\n✅ Model was more accurate when underdogs actually covered")
    elif wrong_cover_rate > correct_cover_rate:
        print(f"\n❌ Model was more accurate when underdogs didn't cover")
    else:
        print(f"\n⚖️ Model accuracy was similar regardless of underdog cover rate")
    
    # Analyze the pattern
    print(f"\n=== PATTERN ANALYSIS ===")
    if correct_cover_rate > wrong_cover_rate:
        print("Model A v2 was more accurate when underdogs covered, suggesting:")
        print("- Model has good underdog identification")
        print("- But struggles when favorites cover")
        print("- May need better favorite identification logic")
    elif wrong_cover_rate > correct_cover_rate:
        print("Model A v2 was more accurate when underdogs didn't cover, suggesting:")
        print("- Model has good favorite identification")
        print("- But struggles with underdog identification")
        print("- May need more aggressive underdog bias")
    else:
        print("Model A v2 accuracy was similar regardless of outcome, suggesting:")
        print("- Model is well-balanced")
        print("- But may need overall improvement")

if __name__ == "__main__":
    analyze_underdog_cover_rates()
