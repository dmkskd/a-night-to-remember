"""
Toronto International Film Festival (TIFF) fetcher.
Uses Wikidata to fetch People's Choice Award winners.
"""

import sys
sys.path.insert(0, str(__file__).rsplit("/", 4)[0])

from .wikidata import WikidataFetcher


class TorontoFetcher(WikidataFetcher):
    """Fetches TIFF People's Choice Award winners from Wikidata."""
    
    def __init__(self):
        # Q39087364 = Toronto International Film Festival People's Choice Award
        super().__init__("Q39087364", "TIFF People's Choice")


if __name__ == "__main__":
    print("Testing Toronto fetcher...")
    fetcher = TorontoFetcher()
    movies = fetcher.fetch(min_year=2015)
    print(f"Found {len(movies)} movies")
    for m in movies:
        print(f"  {m.year} - {m.title} ({m.director})")
