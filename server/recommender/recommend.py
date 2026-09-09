import sqlite3
from collections import Counter

import numpy as np
import pandas as pd

# ── Constants ────────────────────────────────────────────────────────────────

REQUIRED_COLS = [
    'track_id',
    'artists',
    'track_name',
    'duration_ms',
    'explicit',
    'danceability',
    'energy',
    'key',
    'loudness',
    'mode',
    'speechiness',
    'acousticness',
    'instrumentalness',
    'liveness',
    'valence',
    'tempo',
    'time_signature',
    'track_genre'
]

CONT_FEATURES = [
    'danceability',
    'energy',
    'loudness',
    'speechiness',
    'acousticness',
    'instrumentalness',
    'liveness',
    'valence',
    'tempo'
]

BINARY_FEATURES = [
    'explicit',
    'mode'
]

CATEGORICAL_FEATURES = [
    'track_genre'
]

ORDINAL_FEATURES = [
    'key',
    'time_signature'
]

# ── Database ─────────────────────────────────────────────────────────────────

def pandas2db(cols: list, filename: str, output_name: str, limit: int = None) -> None:
    df = pd.read_csv(filename)
    df = df[cols]

    if limit is not None:
        if limit > 0:
            df = df.head(limit)
        else:
            raise ValueError("Limit must be a positive integer or None")

    conn = sqlite3.connect(output_name)
    conn.execute('PRAGMA journal_mode=WAL;')
    df.to_sql('PLAYLIST', conn, if_exists='replace', index=False)
    conn.close()

    print(f"Converted {len(df)} rows to {output_name}")


def get_entry_as_dict(
    db_path: str = "playlist.db",
    entry_number: int = None,
    track_id: str = None
) -> dict:
    conn = sqlite3.connect(db_path)

    if track_id is not None:
        query = f"SELECT * FROM PLAYLIST WHERE track_id = '{track_id}'"
    elif entry_number is not None:
        query = f"SELECT * FROM PLAYLIST LIMIT 1 OFFSET {entry_number}"
    else:
        conn.close()
        raise ValueError("Either entry_number or track_id must be provided")

    df = pd.read_sql_query(query, conn)
    conn.close()

    if df.empty:
        if track_id:
            raise ValueError(f"No entry found with track_id: {track_id}")
        else:
            raise ValueError(f"No entry found at index {entry_number}")

    entry = df.iloc[0].to_dict()

    return {
        "track_id": entry.get('track_id', ''),
        "artists": entry.get('artists', ''),
        "track_name": entry.get('track_name', ''),
        "duration_ms": entry.get('duration_ms', 0),

        "cont_features": {
            "danceability": entry.get('danceability', 0.0),
            "energy": entry.get('energy', 0.0),
            "loudness": entry.get('loudness', 0.0),
            "speechiness": entry.get('speechiness', 0.0),
            "acousticness": entry.get('acousticness', 0.0),
            "instrumentalness": entry.get('instrumentalness', 0.0),
            "liveness": entry.get('liveness', 0.0),
            "valence": entry.get('valence', 0.0),
            "tempo": entry.get('tempo', 0.0)
        },

        "binary_features": {
            "explicit": bool(entry.get('explicit', False)),
            "mode": entry.get('mode', 0)
        },

        "categorical_features": {
            "track_genre": entry.get('track_genre', '')
        },

        "ordinal_features": {
            "key": entry.get('key', 0),
            "time_signature": entry.get('time_signature', 4)
        }
    }

# ── Statistics ───────────────────────────────────────────────────────────────

def compute_statistics(feature: str, db_path: str = 'playlist.db') -> dict:
    conn = sqlite3.connect(db_path)
    df = pd.read_sql_query(
        f"SELECT {feature} FROM PLAYLIST WHERE {feature} IS NOT NULL",
        conn
    )
    conn.close()

    data = df[feature]

    return {
        'name': feature,
        'sample_size': len(data),
        'mean': data.mean(),
        'variance': data.var(ddof=1),
        'std': data.std(ddof=1),
        'sum': data.sum(),
    }


def statistics_vector(cont_features: list = None, db_path: str = 'playlist.db') -> tuple:
    if cont_features is None:
        cont_features = CONT_FEATURES

    statistics = {}
    for i in cont_features:
        stats = compute_statistics(i, db_path=db_path)
        statistics[i] = {'mean': stats['mean'], 'std': stats['std']}

    mean_statistics = [v['mean'] for v in statistics.values()]
    std_statistics = [v['std'] for v in statistics.values()]

    return mean_statistics, std_statistics

# ── Distance Metrics ─────────────────────────────────────────────────────────

def cont_features_euclidean(query: dict, db_song: dict, stats: tuple) -> float:
    mean, std = stats

    normalised_query = (np.array(list(query['cont_features'].values())) - np.array(mean)) / np.array(std)
    normalised_db_song = (np.array(list(db_song['cont_features'].values())) - np.array(mean)) / np.array(std)

    return np.sum((normalised_query - normalised_db_song) ** 2)


def bin_features_hamming(query: dict, db_song: dict) -> int:
    q_values = np.array(list(query['binary_features'].values()))
    db_values = np.array(list(db_song['binary_features'].values()))

    return np.sum(q_values != db_values)


def cat_features_hamming(query: dict, db_song: dict) -> int:
    q_values = np.array(list(query['categorical_features'].values()))
    db_values = np.array(list(db_song['categorical_features'].values()))

    return np.sum(q_values != db_values)


