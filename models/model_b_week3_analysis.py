#!/usr/bin/env python3
"""
Model B Week 3 Performance Analysis
"""

import pandas as pd

def analyze_model_b_week3():
    """Analyze Model B's Week 3 performance against actual results"""
    
    print("=== Model B Week 3 Performance Analysis ===")
    
    # Load Model B predictions
    model_b = pd.read_csv("model_b/model_b_week3_predictions.csv")
    
    # Actual Week 3 results (from performance summary)
    actual_results = {
        ('Dolphins', 'Bills'): {'spread': 12.5, 'underdog': 'Dolphins', 'actual_cover': True},
        ('Falcons', 'Panthers'): {'spread': 5.5, 'underdog': 'Panthers', 'actual_cover': True},
        ('Packers', 'Browns'): {'spread': 8.5, 'underdog': 'Browns', 'actual_cover': True},
        ('Texans', 'Jaguars'): {'spread': 1.5, 'underdog': 'Texans', 'actual_cover': False},
        ('Bengals', 'Vikings'): {'spread': 3.0, 'underdog': 'Bengals', 'actual_cover': False},
        ('Steelers', 'Patriots'): {'spread': 1.5, 'underdog': 'Patriots', 'actual_cover': False},
        ('Rams', 'Eagles'): {'spread': 3.5, 'underdog': 'Rams', 'actual_cover': False},
        ('Jets', 'Buccaneers'): {'spread': 7.0, 'underdog': 'Jets', 'actual_cover': True},
        ('Colts', 'Titans'): {'spread': 3.5, 'underdog': 'Titans', 'actual_cover': False},
        ('Raiders', 'Commanders'): {'spread': 3.5, 'underdog': 'Raiders', 'actual_cover': False},
        ('Broncos', 'Chargers'): {'spread': 2.5, 'underdog': 'Broncos', 'actual_cover': False},
        ('Saints', 'Seahawks'): {'spread': 7.5, 'underdog': 'Saints', 'actual_cover': False},
        ('Cowboys', 'Bears'): {'spread': 1.5, 'underdog': 'Cowboys', 'actual_cover': False},
        ('Cardinals', '49ers'): {'spread': 1.5, 'underdog': 'Cardinals', 'actual_cover': True},
        ('Chiefs', 'Giants'): {'spread': 6.5, 'underdog': 'Giants', 'actual_cover': False},
        ('Lions', 'Ravens'): {'spread': 5.5, 'underdog': 'Lions', 'actual_cover': True}
    }
    
    # Add actual results to Model B data
    model_b['actual_cover'] = model_b.apply(
        lambda row: actual_results.get((row['away_team'], row['home_team']), {}).get('actual_cover', None), 
        axis=1
    )
    
    # Calculate correctness
    model_b['model_correct'] = model_b['predicted_cover'] == model_b['actual_cover']
    
    # Overall performance
    total_games = len(model_b)
    correct_predictions = model_b['model_correct'].sum()
    accuracy = correct_predictions / total_games
    
    print(f"\n=== Overall Performance ===")
    print(f"Total Games: {total_games}")
    print(f"Correct Predictions: {correct_predictions}")
    print(f"Accuracy: {accuracy:.1%}")
    print(f"Incorrect Predictions: {total_games - correct_predictions}")
    
    # Game-by-game analysis
    print(f"\n=== Game-by-Game Analysis ===")
    print(f"{'Game':<25} {'Underdog':<10} {'Spread':<8} {'Predicted':<10} {'Actual':<8} {'Correct':<8} {'Confidence':<12}")
    print("-" * 85)
    
    for _, row in model_b.iterrows():
        game = f"{row['away_team']} @ {row['home_team']}"
        underdog = row['underdog_team']
        spread = f"+{row['spread_line']}"
        predicted = "Cover" if row['predicted_cover'] else "No Cover"
        actual = "Cover" if row['actual_cover'] else "No Cover"
        correct = "✅" if row['model_correct'] else "❌"
        confidence = row['confidence']
        
        print(f"{game:<25} {underdog:<10} {spread:<8} {predicted:<10} {actual:<8} {correct:<8} {confidence:<12}")
    
    # Performance by confidence level
    print(f"\n=== Performance by Confidence Level ===")
    confidence_performance = model_b.groupby('confidence').agg({
        'model_correct': ['count', 'sum', 'mean']
    }).round(3)
    
    for conf in ['VERY_HIGH', 'HIGH', 'MEDIUM', 'LOW', 'VERY_LOW']:
        conf_data = model_b[model_b['confidence'] == conf]
        if not conf_data.empty:
            total = len(conf_data)
            correct = conf_data['model_correct'].sum()
            accuracy = correct / total if total > 0 else 0
            print(f"{conf}: {correct}/{total} correct ({accuracy:.1%})")
    
    # Very High Confidence Analysis
    print(f"\n=== Very High Confidence Games Analysis ===")
    very_high = model_b[model_b['confidence'] == 'VERY_HIGH']
    if not very_high.empty:
        for _, row in very_high.iterrows():
            game = f"{row['away_team']} @ {row['home_team']}"
            underdog = row['underdog_team']
            spread = f"+{row['spread_line']}"
            predicted = "Cover" if row['predicted_cover'] else "No Cover"
            actual = "Cover" if row['actual_cover'] else "No Cover"
            correct = "✅" if row['model_correct'] else "❌"
            prob = row['cover_probability']
            
            print(f"{game}: {underdog} {spread} - Predicted: {predicted} ({prob:.1%}) - Actual: {actual} {correct}")
    
    # Biggest misses
    print(f"\n=== Biggest Prediction Misses ===")
    misses = model_b[~model_b['model_correct']].sort_values('cover_probability', ascending=False)
    
    print(f"High Confidence Misses:")
    high_misses = misses[misses['confidence'].isin(['VERY_HIGH', 'HIGH'])]
    for _, row in high_misses.iterrows():
        game = f"{row['away_team']} @ {row['home_team']}"
        underdog = row['underdog_team']
        spread = f"+{row['spread_line']}"
        predicted = "Cover" if row['predicted_cover'] else "No Cover"
        actual = "Cover" if row['actual_cover'] else "No Cover"
        prob = row['cover_probability']
        confidence = row['confidence']
        
        print(f"  {game}: {underdog} {spread} - Predicted {predicted} ({prob:.1%}, {confidence}) but {underdog} {'covered' if actual else 'did not cover'}")
    
    # Success stories
    print(f"\n=== Correct High Confidence Picks ===")
    correct_high = model_b[(model_b['model_correct']) & (model_b['confidence'].isin(['VERY_HIGH', 'HIGH']))]
    for _, row in correct_high.iterrows():
        game = f"{row['away_team']} @ {row['home_team']}"
        underdog = row['underdog_team']
        spread = f"+{row['spread_line']}"
        predicted = "Cover" if row['predicted_cover'] else "No Cover"
        prob = row['cover_probability']
        confidence = row['confidence']
        
        print(f"  {game}: {underdog} {spread} - Correctly predicted {predicted} ({prob:.1%}, {confidence})")
    
    # Summary insights
    print(f"\n=== Key Insights ===")
    
    # Very High Confidence performance
    very_high_total = len(model_b[model_b['confidence'] == 'VERY_HIGH'])
    very_high_correct = model_b[model_b['confidence'] == 'VERY_HIGH']['model_correct'].sum()
    if very_high_total > 0:
        very_high_accuracy = very_high_correct / very_high_total
        print(f"Very High Confidence: {very_high_correct}/{very_high_total} correct ({very_high_accuracy:.1%})")
    
    # Average probability of correct vs incorrect predictions
    correct_avg_prob = model_b[model_b['model_correct']]['cover_probability'].mean()
    incorrect_avg_prob = model_b[~model_b['model_correct']]['cover_probability'].mean()
    
    print(f"Average probability of correct predictions: {correct_avg_prob:.1%}")
    print(f"Average probability of incorrect predictions: {incorrect_avg_prob:.1%}")
    
    # Underdog cover rate
    actual_underdog_covers = model_b['actual_cover'].sum()
    predicted_underdog_covers = model_b['predicted_cover'].sum()
    
    print(f"Actual underdog covers: {actual_underdog_covers}/{total_games} ({actual_underdog_covers/total_games:.1%})")
    print(f"Predicted underdog covers: {predicted_underdog_covers}/{total_games} ({predicted_underdog_covers/total_games:.1%})")
    
    return model_b

if __name__ == "__main__":
    analyze_model_b_week3()
