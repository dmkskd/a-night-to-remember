"""
Sight & Sound (BFI) fetcher.
Scrapes the annual best films lists from BFI website.
"""

import re
import requests
from bs4 import BeautifulSoup

import sys
sys.path.insert(0, str(__file__).rsplit("/", 4)[0])

from catalog import MovieEntry, Recognition

HEADERS = {
    "User-Agent": "ArtHouseMovieCatalog/1.0",
}

# BFI annual best films URLs (some years 404, removed)
ANNUAL_URLS = {
    2025: "https://www.bfi.org.uk/sight-and-sound/polls/50-best-films-2025",
    2024: "https://www.bfi.org.uk/sight-and-sound/polls/50-best-films-2024",
    2023: "https://www.bfi.org.uk/sight-and-sound/polls/best-films-2023-all-votes",
    2022: "https://www.bfi.org.uk/sight-and-sound/polls/best-films-2022-all-votes",
    2021: "https://www.bfi.org.uk/sight-and-sound/polls/best-films-2021-all-votes",
    2020: "https://www.bfi.org.uk/sight-and-sound/polls/best-films-2020",
}


class SightAndSoundFetcher:
    """Fetches Sight & Sound annual best films lists."""
    
    name = "Sight & Sound Top 10"
    recognition_type = "Sight & Sound Top 10"
    
    def fetch(self, min_year: int = 2005) -> list[MovieEntry]:
        """Fetch top 10 films from each year's Sight & Sound poll."""
        movies = []
        
        for year, url in ANNUAL_URLS.items():
            if year < min_year:
                continue
            
            try:
                year_movies = self._fetch_year(year, url)
                movies.extend(year_movies)
                print(f"  {year}: Found {len(year_movies)} films")
            except Exception as e:
                print(f"  {year}: Error - {e}")
        
        return movies
    
    def _fetch_year(self, year: int, url: str) -> list[MovieEntry]:
        """Fetch films from a single year's list."""
        response = requests.get(url, headers=HEADERS, timeout=30)
        response.raise_for_status()
        soup = BeautifulSoup(response.text, "html.parser")
        
        movies = []
        
        # BFI uses various heading patterns for film titles
        # Look for patterns like "1. Film Title" or "=1. Film Title"
        text = soup.get_text()
        
        # Pattern: number followed by title and director
        # e.g., "1. All We Imagine as Light\nPayal Kapadia, France, India"
        # or "=41. Afternoons of Solitude\nAlbert Serra"
        
        # Find all article/section elements that might contain film entries
        articles = soup.find_all(['article', 'div', 'section'])
        
        # Also try to find h2/h3 headings with film titles
        headings = soup.find_all(['h2', 'h3', 'h4'])
        
        for heading in headings:
            text = heading.get_text(strip=True)
            
            # Match patterns like "1. Film Title" or "=10. Film Title"
            match = re.match(r'^=?\d+\.\s*(.+)$', text)
            if match:
                title = match.group(1).strip()
                
                # Try to find director in next sibling or parent
                director = ""
                next_elem = heading.find_next_sibling()
                if next_elem:
                    next_text = next_elem.get_text(strip=True)
                    # Director is usually first line, format: "Director Name, Country"
                    if ',' in next_text:
                        director = next_text.split(',')[0].strip()
                
                # Only add top 10 (rank 1-10)
                rank_match = re.match(r'^=?(\d+)\.', text)
                if rank_match:
                    rank = int(rank_match.group(1))
                    if rank <= 10:
                        movies.append(MovieEntry(
                            title=title,
                            year=year,
                            director=director,
                            recognitions=[Recognition(
                                type="Sight & Sound Top 10",
                                year=year,
                                details=f"Ranked #{rank}"
                            )]
                        ))
        
        return movies


if __name__ == "__main__":
    print("Testing Sight & Sound fetcher...")
    fetcher = SightAndSoundFetcher()
    movies = fetcher.fetch(min_year=2020)
    print(f"\nTotal: {len(movies)} movies")
    for m in movies[:20]:
        print(f"  {m.year} - {m.title} ({m.director}) - {m.recognitions[0].details}")
