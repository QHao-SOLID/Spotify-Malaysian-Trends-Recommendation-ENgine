import sys
import pandas as pd
from pathlib import Path

# Add project root to sys.path
sys.path.append(str(Path(__file__).resolve().parent.parent))

from config import RAW_DATA_DIR
from utils.helpers import load_dataframe
from ingestion.billboard_my_scraper import MalaysiaChartSignalEnricher


def main():
    raw_path = RAW_DATA_DIR / "raw_tracks.parquet"
    if not raw_path.exists():
        raw_path = RAW_DATA_DIR / "spotify_tracks_114k.csv"
        if not raw_path.exists():
            print("Raw tracks file not found.")
            return

    df = load_dataframe(raw_path)
    print(f"Loaded dataset shape: {df.shape}")

    print("\n--- DYNAMICALLY MATCHING MALAYSIAN TREND SIGNALS (WIKIPEDIA BILLBOARD & RIM) ---")
    enricher = MalaysiaChartSignalEnricher()
    enriched_df = enricher.enrich_dataframe(df)

    matched_df = enriched_df[enriched_df["is_malaysia_trend"] == True]

    print(f"\nTotal tracks dynamically matched with Malaysian chart signals: {len(matched_df)}")
    print("\nSample Matched Tracks:")
    display_cols = [col for col in ["track_id", "track_name", "artist_name", "chart_source", "local_relevance_score", "popularity"] if col in matched_df.columns]
    print(matched_df[display_cols].head(10))


if __name__ == "__main__":
    main()

