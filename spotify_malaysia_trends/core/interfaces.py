"""
Abstract Base Interfaces defining module execution contracts.
Owner: Facilitator
"""

from abc import ABC, abstractmethod
import pandas as pd
from typing import Any, Dict


class BaseCollector(ABC):
    """Abstract Base Class for Data Collection (Stage 1 - Member A)."""

    @abstractmethod
    def fetch_playlist_tracks(self, playlist_id: str) -> pd.DataFrame:
        """Fetches track metadata for a given Spotify playlist ID."""
        pass

    @abstractmethod
    def fetch_audio_features(self, track_ids: list[str]) -> pd.DataFrame:
        """Fetches numeric audio features for a list of track IDs."""
        pass


class BaseCleaner(ABC):
    """Abstract Base Class for Data Cleaning & Preprocessing (Stage 2 - Member B)."""

    @abstractmethod
    def clean(self, raw_df: pd.DataFrame) -> pd.DataFrame:
        """Cleans raw track data, deduplicates, and handles nulls."""
        pass


class BaseFeatureEngineer(ABC):
    """Abstract Base Class for Feature Engineering (Stage 4 - Member B)."""

    @abstractmethod
    def fit_transform(self, df: pd.DataFrame) -> pd.DataFrame:
        """Fits scale transforms on audio features and returns scaled feature matrix."""
        pass

    @abstractmethod
    def transform(self, df: pd.DataFrame) -> pd.DataFrame:
        """Transforms input track audio features using fitted scaler."""
        pass


class BaseMLModel(ABC):
    """Abstract Base Class for Machine Learning Models (Stages 5 & 6 - Member A)."""

    @abstractmethod
    def fit(self, feature_matrix: pd.DataFrame) -> Any:
        """Fits model on feature matrix."""
        pass

    @abstractmethod
    def predict(self, input_data: Any) -> Any:
        """Generates predictions or query results from fitted model."""
        pass
