"""
File I/O Helper Functions for Dataframes and Machine Learning Models.
Owner: Facilitator
"""

from pathlib import Path
import pandas as pd
import joblib


def save_dataframe(df: pd.DataFrame, file_path: Path) -> None:
    """Saves a pandas DataFrame to Parquet format."""
    file_path.parent.mkdir(parents=True, exist_ok=True)
    df.to_parquet(file_path, index=False)
    print(f"[Helper] Saved DataFrame ({len(df)} rows) -> {file_path}")


def load_dataframe(file_path: Path) -> pd.DataFrame:
    """Loads a pandas DataFrame from Parquet format."""
    if not file_path.exists():
        raise FileNotFoundError(f"[Helper] File not found: {file_path}")
    df = pd.read_parquet(file_path)
    print(f"[Helper] Loaded DataFrame ({len(df)} rows) <- {file_path}")
    return df


def save_model(model: object, file_path: Path) -> None:
    """Saves a fitted scikit-learn model artifact using Joblib."""
    file_path.parent.mkdir(parents=True, exist_ok=True)
    joblib.dump(model, file_path)
    print(f"[Helper] Saved Model -> {file_path}")


def load_model(file_path: Path) -> object:
    """Loads a scikit-learn model artifact from Joblib format."""
    if not file_path.exists():
        raise FileNotFoundError(f"[Helper] Model file not found: {file_path}")
    model = joblib.load(file_path)
    print(f"[Helper] Loaded Model <- {file_path}")
    return model
