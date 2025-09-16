#!/usr/bin/env python3
"""
Adjust Bengals EPA data for Jake Browning replacing Joe Burrow
"""

import pandas as pd
import os

def adjust_bengals_for_browning():
    print("=== Adjusting Bengals EPA for Jake Browning ===")
    
    # Load current SumerSports data
    epa_data = pd.read_csv("sumersports_epa_data.csv")
    
    # Find Bengals row
    bengals_idx = epa_data[epa_data['team'] == 'CIN'].index[0]
    bengals_row = epa_data.loc[bengals_idx].copy()
    
    print(f"Current Bengals EPA:")
    print(f"  Offensive EPA per Play: {bengals_row['epa_off_per_play']:.4f}")
    print(f"  Net EPA per Play: {bengals_row['net_epa_per_play']:.4f}")
    
    # Based on our analysis:
    # Browning EPA per play: 0.0871
    # Burrow EPA per play: 0.0932
    # Difference: 0.0061 (Browning is 7% worse)
    
    # Adjust offensive EPA (assuming 60% of offensive EPA comes from passing)
    epa_reduction = 0.0061 * 0.6  # 60% of offense is passing
    adjusted_off_epa = bengals_row['epa_off_per_play'] + epa_reduction
    
    # Adjust net EPA
    defensive_epa_contribution = bengals_row['net_epa_per_play'] - bengals_row['epa_off_per_play']
    adjusted_net_epa = adjusted_off_epa + defensive_epa_contribution
    
    print(f"\nAdjusted Bengals EPA (with Browning):")
    print(f"  Offensive EPA per Play: {adjusted_off_epa:.4f}")
    print(f"  Net EPA per Play: {adjusted_net_epa:.4f}")
    print(f"  EPA Improvement: {adjusted_net_epa - bengals_row['net_epa_per_play']:.4f}")
    
    # Create adjusted dataset
    epa_data_adjusted = epa_data.copy()
    epa_data_adjusted.loc[bengals_idx, 'epa_off_per_play'] = adjusted_off_epa
    epa_data_adjusted.loc[bengals_idx, 'net_epa_per_play'] = adjusted_net_epa
    epa_data_adjusted.loc[bengals_idx, 'last_updated'] = pd.Timestamp.now()
    
    # Save adjusted data
    output_path = "sumersports_epa_data_browning_adjusted.csv"
    epa_data_adjusted.to_csv(output_path, index=False)
    print(f"\n✅ Saved adjusted EPA data to {output_path}")
    
    # Show comparison
    print(f"\n=== Bengals EPA Comparison ===")
    print(f"Original (Burrow): Net EPA = {bengals_row['net_epa_per_play']:.4f}")
    print(f"Adjusted (Browning): Net EPA = {adjusted_net_epa:.4f}")
    print(f"Change: {adjusted_net_epa - bengals_row['net_epa_per_play']:+.4f}")
    
    return epa_data_adjusted

if __name__ == "__main__":
    adjust_bengals_for_browning()
