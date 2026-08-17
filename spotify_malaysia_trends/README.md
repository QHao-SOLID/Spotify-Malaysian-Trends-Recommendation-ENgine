# 🎵 Spotify Malaysian Music Trends & Recommendation Engine

Data analysis, pattern discovery, and song recommendations from Malaysian Spotify listening data.

---

## 👥 Team Roles & Module Ownership

| Role | Stage Ownership | Primary Files & Responsibilities |
| :--- | :--- | :--- |
| **Facilitator** (Tech Lead & Guide) | Architecture, Scaffolding, Mock Generator, Pipeline | `config.py`, `core/`, `utils/`, `pipeline.py` |
| **Member A** (Data & ML Pipeline) | Stage 1 (Collection), Stage 5 (Clustering), Stage 6 (Recommender) | `ingestion/collector.py`, `ml/clustering.py`, `ml/recommender.py` |
| **Member B** (Data Prep & Dashboard) | Stage 2 (Cleaning), Stage 3 (EDA), Stage 4 (Features), Stage 7 (Dashboard) | `processing/cleaner.py`, `processing/feature_engineering.py`, `analytics/eda.py`, `dashboard/` |

---

## 🚀 Quickstart & Setup

### 1. Environment Setup
```bash
python -m venv .venv
# On Windows PowerShell:
.venv\Scripts\Activate.ps1

# Install requirements
pip install -r requirements.txt
```

### 2. Generate Mock Data & Run Pipeline
```bash
python utils/mock_data_generator.py
python pipeline.py
```

### 4. Launch Interactive Streamlit Dashboard
```bash
streamlit run dashboard/app.py
```

---

## ⚡ Parallel Development Guide

* **Mock Data Generator**: Run `python utils/mock_data_generator.py` to populate `data/raw/raw_tracks.parquet` with realistic synthetic tracks.
* **Member A**: Focus on `ingestion/` for API fetching and `ml/` for KMeans and NearestNeighbors models.
* **Member B**: Focus on `processing/` for data cleaning & scaling, `analytics/` for EDA charts, and `dashboard/` for Streamlit UI layout.
* **Facilitator**: Maintains contract interfaces in `core/` and orchestrates integration.
