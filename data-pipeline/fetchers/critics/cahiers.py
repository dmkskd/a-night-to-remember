"""
Fetch Cahiers du Cinéma annual Top 10 lists from Wikipedia.
"""

import re
import requests
from bs4 import BeautifulSoup

import sys
sys.path.insert(0, str(__file__).rsplit("/", 3)[0])

from catalog import MovieEntry, Recognition

HEADERS = {"User-Agent": "ArtHouseMovieCatalog/1.0"}


class CahiersFetcher:
    """Fetches Cahiers du Cinéma Top 10 films from Wikipedia."""
    
    name = "Cahiers du Cinéma Top 10"
    recognition_type = "Cahiers du Cinéma Top 10"
    url = "https://en.wikipedia.org/wiki/Cahiers_du_cin%C3%A9ma%27s_Annual_Top_10_Lists"
    
    def fetch(self, min_year: int = 2005) -> list[MovieEntry]:
        """Fetch Top 10 films from Wikipedia."""
        response = requests.get(self.url, headers=HEADERS)
        response.raise_for_status()
        soup = BeautifulSoup(response.text, "lxml")
        
        movies = []
        tables = soup.find_all("table", class_="wikitable")
        
        for table in tables:
            rows = table.find_all("tr")
            current_year = None
            
            for row in rows:
                cells = row.find_all(["td", "th"])
                if not cells:
                    continue
                
                first_cell = self._clean_text(cells[0].get_text())
                
                # Check if this is a year row (single cell with year)
                year_match = re.match(r"^(19|20)\d{2}", first_cell)
                if year_match and len(cells) == 1:
                    current_year = int(year_match.group())
                    continue
                
                # Skip if year not set or too old
                if not current_year or current_year < min_year:
                    continue
                
                # Check if this is a ranked film (starts with number)
                rank_match = re.match(r"^(\d+)\.$", first_cell)
                if not rank_match:
                    continue
                
                rank = int(rank_match.group(1))
                if rank > 10:  # Only top 10
                    continue
                
                # Extract film data - structure varies
                if len(cells) < 3:
                    continue
                
                title = self._clean_text(cells[1].get_text())
                # Director might be in cell 2 or 3 depending on if original title exists
                director = ""
                for i in [2, 3]:
                    if i < len(cells):
                        potential_director = self._clean_text(cells[i].get_text())
                        # Skip if it looks like a country
                        if potential_director and not any(c in potential_director.lower() for c in ["states", "france", "korea", "japan", "germany", "italy", "china", "kingdom"]):
                            director = potential_director
                            break
                
                if not title:
                    continue
                
                movie = MovieEntry(
                    title=title,
                    year=current_year,
                    director=director,
                    recognitions=[Recognition(
                        type=self.name,
                        year=current_year,
                        details=f"Ranked #{rank}"
                    )]
                )
                movies.append(movie)
        
        return movies
    
    def _clean_text(self, text: str) -> str:
        text = re.sub(r"\[\d+\]", "", text)
        text = re.sub(r"\s*\([^)]*\)", "", text)
        return text.strip()


fetcher = CahiersFetcher()
fetch = fetcher.fetch


if __name__ == "__main__":
    print("Testing Cahiers fetcher...")
    movies = fetch(min_year=2020)
    for m in movies[:15]:
        rec = m.recognitions[0]
        print(f"  {m.year} - {m.title} ({m.director}) - {rec.details}")
