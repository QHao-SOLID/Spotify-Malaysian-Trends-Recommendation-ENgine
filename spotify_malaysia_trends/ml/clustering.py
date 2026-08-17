"""
KMeans Clustering for Pattern Discovery in Listening Tastes.
Owner: Member A (Stage 5)
"""

import pandas as pd
from typing import Dict, Any, List
from sklearn.cluster import KMeans
from core.interfaces import BaseMLModel
from config import RANDOM_SEED


class KMeansClusterer(BaseMLModel):
    """Clusters tracks using KMeans to reveal natural genre/mood groupings."""

    def __init__(self, n_clusters: int = 5):
        self.n_clusters = n_clusters
        self.model = KMeans(n_clusters=n_clusters, random_state=RANDOM_SEED, n_init=10)
        self.is_fitted = False

    def fit(self, feature_matrix: pd.DataFrame) -> "KMeansClusterer":
        """Fits KMeans model on scaled audio feature matrix."""
        print(f"[Member A - ML] Fitting KMeans with {self.n_clusters} clusters on matrix shape: {feature_matrix.shape}...")
        
        # TODO [Member A]: Fit self.model on feature_matrix values
        # Store self.is_fitted = True
        
        self.is_fitted = True
        return self

    def predict(self, feature_matrix: pd.DataFrame) -> List[int]:
        """Predicts cluster assignment labels for tracks."""
        if not self.is_fitted:
            raise ValueError("[KMeansClusterer] Model must be fitted before predicting labels.")
        
        # TODO [Member A]: Return self.model.predict(feature_matrix)
        return [0] * len(feature_matrix)

    def calculate_elbow_inertia(self, feature_matrix: pd.DataFrame, max_k: int = 10) -> Dict[int, float]:
        """Calculates inertia values across k=1..max_k to aid elbow method evaluation."""
        inertia_scores: Dict[int, float] = {}
        
        # TODO [Member A]: Loop k from 1 to max_k, fit KMeans, collect model.inertia_
        
        return inertia_scores
