#!/usr/bin/env python3
"""
Setup script for Week 2 Model Tracker

This script initializes the Week 2 tracker and creates the results template.
Run this first to set up the tracking system.
"""

import sys
import os

# Add the current directory to the path so we can import the tracker
sys.path.append(os.path.dirname(os.path.abspath(__file__)))

from week2_model_tracker import Week2ModelTracker

def main():
    print("=== Setting up Week 2 Model Tracker ===")
    
    tracker = Week2ModelTracker()
    
    # Load predictions
    print("Loading model predictions...")
    if not tracker.load_predictions():
        print("Error: Could not load predictions file")
        print("Make sure week2_underdog_predictions_updated.csv exists")
        return
    
    # Create results template
    print("Creating results template...")
    template = tracker.create_results_template()
    
    if template is not None:
        print(f"\n✅ Results template created successfully!")
        print(f"📁 File: week2_results_template.csv")
        print(f"📊 Games to track: {len(template)}")
        
        print("\n📋 Next steps:")
        print("1. Fill in the actual game results in week2_results_template.csv")
        print("2. Rename the file to week2_results.csv")
        print("3. Run: python week2_model_tracker.py")
        
        print("\n📝 Template columns to fill:")
        print("- actual_home_score: Final home team score")
        print("- actual_away_score: Final away team score")
        print("- actual_margin: Home score - Away score")
        print("- actual_cover: True if underdog covered the spread")
        print("- actual_winner: 'home' or 'away'")
        print("- actual_underdog_win: True if underdog won outright")
        print("- game_completed: True when game is finished")
        print("- notes: Any additional notes about the game")
        
        # Show the template structure
        print(f"\n📊 Template preview:")
        print(template[['game', 'underdog', 'favorite', 'spread', 'cover_probability', 'confidence']].head())
        
    else:
        print("❌ Failed to create results template")

if __name__ == "__main__":
    main()