def ordinal_feature_distance(query: dict, db_song: dict) -> float:
    q_values = list(query['ordinal_features'].values())
    db_values = list(db_song['ordinal_features'].values())

    key_distance = min(abs(q_values[0] - db_values[0]), 12 - abs(q_values[0] - db_values[0])) ** 2
    ts_distance = np.sum(q_values[1] != db_values[1])

    return key_distance + ts_distance


def distance(query: dict, db_song: dict, stats: tuple) -> float:
    return np.sum(
        np.array([
            cont_features_euclidean(query, db_song, stats),
            bin_features_hamming(query, db_song),
            cat_features_hamming(query, db_song),
            ordinal_feature_distance(query, db_song)
        ])
    )

# ── Vectorized Distance ─────────────────────────────────────────────────────

def _load_all(db_path: str) -> pd.DataFrame:
    conn = sqlite3.connect(db_path)
    df = pd.read_sql_query("SELECT * FROM PLAYLIST", conn)
    conn.close()
    return df


def _query_to_vectors(query: dict, mean: np.ndarray, std: np.ndarray):
    q_cont = np.array([query['cont_features'][f] for f in CONT_FEATURES])
    q_cont_norm = (q_cont - mean) / std

    q_bin = np.array([int(query['binary_features'][f]) for f in BINARY_FEATURES])
    q_cat = query['categorical_features']['track_genre']
    q_key = query['ordinal_features']['key']
    q_ts = query['ordinal_features']['time_signature']

    return q_cont_norm, q_bin, q_cat, q_key, q_ts


def compute_distances_fast(query: dict, db_path: str, limit: int = None) -> list:
    df = _load_all(db_path)

    if limit is not None:
        df = df.head(limit)

    mean = df[CONT_FEATURES].mean().values
    std = df[CONT_FEATURES].std(ddof=1).values.copy()
    std[std == 0] = 1

    q_cont_norm, q_bin, q_cat, q_key, q_ts = _query_to_vectors(query, mean, std)

    db_cont = df[CONT_FEATURES].values
    db_cont_norm = (db_cont - mean) / std
    cont_dist = np.sum((db_cont_norm - q_cont_norm) ** 2, axis=1)

    db_bin = df[BINARY_FEATURES].values.astype(int)
    bin_dist = np.sum(db_bin != q_bin, axis=1)

    cat_dist = (df[CATEGORICAL_FEATURES[0]].values != q_cat).astype(int)

    db_key = df['key'].values.astype(int)
    key_diff = np.abs(db_key - q_key)
    key_dist = np.minimum(key_diff, 12 - key_diff) ** 2

    db_ts = df['time_signature'].values.astype(int)
    ts_dist = (db_ts != q_ts).astype(int)

    total = cont_dist + bin_dist + cat_dist + key_dist + ts_dist

    results = []
    for i in np.argsort(total)[:limit if limit else len(total)]:
        row = df.iloc[i]
        results.append({
            'track_id': row['track_id'],
            'track_name': row['track_name'],
            'artists': row['artists'],
            'distance': float(total[i])
        })

    return results

# ── Recommendation ───────────────────────────────────────────────────────────

def get_top_k_track_ids(distance_calculated: list, k: int = 3) -> list:
    sorted_results = sorted(distance_calculated, key=lambda x: x['distance'])
    return [result['track_id'] for result in sorted_results[:k]]


def get_top_k_details(distance_calculated: list, k: int = 3) -> list:
    sorted_results = sorted(distance_calculated, key=lambda x: x['distance'])
    return sorted_results[:k]


def synthetic_feature(tracklist: list, db_path: str = 'playlist.db') -> dict:
    tracksData = [get_entry_as_dict(db_path=db_path, track_id=track) for track in tracklist]

    cont_features = {key: [] for key in tracksData[0]['cont_features']}
    binary_features = {key: [] for key in tracksData[0]['binary_features']}
    categorical_features = {key: [] for key in tracksData[0]['categorical_features']}
    ordinal_features = {key: [] for key in tracksData[0]['ordinal_features']}

    for track in tracksData:
        for key, value in track['cont_features'].items():
            cont_features[key].append(value)
        for key, value in track['binary_features'].items():
            binary_features[key].append(value)
        for key, value in track['categorical_features'].items():
            categorical_features[key].append(value)
        for key, value in track['ordinal_features'].items():
            ordinal_features[key].append(value)

    synthetic = {
        "cont_features": {key: np.mean(values) for key, values in cont_features.items()},
        "binary_features": {key: Counter(values).most_common(1)[0][0] for key, values in binary_features.items()},
        "categorical_features": {key: Counter(values).most_common(1)[0][0] for key, values in categorical_features.items()},
        "ordinal_features": {key: Counter(values).most_common(1)[0][0] for key, values in ordinal_features.items()}
    }

    synthetic['artists'] = f"Synth_{len(tracksData)}_tracks"
    synthetic['track_name'] = f"Synthetic_{len(tracksData)}_tracks"
    synthetic['duration_ms'] = int(np.mean([track['duration_ms'] for track in tracksData]))
    synthetic['track_id'] = f"synth_{len(tracksData)}"

    return synthetic


def recommend(query: dict, k: int = 5, db_path: str = 'playlist.db', limit: int = None) -> list:
    distances = compute_distances_fast(query, db_path, limit=limit)
    top_k = get_top_k_track_ids(distances, k=k)

    synth = synthetic_feature(top_k, db_path=db_path)
    distances2 = compute_distances_fast(synth, db_path, limit=limit)

    return get_top_k_details(distances2, k=k)
