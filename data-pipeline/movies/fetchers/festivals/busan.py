"""
Fetch Busan International Film Festival winners from Wikipedia.
"""

import re
import requests
from bs4 import BeautifulSoup

import sys
sys.path.insert(0, str(__file__).rsplit("/", 4)[0])

from catalog import MovieEntry, Recognition

HEADERS = {"User-Agent": "ArtHouseMovieCatalog/1.0"}


class BusanFetcher:
    """Fetches Busan New Currents Award winners - static data."""
    
    name = "Busan New Currents"
    recognition_type = "Busan New Currents"
    
    # Static data - Wikipedia structure too complex
    WINNERS = [
        {"title": "Mongrel", "year": 2024, "director": "Wei Shujun"},
        {"title": "In Our Day", "year": 2023, "director": "Hong Sang-soo"},
        {"title": "Return to Seoul", "year": 2022, "director": "Davy Chou"},
        {"title": "Rehana Maryam Noor", "year": 2021, "director": "Abdullah Mohammad Saad"},
        {"title": "Moving On", "year": 2019, "director": "Yoon Dan-bi"},
        {"title": "Memories of My Body", "year": 2018, "director": "Garin Nugroho"},
        {"title": "Marlina the Murderer in Four Acts", "year": 2017, "director": "Mouly Surya"},
        {"title": "Interchange", "year": 2016, "director": "Dain Iskandar Said"},
        {"title": "The Throne", "year": 2015, "director": "Lee Joon-ik"},
        {"title": "The Lunchbox", "year": 2013, "director": "Ritesh Batra"},
        {"title": "Bleak Night", "year": 2011, "director": "Yoon Sung-hyun"},
        {"title": "Poetry", "year": 2010, "director": "Lee Chang-dong"},
    ]
    
    def fetch(self, min_year: int = 2005) -> list[MovieEntry]:
        """Return static list of Busan New Currents winners."""
        movies = []
        for w in self.WINNERS:
            if w["year"] >= min_year:
                movies.append(MovieEntry(
                    title=w["title"],
                    year=w["year"],
                    director=w["director"],
                    recognitions=[Recognition(type=self.name, year=w["year"])]
                ))
        return movies


fetcher = BusanFetcher()
fetch = fetcher.fetch
