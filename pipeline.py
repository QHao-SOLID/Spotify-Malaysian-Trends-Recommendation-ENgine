"""
End-to-End Pipeline Orchestrator & CLI Runner.
Owner: Facilitator
"""

import sys
from pathlib import Path
from config import (
    RAW_DATA_DIR, PROCESSED_DATA_DIR, FEATURES_DATA_DIR, MODELS_DIR
)
from utils.helpers import save_dataframe, load_dataframe, save_model
from utils.mock_data_generator import generate_mock_tracks
from ingestion import SpotifyDataCollector
from processing.cleaner import DataCleaner
from processing.feature_engineering import FeatureEngineer
from ml.clustering import KMeansClusterer
from ml.recommender import SongRecommender


def run_pipeline(use_mock: bool = False):
    """Executes Stages 1 through 6 sequentially."""
    print("=" * 60)
    print("      SPOTIFY MALAYSIAN MUSIC TRENDS - PIPELINE RUNNER      ")
    print("=" * 60)

    # Stage 1: Data Collection
    print("\n--- STAGE 1: DATA COLLECTION (Member A) ---")
    raw_path = RAW_DATA_DIR / "raw_tracks.parquet"
    if use_mock:
        print("[Pipeline] Running in Mock Mode. Generating synthetic Spotify data...")
        df_raw = generate_mock_tracks(100)
        save_dataframe(df_raw, raw_path)
    else:
        print("[Pipeline] Running Dataset Collection with Wikipedia Chart Signal Enrichment...")
        collector = SpotifyDataCollector()
        df_raw = collector.collect_dataset()
        save_dataframe(df_raw, raw_path)



    # Stage 2: Data Cleaning
    print("\n--- STAGE 2: CLEANING & PREPROCESSING (Member B) ---")
    cleaner = DataCleaner()
    df_clean = cleaner.clean(df_raw)
    processed_path = PROCESSED_DATA_DIR / "cleaned_tracks.parquet"
    save_dataframe(df_clean, processed_path)

    # Stage 4: Feature Engineering
    print("\n--- STAGE 4: FEATURE ENGINEERING (Member B) ---")
    feat_eng = FeatureEngineer()
    df_features = feat_eng.fit_transform(df_clean)
    features_path = FEATURES_DATA_DIR / "feature_matrix.parquet"
    save_dataframe(df_features, features_path)

    # Stage 5: Pattern Discovery (Clustering)
    print("\n--- STAGE 5: PATTERN DISCOVERY (Member A) ---")
    clusterer = KMeansClusterer(n_clusters=5)
    clusterer.fit(df_features)
    cluster_model_path = MODELS_DIR / "kmeans_model.joblib"
    save_model(clusterer, cluster_model_path)

    # Stage 6: Recommendation Engine
    print("\n--- STAGE 6: RECOMMENDATION ENGINE (Member A) ---")
    recommender = SongRecommender()
    recommender.fit(df_features, df_clean["track_id"].tolist())
    rec_model_path = MODELS_DIR / "recommender_model.joblib"
    save_model(recommender, rec_model_path)

    print("\n" + "=" * 60)
    print("[Pipeline] Pipeline execution finished successfully!")
    print("=" * 60)


if __name__ == "__main__":
    run_pipeline(use_mock=True)
