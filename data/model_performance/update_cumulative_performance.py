#!/usr/bin/env python3
"""
Update cumulative model performance and archive historical snapshots
This script should be run after each week's results are finalized
"""

import pandas as pd
import os
from datetime import datetime
import shutil

def update_cumulative_performance():
    """
    Update cumulative performance and create historical snapshot
    """
    
    # Run the main cumulative performance script
    print("Updating cumulative performance...")
    os.system("python3 create_cumulative_model_performance.py")
    
    # Copy to model_performance directory
    source = "data/model_performance/legacy/cumulative_model_performance.csv"
    dest = "data/model_performance/cumulative_model_performance.csv"
    
    if os.path.exists(source):
        shutil.copy2(source, dest)
        print(f"✅ Updated {dest}")
        
        # Create historical snapshot
        # Get current week from the CSV
        df = pd.read_csv(source)
        week_rows = df[df['Week'] != 'TOTAL']
        if len(week_rows) > 0:
            latest_week = int(week_rows['Week'].max())
            timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
            snapshot = f"data/model_performance/historical/cumulative_model_performance_week{latest_week}_{timestamp}.csv"
            shutil.copy2(source, snapshot)
            print(f"✅ Created historical snapshot: {snapshot}")
            
            # Also create a "final" snapshot for the week
            final_snapshot = f"data/model_performance/historical/cumulative_model_performance_week{latest_week}_final.csv"
            shutil.copy2(source, final_snapshot)
            print(f"✅ Created final snapshot: {final_snapshot}")
    else:
        print(f"❌ Error: {source} not found")

if __name__ == "__main__":
    update_cumulative_performance()

