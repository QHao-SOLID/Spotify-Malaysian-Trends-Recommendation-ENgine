"""
Core contracts and schema definitions package.
Owner: Facilitator
"""

from core.schemas import TrackSchema, AudioFeaturesSchema, RecommendationRequest, RecommendationResult
from core.interfaces import BaseCollector, BaseCleaner, BaseFeatureEngineer, BaseMLModel

__all__ = [
    "TrackSchema",
    "AudioFeaturesSchema",
    "RecommendationRequest",
    "RecommendationResult",
    "BaseCollector",
    "BaseCleaner",
    "BaseFeatureEngineer",
    "BaseMLModel",
]
