"""
Week 9 Actual Results Analysis
Compare model predictions to actual game results
"""

import pandas as pd
import json

def analyze_week9_performance():
    """Analyze Week 9 model performance against actual results"""
    
    # Actual results (from user input)
    actual_results = {
        "Ravens @ Dolphins": {
            "score": "BAL 28, MIA 6",
            "away_team": "Ravens",
            "home_team": "Dolphins",
            "away_score": 28,
            "home_score": 6,
            "spread": -7.5,
            "favorite": "Ravens",
            "underdog": "Dolphins",
            "margin": 22,
            "underdog_covered": False  # Dolphins lost by 22, spread was 7.5
        },
        "Bears @ Bengals": {
            "score": "CHI 47, CIN 42",
            "away_team": "Bears",
            "home_team": "Bengals",
            "away_score": 47,
            "home_score": 42,
            "spread": -2.5,
            "favorite": "Bears",
            "underdog": "Bengals",
            "margin": 5,
            "underdog_covered": False  # Bengals lost by 5, spread was 2.5
        },
        "Vikings @ Lions": {
            "score": "MIN 27, DET 24",
            "away_team": "Vikings",
            "home_team": "Lions",
            "away_score": 27,
            "home_score": 24,
            "spread": -8.5,
            "favorite": "Lions",
            "underdog": "Vikings",
            "margin": -3,  # Vikings won by 3
            "underdog_covered": True  # Vikings covered +8.5
        },
        "Panthers @ Packers": {
            "score": "CAR 16, GB 13",
            "away_team": "Panthers",
            "home_team": "Packers",
            "away_score": 16,
            "home_score": 13,
            "spread": -12.5,
            "favorite": "Packers",
            "underdog": "Panthers",
            "margin": -3,  # Panthers won by 3
            "underdog_covered": True  # Panthers covered +12.5
        },
        "Chargers @ Titans": {
            "score": "LAC 27, TEN 20",
            "away_team": "Chargers",
            "home_team": "Titans",
            "away_score": 27,
            "home_score": 20,
            "spread": -9.5,
            "favorite": "Chargers",
            "underdog": "Titans",
            "margin": -7,  # Chargers won by 7
            "underdog_covered": True  # Titans covered +9.5
        },
        "Falcons @ Patriots": {
            "score": "NE 24, ATL 23",
            "away_team": "Falcons",
            "home_team": "Patriots",
            "away_score": 23,
            "home_score": 24,
            "spread": -5.5,
            "favorite": "Patriots",
            "underdog": "Falcons",
            "margin": 1,  # Patriots won by 1
            "underdog_covered": True  # Falcons covered +5.5
        },
        "49ers @ Giants": {
            "score": "SF 34, NYG 24",
            "away_team": "49ers",
            "home_team": "Giants",
            "away_score": 34,
            "home_score": 24,
            "spread": -2.5,
            "favorite": "49ers",
            "underdog": "Giants",
            "margin": 10,
            "underdog_covered": False  # Giants lost by 10, spread was 2.5
        },
        "Colts @ Steelers": {
            "score": "PIT 27, IND 20",
            "away_team": "Colts",
            "home_team": "Steelers",
            "away_score": 20,
            "home_score": 27,
            "spread": -3.0,
            "favorite": "Steelers",
            "underdog": "Colts",
            "margin": 7,
            "underdog_covered": False  # Colts lost by 7, spread was 3.0
        },
        "Broncos @ Texans": {
            "score": "DEN 18, HOU 15",
            "away_team": "Broncos",
            "home_team": "Texans",
            "away_score": 18,
            "home_score": 15,
            "spread": -1.5,
            "favorite": "Texans",
            "underdog": "Broncos",
            "margin": -3,  # Broncos won by 3
            "underdog_covered": True  # Broncos covered +1.5
        },
        "Jaguars @ Raiders": {
            "score": "JAX 30, LV 29 (OT)",
            "away_team": "Jaguars",
            "home_team": "Raiders",
            "away_score": 30,
            "home_score": 29,
            "spread": -3.0,
            "favorite": "Jaguars",
            "underdog": "Raiders",
            "margin": 1,
            "underdog_covered": True  # Raiders covered +3.0
        },
        "Saints @ Rams": {
            "score": "LAR 34, NO 10",
            "away_team": "Saints",
            "home_team": "Rams",
            "away_score": 10,
            "home_score": 34,
            "spread": -13.5,
            "favorite": "Rams",
            "underdog": "Saints",
            "margin": 24,
            "underdog_covered": False  # Saints lost by 24, spread was 13.5
        },
        "Chiefs @ Bills": {
            "score": "BUF 28, KC 21",
            "away_team": "Chiefs",
            "home_team": "Bills",
            "away_score": 21,
            "home_score": 28,
            "spread": -1.5,
            "favorite": "Chiefs",
            "underdog": "Bills",
            "margin": -7,  # Bills won by 7
            "underdog_covered": True  # Bills covered +1.5
        },
        "Seahawks @ Commanders": {
            "score": "SEA 38, WSH 14",
            "away_team": "Seahawks",
            "home_team": "Commanders",
            "away_score": 38,
            "home_score": 14,
            "spread": -3.5,
            "favorite": "Seahawks",
            "underdog": "Commanders",
            "margin": 24,
            "underdog_covered": False  # Commanders lost by 24, spread was 3.5
        },
        # Cardinals @ Cowboys - game tonight
    }
    
    # Load predictions
    model_a = pd.read_csv("predictions/model_a_week9_predictions.csv")
    model_b = pd.read_csv("predictions/model_b_week9_predictions.csv")
    model_c = pd.read_csv("predictions/model_c_week9_predictions.csv")
    model_d = pd.read_csv("predictions/model_d_week9_predictions.csv")
    model_e = pd.read_csv("predictions/model_e_week9_predictions.csv")
    consensus = pd.read_csv("predictions/week9_consensus_predictions.csv")
    
    # Map predictions to actual results
    results_data = []
    
    for game_name, actual in actual_results.items():
        # Find predictions for this game
        model_a_pred = model_a[model_a['game'] == game_name]
        model_b_pred = model_b[model_b['game'] == game_name]
        model_c_pred = model_c[model_c['game'] == game_name]
        model_d_pred = model_d[model_d['game'] == game_name]
        model_e_pred = model_e[model_e['game'] == game_name]
        consensus_pred = consensus[consensus['game'] == game_name]
        
        if len(model_a_pred) == 0:
            continue
        
        # Get predictions (Cover = True means underdog covers)
        model_a_cover = model_a_pred.iloc[0]['predicted_cover'] if 'predicted_cover' in model_a_pred.columns else None
        model_b_cover = model_b_pred.iloc[0]['predicted_cover'] if 'predicted_cover' in model_b_pred.columns else None
        model_c_cover = model_c_pred.iloc[0]['predicted_cover'] if 'predicted_cover' in model_c_pred.columns else None
        model_d_cover = model_d_pred.iloc[0]['predicted_cover'] if 'predicted_cover' in model_d_pred.columns else None
        model_e_cover = model_e_pred.iloc[0]['predicted_cover'] if 'predicted_cover' in model_e_pred.columns else None
        
        # Consensus prediction
        consensus_cover = None
        if len(consensus_pred) > 0:
            consensus_str = consensus_pred.iloc[0]['consensus_prediction']
            consensus_cover = consensus_str == 'Cover'
        
        # Calculate correctness
        actual_cover = actual['underdog_covered']
        
        model_a_correct = (model_a_cover == actual_cover) if model_a_cover is not None else None
        model_b_correct = (model_b_cover == actual_cover) if model_b_cover is not None else None
        model_c_correct = (model_c_cover == actual_cover) if model_c_cover is not None else None
        model_d_correct = (model_d_cover == actual_cover) if model_d_cover is not None else None
        model_e_correct = (model_e_cover == actual_cover) if model_e_cover is not None else None
        consensus_correct = (consensus_cover == actual_cover) if consensus_cover is not None else None
        
        results_data.append({
            'game': game_name,
            'score': actual['score'],
            'spread': actual['spread'],
            'underdog': actual['underdog'],
            'actual_cover': actual_cover,
            'model_a_pred': model_a_cover,
            'model_a_correct': model_a_correct,
            'model_b_pred': model_b_cover,
            'model_b_correct': model_b_correct,
            'model_c_pred': model_c_cover,
            'model_c_correct': model_c_correct,
            'model_d_pred': model_d_cover,
            'model_d_correct': model_d_correct,
            'model_e_pred': model_e_cover,
            'model_e_correct': model_e_correct,
            'consensus_pred': consensus_cover,
            'consensus_correct': consensus_correct
        })
    
    results_df = pd.DataFrame(results_data)
    
    # Print detailed results
    print("=" * 100)
    print("WEEK 9 MODEL PERFORMANCE ANALYSIS")
    print("=" * 100)
    print(f"\nTotal Games Analyzed: {len(results_df)} (1 game pending - Cardinals @ Cowboys)")
    print(f"Actual Underdog Covers: {results_df['actual_cover'].sum()}/{len(results_df)} ({results_df['actual_cover'].mean():.1%})")
    
    print("\n" + "-" * 100)
    print("GAME-BY-GAME RESULTS")
    print("-" * 100)
    
    for _, row in results_df.iterrows():
        status_a = "✅" if row['model_a_correct'] else "❌" if row['model_a_correct'] is not None else "N/A"
        status_b = "✅" if row['model_b_correct'] else "❌" if row['model_b_correct'] is not None else "N/A"
        status_c = "✅" if row['model_c_correct'] else "❌" if row['model_c_correct'] is not None else "N/A"
        status_d = "✅" if row['model_d_correct'] else "❌" if row['model_d_correct'] is not None else "N/A"
        status_e = "✅" if row['model_e_correct'] else "❌" if row['model_e_correct'] is not None else "N/A"
        status_consensus = "✅" if row['consensus_correct'] else "❌" if row['consensus_correct'] is not None else "N/A"
        
        cover_result = "UNDERDOG COVERED" if row['actual_cover'] else "FAVORITE COVERED"
        
        print(f"\n{row['game']}")
        print(f"  Score: {row['score']} | Spread: {row['spread']} | {cover_result}")
        print(f"  Model A: {status_a} | Model B: {status_b} | Model C: {status_c} | Model D: {status_d} | Model E: {status_e}")
        print(f"  Consensus: {status_consensus}")
    
    # Calculate overall accuracy
    print("\n" + "=" * 100)
    print("OVERALL MODEL ACCURACY")
    print("=" * 100)
    
    models = {
        'Model A': 'model_a_correct',
        'Model B': 'model_b_correct',
        'Model C': 'model_c_correct',
        'Model D': 'model_d_correct',
        'Model E': 'model_e_correct',
        'Consensus': 'consensus_correct'
    }
    
    accuracy_results = []
    for model_name, col in models.items():
        correct_col = results_df[col]
        correct_count = correct_col.sum()
        total_count = correct_col.notna().sum()
        accuracy = correct_count / total_count if total_count > 0 else 0
        
        accuracy_results.append({
            'Model': model_name,
            'Correct': correct_count,
            'Total': total_count,
            'Accuracy': f"{accuracy:.1%}"
        })
        
        print(f"{model_name:12} | {correct_count:2}/{total_count:2} correct | {accuracy:.1%} accuracy")
    
    # Performance by confidence level (Model A)
    print("\n" + "-" * 100)
    print("MODEL A PERFORMANCE BY CONFIDENCE LEVEL")
    print("-" * 100)
    
    model_a_with_conf = model_a.merge(results_df[['game', 'actual_cover']], on='game', how='inner')
    model_a_with_conf['correct'] = model_a_with_conf['predicted_cover'] == model_a_with_conf['actual_cover']
    
    if 'confidence' in model_a_with_conf.columns:
        for conf_level in sorted(model_a_with_conf['confidence'].unique()):
            conf_data = model_a_with_conf[model_a_with_conf['confidence'] == conf_level]
            conf_correct = conf_data['correct'].sum()
            conf_total = len(conf_data)
            conf_accuracy = conf_correct / conf_total if conf_total > 0 else 0
            print(f"{conf_level:12} | {conf_correct:2}/{conf_total:2} correct | {conf_accuracy:.1%} accuracy")
    
    # Save results
    results_df.to_csv("data/week9_actual_results_analysis.csv", index=False)
    print(f"\n\nResults saved to data/week9_actual_results_analysis.csv")
    
    # Summary statistics
    print("\n" + "=" * 100)
    print("SUMMARY")
    print("=" * 100)
    print(f"Best Model: {max([(m, results_df[col].sum() / results_df[col].notna().sum()) for m, col in models.items()], key=lambda x: x[1])[0]}")
    print(f"Worst Model: {min([(m, results_df[col].sum() / results_df[col].notna().sum()) for m, col in models.items()], key=lambda x: x[1])[0]}")

if __name__ == "__main__":
    analyze_week9_performance()

