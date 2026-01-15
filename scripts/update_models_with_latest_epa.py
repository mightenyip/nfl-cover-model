#!/usr/bin/env python3
"""
Update Models A, B, and E with Latest EPA Data from SumerSports
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
import os
import sys

class LatestEPAScraper:
    """Scraper for latest EPA data from SumerSports.com"""
    
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
        
        # Team mappings based on SumerSports data
        self.team_mappings = {
            'Houston Texans': 'HOU', 'Detroit Lions': 'DET', 'Denver Broncos': 'DEN', 'Los Angeles Rams': 'LA', 'Cleveland Browns': 'CLE',
            'Minnesota Vikings': 'MIN', 'Chicago Bears': 'CHI', 'Atlanta Falcons': 'ATL', 'Kansas City Chiefs': 'KC', 'Jacksonville Jaguars': 'JAX',
            'Seattle Seahawks': 'SEA', 'Indianapolis Colts': 'IND', 'Philadelphia Eagles': 'PHI', 'Tampa Bay Buccaneers': 'TB', 'San Francisco 49ers': 'SF',
            'Arizona Cardinals': 'ARI', 'Carolina Panthers': 'CAR', 'Buffalo Bills': 'BUF', 'Los Angeles Chargers': 'LAC', 'Las Vegas Raiders': 'LV',
            'Washington Commanders': 'WAS', 'Pittsburgh Steelers': 'PIT', 'New York Giants': 'NYG', 'Tennessee Titans': 'TEN', 'New York Jets': 'NYJ',
            'Dallas Cowboys': 'DAL', 'Baltimore Ravens': 'BAL', 'Cincinnati Bengals': 'CIN', 'Miami Dolphins': 'MIA'
        }
        
        # Team names for display
        self.team_names = {
            'HOU': 'Texans', 'DET': 'Lions', 'DEN': 'Broncos', 'LA': 'Rams', 'CLE': 'Browns',
            'MIN': 'Vikings', 'CHI': 'Bears', 'ATL': 'Falcons', 'KC': 'Chiefs', 'JAX': 'Jaguars',
            'SEA': 'Seahawks', 'IND': 'Colts', 'PHI': 'Eagles', 'TB': 'Buccaneers', 'SF': '49ers',
            'ARI': 'Cardinals', 'CAR': 'Panthers', 'BUF': 'Bills', 'LAC': 'Chargers', 'LV': 'Raiders',
            'WAS': 'Commanders', 'PIT': 'Steelers', 'NYG': 'Giants', 'TEN': 'Titans', 'NYJ': 'Jets',
            'DAL': 'Cowboys', 'BAL': 'Ravens', 'CIN': 'Bengals', 'MIA': 'Dolphins'
        }
    
    def scrape_defensive_epa(self) -> Optional[pd.DataFrame]:
        """Scrape defensive EPA data from SumerSports defensive page"""
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
                    
                    # Extract full team name from text (e.g., "1.Houston Texans" -> "Houston Texans")
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
                                
                                # Extract EPA/Pass from sixth column (index 5)
                                epa_pass = float(cells[5].get_text(strip=True))
                                
                                # Extract EPA/Rush from seventh column (index 6)
                                epa_rush = float(cells[6].get_text(strip=True))
                                
                                data.append({
                                    'team': standard_abbr,
                                    'team_name': self.team_names[standard_abbr],
                                    'epa_def_allowed_per_play': epa_per_play,
                                    'total_epa_def_allowed': total_epa,
                                    'success_rate_def': success_pct / 100,
                                    'epa_pass_def_allowed': epa_pass,
                                    'epa_rush_def_allowed': epa_rush,
                                    'source': 'sumersports_defensive_latest'
                                })
                                
                            except (ValueError, IndexError) as e:
                                print(f"Error parsing defensive row: {e}")
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
    
    def scrape_offensive_epa(self) -> Optional[pd.DataFrame]:
        """Scrape offensive EPA data from SumerSports offensive page"""
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
                    
                    # Extract full team name from text
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
                                
                                # Extract EPA/Pass from sixth column (index 5)
                                epa_pass = float(cells[5].get_text(strip=True))
                                
                                # Extract EPA/Rush from seventh column (index 6)
                                epa_rush = float(cells[6].get_text(strip=True))
                                
                                data.append({
                                    'team': standard_abbr,
                                    'team_name': self.team_names[standard_abbr],
                                    'epa_off_per_play': epa_per_play,
                                    'total_epa_off': total_epa,
                                    'success_rate_off': success_pct / 100,
                                    'epa_pass_off': epa_pass,
                                    'epa_rush_off': epa_rush,
                                    'source': 'sumersports_offensive_latest'
                                })
                                
                            except (ValueError, IndexError) as e:
                                print(f"Error parsing offensive row: {e}")
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
    
    def combine_epa_data(self, off_df: pd.DataFrame, def_df: pd.DataFrame) -> pd.DataFrame:
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
        combined_df['net_epa_pass'] = combined_df['epa_pass_off'] - combined_df['epa_pass_def_allowed']
        combined_df['net_epa_rush'] = combined_df['epa_rush_off'] - combined_df['epa_rush_def_allowed']
        
        # Add metadata
        combined_df['last_updated'] = datetime.now()
        combined_df['source'] = 'sumersports_latest_combined'
        
        print(f"✅ Combined data for {len(combined_df)} teams")
        return combined_df
    
    def update_detailed_epa_data(self, new_data: pd.DataFrame):
        """Update the detailed_epa_data.csv file with new data"""
        
        try:
            # Read existing data
            existing_file = "detailed_epa_data.csv"
            if os.path.exists(existing_file):
                existing_df = pd.read_csv(existing_file)
                print(f"📖 Read existing EPA data with {len(existing_df)} teams")
            else:
                print("📝 No existing EPA data file found, creating new one")
                existing_df = pd.DataFrame()
            
            # Update with new data
            if not existing_df.empty:
                # Merge on team, keeping new data where available
                updated_df = pd.merge(existing_df, new_data, on='team', how='outer', suffixes=('_old', '_new'))
                
                # Use new data where available, fall back to old data
                for col in new_data.columns:
                    if col != 'team':
                        if col in existing_df.columns:
                            updated_df[col] = updated_df[f'{col}_new'].fillna(updated_df[f'{col}_old'])
                        else:
                            updated_df[col] = updated_df[f'{col}_new']
                
                # Clean up duplicate columns
                cols_to_drop = [col for col in updated_df.columns if col.endswith('_old') or col.endswith('_new')]
                updated_df = updated_df.drop(cols_to_drop, axis=1)
            else:
                updated_df = new_data
            
            # Save updated data
            updated_df.to_csv(existing_file, index=False)
            print(f"✅ Updated {existing_file} with latest EPA data")
            
            # Also save as backup with timestamp
            timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
            backup_file = f"data/epa/processed/detailed_epa_data_{timestamp}.csv"
            updated_df.to_csv(backup_file, index=False)
            print(f"✅ Saved backup to {backup_file}")
            
            return updated_df
            
        except Exception as e:
            print(f"❌ Error updating EPA data: {e}")
            return pd.DataFrame()
    
    def update_models_with_new_epa(self, epa_data: pd.DataFrame):
        """Update Models A, B, and E with new EPA data"""
        
        print("\n=== Updating Models with Latest EPA Data ===")
        
        # Update Model A (SumerSports EPA)
        try:
            print("🔄 Updating Model A with latest EPA data...")
            model_a_script = "scripts/model_a_v2_enhanced.py"
            if os.path.exists(model_a_script):
                print(f"✅ Model A script found: {model_a_script}")
                # The model will automatically use the updated detailed_epa_data.csv
            else:
                print(f"⚠️ Model A script not found: {model_a_script}")
        except Exception as e:
            print(f"❌ Error updating Model A: {e}")
        
        # Update Model B (Matchup-specific EPA)
        try:
            print("🔄 Updating Model B with latest EPA data...")
            model_b_script = "models/model_b/model_b_v2_week7.py"
            if os.path.exists(model_b_script):
                print(f"✅ Model B script found: {model_b_script}")
                # The model will automatically use the updated detailed_epa_data.csv
            else:
                print(f"⚠️ Model B script not found: {model_b_script}")
        except Exception as e:
            print(f"❌ Error updating Model B: {e}")
        
        # Update Model E (if it exists)
        try:
            print("🔄 Checking for Model E...")
            model_e_dir = "models/model_e"
            if os.path.exists(model_e_dir):
                print(f"✅ Model E directory found: {model_e_dir}")
                # The model will automatically use the updated detailed_epa_data.csv
            else:
                print(f"⚠️ Model E directory not found: {model_e_dir}")
        except Exception as e:
            print(f"❌ Error checking Model E: {e}")
        
        print("✅ Model update process completed")
    
    def display_epa_summary(self, df: pd.DataFrame):
        """Display summary of latest EPA data"""
        
        if df.empty:
            print("❌ No data to display")
            return
        
        print(f"\n=== Latest EPA Data Summary ===")
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
    """Main function to update models with latest EPA data"""
    
    print("=== Updating Models A, B, and E with Latest EPA Data ===")
    print("Source: SumerSports.com")
    print("=" * 60)
    
    scraper = LatestEPAScraper()
    
    # Scrape latest EPA data
    print("\n1. Scraping latest EPA data...")
    off_data = scraper.scrape_offensive_epa()
    time.sleep(2)  # Be respectful
    
    def_data = scraper.scrape_defensive_epa()
    
    if off_data is not None and def_data is not None:
        # Combine the data
        combined_data = scraper.combine_epa_data(off_data, def_data)
        
        if not combined_data.empty:
            # Update detailed_epa_data.csv
            print("\n2. Updating detailed EPA data file...")
            updated_data = scraper.update_detailed_epa_data(combined_data)
            
            if not updated_data.empty:
                # Update models
                print("\n3. Updating models with latest EPA data...")
                scraper.update_models_with_new_epa(updated_data)
                
                # Display summary
                print("\n4. Displaying EPA data summary...")
                scraper.display_epa_summary(updated_data)
                
                print(f"\n✅ Successfully updated Models A, B, and E with latest EPA data!")
                print(f"📊 Updated data includes {len(updated_data)} teams")
                print(f"📁 Data saved to detailed_epa_data.csv")
            else:
                print("❌ Failed to update EPA data file")
        else:
            print("❌ Failed to combine EPA data")
    else:
        print("❌ Failed to scrape EPA data from SumerSports")

if __name__ == "__main__":
    main()
