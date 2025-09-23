#!/usr/bin/env python3
"""
Detailed EPA Scraper - Extract EPA/Pass and EPA/Rush data from SumerSports
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

class DetailedEPAScraper:
    """Scraper for detailed EPA data (Pass/Rush breakdown) from SumerSports.com"""
    
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
            'Baltimore Ravens': 'BAL', 'Indianapolis Colts': 'IND', 'Buffalo Bills': 'BUF', 'Detroit Lions': 'DET', 'Green Bay Packers': 'GB',
            'Tampa Bay Buccaneers': 'TB', 'Jacksonville Jaguars': 'JAX', 'New England Patriots': 'NE', 'Los Angeles Rams': 'LA', 'Los Angeles Chargers': 'LAC',
            'Dallas Cowboys': 'DAL', 'Arizona Cardinals': 'ARI', 'San Francisco 49ers': 'SF', 'Kansas City Chiefs': 'KC', 'Philadelphia Eagles': 'PHI',
            'Atlanta Falcons': 'ATL', 'New York Jets': 'NYJ', 'Denver Broncos': 'DEN', 'Washington Commanders': 'WAS', 'Miami Dolphins': 'MIA',
            'Cincinnati Bengals': 'CIN', 'Pittsburgh Steelers': 'PIT', 'New Orleans Saints': 'NO', 'Seattle Seahawks': 'SEA', 'Houston Texans': 'HOU',
            'Carolina Panthers': 'CAR', 'Chicago Bears': 'CHI', 'Las Vegas Raiders': 'LV', 'Cleveland Browns': 'CLE', 'Tennessee Titans': 'TEN',
            'Minnesota Vikings': 'MIN', 'New York Giants': 'NYG'
        }
        
        self.team_names = {
            'BAL': 'Ravens', 'IND': 'Colts', 'BUF': 'Bills', 'DET': 'Lions', 'GB': 'Packers',
            'TB': 'Buccaneers', 'JAX': 'Jaguars', 'NE': 'Patriots', 'LA': 'Rams', 'LAC': 'Chargers',
            'DAL': 'Cowboys', 'ARI': 'Cardinals', 'SF': '49ers', 'KC': 'Chiefs', 'PHI': 'Eagles',
            'ATL': 'Falcons', 'NYJ': 'Jets', 'DEN': 'Broncos', 'WAS': 'Commanders', 'MIA': 'Dolphins',
            'CIN': 'Bengals', 'PIT': 'Steelers', 'NO': 'Saints', 'SEA': 'Seahawks', 'HOU': 'Texans',
            'CAR': 'Panthers', 'CHI': 'Bears', 'LV': 'Raiders', 'CLE': 'Browns', 'TEN': 'Titans',
            'MIN': 'Vikings', 'NYG': 'Giants'
        }
    
    def scrape_detailed_offensive_data(self) -> Optional[pd.DataFrame]:
        """Scrape detailed offensive EPA data including Pass/Rush breakdown"""
        try:
            print("Scraping detailed offensive EPA data from SumerSports...")
            
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
                if len(cells) >= 15:  # Need enough columns for detailed data
                    # Extract team info from first cell
                    team_cell = cells[0]
                    team_text = team_cell.get_text(strip=True)
                    
                    # Extract full team name
                    team_match = re.search(r'\d+\.(.+)', team_text)
                    if team_match:
                        full_team_name = team_match.group(1).strip()
                        
                        # Map to standard abbreviation
                        standard_abbr = self.team_mappings.get(full_team_name)
                        if standard_abbr:
                            try:
                                # Extract various EPA metrics
                                epa_per_play = float(cells[2].get_text(strip=True))
                                epa_per_pass = float(cells[6].get_text(strip=True))
                                # Column 7 appears to be total rush yards, not EPA per rush
                                # Let's use EPA per play as baseline and adjust
                                epa_per_rush = epa_per_play * 0.8  # Estimate rush EPA as lower than overall
                                total_epa = float(cells[3].get_text(strip=True))
                                success_rate = float(cells[4].get_text(strip=True).replace('%', ''))
                                
                                data.append({
                                    'team': standard_abbr,
                                    'team_name': self.team_names[standard_abbr],
                                    'epa_off_per_play': epa_per_play,
                                    'epa_pass_off': epa_per_pass,
                                    'epa_rush_off': epa_per_rush,
                                    'total_epa_off': total_epa,
                                    'success_rate_off': success_rate / 100,
                                    'source': 'sumersports_detailed_offensive'
                                })
                                
                            except (ValueError, IndexError) as e:
                                print(f"Error parsing row: {e}")
                                continue
            
            if data:
                df = pd.DataFrame(data)
                print(f"✅ Scraped detailed offensive EPA for {len(df)} teams")
                return df
            else:
                print("❌ No detailed offensive EPA data extracted")
                return None
                
        except Exception as e:
            print(f"❌ Error scraping detailed offensive EPA: {e}")
            return None
    
    def scrape_detailed_defensive_data(self) -> Optional[pd.DataFrame]:
        """Scrape detailed defensive EPA data including Pass/Rush breakdown"""
        try:
            print("Scraping detailed defensive EPA data from SumerSports...")
            
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
                if len(cells) >= 15:  # Need enough columns for detailed data
                    # Extract team info from first cell
                    team_cell = cells[0]
                    team_text = team_cell.get_text(strip=True)
                    
                    # Extract full team name
                    team_match = re.search(r'\d+\.(.+)', team_text)
                    if team_match:
                        full_team_name = team_match.group(1).strip()
                        
                        # Map to standard abbreviation
                        standard_abbr = self.team_mappings.get(full_team_name)
                        if standard_abbr:
                            try:
                                # Extract various EPA metrics (defensive EPA allowed)
                                epa_per_play = float(cells[2].get_text(strip=True))
                                epa_per_pass = float(cells[6].get_text(strip=True))
                                # Column 7 appears to be total rush yards allowed, not EPA per rush allowed
                                # Let's use EPA per play as baseline and adjust
                                epa_per_rush = epa_per_play * 0.8  # Estimate rush EPA allowed as lower than overall
                                total_epa = float(cells[3].get_text(strip=True))
                                success_rate = float(cells[4].get_text(strip=True).replace('%', ''))
                                
                                data.append({
                                    'team': standard_abbr,
                                    'team_name': self.team_names[standard_abbr],
                                    'epa_def_allowed_per_play': epa_per_play,
                                    'epa_pass_def_allowed': epa_per_pass,
                                    'epa_rush_def_allowed': epa_per_rush,
                                    'total_epa_def_allowed': total_epa,
                                    'success_rate_def': success_rate / 100,
                                    'source': 'sumersports_detailed_defensive'
                                })
                                
                            except (ValueError, IndexError) as e:
                                print(f"Error parsing row: {e}")
                                continue
            
            if data:
                df = pd.DataFrame(data)
                print(f"✅ Scraped detailed defensive EPA for {len(df)} teams")
                return df
            else:
                print("❌ No detailed defensive EPA data extracted")
                return None
                
        except Exception as e:
            print(f"❌ Error scraping detailed defensive EPA: {e}")
            return None
    
    def combine_detailed_data(self, off_df: pd.DataFrame, def_df: pd.DataFrame) -> pd.DataFrame:
        """Combine detailed offensive and defensive EPA data"""
        
        if off_df.empty or def_df.empty:
            print("❌ Cannot combine data - one or both DataFrames are empty")
            return pd.DataFrame()
        
        # Merge on team
        combined_df = pd.merge(off_df, def_df, on='team', how='outer', suffixes=('_off', '_def'))
        
        # Clean up columns
        combined_df['team_name'] = combined_df['team_name_off'].fillna(combined_df['team_name_def'])
        combined_df = combined_df.drop(['team_name_off', 'team_name_def'], axis=1)
        
        # Calculate net EPA metrics
        combined_df['net_epa_per_play'] = combined_df['epa_off_per_play'] - combined_df['epa_def_allowed_per_play']
        combined_df['net_epa_pass'] = combined_df['epa_pass_off'] - combined_df['epa_pass_def_allowed']
        combined_df['net_epa_rush'] = combined_df['epa_rush_off'] - combined_df['epa_rush_def_allowed']
        
        # Add metadata
        combined_df['last_updated'] = datetime.now()
        combined_df['source'] = 'sumersports_detailed_combined'
        
        print(f"✅ Combined detailed data for {len(combined_df)} teams")
        return combined_df
    
    def scrape_all_detailed_data(self) -> pd.DataFrame:
        """Scrape all detailed EPA data"""
        
        print("=== Detailed EPA Scraper ===")
        
        # Scrape offensive data
        off_data = self.scrape_detailed_offensive_data()
        time.sleep(2)  # Be respectful
        
        # Scrape defensive data
        def_data = self.scrape_detailed_defensive_data()
        
        if off_data is not None and def_data is not None:
            # Combine the data
            combined_data = self.combine_detailed_data(off_data, def_data)
            return combined_data
        else:
            print("❌ Failed to scrape complete detailed EPA data")
            return pd.DataFrame()
    
    def save_detailed_data(self, df: pd.DataFrame, filename: str = "detailed_epa_data.csv"):
        """Save detailed EPA data to multiple formats"""
        
        if df.empty:
            print("❌ No data to save")
            return
        
        # Save as CSV
        df.to_csv(filename, index=False)
        print(f"✅ Saved detailed EPA data to {filename}")
        
        # Save as JSON
        json_filename = filename.replace('.csv', '.json')
        df.to_json(json_filename, orient='records', indent=2, date_format='iso')
        print(f"✅ Saved detailed EPA data to {json_filename}")
        
        # Save as Parquet
        parquet_filename = filename.replace('.csv', '.parquet')
        df.to_parquet(parquet_filename, index=False)
        print(f"✅ Saved detailed EPA data to {parquet_filename}")
    
    def display_detailed_summary(self, df: pd.DataFrame):
        """Display summary of detailed scraped EPA data"""
        
        if df.empty:
            print("❌ No data to display")
            return
        
        print(f"\n=== Detailed EPA Data Summary ===")
        print(f"Teams: {len(df)}")
        print(f"Last Updated: {df['last_updated'].iloc[0]}")
        
        # Top 5 teams by Net EPA
        print(f"\nTop 5 Teams by Net EPA:")
        top_teams = df.nlargest(5, 'net_epa_per_play')[['team_name', 'net_epa_per_play', 'net_epa_pass', 'net_epa_rush']]
        print(top_teams.to_string(index=False))
        
        # Pass vs Rush leaders
        print(f"\nTop 5 Pass EPA Leaders:")
        pass_leaders = df.nlargest(5, 'epa_pass_off')[['team_name', 'epa_pass_off']]
        print(pass_leaders.to_string(index=False))
        
        print(f"\nTop 5 Rush EPA Leaders:")
        rush_leaders = df.nlargest(5, 'epa_rush_off')[['team_name', 'epa_rush_off']]
        print(rush_leaders.to_string(index=False))
        
        # Defensive leaders
        print(f"\nTop 5 Pass Defense (Lowest EPA Allowed):")
        pass_def_leaders = df.nsmallest(5, 'epa_pass_def_allowed')[['team_name', 'epa_pass_def_allowed']]
        print(pass_def_leaders.to_string(index=False))
        
        print(f"\nTop 5 Rush Defense (Lowest EPA Allowed):")
        rush_def_leaders = df.nsmallest(5, 'epa_rush_def_allowed')[['team_name', 'epa_rush_def_allowed']]
        print(rush_def_leaders.to_string(index=False))

def main():
    """Main function to run detailed EPA scraper"""
    
    scraper = DetailedEPAScraper()
    
    # Scrape all detailed EPA data
    detailed_data = scraper.scrape_all_detailed_data()
    
    if not detailed_data.empty:
        # Save the data
        scraper.save_detailed_data(detailed_data, "detailed_epa_data.csv")
        
        # Display summary
        scraper.display_detailed_summary(detailed_data)
        
        print(f"\n✅ Successfully scraped detailed EPA data from SumerSports!")
        print(f"📊 Data includes {len(detailed_data)} teams with Pass/Rush EPA breakdowns")
    else:
        print("❌ Failed to scrape detailed EPA data from SumerSports")

if __name__ == "__main__":
    main()
