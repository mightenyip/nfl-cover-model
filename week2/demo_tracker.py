#!/usr/bin/env python3
"""
Demo script for Week 2 Model Tracker

This script demonstrates how the tracker works using sample data.
"""

import sys
import os

# Add the current directory to the path so we can import the tracker
sys.path.append(os.path.dirname(os.path.abspath(__file__)))

from week2_model_tracker import Week2ModelTracker

def main():
    print("=== Week 2 Model Tracker Demo ===")
    print("Using sample data to demonstrate the tracker functionality\n")
    
    tracker = Week2ModelTracker()
    
    # Load predictions
    print("1. Loading model predictions...")
    if not tracker.load_predictions():
        print("Error: Could not load predictions file")
        return
    
    # Load sample results
    print("2. Loading sample results...")
    if not tracker.load_results("week2_results_sample.csv"):
        print("Error: Could not load sample results file")
        return
    
    # Analyze performance
    print("3. Analyzing model performance...")
    performance_summary, completed_games = tracker.analyze_performance()
    
    if performance_summary is None:
        print("No completed games to analyze")
        return
    
    # Print detailed summary
    print("\n" + "="*60)
    print("📊 MODEL PERFORMANCE SUMMARY")
    print("="*60)
    
    print(f"Total Games Analyzed: {performance_summary['total_games']}")
    print(f"Spread Coverage Accuracy: {performance_summary['spread_accuracy']:.1%} ({performance_summary['correct_spread_predictions']}/{performance_summary['total_games']})")
    print(f"Outright Win Accuracy: {performance_summary['outright_accuracy']:.1%} ({performance_summary['correct_outright_predictions']}/{performance_summary['total_games']})")
    
    print(f"\n📈 Performance by Confidence Level:")
    print(f"  HIGH Confidence: {performance_summary['high_confidence_accuracy']:.1%} ({performance_summary['high_confidence_games']} games)")
    print(f"  MEDIUM Confidence: {performance_summary['medium_confidence_accuracy']:.1%} ({performance_summary['medium_confidence_games']} games)")
    print(f"  LOW Confidence: {performance_summary['low_confidence_accuracy']:.1%} ({performance_summary['low_confidence_games']} games)")
    
    # Show game-by-game results
    print(f"\n📋 GAME-BY-GAME RESULTS:")
    print("-" * 100)
    print(f"{'Game':<25} {'Underdog':<10} {'Spread':<8} {'Pred':<6} {'Actual':<6} {'Correct':<8} {'Conf':<6}")
    print("-" * 100)
    
    for _, game in completed_games.iterrows():
        predicted = "Cover" if game['cover_probability'] > 0.5 else "No Cover"
        actual = "Cover" if game['actual_cover'] else "No Cover"
        correct = "✓" if (game['cover_probability'] > 0.5) == game['actual_cover'] else "✗"
        
        print(f"{game['game']:<25} {game['underdog']:<10} {game['spread']:<8} {predicted:<6} {actual:<6} {correct:<8} {game['confidence']:<6}")
    
    # Create visualizations
    print(f"\n4. Creating visualizations...")
    tracker.create_visualizations(completed_games)
    
    # Generate report
    print(f"5. Generating detailed report...")
    tracker.generate_report(performance_summary, completed_games)
    
    # Export results
    print(f"6. Exporting detailed results...")
    tracker.export_results(completed_games)
    
    print(f"\n✅ Demo completed successfully!")
    print(f"\n📁 Files created:")
    print(f"  - week2_model_performance.png (visualizations)")
    print(f"  - week2_model_performance_report.md (detailed report)")
    print(f"  - week2_detailed_results.csv (exported data)")
    
    print(f"\n💡 Key Insights from Sample Data:")
    if performance_summary['spread_accuracy'] > 0.6:
        print(f"  ✅ Model performed well with {performance_summary['spread_accuracy']:.1%} accuracy")
    else:
        print(f"  ⚠️  Model accuracy was {performance_summary['spread_accuracy']:.1%} - needs improvement")
    
    if performance_summary['high_confidence_accuracy'] > 0.7:
        print(f"  ✅ High confidence predictions were very accurate ({performance_summary['high_confidence_accuracy']:.1%})")
    else:
        print(f"  ⚠️  High confidence predictions need improvement ({performance_summary['high_confidence_accuracy']:.1%})")

if __name__ == "__main__":
    main()

