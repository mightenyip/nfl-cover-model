#!/usr/bin/env python3
"""
EPA Scraper - Scrape online EPA results for real-time team metrics
"""

import requests
import pandas as pd
import numpy as np
from bs4 import BeautifulSoup
import time
import json
from typing import Dict, List, Optional
import re

class EPAScraper:
    """Scraper for online EPA data from various sources"""
    
    def __init__(self):
        self.session = requests.Session()
        self.session.headers.update({
            'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/91.0.4472.124 Safari/537.36'
        })
        
        # Team name mappings
        self.team_mappings = {
            'ARI': 'Cardinals', 'ATL': 'Falcons', 'BAL': 'Ravens', 'BUF': 'Bills',
            'CAR': 'Panthers', 'CHI': 'Bears', 'CIN': 'Bengals', 'CLE': 'Browns',
            'DAL': 'Cowboys', 'DEN': 'Broncos', 'DET': 'Lions', 'GB': 'Packers',
            'HOU': 'Texans', 'IND': 'Colts', 'JAX': 'Jaguars', 'KC': 'Chiefs',
            'LA': 'Rams', 'LAC': 'Chargers', 'LV': 'Raiders', 'MIA': 'Dolphins',
            'MIN': 'Vikings', 'NE': 'Patriots', 'NO': 'Saints', 'NYG': 'Giants',
            'NYJ': 'Jets', 'PHI': 'Eagles', 'PIT': 'Steelers', 'SF': '49ers',
            'SEA': 'Seahawks', 'TB': 'Buccaneers', 'TEN': 'Titans', 'WAS': 'Commanders'
        }
        
        self.reverse_mappings = {v: k for k, v in self.team_mappings.items()}
    
    def scrape_espn_epa(self) -> Optional[pd.DataFrame]:
        """Scrape EPA data from ESPN (if available)"""
        try:
            print("Attempting to scrape EPA data from ESPN...")
            
            # ESPN doesn't typically have EPA data publicly available
            # This is a placeholder for future implementation
            print("ESPN EPA scraping not yet implemented")
            return None
            
        except Exception as e:
            print(f"Error scraping ESPN EPA: {e}")
            return None
    
    def scrape_pro_football_reference(self) -> Optional[pd.DataFrame]:
        """Scrape EPA data from Pro Football Reference"""
        try:
            print("Attempting to scrape EPA data from Pro Football Reference...")
            
            # PFR URL for team stats
            url = "https://www.pro-football-reference.com/years/2025/"
            
            response = self.session.get(url, timeout=10)
            response.raise_for_status()
            
            soup = BeautifulSoup(response.content, 'html.parser')
            
            # Look for team stats tables
            tables = soup.find_all('table')
            
            for table in tables:
                if 'team_stats' in table.get('id', '').lower():
                    print("Found team stats table on PFR")
                    # Parse the table here
                    break
            
            print("PFR EPA scraping not yet fully implemented")
            return None
            
        except Exception as e:
            print(f"Error scraping Pro Football Reference: {e}")
            return None
    
    def scrape_nfl_com_stats(self) -> Optional[pd.DataFrame]:
        """Scrape EPA data from NFL.com stats"""
        try:
            print("Attempting to scrape EPA data from NFL.com...")
            
            # NFL.com stats URL
            url = "https://www.nfl.com/stats/team-stats/"
            
            response = self.session.get(url, timeout=10)
            response.raise_for_status()
            
            soup = BeautifulSoup(response.content, 'html.parser')
            
            # Look for stats tables
            tables = soup.find_all('table')
            
            print("NFL.com EPA scraping not yet fully implemented")
            return None
            
        except Exception as e:
            print(f"Error scraping NFL.com: {e}")
            return None
    
    def scrape_fantasy_pros_epa(self) -> Optional[pd.DataFrame]:
        """Scrape EPA data from FantasyPros or similar analytics sites"""
        try:
            print("Attempting to scrape EPA data from FantasyPros...")
            
            # This would be a more likely source for EPA data
            # Many analytics sites provide EPA metrics
            
            print("FantasyPros EPA scraping not yet implemented")
            return None
            
        except Exception as e:
            print(f"Error scraping FantasyPros: {e}")
            return None
    
    def scrape_team_rankings_epa(self) -> Optional[pd.DataFrame]:
        """Scrape EPA data from TeamRankings or similar sites"""
        try:
            print("Attempting to scrape EPA data from TeamRankings...")
            
            # TeamRankings often has advanced metrics
            url = "https://www.teamrankings.com/nfl/stat/expected-points-added"
            
            response = self.session.get(url, timeout=10)
            response.raise_for_status()
            
            soup = BeautifulSoup(response.content, 'html.parser')
            
            # Look for EPA data tables
            tables = soup.find_all('table')
            
            for table in tables:
                if 'epa' in str(table).lower():
                    print("Found potential EPA table on TeamRankings")
                    # Parse the table here
                    break
            
            print("TeamRankings EPA scraping not yet fully implemented")
            return None
            
        except Exception as e:
            print(f"Error scraping TeamRankings: {e}")
            return None
    
    def scrape_all_sources(self) -> pd.DataFrame:
        """Try to scrape EPA data from all available sources"""
        
        print("=== EPA Scraper - Attempting All Sources ===")
        
        scrapers = [
            self.scrape_espn_epa,
            self.scrape_pro_football_reference,
            self.scrape_nfl_com_stats,
            self.scrape_fantasy_pros_epa,
            self.scrape_team_rankings_epa
        ]
        
        results = []
        
        for scraper in scrapers:
            try:
                result = scraper()
                if result is not None:
                    results.append(result)
                    print(f"✅ Successfully scraped data from {scraper.__name__}")
                else:
                    print(f"❌ No data from {scraper.__name__}")
            except Exception as e:
                print(f"❌ Error with {scraper.__name__}: {e}")
            
            # Be respectful with delays
            time.sleep(1)
        
        if results:
            # Combine all results
            combined_df = pd.concat(results, ignore_index=True)
            print(f"✅ Combined {len(results)} data sources")
            return combined_df
        else:
            print("❌ No data scraped from any source")
            return pd.DataFrame()
    
    def create_mock_epa_data(self) -> pd.DataFrame:
        """Create mock EPA data for testing purposes"""
        
        print("Creating mock EPA data for testing...")
        
        # Mock data based on recent performance
        mock_data = {
            'team': list(self.team_mappings.keys()),
            'team_name': list(self.team_mappings.values()),
            'epa_off_per_play': np.random.normal(0, 0.1, 32),
            'epa_def_allowed_per_play': np.random.normal(0, 0.1, 32),
            'net_epa_per_play': np.random.normal(0, 0.15, 32),
            'source': 'mock_data',
            'last_updated': pd.Timestamp.now()
        }
        
        df = pd.DataFrame(mock_data)
        
        # Calculate net EPA
        df['net_epa_per_play'] = df['epa_off_per_play'] - df['epa_def_allowed_per_play']
        
        print(f"✅ Created mock EPA data for {len(df)} teams")
        return df
    
    def save_epa_data(self, df: pd.DataFrame, filename: str = "scraped_epa_data.csv"):
        """Save scraped EPA data to CSV"""
        
        if df.empty:
            print("❌ No data to save")
            return
        
        df.to_csv(filename, index=False)
        print(f"✅ Saved EPA data to {filename}")
        
        # Also save as JSON for API use
        json_filename = filename.replace('.csv', '.json')
        df.to_json(json_filename, orient='records', indent=2)
        print(f"✅ Saved EPA data to {json_filename}")

def main():
    """Main function to run EPA scraper"""
    
    scraper = EPAScraper()
    
    # Try to scrape real data
    scraped_data = scraper.scrape_all_sources()
    
    if scraped_data.empty:
        print("\n=== No real data available, creating mock data ===")
        scraped_data = scraper.create_mock_epa_data()
    
    # Save the data
    scraper.save_epa_data(scraped_data, "scraped_epa_data.csv")
    
    # Display summary
    print(f"\n=== EPA Data Summary ===")
    print(f"Teams: {len(scraped_data)}")
    print(f"Columns: {list(scraped_data.columns)}")
    
    if not scraped_data.empty:
        print(f"\nTop 5 teams by Net EPA:")
        top_teams = scraped_data.nlargest(5, 'net_epa_per_play')[['team_name', 'net_epa_per_play']]
        print(top_teams.to_string(index=False))
        
        print(f"\nBottom 5 teams by Net EPA:")
        bottom_teams = scraped_data.nsmallest(5, 'net_epa_per_play')[['team_name', 'net_epa_per_play']]
        print(bottom_teams.to_string(index=False))

if __name__ == "__main__":
    main()
