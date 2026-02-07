"""
Annecy International Animation Film Festival fetcher.
The most prestigious animation festival in the world.
Cristal d'Or (Crystal Award) for Best Feature Film.
"""

import sys
sys.path.insert(0, str(__file__).rsplit("/", 4)[0])

from catalog import MovieEntry, Recognition

# Annecy Cristal d'Or - Best Animated Feature winners
ANNECY_WINNERS = {
    2025: ("Memoir of a Snail", "Adam Elliot"),
    2024: ("Flow", "Gints Zilbalodis"),
    2023: ("Robot Dreams", "Pablo Berger"),
    2022: ("My Love Affair with Marriage", "Signe Baumane"),
    2021: ("Flee", "Jonas Poher Rasmussen"),
    2020: ("Calamity, a Childhood of Martha Jane Cannary", "Rémi Chayé"),
    2019: ("I Lost My Body", "Jérémy Clapin"),
    2018: ("Mirai", "Mamoru Hosoda"),
    2017: ("The Breadwinner", "Nora Twomey"),
    2016: ("The Red Turtle", "Michaël Dudok de Wit"),
    2015: ("April and the Extraordinary World", "Christian Desmares"),
    2014: ("Boy and the World", "Alê Abreu"),
    2013: ("Ernest & Celestine", "Stéphane Aubier"),
    2012: ("A Cat in Paris", "Jean-Loup Felicioli"),
    2011: ("A Monster in Paris", "Bibo Bergeron"),
    2010: ("The Illusionist", "Sylvain Chomet"),
    2009: ("Mary and Max", "Adam Elliot"),
    2008: ("Waltz with Bashir", "Ari Folman"),
    2007: ("Persepolis", "Marjane Satrapi"),
    2006: ("Renaissance", "Christian Volckman"),
    2005: ("Howl's Moving Castle", "Hayao Miyazaki"),
    2004: ("Ghost in the Shell 2: Innocence", "Mamoru Oshii"),
    2003: ("Belleville Rendez-vous", "Sylvain Chomet"),
    2002: ("Spirited Away", "Hayao Miyazaki"),
    2001: ("Shrek", "Andrew Adamson"),
    2000: ("Chicken Run", "Peter Lord"),
}


class AnnecyFetcher:
    """Fetches Annecy Cristal d'Or winners."""
    
    name = "Annecy Cristal d'Or"
    recognition_type = "Annecy Cristal d'Or"
    
    def fetch(self, min_year: int = 2000) -> list[MovieEntry]:
        """Fetch Annecy winners since min_year."""
        movies = []
        
        for year, (title, director) in ANNECY_WINNERS.items():
            if year < min_year:
                continue
            
            movies.append(MovieEntry(
                title=title,
                year=year,
                director=director,
                recognitions=[Recognition(
                    type="Annecy Cristal d'Or",
                    year=year,
                    details="Winner"
                )]
            ))
        
        print(f"  Added {len(movies)} Annecy winners")
        return movies


if __name__ == "__main__":
    print("Testing Annecy fetcher...")
    fetcher = AnnecyFetcher()
    movies = fetcher.fetch(min_year=2015)
    print(f"Found {len(movies)} movies")
    for m in movies:
        print(f"  {m.year} - {m.title} ({m.director})")
