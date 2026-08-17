import urllib.request
import re
import pandas as pd
from bs4 import BeautifulSoup

WIKI_URLS = [
    "https://en.wikipedia.org/wiki/Malaysia_Songs",
    "https://en.wikipedia.org/wiki/List_of_number-one_songs_of_2026_(Malaysia)",
    "https://en.wikipedia.org/wiki/List_of_number-one_songs_of_2025_(Malaysia)",
    "https://en.wikipedia.org/wiki/List_of_number-one_songs_of_2024_(Malaysia)",
    "https://en.wikipedia.org/wiki/List_of_number-one_songs_of_2023_(Malaysia)",
    "https://en.wikipedia.org/wiki/List_of_number-one_songs_of_2022_(Malaysia)",
]

HEADERS = {
    "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/120.0.0.0 Safari/537.36"
}


def scrape_wikipedia_charts():
    scraped_rows = []

    for url in WIKI_URLS:
        print(f"Scraping Wikipedia URL: {url}...")
        try:
            req = urllib.request.Request(url, headers=HEADERS)
            with urllib.request.urlopen(req) as resp:
                html = resp.read().decode("utf-8")

            soup = BeautifulSoup(html, "html.parser")
            tables = soup.find_all("table", class_="wikitable")

            for t_idx, table in enumerate(tables):
                df_list = pd.read_html(str(table))
                if not df_list:
                    continue
                df_table = df_list[0]

                # Flatten multi-index columns if present
                if isinstance(df_table.columns, pd.MultiIndex):
                    df_table.columns = ["_".join(col).strip() for col in df_table.columns.values]

                cols = [str(c).lower() for c in df_table.columns]
                print(f"  Table {t_idx+1} Columns: {cols}")

                # Identify song and artist columns dynamically
                song_col = next((c for c in df_table.columns if any(k in str(c).lower() for k in ["song", "title", "track", "single"])), None)
                artist_col = next((c for c in df_table.columns if "artist" in str(c).lower()), None)

                if song_col and artist_col:
                    for _, row in df_table.iterrows():
                        song = str(row[song_col])
                        artist = str(row[artist_col])

                        # Clean Wikipedia bracket citations like [1] or quotes
                        song = re.sub(r'\[.*?\]|"', '', song).strip()
                        artist = re.sub(r'\[.*?\]|"', '', artist).strip()

                        if song and artist and song.lower() != "nan" and artist.lower() != "nan":
                            scraped_rows.append({
                                "song": song,
                                "artist": artist,
                                "source_url": url,
                                "table_id": t_idx + 1
                            })
        except Exception as e:
            print(f"  Error scraping {url}: {e}")

    df_scraped = pd.DataFrame(scraped_rows)
    if not df_scraped.empty:
        df_scraped.drop_duplicates(subset=["song", "artist"], inplace=True)
    print(f"\nTotal Scraped Wikipedia Chart Entries: {len(df_scraped)}")
    print(df_scraped.head(15))
    return df_scraped


if __name__ == "__main__":
    scrape_wikipedia_charts()
