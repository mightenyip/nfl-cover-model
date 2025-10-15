#!/usr/bin/env python3
"""
Analyze Model A v2 performance against Week 6 actual results
"""

import pandas as pd

def analyze_model_a_v2_performance():
    """Compare Model A v2 predictions with actual Week 6 results"""
    
    # Model A v2 predictions
    model_a_v2_predictions = {
        'Eagles @ Giants': {'prediction': 'Cover', 'probability': 61.9, 'confidence': 'HIGH'},
        'Broncos @ Jets': {'prediction': 'Cover', 'probability': 52.5, 'confidence': 'MEDIUM'},
        'Cardinals @ Colts': {'prediction': 'No Cover', 'probability': 14.6, 'confidence': 'VERY_LOW'},
        'Chargers @ Dolphins': {'prediction': 'Cover', 'probability': 66.1, 'confidence': 'HIGH'},
        'Patriots @ Saints': {'prediction': 'Cover', 'probability': 64.4, 'confidence': 'HIGH'},
        'Browns @ Steelers': {'prediction': 'Cover', 'probability': 64.7, 'confidence': 'HIGH'},
        'Cowboys @ Panthers': {'prediction': 'No Cover', 'probability': 40.0, 'confidence': 'LOW'},
        'Seahawks @ Jaguars': {'prediction': 'No Cover', 'probability': 48.3, 'confidence': 'MEDIUM'},
        'Rams @ Ravens': {'prediction': 'No Cover', 'probability': 27.8, 'confidence': 'VERY_LOW'},
        'Titans @ Raiders': {'prediction': 'Cover', 'probability': 69.8, 'confidence': 'HIGH'},
        'Bengals @ Packers': {'prediction': 'No Cover', 'probability': 31.8, 'confidence': 'LOW'},
        '49ers @ Buccaneers': {'prediction': 'No Cover', 'probability': 45.7, 'confidence': 'MEDIUM'},
        'Lions @ Chiefs': {'prediction': 'Cover', 'probability': 85.2, 'confidence': 'VERY_HIGH'},
        'Bills @ Falcons': {'prediction': 'Cover', 'probability': 61.0, 'confidence': 'HIGH'},
        'Bears @ Commanders': {'prediction': 'Cover', 'probability': 69.0, 'confidence': 'HIGH'}
    }
    
    # Actual Week 6 results
    actual_results = {
        'Eagles @ Giants': {'underdog_covered': True, 'actual': 'Giants 34-17'},
        'Broncos @ Jets': {'underdog_covered': True, 'actual': 'Broncos 13-11'},
        'Cardinals @ Colts': {'underdog_covered': True, 'actual': 'Colts 31-27'},
        'Chargers @ Dolphins': {'underdog_covered': True, 'actual': 'Chargers 29-27'},
        'Patriots @ Saints': {'underdog_covered': True, 'actual': 'Patriots 28-17'},
        'Browns @ Steelers': {'underdog_covered': False, 'actual': 'Steelers 23-9'},
        'Cowboys @ Panthers': {'underdog_covered': True, 'actual': 'Panthers 30-27'},
        'Seahawks @ Jaguars': {'underdog_covered': True, 'actual': 'Seahawks 20-12'},
        'Rams @ Ravens': {'underdog_covered': False, 'actual': 'Rams 17-3'},
        'Titans @ Raiders': {'underdog_covered': False, 'actual': 'Raiders 20-10'},
        'Bengals @ Packers': {'underdog_covered': True, 'actual': 'Packers 27-18'},
        '49ers @ Buccaneers': {'underdog_covered': True, 'actual': 'Buccaneers 30-19'},
        'Lions @ Chiefs': {'underdog_covered': False, 'actual': 'Chiefs 30-17'},
        'Bills @ Falcons': {'underdog_covered': True, 'actual': 'Falcons 24-14'},
        'Bears @ Commanders': {'underdog_covered': True, 'actual': 'Bears 25-24'}
    }
    
    print("=== Model A v2 Performance Analysis ===")
    print("Enhanced EPA Model with 5-Tier Defense Classification")
    print("=" * 60)
    
    correct_predictions = 0
    total_games = len(model_a_v2_predictions)
    
    print(f"\nGame-by-Game Results:")
    print("-" * 80)
    
    for game, prediction in model_a_v2_predictions.items():
        actual = actual_results[game]
        predicted_cover = prediction['prediction'] == 'Cover'
        actual_cover = actual['underdog_covered']
        correct = predicted_cover == actual_cover
        
        if correct:
            correct_predictions += 1
        
        status = "✅" if correct else "❌"
        print(f"{game}")
        print(f"  Model A v2: {prediction['prediction']} ({prediction['probability']:.1f}%, {prediction['confidence']})")
        print(f"  Actual: {actual['actual']} | Underdog Covered: {actual_cover}")
        print(f"  Result: {status}")
        print()
    
    accuracy = (correct_predictions / total_games) * 100
    
    print(f"=== Model A v2 Performance Summary ===")
    print(f"Correct Predictions: {correct_predictions}/{total_games}")
    print(f"Accuracy: {accuracy:.1f}%")
    
    # Compare with other models
    print(f"\n=== Model Comparison (Week 6) ===")
    print(f"Model A (Original): 40.0% (6/15)")
    print(f"Model A v2 (Enhanced): {accuracy:.1f}% ({correct_predictions}/15)")
    print(f"Model B: 60.0% (9/15)")
    print(f"Model C: 26.7% (4/15)")
    print(f"Model D: 73.3% (11/15)")
    
    # Confidence level analysis
    print(f"\n=== Confidence Level Performance ===")
    confidence_results = {}
    
    for game, prediction in model_a_v2_predictions.items():
        actual = actual_results[game]
        predicted_cover = prediction['prediction'] == 'Cover'
        actual_cover = actual['underdog_covered']
        correct = predicted_cover == actual_cover
        
        conf = prediction['confidence']
        if conf not in confidence_results:
            confidence_results[conf] = {'correct': 0, 'total': 0}
        
        confidence_results[conf]['total'] += 1
        if correct:
            confidence_results[conf]['correct'] += 1
    
    for conf in ['VERY_HIGH', 'HIGH', 'MEDIUM', 'LOW', 'VERY_LOW']:
        if conf in confidence_results:
            stats = confidence_results[conf]
            accuracy = (stats['correct'] / stats['total']) * 100
            print(f"{conf}: {stats['correct']}/{stats['total']} ({accuracy:.1f}%)")
    
    return accuracy

if __name__ == "__main__":
    analyze_model_a_v2_performance()
