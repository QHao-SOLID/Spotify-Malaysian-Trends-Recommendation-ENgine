import sys
import pandas as pd
from pathlib import Path

sys.path.append(str(Path(__file__).resolve().parent.parent))

from config import RAW_DATA_DIR
from utils.helpers import load_dataframe

def main():
    raw_path = RAW_DATA_DIR / "spotify_tracks_114k.csv"
    if not raw_path.exists():
        print("Dataset CSV not found.")
        return

    df = pd.read_csv(raw_path)
    df["artist_lower"] = df["artists"].astype(str).str.lower()
    df["track_lower"] = df["track_name"].astype(str).str.lower()

    search_artists = ["bruno mars", "taylor swift", "bts", "blackpink", "newjeans", "jung kook", "fifty fifty", "coldplay", "ed sheeran"]

    print("--- SEARCHING KAGGLE 114K DATASET FOR GLOBAL BILLBOARD MY ARTISTS ---")
    for artist in search_artists:
        matches = df[df["artist_lower"].str.contains(artist, na=False)]
        print(f"\nArtist: '{artist}' -> Found {len(matches)} tracks in Kaggle dataset.")
        if not matches.empty:
            print("Sample Tracks:")
            print(matches[["artists", "track_name", "popularity", "track_genre"]].head(5))

if __name__ == "__main__":
    main()
