import sys
import os
import pandas as pd
from pathlib import Path

# Add project root to sys.path
sys.path.append(str(Path(__file__).resolve().parent.parent))

from config import RAW_DATA_DIR
from ingestion.collector import SpotifyDataCollector
from ingestion.billboard_my_scraper import WikipediaMalaysiaChartScraper
from utils.helpers import save_dataframe, load_dataframe


def main():
    print("--- DYNAMIC WIKIPEDIA WEB SCRAPING & DATASET ENRICHMENT ---")
    
    pd.set_option("display.max_columns", None)
    pd.set_option("display.width", 1000)

    # Force fresh scraping by removing old cache if present
    cache_path = RAW_DATA_DIR / "scraped_wikipedia_malaysia_charts.csv"
    if cache_path.exists():
        os.remove(cache_path)
        print(f"Removed previous cache {cache_path} to trigger fresh Wikipedia web scraping.")

    # 1. Trigger dynamic Wikipedia scraping
    scraper = WikipediaMalaysiaChartScraper()
    df_scraped = scraper.scrape_all_charts(cache_path)
    print(f"\nLive Web Scraped Wikipedia Chart Entries: {len(df_scraped)}")
    print(df_scraped.head(10))

    # 2. Trigger collector to load 114k Kaggle dataset and match against scraped Wikipedia entries
    collector = SpotifyDataCollector()
    df = collector.collect_dataset()

    print(f"\nTotal Dataset Shape: {df.shape} (Rows: {df.shape[0]:,}, Columns: {df.shape[1]})")

    target_path = RAW_DATA_DIR / "raw_tracks.parquet"
    save_dataframe(df, target_path)
    print(f"\nSaved raw tracks parquet to: {target_path}")

    print("\n--- MALAYSIAN CHART TREND BREAKDOWN ---")
    print(df["chart_source"].value_counts())

    trend_df = df[df["is_malaysia_trend"] == True]
    print(f"\n--- MATCHED MALAYSIAN TRENDING TRACKS ({len(trend_df)} matched) ---")
    cols_to_show = ["track_name", "artist_name", "chart_source", "local_relevance_score", "popularity", "danceability", "energy", "valence"]
    print(trend_df[cols_to_show].head(15))


if __name__ == "__main__":
    main()
