"""
Top Directors fetcher.
Fetches filmographies of acclaimed art-house directors from TMDB.
"""

import os
import time
import requests
from dotenv import load_dotenv

import sys
sys.path.insert(0, str(__file__).rsplit("/", 4)[0])

from catalog import MovieEntry, Recognition

load_dotenv()

TMDB_API_KEY = os.getenv("TMDB_API_KEY")

# Top 40+ art-house directors (active since 2000)
# Curated list focusing on critically acclaimed auteurs
# TMDB person IDs verified via API search
TOP_DIRECTORS = [
    # European masters
    ("Michael Haneke", 6011),        # Caché, Amour, The White Ribbon
    ("Pedro Almodóvar", 309),        # Talk to Her, Volver, Pain and Glory
    ("Lars von Trier", 42),          # Melancholia, Dancer in the Dark
    ("Claire Denis", 9888),          # Beau Travail, High Life
    ("Cristian Mungiu", 20657),      # 4 Months 3 Weeks, Graduation
    ("Paolo Sorrentino", 56194),     # The Great Beauty, Youth
    ("Ruben Östlund", 56370),        # The Square, Triangle of Sadness
    ("Andrey Zvyagintsev", 68519),   # Leviathan, Loveless
    ("Nuri Bilge Ceylan", 56214),    # Winter Sleep, Once Upon a Time in Anatolia
    ("Asghar Farhadi", 229931),      # A Separation, The Salesman
    ("Jacques Audiard", 2294),       # A Prophet, Dheepan
    ("Olivier Assayas", 21678),      # Personal Shopper, Summer Hours
    ("Mia Hansen-Løve", 222686),     # Things to Come, Bergman Island
    ("Luca Guadagnino", 78160),      # Call Me by Your Name, Suspiria
    ("Pawel Pawlikowski", 64194),    # Ida, Cold War
    
    # Asian masters
    ("Wong Kar-wai", 12453),         # In the Mood for Love, 2046
    ("Park Chan-wook", 10099),       # Oldboy, The Handmaiden
    ("Bong Joon-ho", 21684),         # Parasite, Memories of Murder
    ("Hirokazu Kore-eda", 25645),    # Shoplifters, Nobody Knows
    ("Apichatpong Weerasethakul", 69759),  # Uncle Boonmee, Memoria
    ("Jia Zhangke", 24011),          # A Touch of Sin, Mountains May Depart
    ("Lee Chang-dong", 21683),       # Burning, Poetry
    ("Naomi Kawase", 20658),         # Still the Water, True Mothers
    ("Hou Hsiao-hsien", 54697),      # The Assassin, Flight of the Red Balloon
    ("Tsai Ming-liang", 71174),      # Stray Dogs, What Time Is It There?
    ("Hong Sang-soo", 150975),       # Right Now, Wrong Then, The Woman Who Ran
    
    # American independents
    ("Paul Thomas Anderson", 4762),  # There Will Be Blood, Phantom Thread
    ("Terrence Malick", 30715),      # The Tree of Life, The New World
    ("Kelly Reichardt", 56383),      # First Cow, Certain Women
    ("David Lynch", 5602),           # Mulholland Drive, Inland Empire
    ("Wes Anderson", 5655),          # Grand Budapest Hotel, Moonrise Kingdom
    ("Noah Baumbach", 5656),         # Marriage Story, The Squid and the Whale
    ("Sofia Coppola", 1769),         # Lost in Translation, The Beguiled
    ("Jim Jarmusch", 4429),          # Paterson, Only Lovers Left Alive
    ("Richard Linklater", 564),      # Boyhood, Before Midnight
    ("Sean Baker", 118415),          # The Florida Project, Tangerine
    
    # Contemporary auteurs
    ("Yorgos Lanthimos", 122423),    # The Favourite, Poor Things
    ("Denis Villeneuve", 137427),    # Arrival, Sicario
    ("Céline Sciamma", 68813),       # Portrait of a Lady on Fire
    ("Barry Jenkins", 136495),       # Moonlight, If Beale Street Could Talk
    ("Ryusuke Hamaguchi", 1487492),  # Drive My Car, Wheel of Fortune
    
    # Animation masters
    ("Hayao Miyazaki", 608),         # Spirited Away, The Wind Rises, The Boy and the Heron
    ("Makoto Shinkai", 74091),       # Your Name, Weathering with You, Suzume
    ("Mamoru Hosoda", 81718),        # Wolf Children, Mirai, Belle
    ("Isao Takahata", 628),          # Grave of the Fireflies, The Tale of Princess Kaguya
    ("Satoshi Kon", 40333),          # Perfect Blue, Paprika, Tokyo Godfathers
    ("Masaaki Yuasa", 93107),        # Mind Game, Ride Your Wave
    ("Sylvain Chomet", 21768),       # Belleville Rendez-vous, The Illusionist
    ("Tomm Moore", 96676),           # The Secret of Kells, Wolfwalkers
]


class DirectorsFetcher:
    """Fetches filmographies of top art-house directors."""
    
    name = "Top Directors"
    recognition_type = None  # Directors don't add a recognition type
    
    def fetch(self, min_year: int = 2000) -> list[MovieEntry]:
        """Fetch films from top directors since min_year."""
        if not TMDB_API_KEY:
            print("  Warning: TMDB_API_KEY not set, skipping directors fetch")
            return []
        
        movies = []
        
        for director_name, tmdb_id in TOP_DIRECTORS:
            try:
                director_movies = self._fetch_director(director_name, tmdb_id, min_year)
                movies.extend(director_movies)
                print(f"  {director_name}: {len(director_movies)} films")
                time.sleep(0.25)  # Rate limiting
            except Exception as e:
                print(f"  {director_name}: Error - {e}")
        
        return movies
    
    def _fetch_director(self, name: str, tmdb_id: int, min_year: int) -> list[MovieEntry]:
        """Fetch films directed by a specific person."""
        url = f"https://api.themoviedb.org/3/person/{tmdb_id}/movie_credits"
        params = {"api_key": TMDB_API_KEY}
        
        response = requests.get(url, params=params, timeout=30)
        response.raise_for_status()
        data = response.json()
        
        movies = []
        
        for credit in data.get("crew", []):
            # Only include films they directed
            if credit.get("job") != "Director":
                continue
            
            title = credit.get("title", "")
            release_date = credit.get("release_date", "")
            
            if not title or not release_date:
                continue
            
            try:
                year = int(release_date[:4])
            except (ValueError, IndexError):
                continue
            
            if year < min_year:
                continue
            
            # Skip very minor works (shorts, music videos, etc.)
            vote_count = credit.get("vote_count", 0)
            if vote_count < 20:
                continue
            
            movies.append(MovieEntry(
                title=title,
                year=year,
                director=name,
                recognitions=[]  # No specific recognition, just notable director
            ))
        
        return movies


if __name__ == "__main__":
    print("Testing Directors fetcher...")
    fetcher = DirectorsFetcher()
    movies = fetcher.fetch(min_year=2015)
    print(f"\nTotal: {len(movies)} movies")
    for m in movies[:20]:
        print(f"  {m.year} - {m.title} ({m.director})")
