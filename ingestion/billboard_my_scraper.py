"""
Kworb Spotify Malaysia Weekly Totals Chart Scraper & Signal Enricher.
Scrapes live Spotify weekly totals chart data from Kworb (https://kworb.net/spotify/country/my_weekly_totals.html)
and matches chart hits against the global Spotify dataset.
Owner: Member A (Stage 1)
"""

import sys
import re
import os
import urllib.request
import pandas as pd
from typing import List, Dict, Any
from pathlib import Path
from bs4 import BeautifulSoup

# Ensure project root is in sys.path
sys.path.append(str(Path(__file__).resolve().parent.parent))

from config import RAW_DATA_DIR

KWORB_MALAYSIA_WEEKLY_URL = "https://kworb.net/spotify/country/my_weekly_totals.html"

HTTP_HEADERS = {
    "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/120.0.0.0 Safari/537.36"
}


def clean_text(text: str) -> str:
    """Standardizes string for fuzzy token matching."""
    if not text or pd.isna(text):
        return ""
    text = str(text).lower()
    text = re.sub(r"\[.*?\]|\"|'", "", text)
    return re.sub(r"[^\w\s]", "", text).strip()


class KworbMalaysiaChartScraper:
    """Scrapes Spotify Malaysia Weekly Totals chart dynamically from Kworb."""

    def __init__(self, url: str = KWORB_MALAYSIA_WEEKLY_URL):
        self.url = url

    def scrape_all_charts(self, cache_path: Path = None) -> pd.DataFrame:
        """Scrapes Kworb Spotify Malaysia Weekly Totals chart and returns a standardized DataFrame."""
        if cache_path is None:
            cache_path = RAW_DATA_DIR / "scraped_kworb_malaysia_charts.csv"

        legacy_cache = RAW_DATA_DIR / "scraped_wikipedia_malaysia_charts.csv"

        scraped_records: List[Dict[str, Any]] = []

        print(f"[KworbScraper] Starting live web scraping from Kworb Spotify Malaysia page: {self.url}...")
        try:
            req = urllib.request.Request(self.url, headers=HTTP_HEADERS)
            with urllib.request.urlopen(req) as resp:
                html_content = resp.read().decode("utf-8")

            soup = BeautifulSoup(html_content, "html.parser")
            table = soup.find("table", class_="addpos")
            if not table:
                table = soup.find("table")

            if not table:
                print("[KworbScraper] Error: Could not locate chart table on Kworb page.")
                return pd.DataFrame()

            rows = table.find_all("tr")
            print(f"[KworbScraper] Found chart table with {len(rows)} rows.")

            for tr in rows:
                cols = tr.find_all("td")
                if not cols or len(cols) < 6:
                    continue

                # Column 0: Artist and Title separated by "-"
                artist_title_div = cols[0].find("div")
                artist_name = ""
                song_title = ""

                if artist_title_div:
                    links = artist_title_div.find_all("a")
                    if len(links) >= 2:
                        artist_name = links[0].get_text().strip()
                        song_title = links[1].get_text().strip()
                    else:
                        div_text = artist_title_div.get_text().strip()
                        if " - " in div_text:
                            artist_name, song_title = div_text.split(" - ", 1)
                else:
                    col_text = cols[0].get_text().strip()
                    if " - " in col_text:
                        artist_name, song_title = col_text.split(" - ", 1)

                artist_name = artist_name.strip()
                song_title = song_title.strip()

                if not artist_name or not song_title:
                    continue

                # Parse numerical metrics
                try:
                    wks = int(re.sub(r"[^\d]", "", cols[1].get_text()) or 0)
                    t10 = int(re.sub(r"[^\d]", "", cols[2].get_text()) or 0)
                    pk = int(re.sub(r"[^\d]", "", cols[3].get_text()) or 0)

                    if len(cols) >= 7:
                        pk_streams = int(re.sub(r"[^\d]", "", cols[5].get_text()) or 0)
                        total_streams = int(re.sub(r"[^\d]", "", cols[6].get_text()) or 0)
                    else:
                        pk_streams = int(re.sub(r"[^\d]", "", cols[4].get_text()) or 0)
                        total_streams = int(re.sub(r"[^\d]", "", cols[5].get_text()) or 0)

                    scraped_records.append({
                        "artist_name": artist_name,
                        "song_title": song_title,
                        "wks": wks,
                        "t10": t10,
                        "pk": pk,
                        "pk_streams": pk_streams,
                        "total_streams": total_streams,
                        "chart_category": "Spotify MY Weekly Chart",
                        "source_url": self.url
                    })
                except Exception as parse_err:
                    continue

        except Exception as e:
            print(f"[KworbScraper] Error scraping Kworb chart page: {e}")

        df_scraped = pd.DataFrame(scraped_records)
        if not df_scraped.empty:
            df_scraped.drop_duplicates(subset=["song_title", "artist_name"], inplace=True)
            df_scraped.reset_index(drop=True, inplace=True)
            df_scraped.to_csv(cache_path, index=False)
            df_scraped.to_csv(legacy_cache, index=False)
            print(f"[KworbScraper] Successfully scraped {len(df_scraped)} clean Malaysian Spotify weekly chart tracks!")
            print(f"[KworbScraper] Scraped data saved to: {cache_path}")

        return df_scraped


