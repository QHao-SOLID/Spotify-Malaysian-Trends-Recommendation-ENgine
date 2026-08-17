"""
Streamlit Reusable UI Components.
Owner: Member B (Stage 7)
"""

import streamlit as st
import pandas as pd


def render_header():
    """Renders dashboard title banner and introduction."""
    st.title("🎵 Spotify Malaysian Music Trends & Recommender")
    st.markdown(
        "Explore audio features, listening clusters, and song recommendations from Malaysian charts."
    )
    st.divider()


def render_track_card(track_row: pd.Series):
    """Renders formatted UI card for a single track."""
    with st.container():
        st.subheader(f"🎧 {track_row['track_name']}")
        st.caption(f"Artist: **{track_row['artist_name']}** | Album: {track_row['album_name']}")
        
        col1, col2, col3 = st.columns(3)
        col1.metric("Popularity", f"{track_row['popularity']}/100")
        col2.metric("Danceability", f"{track_row['danceability']}")
        col3.metric("Energy", f"{track_row['energy']}")
        st.divider()
