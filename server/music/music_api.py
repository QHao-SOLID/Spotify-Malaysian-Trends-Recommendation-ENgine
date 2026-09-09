import json
import os
from urllib.parse import quote

import requests
from dotenv import load_dotenv

load_dotenv()

CLIENT_ID = os.getenv('CLIENT_ID')
CLIENT_SECRET = os.getenv('CLIENT_SECRET')

def get_access_token(
    client_id,
    client_secret
):

    url = "https://account.soundcharts.com/oauth/token"

    data = {
        "grant_type": "client_credentials",
    }

    response = requests.post(
        url,
        auth=(CLIENT_ID, CLIENT_SECRET),
        data=data
    )

    response.raise_for_status()

    return response.json().get("access_token")

def request_song_metadata(
    uuid,
    access_token = get_access_token(CLIENT_ID, CLIENT_SECRET)
):

    url = f"https://customer.api.soundcharts.com/api/v2.25/song/{uuid}"

    headers = {
        "Authorization": f"Bearer {access_token}"
    }

    response = requests.get(url, headers=headers)

    response.raise_for_status()

    return response.json()

def search_song(
    term,
    access_token = get_access_token(CLIENT_ID, CLIENT_SECRET)
):

    url = f"https://customer.api.soundcharts.com/api/v2/song/search/{term}"

    headers = {
        "Authorization": f"Bearer {access_token}"
    }

    params = {
        "limit": 5
    }

    response = requests.get(
        url,
        headers=headers,
        params=params
    )

    response.raise_for_status()

    return response.json()

def get_selected_uuid(
    data,
    selection
):

    items = data["items"]

    # Convert user selection (1-based) to Python index (0-based)
    index = selection - 1

    if index < 0 or index >= len(items):
        raise ValueError("Invalid selection")

    return items[index]["uuid"]

def extract_artwork(
    search_result
):

    obj = search_result.get("object", search_result)
    return {
        "imageUrl": obj.get("imageUrl", ""),
        "artist_images": [
            {"name": a.get("name", ""), "imageUrl": a.get("imageUrl", "")}
            for a in obj.get("artists", [])
        ]
    }

def query_to_entry(
    search_result
):
    track_data = {
        "isrc": search_result["object"]["isrc"]["value"],
        "artists": search_result["object"]["creditName"],
        "track_name": search_result["object"]["name"],
        "duration_ms": search_result["object"]["duration"] * 60000,
        "explicit": search_result["object"]["explicit"],

        "danceability": search_result["object"]["audio"]["danceability"],
        "energy": search_result["object"]["audio"]["energy"],
        "key": search_result["object"]["audio"]["key"],
        "loudness": search_result["object"]["audio"]["loudness"],
        "mode": search_result["object"]["audio"]["mode"],
        "speechiness": search_result["object"]["audio"]["speechiness"],
        "acousticness": search_result["object"]["audio"]["acousticness"],
        "instrumentalness": search_result["object"]["audio"]["instrumentalness"],
        "liveness": search_result["object"]["audio"]["liveness"],
        "valence": search_result["object"]["audio"]["valence"],
        "tempo": search_result["object"]["audio"]["tempo"],
        "time_signature": search_result["object"]["audio"]["timeSignature"],

        "track_genre": search_result["object"]["genres"][0]["root"]
    }

    return track_data
