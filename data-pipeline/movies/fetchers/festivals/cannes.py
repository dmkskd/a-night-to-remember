"""
Fetch Cannes Film Festival Palme d'Or winners from Wikipedia.
"""

import re
import requests
from bs4 import BeautifulSoup

import sys
sys.path.insert(0, str(__file__).rsplit("/", 4)[0])

from catalog import MovieEntry, Recognition

HEADERS = {"User-Agent": "ArtHouseMovieCatalog/1.0"}


class CannesFetcher:
    """Fetches Palme d'Or winners from Wikipedia."""
    
    name = "Cannes Palme d'Or"
    url = "https://en.wikipedia.org/wiki/Palme_d%27Or"
    
    def fetch(self, min_year: int = 2005) -> list[MovieEntry]:
        """Fetch Palme d'Or winners from Wikipedia."""
        response = requests.get(self.url, headers=HEADERS)
        response.raise_for_status()
        soup = BeautifulSoup(response.text, "lxml")
        
        movies = []
        
        # Find the winners table with Film column
        tables = soup.find_all("table", class_="wikitable")
        for table in tables:
            headers = [th.get_text().strip().lower() for th in table.find_all("th")]
            if "film" not in headers and "english title" not in headers:
                continue
            
            rows = table.find_all("tr")
            for row in rows[1:]:
                cells = row.find_all(["td", "th"])
                if len(cells) < 3:
                    continue
                
                year = self._extract_year(cells[0].get_text())
                if not year or year < min_year:
                    continue
                
                title = self._clean_text(cells[1].get_text())
                director = self._clean_text(cells[3].get_text()) if len(cells) > 3 else ""
                
                # Skip non-film entries
                if not title or any(skip in title.lower() for skip in ["actor", "actress", "honorary"]):
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
        """Clean Wikipedia text."""
        text = re.sub(r"\[\d+\]", "", text)  # Remove citations
        text = re.sub(r"\s*\([^)]*\)", "", text)  # Remove parentheticals
        return text.strip()
    
    def _extract_year(self, text: str) -> int | None:
        """Extract a 4-digit year from text."""
        match = re.search(r"\b(19|20)\d{2}\b", text)
        return int(match.group()) if match else None


# Module-level instance for convenience
fetcher = CannesFetcher()
fetch = fetcher.fetch
