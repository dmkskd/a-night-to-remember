"""
Fetch festival winners from Wikidata using SPARQL.
Much cleaner than scraping Wikipedia HTML.
"""

import requests

import sys
sys.path.insert(0, str(__file__).rsplit("/", 3)[0])

from catalog import MovieEntry, Recognition

WIKIDATA_ENDPOINT = "https://query.wikidata.org/sparql"
HEADERS = {
    "User-Agent": "ArtHouseMovieCatalog/1.0",
    "Accept": "application/json",
}

# Wikidata IDs for awards (verified)
AWARDS = {
    # Cannes
    "Cannes Palme d'Or": "Q179808",
    "Cannes Grand Prix": "Q844804",
    "Cannes Best Director": "Q510175",
    "Cannes Jury Prize": "Q164200",
    # Berlin
    "Berlin Golden Bear": "Q154590",
    "Berlin Grand Jury Prize": "Q154591",
    "Berlin Best Director": "Q154592",
    # Venice
    "Venice Golden Lion": "Q209459",
    "Venice Grand Jury Prize": "Q209460",
    "Venice Best Director": "Q209461",
    # Others
    "Hong Kong Best Film": "Q4722629",
    # Tokyo and Busan have limited/no data in Wikidata
}


def query_wikidata(sparql: str) -> list[dict]:
    """Execute a SPARQL query against Wikidata."""
    response = requests.get(
        WIKIDATA_ENDPOINT,
        params={"query": sparql, "format": "json"},
        headers=HEADERS,
    )
    response.raise_for_status()
    data = response.json()
    return data.get("results", {}).get("bindings", [])


def fetch_award_winners(award_id: str, award_name: str, min_year: int = 2005) -> list[MovieEntry]:
    """
    Fetch winners of a specific award from Wikidata.
    
    Args:
        award_id: Wikidata Q-ID for the award
        award_name: Human-readable name for the recognition
        min_year: Only return winners from this year onwards
    """
    sparql = f"""
    SELECT DISTINCT ?film ?filmLabel ?awardYear ?directorLabel WHERE {{
      ?film p:P166 ?statement .
      ?statement ps:P166 wd:{award_id} .
      ?statement pq:P585 ?awardDate .
      ?film wdt:P31 wd:Q11424 .  # instance of: film (filters out people)
      OPTIONAL {{ ?film wdt:P57 ?director . }}
      BIND(YEAR(?awardDate) AS ?awardYear)
      FILTER(?awardYear >= {min_year})
      SERVICE wikibase:label {{ bd:serviceParam wikibase:language "en". }}
    }}
    ORDER BY DESC(?awardYear)
    """
    
    results = query_wikidata(sparql)
    movies = []
    seen = set()  # Dedupe
    
    for row in results:
        title = row.get("filmLabel", {}).get("value", "")
        year_str = row.get("awardYear", {}).get("value", "")
        director = row.get("directorLabel", {}).get("value", "")
        
        if not title or not year_str:
            continue
        
        # Skip if title is just a Q-ID (no English label)
        if title.startswith("Q"):
            continue
        
        year = int(year_str)
        key = (title.lower(), year)
        
        if key in seen:
            continue
        seen.add(key)
        
        movies.append(MovieEntry(
            title=title,
            year=year,
            director=director,
            recognitions=[Recognition(type=award_name, year=year)]
        ))
    
    return movies


class WikidataFetcher:
    """Generic Wikidata-based fetcher for any award."""
    
    def __init__(self, award_id: str, name: str):
        self.award_id = award_id
        self.name = name
        self.recognition_type = name  # Same as name for awards
    
    def fetch(self, min_year: int = 2005) -> list[MovieEntry]:
        return fetch_award_winners(self.award_id, self.name, min_year)


# Pre-configured fetchers for major awards
class CannesWikidataFetcher(WikidataFetcher):
    def __init__(self):
        super().__init__("Q179808", "Cannes Palme d'Or")


class CannesGrandPrixFetcher(WikidataFetcher):
    def __init__(self):
        super().__init__("Q844804", "Cannes Grand Prix")


class CannesBestDirectorFetcher(WikidataFetcher):
    def __init__(self):
        super().__init__("Q510175", "Cannes Best Director")


class CannesJuryPrizeFetcher(WikidataFetcher):
    def __init__(self):
        super().__init__("Q164200", "Cannes Jury Prize")


class BerlinWikidataFetcher(WikidataFetcher):
    def __init__(self):
        super().__init__("Q154590", "Berlin Golden Bear")


class VeniceWikidataFetcher(WikidataFetcher):
    def __init__(self):
        super().__init__("Q209459", "Venice Golden Lion")


class HongKongWikidataFetcher(WikidataFetcher):
    def __init__(self):
        super().__init__("Q4722629", "Hong Kong Best Film")


if __name__ == "__main__":
    # Test
    print("Testing Wikidata fetcher...")
    fetcher = CannesWikidataFetcher()
    movies = fetcher.fetch(min_year=2020)
    for m in movies:
        print(f"  {m.year} - {m.title} ({m.director})")
