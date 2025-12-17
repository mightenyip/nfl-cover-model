#!/usr/bin/env python3
"""
Fix the EPA calculation bug in all model prediction scripts
The bug: using away_net - home_net instead of underdog_net - favorite_net
"""

import os
import re
import glob

def fix_model_file(filepath):
    """Fix the EPA calculation in a model file"""
    print(f"Fixing {filepath}...")
    
    with open(filepath, 'r') as f:
        content = f.read()
    
    # Pattern to find the buggy calculation
    # Look for: net_epa_diff = away_net - home_net (or similar variations)
    old_patterns = [
        r'net_epa_diff\s*=\s*away_net.*?-\s*home_net',
        r'net_epa_diff\s*=\s*away_net_epa\s*-\s*home_net_epa',
    ]
    
    # Check if file has the bug
    has_bug = False
    for pattern in old_patterns:
        if re.search(pattern, content):
            has_bug = True
            break
    
    if not has_bug:
        print(f"  No bug found in {filepath}")
        return False
    
    # Find the section to replace
    # We need to find where net_epa_diff is calculated and replace it
    # with the correct logic
    
    # Pattern to match the calculation section
    calc_pattern = r'(away_net.*?=\s*away_off.*?-\s*away_def.*?\n.*?home_net.*?=\s*home_off.*?-\s*home_def.*?\n.*?net_epa_diff\s*=\s*away_net.*?-\s*home_net)'
    
    replacement = """away_net = away_off - away_def
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
    
    # Try to replace with the pattern that matches the exact format
    # First, let's try a more flexible approach - find the lines and replace them
    lines = content.split('\n')
    new_lines = []
    i = 0
    replaced = False
    
    while i < len(lines):
        line = lines[i]
        
        # Check if this is the net_epa_diff calculation line
        if 'net_epa_diff' in line and ('away_net' in line or 'away_net_epa' in line) and 'home_net' in line:
            # We found the buggy line - need to replace it with correct logic
            # First, find where away_net and home_net are calculated
            # Go back a few lines to find the context
            start_idx = max(0, i - 5)
            context = '\n'.join(lines[start_idx:i])
            
            # Check if we already have the favorite/underdog logic
            if 'favorite_net' in context or 'underdog_net' in context:
                # Already fixed, skip
                new_lines.append(line)
                i += 1
                continue
            
            # Find the away_net and home_net calculation lines
            away_net_line_idx = None
            home_net_line_idx = None
            
            for j in range(max(0, i-10), i):
                if 'away_net' in lines[j] and '=' in lines[j] and 'away_off' in lines[j]:
                    away_net_line_idx = j
                if 'home_net' in lines[j] and '=' in lines[j] and 'home_off' in lines[j]:
                    home_net_line_idx = j
            
            if away_net_line_idx is not None and home_net_line_idx is not None:
                # Replace the section
                # Keep everything before away_net calculation
                new_lines.extend(lines[:away_net_line_idx])
                
                # Add the fixed calculation
                indent = '        '  # Standard indent
                new_lines.append(f"{indent}away_net = away_off - away_def")
                new_lines.append(f"{indent}home_net = home_off - home_def")
                new_lines.append(f"{indent}")
                new_lines.append(f"{indent}# Calculate from underdog's perspective (underdog_net - favorite_net)")
                new_lines.append(f"{indent}# Positive means underdog is stronger (more likely to cover)")
                new_lines.append(f"{indent}if favorite == away_team:")
                new_lines.append(f"{indent}    favorite_net = away_net")
                new_lines.append(f"{indent}    underdog_net = home_net")
                new_lines.append(f"{indent}else:")
                new_lines.append(f"{indent}    favorite_net = home_net")
                new_lines.append(f"{indent}    underdog_net = away_net")
                new_lines.append(f"{indent}")
                new_lines.append(f"{indent}net_epa_diff = underdog_net - favorite_net")
                
                # Skip the old lines and continue from after net_epa_diff
                i = i + 1
                replaced = True
                continue
        
        new_lines.append(line)
        i += 1
    
    if replaced:
        with open(filepath, 'w') as f:
            f.write('\n'.join(new_lines))
        print(f"  ✅ Fixed {filepath}")
        return True
    else:
        # Try a simpler replacement approach
        # Replace the specific line
        new_content = content
        for pattern in old_patterns:
            if re.search(pattern, new_content):
                # Find the context around this line
                match = re.search(pattern, new_content)
                if match:
                    # Get the lines before and after
                    start = match.start()
                    end = match.end()
                    
                    # Find the line numbers
                    before = new_content[:start]
                    after = new_content[end:]
                    
                    # Count newlines to find line number
                    line_num = before.count('\n')
                    
                    # Get the indentation from the line
                    lines_before = before.split('\n')
                    if lines_before:
                        last_line = lines_before[-1]
                        indent = len(last_line) - len(last_line.lstrip())
                        indent_str = ' ' * indent
                    else:
                        indent_str = '        '
                    
                    # Create replacement
                    replacement_text = f"""away_net = away_off - away_def
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
                    
                    # This is complex - let's use a simpler approach
                    # Just replace the specific calculation line
                    simple_replacement = """net_epa_diff = underdog_net - favorite_net"""
                    
                    # But we need to add the favorite/underdog calculation before it
                    # Let's do a more targeted replacement
                    pass
        
        print(f"  ⚠️  Could not automatically fix {filepath} - manual fix needed")
        return False

def main():
    """Fix all model files"""
    print("="*80)
    print("FIXING EPA CALCULATION BUG IN ALL MODEL FILES")
    print("="*80)
    print()
    
    # Find all model_a and model_b prediction files
    model_files = []
    model_files.extend(glob.glob("scripts/model_a_week*.py"))
    model_files.extend(glob.glob("scripts/model_b_week*.py"))
    model_files.extend(glob.glob("scripts/generate_week*.py"))
    
    # Also check the create_week16 script (already fixed, but check)
    if os.path.exists("scripts/create_week16_predictions_final.py"):
        model_files.append("scripts/create_week16_predictions_final.py")
    
    fixed_count = 0
    for filepath in sorted(set(model_files)):
        if os.path.exists(filepath):
            if fix_model_file(filepath):
                fixed_count += 1
    
    print()
    print("="*80)
    print(f"Fixed {fixed_count} files")
    print("="*80)
    print()
    print("NOTE: Some files may need manual review if the pattern matching")
    print("      couldn't find the exact location. Please verify the fixes.")

if __name__ == "__main__":
    main()

