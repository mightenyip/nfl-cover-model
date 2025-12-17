#!/usr/bin/env python3
"""
Scrape Week 16 EPA Data from SumerSports
Creates a comprehensive CSV with both offensive and defensive EPA metrics
"""

import requests
import pandas as pd
from bs4 import BeautifulSoup
import time
import re
from datetime import datetime
from typing import Optional

class Week16EPAScraper:
    """Scraper for Week 16 EPA data from SumerSports.com"""
    
    def __init__(self):
        self.session = requests.Session()
        self.session.headers.update({
            'User-Agent': 'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/120.0.0.0 Safari/537.36',
            'Accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,image/webp,*/*;q=0.8',
            'Accept-Language': 'en-US,en;q=0.5',
            'Accept-Encoding': 'gzip, deflate',
            'Connection': 'keep-alive',
            'Referer': 'https://sumersports.com/',
        })
        
        # Team mappings
        self.team_mappings = {
            'Baltimore Ravens': 'BAL', 'Indianapolis Colts': 'IND', 'Buffalo Bills': 'BUF', 
            'Detroit Lions': 'DET', 'Green Bay Packers': 'GB', 'Tampa Bay Buccaneers': 'TB', 
            'Jacksonville Jaguars': 'JAX', 'New England Patriots': 'NE', 
            'Los Angeles Rams': 'LA', 'Los Angeles Chargers': 'LAC', 'Dallas Cowboys': 'DAL', 
            'Arizona Cardinals': 'ARI', 'San Francisco 49ers': 'SF', 'Kansas City Chiefs': 'KC', 
            'Philadelphia Eagles': 'PHI', 'Atlanta Falcons': 'ATL', 'New York Jets': 'NYJ', 
            'Denver Broncos': 'DEN', 'Washington Commanders': 'WAS', 'Miami Dolphins': 'MIA',
            'Cincinnati Bengals': 'CIN', 'Pittsburgh Steelers': 'PIT', 'New Orleans Saints': 'NO', 
            'Seattle Seahawks': 'SEA', 'Houston Texans': 'HOU', 'Carolina Panthers': 'CAR', 
            'Chicago Bears': 'CHI', 'Las Vegas Raiders': 'LV', 'Cleveland Browns': 'CLE', 
            'Tennessee Titans': 'TEN', 'Minnesota Vikings': 'MIN', 'New York Giants': 'NYG'
        }
    
    def parse_number(self, text: str) -> float:
        """Parse a number from text, handling commas and negative signs"""
        if not text or text.strip() == '-':
            return 0.0
        text = text.strip().replace(',', '').replace('%', '')
        try:
            return float(text)
        except ValueError:
            return 0.0
    
    def scrape_offensive_epa(self) -> Optional[pd.DataFrame]:
        """Scrape offensive EPA data from SumerSports"""
        try:
            print("Scraping offensive EPA data from https://sumersports.com/teams/offensive/...")
            
            url = "https://sumersports.com/teams/offensive/"
            response = self.session.get(url, timeout=15)
            response.raise_for_status()
            
            soup = BeautifulSoup(response.content, 'html.parser')
            
            # Find the main data table
            table = soup.find('table', class_='w-full')
            
            if not table:
                print("❌ No table found on offensive page")
                return None
            
            rows = table.find_all('tr')[1:]  # Skip header row
            
            data = []
            for row in rows:
                cells = row.find_all('td')
                if len(cells) < 4:
                    continue
                
                # Extract team info from first cell
                team_cell = cells[0]
                team_text = team_cell.get_text(strip=True)
                
                # Extract full team name (e.g., "1.Baltimore Ravens" -> "Baltimore Ravens")
                team_match = re.search(r'\d+\.(.+)', team_text)
                if not team_match:
                    continue
                
                full_team_name = team_match.group(1).strip()
                standard_abbr = self.team_mappings.get(full_team_name)
                
                if not standard_abbr:
                    print(f"⚠️  Unknown team: {full_team_name}")
                    continue
                
                try:
                    # Extract data based on column positions
                    row_data = {
                        'team': standard_abbr,
                        'team_name': full_team_name,
                    }
                    
                    # EPA/Play (usually index 2)
                    if len(cells) > 2:
                        row_data['epa_off_per_play'] = self.parse_number(cells[2].get_text(strip=True))
                    
                    # Total EPA (usually index 3)
                    if len(cells) > 3:
                        row_data['total_epa_off'] = self.parse_number(cells[3].get_text(strip=True))
                    
                    # Success % (usually index 4)
                    if len(cells) > 4:
                        success_text = cells[4].get_text(strip=True)
                        row_data['success_rate_off'] = self.parse_number(success_text) / 100
                    
                    # EPA/Pass (usually index 5)
                    if len(cells) > 5:
                        row_data['epa_pass_off'] = self.parse_number(cells[5].get_text(strip=True))
                    
                    # EPA/Rush (usually index 6)
                    if len(cells) > 6:
                        row_data['epa_rush_off'] = self.parse_number(cells[6].get_text(strip=True))
                    
                    data.append(row_data)
                    
                except (ValueError, IndexError) as e:
                    print(f"⚠️  Error parsing row for {full_team_name}: {e}")
                    continue
            
            if data:
                df = pd.DataFrame(data)
                print(f"✅ Scraped offensive EPA for {len(df)} teams")
                return df
            else:
                print("❌ No offensive EPA data extracted")
                return None
                
        except Exception as e:
            print(f"❌ Error scraping offensive EPA: {e}")
            import traceback
            traceback.print_exc()
            return None
    
    def scrape_defensive_epa(self) -> Optional[pd.DataFrame]:
        """Scrape defensive EPA data from SumerSports"""
        try:
            print("Scraping defensive EPA data from https://sumersports.com/teams/defensive/...")
            
            url = "https://sumersports.com/teams/defensive/"
            response = self.session.get(url, timeout=15)
            response.raise_for_status()
            
            soup = BeautifulSoup(response.content, 'html.parser')
            
            # Find the main data table
            table = soup.find('table', class_='w-full')
            
            if not table:
                print("❌ No table found on defensive page")
                return None
            
            rows = table.find_all('tr')[1:]  # Skip header row
            
            data = []
            for row in rows:
                cells = row.find_all('td')
                if len(cells) < 4:
                    continue
                
                # Extract team info from first cell
                team_cell = cells[0]
                team_text = team_cell.get_text(strip=True)
                
                # Extract full team name
                team_match = re.search(r'\d+\.(.+)', team_text)
                if not team_match:
                    continue
                
                full_team_name = team_match.group(1).strip()
                standard_abbr = self.team_mappings.get(full_team_name)
                
                if not standard_abbr:
                    print(f"⚠️  Unknown team: {full_team_name}")
                    continue
                
                try:
                    # Extract defensive data
                    row_data = {
                        'team': standard_abbr,
                        'team_name': full_team_name,
                    }
                    
                    # EPA/Play (defensive EPA allowed, usually index 2)
                    if len(cells) > 2:
                        row_data['epa_def_allowed_per_play'] = self.parse_number(cells[2].get_text(strip=True))
                    
                    # Total EPA (usually index 3)
                    if len(cells) > 3:
                        row_data['total_epa_def_allowed'] = self.parse_number(cells[3].get_text(strip=True))
                    
                    # Success % (usually index 4)
                    if len(cells) > 4:
                        success_text = cells[4].get_text(strip=True)
                        row_data['success_rate_def'] = self.parse_number(success_text) / 100
                    
                    # EPA/Pass (usually index 5)
                    if len(cells) > 5:
                        row_data['epa_pass_def_allowed'] = self.parse_number(cells[5].get_text(strip=True))
                    
                    # EPA/Rush (usually index 6)
                    if len(cells) > 6:
                        row_data['epa_rush_def_allowed'] = self.parse_number(cells[6].get_text(strip=True))
                    
                    data.append(row_data)
                    
                except (ValueError, IndexError) as e:
                    print(f"⚠️  Error parsing row for {full_team_name}: {e}")
                    continue
            
            if data:
                df = pd.DataFrame(data)
                print(f"✅ Scraped defensive EPA for {len(df)} teams")
                return df
            else:
                print("❌ No defensive EPA data extracted")
                return None
                
        except Exception as e:
            print(f"❌ Error scraping defensive EPA: {e}")
            import traceback
            traceback.print_exc()
            return None
    
    def combine_data(self, off_df: pd.DataFrame, def_df: pd.DataFrame) -> pd.DataFrame:
        """Combine offensive and defensive EPA data into a single DataFrame"""
        
        if off_df.empty or def_df.empty:
            print("❌ Cannot combine data - one or both DataFrames are empty")
            return pd.DataFrame()
        
        # Merge on team abbreviation
        combined_df = pd.merge(off_df, def_df, on='team', how='outer', suffixes=('', '_def'))
        
        # Clean up team_name column (keep the one from offensive data, fallback to defensive)
        if 'team_name_def' in combined_df.columns:
            combined_df['team_name'] = combined_df['team_name'].fillna(combined_df['team_name_def'])
            combined_df = combined_df.drop('team_name_def', axis=1)
        
        # Calculate net EPA per play
        if 'epa_off_per_play' in combined_df.columns and 'epa_def_allowed_per_play' in combined_df.columns:
            combined_df['net_epa_per_play'] = combined_df['epa_off_per_play'] - combined_df['epa_def_allowed_per_play']
        
        # Sort by net EPA (best teams first)
        if 'net_epa_per_play' in combined_df.columns:
            combined_df = combined_df.sort_values('net_epa_per_play', ascending=False)
        
        # Add metadata
        combined_df['last_updated'] = datetime.now().strftime('%Y-%m-%d %H:%M:%S')
        combined_df['week'] = 16
        combined_df['season'] = 2025
        
        # Reorder columns to match Week10-14 format
        column_order = ['team', 'team_name', 'week', 'season', 'last_updated',
                       'epa_def_allowed_per_play', 'epa_off_per_play', 'epa_pass_def_allowed', 
                       'epa_pass_off', 'epa_rush_def_allowed', 'epa_rush_off', 
                       'net_epa_per_play', 'success_rate_def', 'success_rate_off',
                       'total_epa_def_allowed', 'total_epa_off']
        
        # Only include columns that exist
        final_columns = [col for col in column_order if col in combined_df.columns]
        # Add any remaining columns
        remaining_cols = [col for col in combined_df.columns if col not in final_columns]
        combined_df = combined_df[final_columns + remaining_cols]
        
        print(f"✅ Combined data for {len(combined_df)} teams")
        return combined_df
    
    def save_to_csv(self, df: pd.DataFrame, filename: str = "data/Week16_EPA.csv"):
        """Save EPA data to CSV"""
        
        if df.empty:
            print("❌ No data to save")
            return
        
        df.to_csv(filename, index=False)
        print(f"✅ Saved Week 16 EPA data to {filename}")
        print(f"   Total teams: {len(df)}")
        print(f"   Columns: {', '.join(df.columns.tolist())}")

def main():
    """Main function to scrape Week 16 EPA data"""
    
    print("="*80)
    print("WEEK 16 EPA DATA SCRAPER")
    print("="*80)
    print()
    
    scraper = Week16EPAScraper()
    
    # Scrape offensive data
    off_data = scraper.scrape_offensive_epa()
    time.sleep(2)  # Be respectful to the server
    
    # Scrape defensive data
    def_data = scraper.scrape_defensive_epa()
    
    if off_data is not None and def_data is not None:
        # Combine the data
        combined_data = scraper.combine_data(off_data, def_data)
        
        if not combined_data.empty:
            # Save to CSV
            scraper.save_to_csv(combined_data, "data/Week16_EPA.csv")
            
            print(f"\n✅ Successfully created Week16_EPA.csv!")
            print(f"📊 Data includes {len(combined_data)} teams with offensive and defensive EPA metrics")
        else:
            print("❌ Failed to combine EPA data")
    else:
        print("❌ Failed to scrape EPA data from SumerSports")
        print("   Please check your internet connection and try again")

if __name__ == "__main__":
    main()

