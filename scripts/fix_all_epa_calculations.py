#!/usr/bin/env python3
"""
Comprehensive fix for EPA calculation bug across all model files
This fixes the bug where net_epa_diff = away_net - home_net
Should be: net_epa_diff = underdog_net - favorite_net
"""

import re
import glob
import os

def fix_epa_calculation(content, var_suffix=""):
    """
    Fix EPA calculation in content
    var_suffix can be "_epa" or "" depending on variable naming
    """
    away_var = f"away_net{var_suffix}"
    home_var = f"home_net{var_suffix}"
    away_off_var = f"away_off{var_suffix}"
    away_def_var = f"away_def{var_suffix}"
    home_off_var = f"home_off{var_suffix}"
    home_def_var = f"home_def{var_suffix}"
    
    # Pattern to match the buggy calculation
    pattern = rf'({away_var}\s*=\s*{away_off_var}\s*-\s*{away_def_var}\s*\n\s*{home_var}\s*=\s*{home_off_var}\s*-\s*{home_def_var}\s*\n\s*net_epa_diff\s*=\s*{away_var}\s*-\s*{home_var})'
    
    replacement = f"""{away_var} = {away_off_var} - {away_def_var}
        {home_var} = {home_off_var} - {home_def_var}
        
        # Calculate from underdog's perspective (underdog_net - favorite_net)
        # Positive means underdog is stronger (more likely to cover)
        if favorite == away_team:
            favorite_net{var_suffix} = {away_var}
            underdog_net{var_suffix} = {home_var}
        else:
            favorite_net{var_suffix} = {home_var}
            underdog_net{var_suffix} = {away_var}
        
        net_epa_diff = underdog_net{var_suffix} - favorite_net{var_suffix}"""
    
    # Check if already fixed
    if 'underdog_net' in content and 'favorite_net' in content:
        return content, False
    
    # Try to replace
    new_content = re.sub(pattern, replacement, content, flags=re.MULTILINE)
    
    if new_content != content:
        return new_content, True
    
    return content, False

def fix_file(filepath):
    """Fix a single file"""
    print(f"Processing {filepath}...")
    
    if not os.path.exists(filepath):
        print(f"  File not found: {filepath}")
        return False
    
    with open(filepath, 'r') as f:
        content = f.read()
    
    # Check if already fixed
    if 'underdog_net' in content and 'favorite_net' in content and 'net_epa_diff = underdog_net' in content:
        print(f"  Already fixed: {filepath}")
        return False
    
    # Try with _epa suffix
    new_content, fixed = fix_epa_calculation(content, "_epa")
    if not fixed:
        # Try without suffix
        new_content, fixed = fix_epa_calculation(content, "")
    
    if fixed:
        with open(filepath, 'w') as f:
            f.write(new_content)
        print(f"  ✅ Fixed: {filepath}")
        return True
    else:
        print(f"  ⚠️  Could not auto-fix: {filepath} (may need manual review)")
        return False

def main():
    """Fix all model files"""
    print("="*80)
    print("FIXING EPA CALCULATION BUG IN ALL MODEL FILES")
    print("="*80)
    print()
    
    # Find all model files
    files = []
    files.extend(glob.glob("scripts/model_a_week*.py"))
    files.extend(glob.glob("scripts/model_b_week*.py"))
    files.extend(glob.glob("scripts/generate_week*.py"))
    
    # Remove duplicates and sort
    files = sorted(set(files))
    
    fixed_count = 0
    for filepath in files:
        if fix_file(filepath):
            fixed_count += 1
    
    print()
    print("="*80)
    print(f"Fixed {fixed_count} files")
    print("="*80)
    print()
    print("Next step: Run scripts/regenerate_all_predictions.py to regenerate")
    print("all predictions with the corrected calculation.")

if __name__ == "__main__":
    main()

