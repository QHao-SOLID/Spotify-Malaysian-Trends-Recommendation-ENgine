"""
Data Schemas and Pydantic Contracts for Pipeline Data Validation.
Owner: Facilitator
"""

from typing import List, Optional
from pydantic import BaseModel, Field


class AudioFeaturesSchema(BaseModel):
    """Schema representing audio features for a Spotify track."""
    track_id: str
    danceability: float = Field(ge=0.0, le=1.0)
    energy: float = Field(ge=0.0, le=1.0)
    key: int
    loudness: float
    mode: int
    speechiness: float = Field(ge=0.0, le=1.0)
    acousticness: float = Field(ge=0.0, le=1.0)
    instrumentalness: float = Field(ge=0.0, le=1.0)
    liveness: float = Field(ge=0.0, le=1.0)
    valence: float = Field(ge=0.0, le=1.0)
    tempo: float = Field(ge=0.0)


class TrackSchema(BaseModel):
    """Schema representing full track metadata combined with audio features."""
    track_id: str
    track_name: str
    artist_name: str
    album_name: str
    playlist_id: str
    playlist_name: str
    popularity: int = Field(ge=0, le=100)
    release_date: Optional[str] = None
    duration_ms: int
    explicit: bool = False
    
    # Audio feature fields
    danceability: Optional[float] = None
    energy: Optional[float] = None
    key: Optional[int] = None
    loudness: Optional[float] = None
    mode: Optional[int] = None
    speechiness: Optional[float] = None
    acousticness: Optional[float] = None
    instrumentalness: Optional[float] = None
    liveness: Optional[float] = None
    valence: Optional[float] = None
    tempo: Optional[float] = None


class RecommendationRequest(BaseModel):
    """Input contract for the recommendation engine."""
    seed_track_id: str
    n_recommendations: int = 5


class RecommendationResult(BaseModel):
    """Output contract for recommended tracks."""
    seed_track_id: str
    recommended_track_ids: List[str]
    similarity_scores: List[float]
