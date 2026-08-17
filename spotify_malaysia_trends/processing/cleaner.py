"""
Data Cleaner and Preprocessor for Spotify Track Data.
Owner: Member B (Stage 2)
"""

import pandas as pd
from core.interfaces import BaseCleaner


class DataCleaner(BaseCleaner):
    """Cleans raw track data, removes duplicates, handles missing values."""

    def clean(self, raw_df: pd.DataFrame) -> pd.DataFrame:
        """Applies data cleaning steps on raw tracks dataframe."""
        print(f"[Member B - Cleaner] Cleaning input dataframe with shape: {raw_df.shape}...")
        
        if raw_df.empty:
            print("[Member B - Cleaner] WARNING: Input raw dataframe is empty.")
            return raw_df
            
        df = raw_df.copy()
        
        # TODO [Member B]:
        # 1. Deduplicate by track_id: df.drop_duplicates(subset=["track_id"], inplace=True)
        # 2. Handle missing audio features (impute mean or drop rows with null audio features)
        # 3. Ensure correct numeric datatypes for audio feature columns
        # 4. Standardize text fields (strip spaces from artist_name, track_name)
        
        cleaned_df = df
        print(f"[Member B - Cleaner] Cleaned dataframe ready. Final shape: {cleaned_df.shape}")
        return cleaned_df
