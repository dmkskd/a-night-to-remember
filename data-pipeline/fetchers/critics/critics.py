"""
Critics' awards fetchers.
Scrapes Wikipedia for major film critics' associations awards.
"""

import re
import requests
from bs4 import BeautifulSoup

import sys
sys.path.insert(0, str(__file__).rsplit("/", 3)[0])

from catalog import MovieEntry, Recognition

HEADERS = {
    "User-Agent": "ArtHouseMovieCatalog/1.0",
}


def fetch_wikipedia_table(url: str, table_index: int = 0) -> list[dict]:
    """Fetch and parse a Wikipedia table."""
    response = requests.get(url, headers=HEADERS)
    response.raise_for_status()
    soup = BeautifulSoup(response.text, "html.parser")
    
    tables = soup.find_all("table", class_="wikitable")
    if table_index >= len(tables):
        return []
    
    table = tables[table_index]
    rows = table.find_all("tr")
    
    # Get headers
    headers = []
    header_row = rows[0]
    for th in header_row.find_all(["th", "td"]):
        headers.append(th.get_text(strip=True).lower())
    
    # Parse data rows
    data = []
    for row in rows[1:]:
        cells = row.find_all(["td", "th"])
        if len(cells) >= 2:
            row_data = {}
            for i, cell in enumerate(cells):
                if i < len(headers):
                    row_data[headers[i]] = cell.get_text(strip=True)
            data.append(row_data)
    
    return data


class NSFCFetcher:
    """National Society of Film Critics - Best Film winners."""
    
    name = "NSFC Best Film"
    recognition_type = "NSFC Best Film"
    url = "https://en.wikipedia.org/wiki/National_Society_of_Film_Critics_Award_for_Best_Film"
    
    def fetch(self, min_year: int = 2005) -> list[MovieEntry]:
        """Fetch NSFC Best Film winners from Wikipedia."""
        response = requests.get(self.url, headers=HEADERS)
        response.raise_for_status()
        soup = BeautifulSoup(response.text, "html.parser")
        
        movies = []
        tables = soup.find_all("table", class_="wikitable")
        
        for table in tables:
            rows = table.find_all("tr")
            for row in rows[1:]:  # Skip header
                cells = row.find_all(["td", "th"])
                if len(cells) >= 3:
                    year_text = cells[0].get_text(strip=True)
                    title = cells[1].get_text(strip=True)
                    director = cells[2].get_text(strip=True)
                    
                    # Clean up title (remove footnote markers)
                    title = re.sub(r'\[.*?\]', '', title).strip()
                    director = re.sub(r'\[.*?\]', '', director).strip()
                    
                    # Parse year
                    try:
                        year = int(year_text[:4])
                    except (ValueError, IndexError):
                        continue
                    
                    if year < min_year:
                        continue
                    
                    movies.append(MovieEntry(
                        title=title,
                        year=year,
                        director=director,
                        recognitions=[Recognition(type="NSFC Best Film", year=year)]
                    ))
        
        return movies


class NYFCCFetcher:
    """New York Film Critics Circle - Best Film winners."""
    
    name = "NYFCC Best Film"
    url = "https://en.wikipedia.org/wiki/New_York_Film_Critics_Circle_Award_for_Best_Film"
    
    def fetch(self, min_year: int = 2005) -> list[MovieEntry]:
        """Fetch NYFCC Best Film winners from Wikipedia."""
        response = requests.get(self.url, headers=HEADERS)
        response.raise_for_status()
        soup = BeautifulSoup(response.text, "html.parser")
        
        movies = []
        tables = soup.find_all("table", class_="wikitable")
        
        for table in tables:
            rows = table.find_all("tr")
            for row in rows[1:]:
                cells = row.find_all(["td", "th"])
                if len(cells) >= 2:
                    year_text = cells[0].get_text(strip=True)
                    title = cells[1].get_text(strip=True)
                    
                    # Try to get director if available
                    director = ""
                    if len(cells) >= 3:
                        director = cells[2].get_text(strip=True)
                    
                    # Clean up
                    title = re.sub(r'\[.*?\]', '', title).strip()
                    director = re.sub(r'\[.*?\]', '', director).strip()
                    
                    try:
                        year = int(year_text[:4])
                    except (ValueError, IndexError):
                        continue
                    
                    if year < min_year:
                        continue
                    
                    movies.append(MovieEntry(
                        title=title,
                        year=year,
                        director=director,
                        recognitions=[Recognition(type="NYFCC Best Film", year=year)]
                    ))
        
        return movies


class LAFCAFetcher:
    """Los Angeles Film Critics Association - Best Film winners."""
    
    name = "LAFCA Best Film"
    url = "https://en.wikipedia.org/wiki/Los_Angeles_Film_Critics_Association_Award_for_Best_Film"
    
    def fetch(self, min_year: int = 2005) -> list[MovieEntry]:
        """Fetch LAFCA Best Film winners from Wikipedia."""
        response = requests.get(self.url, headers=HEADERS)
        response.raise_for_status()
        soup = BeautifulSoup(response.text, "html.parser")
        
        movies = []
        tables = soup.find_all("table", class_="wikitable")
        
        for table in tables:
            rows = table.find_all("tr")
            for row in rows[1:]:
                cells = row.find_all(["td", "th"])
                if len(cells) >= 2:
                    year_text = cells[0].get_text(strip=True)
                    title = cells[1].get_text(strip=True)
                    
                    director = ""
                    if len(cells) >= 3:
                        director = cells[2].get_text(strip=True)
                    
                    title = re.sub(r'\[.*?\]', '', title).strip()
                    director = re.sub(r'\[.*?\]', '', director).strip()
                    
                    try:
                        year = int(year_text[:4])
                    except (ValueError, IndexError):
                        continue
                    
                    if year < min_year:
                        continue
                    
                    movies.append(MovieEntry(
                        title=title,
                        year=year,
                        director=director,
                        recognitions=[Recognition(type="LAFCA Best Film", year=year)]
                    ))
        
        return movies


if __name__ == "__main__":
    print("Testing NSFC fetcher...")
    fetcher = NSFCFetcher()
    movies = fetcher.fetch(min_year=2015)
    print(f"Found {len(movies)} movies")
    for m in movies:
        print(f"  {m.year} - {m.title} ({m.director})")
    
    print("\nTesting NYFCC fetcher...")
    fetcher = NYFCCFetcher()
    movies = fetcher.fetch(min_year=2015)
    print(f"Found {len(movies)} movies")
    for m in movies:
        print(f"  {m.year} - {m.title} ({m.director})")
    
    print("\nTesting LAFCA fetcher...")
    fetcher = LAFCAFetcher()
    movies = fetcher.fetch(min_year=2015)
    print(f"Found {len(movies)} movies")
    for m in movies:
        print(f"  {m.year} - {m.title} ({m.director})")
