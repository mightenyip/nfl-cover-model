#!/usr/bin/env python3
"""
CSV to JSON Converter
Converts CSV files to JSON format with various output options
"""

import pandas as pd
import json
import sys
import os
from pathlib import Path

def convert_csv_to_json(csv_file, json_file=None, output_format='records'):
    """
    Convert CSV file to JSON format
    
    Args:
        csv_file (str): Path to input CSV file
        json_file (str): Path to output JSON file (optional)
        output_format (str): JSON output format ('records', 'index', 'values', 'table')
    
    Returns:
        str: Path to output JSON file
    """
    
    if not os.path.exists(csv_file):
        raise FileNotFoundError(f"CSV file not found: {csv_file}")
    
    # Read CSV file
    print(f"📖 Reading CSV file: {csv_file}")
    df = pd.read_csv(csv_file)
    print(f"✅ Loaded {len(df)} rows and {len(df.columns)} columns")
    
    # Generate output filename if not provided
    if json_file is None:
        csv_path = Path(csv_file)
        json_file = csv_path.parent / f"{csv_path.stem}.json"
    
    # Convert to JSON
    print(f"🔄 Converting to JSON format: {output_format}")
    df.to_json(json_file, orient=output_format, indent=2, date_format='iso')
    print(f"✅ JSON file saved: {json_file}")
    
    return str(json_file)

def main():
    """Main function for command line usage"""
    if len(sys.argv) < 2:
        print("Usage: python csv_to_json_converter.py <csv_file> [json_file] [format]")
        print("Formats: records, index, values, table")
        print("Example: python csv_to_json_converter.py data/file.csv")
        return
    
    csv_file = sys.argv[1]
    json_file = sys.argv[2] if len(sys.argv) > 2 else None
    output_format = sys.argv[3] if len(sys.argv) > 3 else 'records'
    
    try:
        output_path = convert_csv_to_json(csv_file, json_file, output_format)
        print(f"🎉 Conversion complete: {output_path}")
    except Exception as e:
        print(f"❌ Error: {e}")

if __name__ == "__main__":
    main()
