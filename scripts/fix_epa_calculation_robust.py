#!/usr/bin/env python3
"""
Robust fix for EPA calculation bug - handles different variable naming conventions
"""

import re
import glob

def fix_file(filepath):
    """Fix EPA calculation in a file"""
    print(f"Fixing {filepath}...")
    
    with open(filepath, 'r') as f:
        content = f.read()
    
    # Check if already fixed
    if 'underdog_net' in content and 'favorite_net' in content:
        print(f"  Already fixed: {filepath}")
        return False
    
    # Pattern 1: away_net_epa - home_net_epa
    pattern1 = r'(away_net_epa\s*=\s*away_off_epa\s*-\s*away_def_epa\s*\n\s*home_net_epa\s*=\s*home_off_epa\s*-\s*home_def_epa\s*\n\s*net_epa_diff\s*=\s*away_net_epa\s*-\s*home_net_epa)'
    
    replacement1 = """away_net_epa = away_off_epa - away_def_epa
        home_net_epa = home_off_epa - home_def_epa
        
        # Calculate from underdog's perspective (underdog_net - favorite_net)
        # Positive means underdog is stronger (more likely to cover)
        if favorite == away_team:
            favorite_net_epa = away_net_epa
            underdog_net_epa = home_net_epa
        else:
            favorite_net_epa = home_net_epa
            underdog_net_epa = away_net_epa
        
        net_epa_diff = underdog_net_epa - favorite_net_epa"""
    
    # Pattern 2: away_net - home_net (with away_off, away_def)
    pattern2 = r'(away_net\s*=\s*away_off\s*-\s*away_def\s*\n\s*home_net\s*=\s*home_off\s*-\s*home_def\s*\n\s*net_epa_diff\s*=\s*away_net\s*-\s*home_net)'
    
    replacement2 = """away_net = away_off - away_def
        home_net = home_off - home_def
        
        # Calculate from underdog's perspective (underdog_net - favorite_net)
        # Positive means underdog is stronger (more likely to cover)
        if favorite == away_team:
            favorite_net = away_net
            underdog_net = home_net
        else:
            favorite_net = home_net
            underdog_net = away_net
        
        net_epa_diff = underdog_net - favorite_net"""
    
    # Try pattern 1 first
    if re.search(pattern1, content):
        new_content = re.sub(pattern1, replacement1, content)
        with open(filepath, 'w') as f:
            f.write(new_content)
        print(f"  ✅ Fixed {filepath} (pattern 1)")
        return True
    
    # Try pattern 2
    if re.search(pattern2, content):
        new_content = re.sub(pattern2, replacement2, content)
        with open(filepath, 'w') as f:
            f.write(new_content)
        print(f"  ✅ Fixed {filepath} (pattern 2)")
        return True
    
    # Check if it has the bug but different format
    if 'net_epa_diff' in content and ('away_net' in content or 'away_net_epa' in content):
        print(f"  ⚠️  Needs manual fix: {filepath}")
        return False
    
    print(f"  No bug found: {filepath}")
    return False

def main():
    """Fix all model files"""
    files = []
    files.extend(glob.glob("scripts/model_a_week*.py"))
    files.extend(glob.glob("scripts/model_b_week*.py"))
    files.extend(glob.glob("scripts/generate_week*.py"))
    
    fixed = 0
    for f in sorted(set(files)):
        if fix_file(f):
            fixed += 1
    
    print(f"\nFixed {fixed} files")

if __name__ == "__main__":
    main()

