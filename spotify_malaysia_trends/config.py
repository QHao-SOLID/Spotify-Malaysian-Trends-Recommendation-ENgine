"""
Global Configuration & Path Constants for Spotify Malaysian Music Trends Project.
Owner: Facilitator
"""

import os
from pathlib import Path
from dotenv import load_dotenv

# Load environment variables from .env file if present
load_dotenv()

# Base Project Paths
BASE_DIR = Path(__file__).resolve().parent
DATA_DIR = BASE_DIR / os.getenv("DATA_DIR", "data")

RAW_DATA_DIR = DATA_DIR / "raw"
PROCESSED_DATA_DIR = DATA_DIR / "processed"
FEATURES_DATA_DIR = DATA_DIR / "features"
MODELS_DIR = DATA_DIR / "models"

# Ensure all data directories exist
for path in [RAW_DATA_DIR, PROCESSED_DATA_DIR, FEATURES_DATA_DIR, MODELS_DIR]:
    path.mkdir(parents=True, exist_ok=True)

# Feature List for Downstream ML
AUDIO_FEATURE_COLUMNS = [
    "danceability",
    "energy",
    "key",
    "loudness",
    "mode",
    "speechiness",
    "acousticness",
    "instrumentalness",
    "liveness",
    "valence",
    "tempo",
]

# Random Seed for Reproducibility
RANDOM_SEED = 42