# Alias for backward compatibility
WikipediaMalaysiaChartScraper = KworbMalaysiaChartScraper


class MalaysiaChartSignalEnricher:
    """Enriches global Spotify tracks using dynamically scraped Kworb Spotify Malaysia weekly totals data."""

    def __init__(self, scraper: KworbMalaysiaChartScraper = None):
        self.scraper = scraper or KworbMalaysiaChartScraper()

    def enrich_dataframe(self, df: pd.DataFrame) -> pd.DataFrame:
        """Enriches DataFrame with Kworb Spotify Malaysia weekly totals chart signals."""
        cache_path = RAW_DATA_DIR / "scraped_kworb_malaysia_charts.csv"
        
        if cache_path.exists():
            print(f"[MalaysiaChartSignalEnricher] Loading cached scraped Kworb chart data from {cache_path}...")
            df_charts = pd.read_csv(cache_path)
            if df_charts.empty or "song_title" not in df_charts.columns or len(df_charts) == 0:
                print("[MalaysiaChartSignalEnricher] Cached chart file is empty or invalid. Triggering fresh Kworb scrape...")
                df_charts = self.scraper.scrape_all_charts(cache_path)
        else:
            df_charts = self.scraper.scrape_all_charts(cache_path)

        if df_charts.empty:
            print("[MalaysiaChartSignalEnricher] Warning: No scraped Kworb chart data available.")
            df["is_malaysia_trend"] = False
            df["chart_source"] = "Global Catalog"
            df["local_relevance_score"] = 0.10
            return df

        df = df.copy()
        df["artist_clean"] = df["artist_name"].apply(clean_text)
        df["track_clean"] = df["track_name"].apply(clean_text)

        df_charts["artist_clean"] = df_charts["artist_name"].apply(clean_text)
        df_charts["track_clean"] = df_charts["song_title"].apply(clean_text)

        chart_dict = {}
        for _, row in df_charts.iterrows():
            key = (row["track_clean"], row["artist_clean"])
            chart_dict[key] = {
                "wks": row.get("wks", 0),
                "t10": row.get("t10", 0),
                "pk": row.get("pk", 999),
                "pk_streams": row.get("pk_streams", 0),
                "total_streams": row.get("total_streams", 0),
                "chart_category": row.get("chart_category", "Spotify MY Weekly Chart")
            }

        scraped_chart_list = list(zip(df_charts["track_clean"], df_charts["artist_clean"], df_charts["chart_category"]))

        chart_sources = ["Global Catalog"] * len(df)
        relevance_scores = [0.10] * len(df)
        is_trend = [False] * len(df)

        print(f"[MalaysiaChartSignalEnricher] Matching {len(df):,} tracks against {len(scraped_chart_list)} scraped Kworb Spotify MY chart songs...")

        for idx, row in df.iterrows():
            a_clean = row["artist_clean"]
            t_clean = row["track_clean"]
            p_name = str(row.get("playlist_name", "")).lower()

            matched = False
            
            for c_title, c_artist, c_cat in scraped_chart_list:
                artist_match = (c_artist == a_clean) or (c_artist in a_clean) or (a_clean in c_artist)
                title_match = (c_title == t_clean) or (c_title in t_clean and len(c_title) > 3) or (t_clean in c_title and len(t_clean) > 3)

                if artist_match and title_match:
                    meta = chart_dict.get((c_title, c_artist), {})
                    pk = meta.get("pk", 100)
                    t10 = meta.get("t10", 0)

                    chart_sources[idx] = c_cat
                    if pk <= 10 or t10 > 10:
                        relevance_scores[idx] = 1.00
                    elif pk <= 50:
                        relevance_scores[idx] = 0.90
                    else:
                        relevance_scores[idx] = 0.80

                    is_trend[idx] = True
                    matched = True
                    break

            if not matched:
                if "malay" in p_name or "nusantara" in p_name:
                    relevance_scores[idx] = 0.65
                elif "k-pop" in p_name or "mandopop" in p_name:
                    relevance_scores[idx] = 0.40

        df["is_malaysia_trend"] = is_trend
        df["chart_source"] = chart_sources
        df["local_relevance_score"] = relevance_scores

        df.drop(columns=["artist_clean", "track_clean"], inplace=True)

        trend_count = sum(is_trend)
        print(f"[MalaysiaChartSignalEnricher] Dynamic enrichment complete!")
        print(f"[MalaysiaChartSignalEnricher] Identified {trend_count:,} tracks matching Kworb Spotify Malaysia Weekly Totals.")
        print(f"Chart Sources Breakdown:\n{df['chart_source'].value_counts()}")

        return df


if __name__ == "__main__":
    print("--- TESTING KWORB SPOTIFY MALAYSIA WEEKLY TOTALS SCRAPER ---")
    scraper = KworbMalaysiaChartScraper()
    df_scraped = scraper.scrape_all_charts()
    print("\nScraped Results Summary:")
    print(f"Total Scraped Chart Tracks: {len(df_scraped)}")
    if not df_scraped.empty:
        print("\nColumns:", list(df_scraped.columns))
        print("\nSample Scraped Tracks:")
        print(df_scraped.head(25))
