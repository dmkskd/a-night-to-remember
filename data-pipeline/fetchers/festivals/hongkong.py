"""
Fetch Hong Kong Film Awards Best Film winners from Wikipedia.
"""

import re
import requests
from bs4 import BeautifulSoup

import sys
sys.path.insert(0, str(__file__).rsplit("/", 3)[0])

from catalog import MovieEntry, Recognition

HEADERS = {"User-Agent": "ArtHouseMovieCatalog/1.0"}


class HongKongFetcher:
    """Fetches Hong Kong Film Awards Best Film winners from Wikipedia."""
    
    name = "Hong Kong Best Film"
    url = "https://en.wikipedia.org/wiki/Hong_Kong_Film_Award_for_Best_Film"
    
    def fetch(self, min_year: int = 2005) -> list[MovieEntry]:
        """Fetch Best Film winners from Wikipedia."""
        response = requests.get(self.url, headers=HEADERS)
        response.raise_for_status()
        soup = BeautifulSoup(response.text, "lxml")
        
        movies = []
        tables = soup.find_all("table", class_="wikitable")
        
        for table in tables:
            rows = table.find_all("tr")
            for row in rows[1:]:
                cells = row.find_all(["td", "th"])
                if len(cells) < 2:
                    continue
                
                year = self._extract_year(cells[0].get_text())
                if not year or year < min_year:
                    continue
                
                title = self._clean_text(cells[1].get_text())
                director = self._clean_text(cells[2].get_text()) if len(cells) > 2 else ""
                
                if not title or title.lower().startswith("year") or title.lower().startswith("ceremony"):
                    continue
                
                movie = MovieEntry(
                    title=title,
                    year=year,
                    director=director,
                    recognitions=[Recognition(type=self.name, year=year)]
                )
                movies.append(movie)
        
        return movies
    
    def _clean_text(self, text: str) -> str:
        text = re.sub(r"\[\d+\]", "", text)
        text = re.sub(r"\s*\([^)]*\)", "", text)
        return text.strip()
    
    def _extract_year(self, text: str) -> int | None:
        match = re.search(r"\b(19|20)\d{2}\b", text)
        return int(match.group()) if match else None


fetcher = HongKongFetcher()
fetch = fetcher.fetch
