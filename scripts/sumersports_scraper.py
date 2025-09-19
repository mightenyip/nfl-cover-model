#!/usr/bin/env python3
"""
SumerSports EPA Scraper - Extract EPA data from SumerSports.com
"""

import requests
import pandas as pd
import numpy as np
from bs4 import BeautifulSoup
import time
import json
from typing import Dict, List, Optional
import re
from datetime import datetime

class SumerSportsScraper:
    """Scraper for EPA data from SumerSports.com"""
    
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
        
        # Team mappings based on SumerSports data (full team names)
        self.team_mappings = {
            'Baltimore Ravens': 'BAL', 'Indianapolis Colts': 'IND', 'Buffalo Bills': 'BUF', 'Detroit Lions': 'DET', 'Green Bay Packers': 'GB',
            'Tampa Bay Buccaneers': 'TB', 'Jacksonville Jaguars': 'JAX', 'New England Patriots': 'NE', 'Los Angeles Rams': 'LA', 'Los Angeles Chargers': 'LAC',
            'Dallas Cowboys': 'DAL', 'Arizona Cardinals': 'ARI', 'San Francisco 49ers': 'SF', 'Kansas City Chiefs': 'KC', 'Philadelphia Eagles': 'PHI',
            'Atlanta Falcons': 'ATL', 'New York Jets': 'NYJ', 'Denver Broncos': 'DEN', 'Washington Commanders': 'WAS', 'Miami Dolphins': 'MIA',
            'Cincinnati Bengals': 'CIN', 'Pittsburgh Steelers': 'PIT', 'New Orleans Saints': 'NO', 'Seattle Seahawks': 'SEA', 'Houston Texans': 'HOU',
            'Carolina Panthers': 'CAR', 'Chicago Bears': 'CHI', 'Las Vegas Raiders': 'LV', 'Cleveland Browns': 'CLE', 'Tennessee Titans': 'TEN',
            'Minnesota Vikings': 'MIN', 'New York Giants': 'NYG'
        }
        
        # Full team names
        self.team_names = {
            'BAL': 'Ravens', 'IND': 'Colts', 'BUF': 'Bills', 'DET': 'Lions', 'GB': 'Packers',
            'TB': 'Buccaneers', 'JAX': 'Jaguars', 'NE': 'Patriots', 'LA': 'Rams', 'LAC': 'Chargers',
            'DAL': 'Cowboys', 'ARI': 'Cardinals', 'SF': '49ers', 'KC': 'Chiefs', 'PHI': 'Eagles',
            'ATL': 'Falcons', 'NYJ': 'Jets', 'DEN': 'Broncos', 'WAS': 'Commanders', 'MIA': 'Dolphins',
            'CIN': 'Bengals', 'PIT': 'Steelers', 'NO': 'Saints', 'SEA': 'Seahawks', 'HOU': 'Texans',
            'CAR': 'Panthers', 'CHI': 'Bears', 'LV': 'Raiders', 'CLE': 'Browns', 'TEN': 'Titans',
            'MIN': 'Vikings', 'NYG': 'Giants'
        }
    
    def scrape_offensive_epa(self) -> Optional[pd.DataFrame]:
        """Scrape offensive EPA data from SumerSports"""
        try:
            print("Scraping offensive EPA data from SumerSports...")
            
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
                if len(cells) >= 4:
                    # Extract team info from first cell
                    team_cell = cells[0]
                    team_text = team_cell.get_text(strip=True)
                    
                    # Extract full team name from text (e.g., "1.Baltimore Ravens" -> "Baltimore Ravens")
                    # The text format is "1.Baltimore Ravens" so we need to extract the full team name
                    team_match = re.search(r'\d+\.(.+)', team_text)
                    if team_match:
                        full_team_name = team_match.group(1).strip()
                        
                        # Map to standard abbreviation
                        standard_abbr = self.team_mappings.get(full_team_name)
                        if standard_abbr:
                            try:
                                # Extract EPA/Play from third column (index 2)
                                epa_per_play = float(cells[2].get_text(strip=True))
                                
                                # Extract Total EPA from fourth column (index 3)
                                total_epa = float(cells[3].get_text(strip=True))
                                
                                # Extract Success % from fifth column (index 4)
                                success_pct = float(cells[4].get_text(strip=True).replace('%', ''))
                                
                                data.append({
                                    'team': standard_abbr,
                                    'team_name': self.team_names[standard_abbr],
                                    'epa_off_per_play': epa_per_play,
                                    'total_epa_off': total_epa,
                                    'success_rate_off': success_pct / 100,
                                    'source': 'sumersports_offensive'
                                })
                                
                            except (ValueError, IndexError) as e:
                                print(f"Error parsing row: {e}")
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
            return None
    
    def scrape_defensive_epa(self) -> Optional[pd.DataFrame]:
        """Scrape defensive EPA data from SumerSports"""
        try:
            print("Scraping defensive EPA data from SumerSports...")
            
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
                if len(cells) >= 4:
                    # Extract team info from first cell
                    team_cell = cells[0]
                    team_text = team_cell.get_text(strip=True)
                    
                    # Extract full team name from text
                    team_match = re.search(r'\d+\.(.+)', team_text)
                    if team_match:
                        full_team_name = team_match.group(1).strip()
                        
                        # Map to standard abbreviation
                        standard_abbr = self.team_mappings.get(full_team_name)
                        if standard_abbr:
                            try:
                                # Extract EPA/Play from third column (index 2) - defensive EPA allowed
                                epa_per_play = float(cells[2].get_text(strip=True))
                                
                                # Extract Total EPA from fourth column (index 3)
                                total_epa = float(cells[3].get_text(strip=True))
                                
                                # Extract Success % from fifth column (index 4)
                                success_pct = float(cells[4].get_text(strip=True).replace('%', ''))
                                
                                data.append({
                                    'team': standard_abbr,
                                    'team_name': self.team_names[standard_abbr],
                                    'epa_def_allowed_per_play': epa_per_play,
                                    'total_epa_def_allowed': total_epa,
                                    'success_rate_def': success_pct / 100,
                                    'source': 'sumersports_defensive'
                                })
                                
                            except (ValueError, IndexError) as e:
                                print(f"Error parsing row: {e}")
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
            return None
    
    def combine_offensive_defensive_data(self, off_df: pd.DataFrame, def_df: pd.DataFrame) -> pd.DataFrame:
        """Combine offensive and defensive EPA data"""
        
        if off_df.empty or def_df.empty:
            print("❌ Cannot combine data - one or both DataFrames are empty")
            return pd.DataFrame()
        
        # Merge on team
        combined_df = pd.merge(off_df, def_df, on='team', how='outer', suffixes=('_off', '_def'))
        
        # Clean up columns
        combined_df['team_name'] = combined_df['team_name_off'].fillna(combined_df['team_name_def'])
        combined_df = combined_df.drop(['team_name_off', 'team_name_def'], axis=1)
        
        # Calculate net EPA
        combined_df['net_epa_per_play'] = combined_df['epa_off_per_play'] - combined_df['epa_def_allowed_per_play']
        
        # Add metadata
        combined_df['last_updated'] = datetime.now()
        combined_df['source'] = 'sumersports_combined'
        
        print(f"✅ Combined data for {len(combined_df)} teams")
        return combined_df
    
    def scrape_all_epa_data(self) -> pd.DataFrame:
        """Scrape both offensive and defensive EPA data"""
        
        print("=== SumerSports EPA Scraper ===")
        
        # Scrape offensive data
        off_data = self.scrape_offensive_epa()
        time.sleep(2)  # Be respectful
        
        # Scrape defensive data
        def_data = self.scrape_defensive_epa()
        
        if off_data is not None and def_data is not None:
            # Combine the data
            combined_data = self.combine_offensive_defensive_data(off_data, def_data)
            return combined_data
        else:
            print("❌ Failed to scrape complete EPA data")
            return pd.DataFrame()
    
    def save_epa_data(self, df: pd.DataFrame, filename: str = "sumersports_epa_data.csv"):
        """Save EPA data to multiple formats"""
        
        if df.empty:
            print("❌ No data to save")
            return
        
        # Save as CSV
        df.to_csv(filename, index=False)
        print(f"✅ Saved EPA data to {filename}")
        
        # Save as JSON
        json_filename = filename.replace('.csv', '.json')
        df.to_json(json_filename, orient='records', indent=2, date_format='iso')
        print(f"✅ Saved EPA data to {json_filename}")
        
        # Save as Parquet
        parquet_filename = filename.replace('.csv', '.parquet')
        df.to_parquet(parquet_filename, index=False)
        print(f"✅ Saved EPA data to {parquet_filename}")
    
    def display_summary(self, df: pd.DataFrame):
        """Display summary of scraped EPA data"""
        
        if df.empty:
            print("❌ No data to display")
            return
        
        print(f"\n=== SumerSports EPA Data Summary ===")
        print(f"Teams: {len(df)}")
        print(f"Last Updated: {df['last_updated'].iloc[0]}")
        
        # Top 5 teams by Net EPA
        print(f"\nTop 5 Teams by Net EPA:")
        top_teams = df.nlargest(5, 'net_epa_per_play')[['team_name', 'epa_off_per_play', 'epa_def_allowed_per_play', 'net_epa_per_play']]
        print(top_teams.to_string(index=False))
        
        # Bottom 5 teams by Net EPA
        print(f"\nBottom 5 Teams by Net EPA:")
        bottom_teams = df.nsmallest(5, 'net_epa_per_play')[['team_name', 'epa_off_per_play', 'epa_def_allowed_per_play', 'net_epa_per_play']]
        print(bottom_teams.to_string(index=False))
        
        # Offensive leaders
        print(f"\nTop 5 Offensive EPA/Play:")
        off_leaders = df.nlargest(5, 'epa_off_per_play')[['team_name', 'epa_off_per_play']]
        print(off_leaders.to_string(index=False))
        
        # Defensive leaders (lowest EPA allowed)
        print(f"\nTop 5 Defensive EPA/Play (Lowest Allowed):")
        def_leaders = df.nsmallest(5, 'epa_def_allowed_per_play')[['team_name', 'epa_def_allowed_per_play']]
        print(def_leaders.to_string(index=False))

def main():
    """Main function to run SumerSports scraper"""
    
    scraper = SumerSportsScraper()
    
    # Scrape all EPA data
    epa_data = scraper.scrape_all_epa_data()
    
    if not epa_data.empty:
        # Save the data
        scraper.save_epa_data(epa_data, "sumersports_epa_data.csv")
        
        # Display summary
        scraper.display_summary(epa_data)
        
        print(f"\n✅ Successfully scraped EPA data from SumerSports!")
        print(f"📊 Data includes {len(epa_data)} teams with offensive and defensive EPA metrics")
    else:
        print("❌ Failed to scrape EPA data from SumerSports")

if __name__ == "__main__":
    main()
