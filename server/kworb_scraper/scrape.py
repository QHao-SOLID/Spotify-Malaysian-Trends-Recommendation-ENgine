import argparse
import csv
import json
import sys
from pathlib import Path

import requests
from bs4 import BeautifulSoup

CONFIG_PATH = Path(__file__).parent / "countries.json"
TARGET_ID = "spotifydaily"


def load_countries() -> dict:
    with open(CONFIG_PATH, encoding="utf-8") as f:
        return json.load(f)


def scrape_country(name: str, url: str) -> None:
    res = requests.get(url)
    res.raise_for_status()

    soup = BeautifulSoup(res.content, "html.parser")
    table = soup.find("table", {"id": TARGET_ID})

    if not table:
        print(f"[WARN] No table found for {name}, skipping")
        return

    headers = []
    rows = []

    for i, row in enumerate(table.find_all("tr")):
        if i == 0:
            headers = [el.text.strip() for el in row.find_all("th")]
        else:
            rows.append([el.text.strip() for el in row.find_all("td")])

    out_path = Path(__file__).parent / f"{name}.csv"
    with open(out_path, "w", newline="", encoding="utf-8") as f:
        writer = csv.writer(f)
        writer.writerow(headers)
        writer.writerows(rows)

    print(f"[OK] {name}: {len(rows)} rows -> {out_path.name}")


def main():
    parser = argparse.ArgumentParser(description="Scrape kworb Spotify charts")
    parser.add_argument("--country", default="all", help="Country name or 'all'")
    args = parser.parse_args()

    countries = load_countries()

    if args.country == "all":
        targets = countries
    elif args.country in countries:
        targets = {args.country: countries[args.country]}
    else:
        print(f"[ERROR] '{args.country}' not in {CONFIG_PATH.name}")
        print(f"Available: {', '.join(countries.keys())}")
        sys.exit(1)

    for name, url in targets.items():
        scrape_country(name, url)


if __name__ == "__main__":
    main()
