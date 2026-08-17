"""
Spotify Data Collector supporting Maharshi Pandya's Kaggle/HuggingFace 114k Tracks Dataset & Dynamic Wikipedia Charts.
Owner: Member A (Stage 1)
"""

import sys
import os
import urllib.request
import pandas as pd
from typing import List, Dict, Any
from pathlib import Path

# Ensure project root is in sys.path
sys.path.append(str(Path(__file__).resolve().parent.parent))

from core.interfaces import BaseCollector
from config import RAW_DATA_DIR, AUDIO_FEATURE_COLUMNS
from ingestion.billboard_my_scraper import MalaysiaChartSignalEnricher


# Primary direct download URL for Maharshi Pandya's 114k Spotify Tracks Dataset
KAGGLE_DATASET_URL = "https://huggingface.co/datasets/maharshipandya/spotify-tracks-dataset/resolve/main/dataset.csv"


class SpotifyDataCollector(BaseCollector):
    """Collects Spotify tracks and audio features from Kaggle 114k dataset enriched by Wikipedia chart signals."""

    def __init__(self):
        self.enricher = MalaysiaChartSignalEnricher()

    def fetch_kaggle_dataset(self, target_path: Path = None, sample_size: int = None) -> pd.DataFrame:
        """Downloads and loads Maharshi Pandya's 114k Spotify Tracks Dataset."""
        if target_path is None:
            target_path = RAW_DATA_DIR / "spotify_tracks_114k.csv"

        if not target_path.exists():
            print(f"[SpotifyDataCollector] Downloading Kaggle 114k Spotify Dataset from HuggingFace...")
            try:
                urllib.request.urlretrieve(KAGGLE_DATASET_URL, target_path)
                print(f"[SpotifyDataCollector] Successfully downloaded dataset to {target_path}")
            except Exception as e:
                print(f"[SpotifyDataCollector] Download error: {e}")
                raise RuntimeError(f"Failed to download dataset from {KAGGLE_DATASET_URL}: {e}")
        else:
            print(f"[SpotifyDataCollector] Loading local dataset from {target_path}...")

        df = pd.read_csv(target_path)
        print(f"[SpotifyDataCollector] Raw dataset loaded with shape: {df.shape}")

        # Standardize column names to match TrackSchema & AudioFeaturesSchema
        column_mapping = {
            "artists": "artist_name",
            "track_genre": "playlist_name",
        }
        df.rename(columns=column_mapping, inplace=True)

        if "playlist_id" not in df.columns:
            df["playlist_id"] = df["playlist_name"].apply(lambda g: f"genre_{str(g).lower().replace(' ', '_')}")

        if "release_date" not in df.columns:
            df["release_date"] = "2023-01-01"

        # Ensure explicit is boolean
        if "explicit" in df.columns:
            df["explicit"] = df["explicit"].astype(bool)

        # Drop internal indexing column if present
        if "Unnamed: 0" in df.columns:
            df.drop(columns=["Unnamed: 0"], inplace=True)

        if sample_size and len(df) > sample_size:
            df = df.sample(n=sample_size, random_state=42).reset_index(drop=True)
            print(f"[SpotifyDataCollector] Sampled {sample_size} tracks for pipeline execution.")

        return df

    def fetch_playlist_tracks(self, playlist_id: str) -> pd.DataFrame:
        """Fallback method for playlist tracks interface contract."""
        print("[Collector] Fetching Kaggle dataset (Live API disabled)...")
        return self.fetch_kaggle_dataset()

    def fetch_audio_features(self, track_ids: List[str]) -> pd.DataFrame:
        """Fallback method for audio features interface contract."""
        print("[Collector] Live audio features API call disabled.")
        return pd.DataFrame()

    def collect_dataset(self, playlist_ids: List[str] = None) -> pd.DataFrame:
        """Orchestrates dataset collection using Kaggle 114k Dataset with Malaysian chart signal enrichment."""
        print("[SpotifyDataCollector] Loading 114k Spotify Tracks Dataset...")
        try:
            df = self.fetch_kaggle_dataset()
            print(f"[SpotifyDataCollector] Raw dataset loaded! Shape: {df.shape}")
            
            # Deduplicate multiple track re-releases by keeping max popularity entry
            if "popularity" in df.columns and "track_name" in df.columns and "artist_name" in df.columns:
                print("[SpotifyDataCollector] Deduplicating tracks by (track_name, artist_name) keeping highest popularity...")
                df.sort_values(by="popularity", ascending=False, inplace=True)
                df.drop_duplicates(subset=["track_name", "artist_name"], keep="first", inplace=True)
                df.reset_index(drop=True, inplace=True)
                print(f"[SpotifyDataCollector] Deduplicated dataset shape: {df.shape}")

            # Enrich with Billboard MY & RIM Domestic Chart Signals
            enriched_df = self.enricher.enrich_dataframe(df)
            print(f"[SpotifyDataCollector] Final Enriched Dataset Shape: {enriched_df.shape}")
            return enriched_df
        except Exception as e:
            print(f"[SpotifyDataCollector] Error loading Kaggle dataset: {e}")
            return pd.DataFrame()



