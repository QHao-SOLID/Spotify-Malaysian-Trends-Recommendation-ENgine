"""
Main Streamlit Interactive Dashboard Application.
Owner: Member B (Stage 7)
"""

import streamlit as st
import pandas as pd
from pathlib import Path
import sys

# Add project root directory to Python path
sys.path.append(str(Path(__file__).resolve().parent.parent))

from config import PROCESSED_DATA_DIR, RAW_DATA_DIR
from utils.helpers import load_dataframe
from utils.mock_data_generator import generate_mock_tracks
from analytics.eda import EDAVisualizer
from dashboard.components import render_header, render_track_card

st.set_page_config(
    page_title="Spotify Malaysia Trends",
    page_icon="🎵",
    layout="wide",
)


@st.cache_data
def get_data() -> pd.DataFrame:
    """Loads processed track dataset or generates mock fallback."""
    processed_path = PROCESSED_DATA_DIR / "cleaned_tracks.parquet"
    raw_path = RAW_DATA_DIR / "raw_tracks.parquet"
    
    if processed_path.exists():
        return load_dataframe(processed_path)
    elif raw_path.exists():
        return load_dataframe(raw_path)
    else:
        return generate_mock_tracks(num_tracks=50)


def main():
    render_header()
    df = get_data()
    
    tab1, tab2, tab3 = st.tabs(["📊 Exploratory Trends", "🔍 Listening Clusters", "💡 Recommender"])
    
    with tab1:
        st.header("Malaysian Audio Trends & EDA")
        visualizer = EDAVisualizer(df)
        
        col1, col2 = st.columns(2)
        with col1:
            st.plotly_chart(visualizer.plot_popularity_distribution(), use_container_width=True)
        with col2:
            st.plotly_chart(visualizer.plot_audio_features_radar(), use_container_width=True)
            
        st.plotly_chart(visualizer.plot_feature_correlations(), use_container_width=True)

    with tab2:
        st.header("KMeans Pattern Discovery")
        st.info("Member A's cluster labels will be visualized here.")
        st.dataframe(df[["track_name", "artist_name", "popularity", "danceability", "energy"]].head(10))

    with tab3:
        st.header("Song Recommendation Engine")
        st.info("Select a seed song to view nearest neighbor recommendations.")
        selected_track = st.selectbox("Choose a Track", df["track_name"].tolist())
        
        if selected_track:
            seed_row = df[df["track_name"] == selected_track].iloc[0]
            st.subheader("Selected Seed Track:")
            render_track_card(seed_row)


if __name__ == "__main__":
    main()
