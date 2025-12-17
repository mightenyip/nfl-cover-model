#!/usr/bin/env python3
"""
Regenerate all week predictions with corrected EPA calculation
"""

import os
import subprocess
import sys

def get_available_weeks():
    """Get list of weeks that have odds files"""
    weeks = []
    for week in range(1, 17):
        odds_file = f"schedule/week{week}_2025_odds.csv"
        if os.path.exists(odds_file):
            weeks.append(week)
    return weeks

def regenerate_week_predictions(week_num):
    """Regenerate predictions for a specific week"""
    print(f"\n{'='*80}")
    print(f"REGENERATING WEEK {week_num} PREDICTIONS")
    print(f"{'='*80}")
    
    # Check if we have the necessary scripts
    model_a_script = f"scripts/model_a_week{week_num}_predictions.py"
    model_b_script = f"scripts/model_b_week{week_num}_predictions.py"
    
    # For weeks 10-11, use generate_week scripts
    if week_num in [10, 11]:
        script = f"scripts/generate_week{week_num}_predictions.py"
        if os.path.exists(script):
            print(f"Running {script}...")
            result = subprocess.run([sys.executable, script], capture_output=True, text=True)
            if result.returncode == 0:
                print(f"✅ Week {week_num} predictions regenerated")
                return True
            else:
                print(f"❌ Error regenerating Week {week_num}:")
                print(result.stderr)
                return False
    
    # For other weeks, run model scripts individually
    success = True
    
    # Model A
    if os.path.exists(model_a_script):
        print(f"Running {model_a_script}...")
        result = subprocess.run([sys.executable, model_a_script], capture_output=True, text=True)
        if result.returncode == 0:
            print(f"✅ Model A Week {week_num} regenerated")
        else:
            print(f"❌ Error with Model A Week {week_num}:")
            print(result.stderr)
            success = False
    
    # Model B
    if os.path.exists(model_b_script):
        print(f"Running {model_b_script}...")
        result = subprocess.run([sys.executable, model_b_script], capture_output=True, text=True)
        if result.returncode == 0:
            print(f"✅ Model B Week {week_num} regenerated")
        else:
            print(f"❌ Error with Model B Week {week_num}:")
            print(result.stderr)
            success = False
    
    # Model E (if exists)
    model_e_script = f"scripts/model_e_week{week_num}_predictions.py"
    if os.path.exists(model_e_script):
        print(f"Running {model_e_script}...")
        result = subprocess.run([sys.executable, model_e_script], capture_output=True, text=True)
        if result.returncode == 0:
            print(f"✅ Model E Week {week_num} regenerated")
        else:
            print(f"⚠️  Warning with Model E Week {week_num} (non-critical)")
    
    return success

def create_predictions_final(week_num):
    """Create predictions_final.csv for a week"""
    # Check if there's a script to create predictions_final
    create_script = f"scripts/create_week{week_num}_predictions_final.py"
    if os.path.exists(create_script):
        print(f"Creating predictions_final for Week {week_num}...")
        result = subprocess.run([sys.executable, create_script], capture_output=True, text=True)
        if result.returncode == 0:
            print(f"✅ Week {week_num} predictions_final created")
            return True
        else:
            print(f"⚠️  Could not create predictions_final for Week {week_num}")
            return False
    
    # For week 16, use the create_week16 script
    if week_num == 16:
        script = "scripts/create_week16_predictions_final.py"
        if os.path.exists(script):
            print(f"Creating predictions_final for Week {week_num}...")
            result = subprocess.run([sys.executable, script], capture_output=True, text=True)
            if result.returncode == 0:
                print(f"✅ Week {week_num} predictions_final created")
                return True
    
    return False

def main():
    """Main function"""
    print("="*80)
    print("REGENERATING ALL PREDICTIONS WITH CORRECTED EPA CALCULATION")
    print("="*80)
    
    weeks = get_available_weeks()
    print(f"\nFound {len(weeks)} weeks with odds files: {weeks}")
    
    successful_weeks = []
    failed_weeks = []
    
    for week in weeks:
        if regenerate_week_predictions(week):
            successful_weeks.append(week)
            # Try to create predictions_final
            create_predictions_final(week)
        else:
            failed_weeks.append(week)
    
    print("\n" + "="*80)
    print("SUMMARY")
    print("="*80)
    print(f"Successfully regenerated: {len(successful_weeks)} weeks")
    print(f"  Weeks: {successful_weeks}")
    if failed_weeks:
        print(f"Failed to regenerate: {len(failed_weeks)} weeks")
        print(f"  Weeks: {failed_weeks}")
    print("="*80)

if __name__ == "__main__":
    main()

