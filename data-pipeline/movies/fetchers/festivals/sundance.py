"""
Sundance Film Festival fetcher.
Uses Wikidata to fetch Grand Jury Prize winners (US Dramatic and World Cinema).
"""

import sys
sys.path.insert(0, str(__file__).rsplit("/", 4)[0])

from .wikidata import WikidataFetcher, fetch_award_winners
from catalog import MovieEntry


class SundanceFetcher:
    """Fetches Sundance Grand Jury Prize winners from Wikidata."""
    
    name = "Sundance"
    recognition_type = "Sundance Grand Jury Prize"  # Primary type
    recognition_types = ["Sundance Grand Jury Prize", "Sundance World Cinema Prize"]
    
    def __init__(self):
        # Q3774974 = Sundance US Dramatic Grand Jury Prize
        # Q969394 = Sundance World Cinema Dramatic Grand Jury Prize
        self.us_dramatic_id = "Q3774974"
        self.world_cinema_id = "Q969394"
    
    def fetch(self, min_year: int = 2005) -> list[MovieEntry]:
        """Fetch both US Dramatic and World Cinema Grand Jury Prize winners."""
        movies = []
        
        # Fetch US Dramatic winners
        us_movies = fetch_award_winners(
            self.us_dramatic_id, 
            "Sundance Grand Jury Prize", 
            min_year
        )
        movies.extend(us_movies)
        
        # Fetch World Cinema winners
        world_movies = fetch_award_winners(
            self.world_cinema_id, 
            "Sundance World Cinema Prize", 
            min_year
        )
        movies.extend(world_movies)
        
        return movies


if __name__ == "__main__":
    print("Testing Sundance fetcher...")
    fetcher = SundanceFetcher()
    movies = fetcher.fetch(min_year=2015)
    print(f"Found {len(movies)} movies")
    for m in movies:
        print(f"  {m.year} - {m.title} ({m.director}) - {m.recognitions[0].type}")
