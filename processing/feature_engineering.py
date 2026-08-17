"""
Feature Engineering and Scaling Module for Audio Features.
Owner: Member B (Stage 4)
"""

import pandas as pd
from typing import List, Tuple
from sklearn.preprocessing import StandardScaler
from core.interfaces import BaseFeatureEngineer
from config import AUDIO_FEATURE_COLUMNS


class FeatureEngineer(BaseFeatureEngineer):
    """Normalizes numeric audio features into scaled feature matrices for downstream ML models."""

    def __init__(self, feature_cols: List[str] = AUDIO_FEATURE_COLUMNS):
        self.feature_cols = feature_cols
        self.scaler = StandardScaler()
        self.is_fitted = False

    def fit_transform(self, df: pd.DataFrame) -> pd.DataFrame:
        """Fits StandardScaler on input audio features and returns scaled feature matrix."""
        print(f"[Member B - FeatureEng] Fitting StandardScaler on columns: {self.feature_cols}...")
        
        # TODO [Member B]:
        # 1. Extract df[self.feature_cols]
        # 2. Fit and transform using self.scaler
        # 3. Return scaled values as pandas DataFrame indexed by df["track_id"]
        
        scaled_df = pd.DataFrame(df[self.feature_cols].copy())
        self.is_fitted = True
        return scaled_df

    def transform(self, df: pd.DataFrame) -> pd.DataFrame:
        """Transforms input audio features using already fitted StandardScaler."""
        if not self.is_fitted:
            raise ValueError("[FeatureEngineer] Scaler must be fitted before transform.")
            
        # TODO [Member B]: Transform df[self.feature_cols] using self.scaler
        
        return pd.DataFrame(df[self.feature_cols].copy())
