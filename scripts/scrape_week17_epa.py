#!/usr/bin/env python3
"""
Scrape Week 17 EPA Data from SumerSports
Creates a comprehensive CSV with both offensive and defensive EPA metrics
"""

import re
import time
from datetime import datetime
from typing import Optional

import pandas as pd
import requests
from bs4 import BeautifulSoup


class Week17EPAScraper:
    """Scraper for Week 17 EPA data from SumerSports.com"""

    def __init__(self):
        self.session = requests.Session()
        self.session.headers.update(
            {
                "User-Agent": "Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/120.0.0.0 Safari/537.36",
                "Accept": "text/html,application/xhtml+xml,application/xml;q=0.9,image/webp,*/*;q=0.8",
                "Accept-Language": "en-US,en;q=0.5",
                "Accept-Encoding": "gzip, deflate",
                "Connection": "keep-alive",
                "Referer": "https://sumersports.com/",
            }
        )

        # Team mappings
        self.team_mappings = {
            "Arizona Cardinals": "ARI",
            "Atlanta Falcons": "ATL",
            "Baltimore Ravens": "BAL",
            "Buffalo Bills": "BUF",
            "Carolina Panthers": "CAR",
            "Chicago Bears": "CHI",
            "Cincinnati Bengals": "CIN",
            "Cleveland Browns": "CLE",
            "Dallas Cowboys": "DAL",
            "Denver Broncos": "DEN",
            "Detroit Lions": "DET",
            "Green Bay Packers": "GB",
            "Houston Texans": "HOU",
            "Indianapolis Colts": "IND",
            "Jacksonville Jaguars": "JAX",
            "Kansas City Chiefs": "KC",
            "Las Vegas Raiders": "LV",
            "Los Angeles Chargers": "LAC",
            "Los Angeles Rams": "LA",
            "Miami Dolphins": "MIA",
            "Minnesota Vikings": "MIN",
            "New England Patriots": "NE",
            "New Orleans Saints": "NO",
            "New York Giants": "NYG",
            "New York Jets": "NYJ",
            "Philadelphia Eagles": "PHI",
            "Pittsburgh Steelers": "PIT",
            "San Francisco 49ers": "SF",
            "Seattle Seahawks": "SEA",
            "Tampa Bay Buccaneers": "TB",
            "Tennessee Titans": "TEN",
            "Washington Commanders": "WAS",
        }

    def parse_number(self, text: str) -> float:
        """Parse a number from text, handling commas and negative signs"""
        if not text or text.strip() == "-":
            return 0.0
        cleaned = text.strip().replace(",", "").replace("%", "")
        try:
            return float(cleaned)
        except ValueError:
            return 0.0

    def scrape_offensive_epa(self) -> Optional[pd.DataFrame]:
        """Scrape offensive EPA data from SumerSports"""
        try:
            print("Scraping offensive EPA data from https://sumersports.com/teams/offensive/...")
            url = "https://sumersports.com/teams/offensive/"
            response = self.session.get(url, timeout=15)
            response.raise_for_status()

            soup = BeautifulSoup(response.content, "html.parser")
            table = soup.find("table", class_="w-full")
            if not table:
                print("❌ No table found on offensive page")
                return None

            rows = table.find_all("tr")[1:]  # Skip header row
            data = []
            for row in rows:
                cells = row.find_all("td")
                if len(cells) < 4:
                    continue

                team_text = cells[0].get_text(strip=True)
                team_match = re.search(r"\d+\.(.+)", team_text)
                if not team_match:
                    continue

                full_team_name = team_match.group(1).strip()
                standard_abbr = self.team_mappings.get(full_team_name)
                if not standard_abbr:
                    print(f"⚠️  Unknown team: {full_team_name}")
                    continue

                row_data = {"team": standard_abbr, "team_name": full_team_name}

                # Column indices based on observed SumerSports layout:
                # 2: EPA/Play, 3: Total EPA, 4: Success %, 5: EPA/Pass, 6: EPA/Rush
                if len(cells) > 2:
                    row_data["epa_off_per_play"] = self.parse_number(cells[2].get_text(strip=True))
                if len(cells) > 3:
                    row_data["total_epa_off"] = self.parse_number(cells[3].get_text(strip=True))
                if len(cells) > 4:
                    row_data["success_rate_off"] = self.parse_number(cells[4].get_text(strip=True)) / 100
                if len(cells) > 5:
                    row_data["epa_pass_off"] = self.parse_number(cells[5].get_text(strip=True))
                if len(cells) > 6:
                    row_data["epa_rush_off"] = self.parse_number(cells[6].get_text(strip=True))

                data.append(row_data)

            if not data:
                print("❌ No offensive EPA data extracted")
                return None

            df = pd.DataFrame(data)
            print(f"✅ Scraped offensive EPA for {len(df)} teams")
            return df

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

            soup = BeautifulSoup(response.content, "html.parser")
            table = soup.find("table", class_="w-full")
            if not table:
                print("❌ No table found on defensive page")
                return None

            rows = table.find_all("tr")[1:]  # Skip header row
            data = []
            for row in rows:
                cells = row.find_all("td")
                if len(cells) < 4:
                    continue

                team_text = cells[0].get_text(strip=True)
                team_match = re.search(r"\d+\.(.+)", team_text)
                if not team_match:
                    continue

                full_team_name = team_match.group(1).strip()
                standard_abbr = self.team_mappings.get(full_team_name)
                if not standard_abbr:
                    print(f"⚠️  Unknown team: {full_team_name}")
                    continue

                row_data = {"team": standard_abbr, "team_name": full_team_name}

                # Column indices based on observed SumerSports layout:
                # 2: EPA/Play, 3: Total EPA, 4: Success %, 5: EPA/Pass, 6: EPA/Rush
                if len(cells) > 2:
                    row_data["epa_def_allowed_per_play"] = self.parse_number(cells[2].get_text(strip=True))
                if len(cells) > 3:
                    row_data["total_epa_def_allowed"] = self.parse_number(cells[3].get_text(strip=True))
                if len(cells) > 4:
                    row_data["success_rate_def"] = self.parse_number(cells[4].get_text(strip=True)) / 100
                if len(cells) > 5:
                    row_data["epa_pass_def_allowed"] = self.parse_number(cells[5].get_text(strip=True))
                if len(cells) > 6:
                    row_data["epa_rush_def_allowed"] = self.parse_number(cells[6].get_text(strip=True))

                data.append(row_data)

            if not data:
                print("❌ No defensive EPA data extracted")
                return None

            df = pd.DataFrame(data)
            print(f"✅ Scraped defensive EPA for {len(df)} teams")
            return df

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

        combined_df = pd.merge(off_df, def_df, on="team", how="outer", suffixes=("", "_def"))

        # Prefer offensive team_name, fallback to defensive
        if "team_name_def" in combined_df.columns:
            combined_df["team_name"] = combined_df["team_name"].fillna(combined_df["team_name_def"])
            combined_df = combined_df.drop("team_name_def", axis=1)

        if "epa_off_per_play" in combined_df.columns and "epa_def_allowed_per_play" in combined_df.columns:
            combined_df["net_epa_per_play"] = combined_df["epa_off_per_play"] - combined_df["epa_def_allowed_per_play"]

        if "net_epa_per_play" in combined_df.columns:
            combined_df = combined_df.sort_values("net_epa_per_play", ascending=False)

        combined_df["last_updated"] = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
        combined_df["week"] = 17
        combined_df["season"] = 2025

        column_order = [
            "team",
            "team_name",
            "week",
            "season",
            "last_updated",
            "epa_def_allowed_per_play",
            "epa_off_per_play",
            "epa_pass_def_allowed",
            "epa_pass_off",
            "epa_rush_def_allowed",
            "epa_rush_off",
            "net_epa_per_play",
            "success_rate_def",
            "success_rate_off",
            "total_epa_def_allowed",
            "total_epa_off",
        ]

        final_columns = [col for col in column_order if col in combined_df.columns]
        remaining_cols = [col for col in combined_df.columns if col not in final_columns]
        combined_df = combined_df[final_columns + remaining_cols]

        print(f"✅ Combined data for {len(combined_df)} teams")
        return combined_df

    def save_to_csv(self, df: pd.DataFrame, filename: str = "data/Week17_EPA.csv"):
        """Save EPA data to CSV"""
        if df.empty:
            print("❌ No data to save")
            return

        df.to_csv(filename, index=False)
        print(f"✅ Saved Week 17 EPA data to {filename}")
        print(f"   Total teams: {len(df)}")
        print(f"   Columns: {', '.join(df.columns.tolist())}")


def main():
    print("=" * 80)
    print("WEEK 17 EPA DATA SCRAPER")
    print("=" * 80)
    print()

    scraper = Week17EPAScraper()

    off_data = scraper.scrape_offensive_epa()
    time.sleep(2)  # Be respectful to the server
    def_data = scraper.scrape_defensive_epa()

    if off_data is None or def_data is None:
        print("❌ Failed to scrape EPA data from SumerSports")
        return

    combined_data = scraper.combine_data(off_data, def_data)
    if combined_data.empty:
        print("❌ Failed to combine EPA data")
        return

    scraper.save_to_csv(combined_data, "data/Week17_EPA.csv")
    print("\n✅ Successfully created Week17_EPA.csv!")
    print(f"📊 Data includes {len(combined_data)} teams with offensive and defensive EPA metrics")


if __name__ == "__main__":
    main()


