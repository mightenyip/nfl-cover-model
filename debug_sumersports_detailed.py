#!/usr/bin/env python3
"""
Detailed debug script for SumerSports table structure
"""

import requests
from bs4 import BeautifulSoup

def debug_detailed():
    """Debug the detailed table structure"""
    
    session = requests.Session()
    session.headers.update({
        'User-Agent': 'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/120.0.0.0 Safari/537.36',
    })
    
    # Test offensive page
    print("=== Detailed SumerSports Offensive Page Debug ===")
    try:
        url = "https://sumersports.com/teams/offensive/"
        response = session.get(url, timeout=15)
        response.raise_for_status()
        
        soup = BeautifulSoup(response.content, 'html.parser')
        table = soup.find('table', class_='w-full')
        
        if table:
            rows = table.find_all('tr')
            print(f"Total rows: {len(rows)}")
            
            # Show header row
            if len(rows) > 0:
                header_cells = rows[0].find_all(['th', 'td'])
                print(f"\nHeader row ({len(header_cells)} cells):")
                for i, cell in enumerate(header_cells):
                    print(f"  {i}: {cell.get_text(strip=True)}")
            
            # Show first few data rows
            for i, row in enumerate(rows[1:4], 1):
                cells = row.find_all('td')
                print(f"\nRow {i} ({len(cells)} cells):")
                for j, cell in enumerate(cells):
                    text = cell.get_text(strip=True)
                    print(f"  {j}: {text}")
        
    except Exception as e:
        print(f"Error: {e}")

if __name__ == "__main__":
    debug_detailed()
