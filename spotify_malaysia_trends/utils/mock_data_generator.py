"""
Mock Data Generator to enable parallel development from Day 1.
Owner: Facilitator
"""

import numpy as np
import pandas as pd
from typing import Optional
from config import AUDIO_FEATURE_COLUMNS, RANDOM_SEED, RAW_DATA_DIR
from utils.helpers import save_dataframe


def generate_mock_tracks(num_tracks: int = 100, seed: int = RANDOM_SEED) -> pd.DataFrame:
    """Generates synthetic track metadata and audio features matching Spotify schemas."""
    np.random.seed(seed)
    
    genres = ["Malaysian Pop", "Malay Hip-Hop", "Indie Nusantara", "K-Pop", "Global Pop"]
    artists = ["Yuna", "Siti Nurhaliza", "Insomniacks", "Hael Husaini", "Joe Flizzow", "K-Clique"]
    
    data = []
    for i in range(num_tracks):
        track_id = f"mock_track_{i+1:03d}"
        artist = np.random.choice(artists)
        genre = np.random.choice(genres)
        
        row = {
            "track_id": track_id,
            "track_name": f"{genre} Track {i+1}",
            "artist_name": artist,
            "album_name": f"{artist}'s Album Vol. {(i%3)+1}",
            "playlist_id": "37i9dQZEVXbJJBTrSlkfiB",
            "playlist_name": "Malaysia Top 50 (Mock)",
            "popularity": int(np.random.randint(40, 100)),
            "release_date": f"2023-{(i%12)+1:02d}-15",
            "duration_ms": int(np.random.randint(180000, 240000)),
            "explicit": bool(np.random.choice([True, False], p=[0.1, 0.9])),
            # Audio features
            "danceability": round(float(np.random.uniform(0.3, 0.9)), 3),
            "energy": round(float(np.random.uniform(0.3, 0.95)), 3),
            "key": int(np.random.randint(0, 12)),
            "loudness": round(float(np.random.uniform(-15.0, -3.0)), 2),
            "mode": int(np.random.choice([0, 1])),
            "speechiness": round(float(np.random.uniform(0.02, 0.3)), 3),
            "acousticness": round(float(np.random.uniform(0.01, 0.85)), 3),
            "instrumentalness": round(float(np.random.uniform(0.0, 0.5)), 3),
            "liveness": round(float(np.random.uniform(0.05, 0.4)), 3),
            "valence": round(float(np.random.uniform(0.2, 0.9)), 3),
            "tempo": round(float(np.random.uniform(75.0, 165.0)), 2),
        }
        data.append(row)
        
    df = pd.DataFrame(data)
    return df


if __name__ == "__main__":
    mock_df = generate_mock_tracks(100)
    target_path = RAW_DATA_DIR / "raw_tracks.parquet"
    save_dataframe(mock_df, target_path)
    print(f"[Mock Generator] Successfully created mock dataset at {target_path}")
