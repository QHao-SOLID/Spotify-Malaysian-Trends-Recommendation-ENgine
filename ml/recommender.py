"""
NearestNeighbors Similarity Recommender Engine.
Owner: Member A (Stage 6)
"""

import pandas as pd
import numpy as np
from typing import List, Tuple
from sklearn.neighbors import NearestNeighbors
from core.interfaces import BaseMLModel
from core.schemas import RecommendationResult


class SongRecommender(BaseMLModel):
    """Recommends similar tracks using scikit-learn NearestNeighbors with Cosine distance."""

    def __init__(self, metric: str = "cosine", n_neighbors: int = 5):
        self.metric = metric
        self.n_neighbors = n_neighbors
        self.model = NearestNeighbors(n_neighbors=n_neighbors + 1, metric=metric)
        self.track_ids: List[str] = []
        self.is_fitted = False

    def fit(self, feature_matrix: pd.DataFrame, track_ids: List[str]) -> "SongRecommender":
        """Fits NearestNeighbors index on scaled feature matrix."""
        print(f"[Member A - ML] Indexing {len(track_ids)} tracks for recommendations ({self.metric} metric)...")
        
        # TODO [Member A]: Store self.track_ids = track_ids, fit self.model on feature_matrix
        
        self.track_ids = track_ids
        self.is_fitted = True
        return self

    def predict(self, seed_feature_vector: np.ndarray) -> Tuple[List[int], List[float]]:
        """Finds nearest neighbor indices and distance scores for a given seed track feature vector."""
        if not self.is_fitted:
            raise ValueError("[SongRecommender] Model must be fitted before querying recommendations.")
        
        # TODO [Member A]: Call self.model.kneighbors(seed_feature_vector)
        # Return (neighbor_indices, distance_scores)
        
        return ([0], [0.0])

    def recommend(self, seed_track_id: str, df_tracks: pd.DataFrame, n_recs: int = 5) -> RecommendationResult:
        """Finds similar songs by matching seed_track_id against indexed catalog."""
        # TODO [Member A]: Look up seed track vector, call predict(), map back to track_ids
        
        return RecommendationResult(
            seed_track_id=seed_track_id,
            recommended_track_ids=[],
            similarity_scores=[]
        )
