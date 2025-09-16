#!/usr/bin/env python3
"""
Debug script to see what's on SumerSports pages
"""

import requests
from bs4 import BeautifulSoup

def debug_sumersports():
    """Debug what's on SumerSports pages"""
    
    session = requests.Session()
    session.headers.update({
        'User-Agent': 'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/120.0.0.0 Safari/537.36',
        'Accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,image/webp,*/*;q=0.8',
        'Accept-Language': 'en-US,en;q=0.5',
        'Accept-Encoding': 'gzip, deflate',
        'Connection': 'keep-alive',
    })
    
    # Test offensive page
    print("=== Debugging SumerSports Offensive Page ===")
    try:
        url = "https://sumersports.com/teams/offensive/"
        response = session.get(url, timeout=15)
        response.raise_for_status()
        
        print(f"Status Code: {response.status_code}")
        print(f"Content Length: {len(response.content)}")
        
        soup = BeautifulSoup(response.content, 'html.parser')
        
        # Look for all tables
        tables = soup.find_all('table')
        print(f"Found {len(tables)} tables")
        
        for i, table in enumerate(tables):
            print(f"\nTable {i+1}:")
            print(f"  Classes: {table.get('class', [])}")
            print(f"  ID: {table.get('id', 'None')}")
            
            # Look for rows
            rows = table.find_all('tr')
            print(f"  Rows: {len(rows)}")
            
            if len(rows) > 0:
                # Show first few rows
                for j, row in enumerate(rows[:3]):
                    cells = row.find_all(['td', 'th'])
                    print(f"    Row {j+1}: {len(cells)} cells")
                    if len(cells) > 0:
                        print(f"      First cell: {cells[0].get_text(strip=True)[:50]}...")
        
        # Look for any divs that might contain the data
        print(f"\nLooking for data containers...")
        data_divs = soup.find_all('div', class_=lambda x: x and ('table' in x.lower() or 'data' in x.lower() or 'stats' in x.lower()))
        print(f"Found {len(data_divs)} potential data divs")
        
        # Look for any elements with EPA in the text
        epa_elements = soup.find_all(text=lambda text: text and 'EPA' in text)
        print(f"Found {len(epa_elements)} elements containing 'EPA'")
        
        if epa_elements:
            print("Sample EPA elements:")
            for elem in epa_elements[:5]:
                print(f"  {elem.strip()}")
        
    except Exception as e:
        print(f"Error: {e}")
    
    print("\n" + "="*50)
    
    # Test defensive page
    print("=== Debugging SumerSports Defensive Page ===")
    try:
        url = "https://sumersports.com/teams/defensive/"
        response = session.get(url, timeout=15)
        response.raise_for_status()
        
        print(f"Status Code: {response.status_code}")
        print(f"Content Length: {len(response.content)}")
        
        soup = BeautifulSoup(response.content, 'html.parser')
        
        # Look for all tables
        tables = soup.find_all('table')
        print(f"Found {len(tables)} tables")
        
        for i, table in enumerate(tables):
            print(f"\nTable {i+1}:")
            print(f"  Classes: {table.get('class', [])}")
            print(f"  ID: {table.get('id', 'None')}")
            
            # Look for rows
            rows = table.find_all('tr')
            print(f"  Rows: {len(rows)}")
            
            if len(rows) > 0:
                # Show first few rows
                for j, row in enumerate(rows[:3]):
                    cells = row.find_all(['td', 'th'])
                    print(f"    Row {j+1}: {len(cells)} cells")
                    if len(cells) > 0:
                        print(f"      First cell: {cells[0].get_text(strip=True)[:50]}...")
        
    except Exception as e:
        print(f"Error: {e}")

if __name__ == "__main__":
    debug_sumersports()
