"""
Exploratory Data Analysis (EDA) & Trend Visualization Engine.
Owner: Member B (Stage 3)
"""

import pandas as pd
import plotly.express as px
import plotly.graph_objects as go
from typing import Any
from config import AUDIO_FEATURE_COLUMNS


class EDAVisualizer:
    """Generates interactive Plotly figures for track popularity, audio feature radar charts, and correlations."""

    def __init__(self, df: pd.DataFrame):
        self.df = df

    def plot_popularity_distribution(self) -> go.Figure:
        """Generates histogram of track popularity."""
        # TODO [Member B]: Return px.histogram(self.df, x="popularity", title="Track Popularity Distribution in Malaysia")
        fig = px.histogram(self.df, x="popularity", title="Track Popularity Distribution in Malaysia")
        return fig

    def plot_audio_features_radar(self) -> go.Figure:
        """Generates radar / polar chart comparing mean audio feature scores."""
        # TODO [Member B]: Compute mean of AUDIO_FEATURE_COLUMNS, generate px.line_polar or go.Scatterpolar
        feature_means = self.df[AUDIO_FEATURE_COLUMNS].mean().reset_index()
        feature_means.columns = ["feature", "value"]
        fig = px.line_polar(feature_means, r="value", theta="feature", line_close=True, title="Average Audio Feature Profile")
        return fig

    def plot_feature_correlations(self) -> go.Figure:
        """Generates correlation matrix heatmap for audio features."""
        # TODO [Member B]: Compute correlation matrix and generate px.imshow()
        corr = self.df[AUDIO_FEATURE_COLUMNS].corr()
        fig = px.imshow(corr, title="Audio Feature Correlation Heatmap", text_auto=True)
        return fig
