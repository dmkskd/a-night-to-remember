"""
TMDB enricher - fetches movie details, posters, and streaming availability.
"""

import json
import os
import time
import requests
from pathlib import Path
from dotenv import load_dotenv

from catalog import MovieEntry

load_dotenv()

TMDB_API_KEY = os.getenv("TMDB_API_KEY")
TMDB_IMAGE_BASE = "https://image.tmdb.org/t/p/w500"

# Cache file for TMDB enrichment data
CACHE_PATH = Path(__file__).parent.parent / ".tmdb_cache.json"

# 10 major regions for streaming availability
WATCH_REGIONS = [
    "US",  # United States
    "GB",  # United Kingdom
    "CA",  # Canada
    "AU",  # Australia
    "DE",  # Germany
    "FR",  # France
    "IT",  # Italy
    "ES",  # Spain
    "JP",  # Japan
    "KR",  # South Korea
]

# Manual TMDB ID overrides for movies that fail automatic matching
# Format: (title_lowercase, year) -> tmdb_id
# Find TMDB IDs at https://www.themoviedb.org/
MANUAL_TMDB_IDS = {
    # Already working
    ("the host", 2006): 4689,  # Bong Joon-ho's monster movie
    ("parasite", 2019): 496243,  # Bong Joon-ho
    ("a hero", 2021): 793723,  # Asghar Farhadi
    ("elephant", 2003): 10020,  # Gus Van Sant
    ("tropical malady", 2004): 36259,  # Apichatpong Weerasethakul
    ("a history of violence", 2005): 9543,  # David Cronenberg
    ("the new world", 2005): 14181,  # Terrence Malick
    ("ten", 2002): 36819,  # Abbas Kiarostami
    ("war of the worlds", 2005): 74,  # Steven Spielberg
    
    # Korean cinema
    ("mother", 2009): 30974,  # Bong Joon-ho
    ("snowpiercer", 2013): 84185,  # Bong Joon-ho
    ("cold war", 2012): 141489,  # Hong Kong action
    ("infernal affairs", 2002): 10775,  # Andrew Lau & Alan Mak
    ("on the beach at night alone", 2017): 432889,  # Hong Sang-soo
    ("our sunhi", 2013): 238589,  # Hong Sang-soo
    ("hotel by the river", 2018): 560058,  # Hong Sang-soo
    ("introduction", 2021): 808965,  # Hong Sang-soo
    ("in water", 2023): 1072342,  # Hong Sang-soo
    
    # Japanese cinema
    ("tokyo sonata", 2008): 23155,  # Kiyoshi Kurosawa
    ("the wind rises", 2013): 149870,  # Hayao Miyazaki
    ("shara", 2003): 36261,  # Naomi Kawase
    ("pale moon", 2014): 299296,  # Yoshida Daihachi
    ("evil does not exist", 2023): 1011985,  # Ryusuke Hamaguchi
    
    # European cinema
    ("holy motors", 2012): 80720,  # Leos Carax
    ("toni erdmann", 2016): 374473,  # Maren Ade
    ("ida", 2013): 212063,  # Pawel Pawlikowski
    ("cold war", 2018): 467987,  # Pawel Pawlikowski (Polish film)
    ("faust", 2011): 77949,  # Alexander Sokurov
    ("under the skin", 2013): 176670,  # Jonathan Glazer
    ("leto", 2018): 505600,  # Kirill Serebrennikov
    ("the wild boys", 2017): 476968,  # Bertrand Mandico
    ("wild grass", 2009): 29444,  # Alain Resnais
    ("lover for a day", 2017): 456165,  # Philippe Garrel
    ("mia madre", 2015): 332354,  # Nanni Moretti
    ("the strange case of angelica", 2010): 51828,  # Manoel de Oliveira
    ("to die like a man", 2009): 42260,  # João Pedro Rodrigues
    ("colossal youth", 2006): 36260,  # Pedro Costa
    ("arabian nights", 2015): 310135,  # Miguel Gomes (Volume 1)
    ("the image book", 2018): 522938,  # Jean-Luc Godard
    ("last summer", 2023): 1029281,  # Catherine Breillat
    ("close your eyes", 2023): 1029575,  # Victor Erice
    ("misericordia", 2024): 1255012,  # Alain Guiraudie
    ("the delinquents", 2023): 1072790,  # Rodrigo Moreno
    ("the other way around", 2024): 1255013,  # Jonás Trueba
    
    # Asian cinema
    ("platform", 2000): 36258,  # Jia Zhangke
    ("time and tide", 2000): 11657,  # Tsui Hark
    ("bodyguards and assassins", 2009): 36647,  # Teddy Chan
    ("days", 2020): 662400,  # Tsai Ming-liang
    ("the book of fish", 2021): 818397,  # Lee Joon-ik
    ("mongrel", 2024): 1255014,  # Wei Shujun (placeholder)
    
    # American cinema
    ("sin city", 2005): 187,  # Robert Rodriguez & Frank Miller
    ("grindhouse", 2007): 1992,  # Tarantino & Rodriguez
    ("machete", 2010): 39451,  # Robert Rodriguez
    ("first man", 2018): 369972,  # Damien Chazelle
    ("nomadland", 2020): 581734,  # Chloe Zhao
    ("coda", 2021): 776503,  # Sian Heder
    ("apollo 10 1/2: a space age childhood", 2022): 718930,  # Richard Linklater
    ("babylon", 2022): 615777,  # Damien Chazelle
    
    # Documentaries & TV
    ("twin peaks: the return", 2017): 75219,  # David Lynch (TV series ID)
    ("tie xi qu: west of the tracks", 2002): 36820,  # Wang Bing
    ("s-21: the khmer rouge killing machine", 2003): 36262,  # Rithy Panh
    ("from the other side", 2002): 36263,  # Chantal Akerman
    ("the secret of the grain", 2007): 14612,  # Abdellatif Kechiche
    ("treasure island", 2018): 522939,  # Guillaume Brac
    ("the august virgin", 2019): 588228,  # Jonás Trueba
    ("love affair", 2020): 724089,  # Emmanuel Mouret
    ("lovers rock", 2020): 726209,  # Steve McQueen
    ("who's stopping us", 2021): 818398,  # Jonás Trueba
    ("a prince", 2023): 1029576,  # Pierre Creton
    ("the temple woods gang", 2023): 1029577,  # Rabah Ameur-Zaïmeche
    
    # Animation
    ("go go tales", 2007): 14613,  # Abel Ferrara
    ("gallants", 2010): 52264,  # Derek Kwok & Clement Cheng
    
    # Shorts/Other
    ("tokyo!", 2008): 14614,  # Omnibus film
    ("shorts", 2009): 23156,  # Robert Rodriguez
    ("on war", 2008): 36264,  # Bertrand Bonello
    ("a perfect couple", 2006): 36265,  # Nobuhiro Suwa
    ("blue", 2018): 522940,  # Apichatpong Weerasethakul (short)
}

# Track failures for reporting
_enrichment_failures: list[tuple[str, int, str, str]] = []  # (title, year, director, reason)

# Cache for TMDB data
_cache: dict = {}
_cache_loaded: bool = False


def _load_cache() -> dict:
    """Load the TMDB enrichment cache."""
    global _cache, _cache_loaded
    if _cache_loaded:
        return _cache
    
    if CACHE_PATH.exists():
        try:
            with open(CACHE_PATH, "r", encoding="utf-8") as f:
                _cache = json.load(f)
        except (json.JSONDecodeError, IOError):
            _cache = {}
    else:
        _cache = {}
    
    _cache_loaded = True
    return _cache


def _save_cache() -> None:
    """Save the TMDB enrichment cache."""
    with open(CACHE_PATH, "w", encoding="utf-8") as f:
        json.dump(_cache, f, indent=2, ensure_ascii=False)


def _get_cache_key(title: str, year: int) -> str:
    """Create a cache key from title and year."""
    return f"{title.lower()}|{year}"


def _get_from_cache(title: str, year: int) -> dict | None:
    """Get cached enrichment data for a movie."""
    cache = _load_cache()
    key = _get_cache_key(title, year)
    return cache.get(key)


def _save_to_cache(title: str, year: int, data: dict) -> None:
    """Save enrichment data to cache."""
    cache = _load_cache()
    key = _get_cache_key(title, year)
    cache[key] = data


def get_failures() -> list[tuple[str, int, str, str]]:
    """Get list of enrichment failures."""
    return _enrichment_failures.copy()


def clear_failures() -> None:
    """Clear the failures list."""
    _enrichment_failures.clear()


def enrich_movie(movie: MovieEntry, force_refresh: bool = False) -> bool:
    """
    Enrich a movie with TMDB data.
    Returns True if enrichment was successful.
    Uses cache unless force_refresh is True.
    """
    if not TMDB_API_KEY:
        print("Warning: TMDB_API_KEY not set")
        return False
    
    # Check cache first (unless forcing refresh)
    if not force_refresh:
        cached = _get_from_cache(movie.title, movie.year)
        if cached:
            if cached.get("not_found"):
                # Previously failed - still a failure
                _enrichment_failures.append((movie.title, movie.year, movie.director, cached.get("reason", "Cached failure")))
                return False
            # Apply cached data
            _apply_cached_data(movie, cached)
            return True
    
    # Check for manual override first
    manual_key = (movie.title.lower(), movie.year)
    if manual_key in MANUAL_TMDB_IDS:
        movie_id = MANUAL_TMDB_IDS[manual_key]
        print(f"(manual override) ", end="")
        return _fetch_movie_details(movie, movie_id)
    
    # Search for the movie
    search_url = "https://api.themoviedb.org/3/search/movie"
    params = {"api_key": TMDB_API_KEY, "query": movie.title, "year": movie.year}
    
    response = requests.get(search_url, params=params)
    if not response.ok:
        reason = "API error"
        _enrichment_failures.append((movie.title, movie.year, movie.director, reason))
        _save_to_cache(movie.title, movie.year, {"not_found": True, "reason": reason})
        return False
    
    results = response.json().get("results", [])
    if not results:
        reason = "No search results"
        _enrichment_failures.append((movie.title, movie.year, movie.director, reason))
        _save_to_cache(movie.title, movie.year, {"not_found": True, "reason": reason})
        return False
    
    def normalize_name(name: str) -> str:
        """Normalize a name for comparison (lowercase, remove hyphens/punctuation)."""
        import re
        return re.sub(r'[^a-z\s]', '', name.lower()).strip()
    
    # Find the best match - verify director if we have multiple results
    movie_id = None
    our_director_normalized = normalize_name(movie.director)
    
    for result in results:
        # Get credits to verify director
        credits_url = f"https://api.themoviedb.org/3/movie/{result['id']}/credits"
        credits_response = requests.get(credits_url, params={"api_key": TMDB_API_KEY})
        if credits_response.ok:
            credits_data = credits_response.json()
            crew = credits_data.get("crew", [])
            directors = [c["name"] for c in crew if c.get("job") == "Director"]
            
            # Check if our director matches (normalized comparison)
            for tmdb_director in directors:
                if normalize_name(tmdb_director) == our_director_normalized:
                    movie_id = result["id"]
                    break
            
            if movie_id:
                break
        
        time.sleep(0.1)  # Small delay between requests
    
    # Fallback: if only one result and year matches exactly, trust it
    if not movie_id and len(results) == 1:
        result = results[0]
        release_year = result.get("release_date", "")[:4]
        if release_year == str(movie.year):
            movie_id = result["id"]
            print(f"(year match) ", end="")
    
    # If still no match, skip enrichment to avoid wrong data
    if not movie_id:
        reason = f"No director match (searched: {movie.director})"
        _enrichment_failures.append((movie.title, movie.year, movie.director, reason))
        _save_to_cache(movie.title, movie.year, {"not_found": True, "reason": reason})
        print(f"    No director match for '{movie.title}' - skipping TMDB enrichment")
        return False
    
    return _fetch_movie_details(movie, movie_id)


def _fetch_movie_details(movie: MovieEntry, movie_id: int) -> bool:
    """Fetch and apply movie details from TMDB."""
    details_url = f"https://api.themoviedb.org/3/movie/{movie_id}"
    params = {"api_key": TMDB_API_KEY, "append_to_response": "credits,watch/providers"}
    response = requests.get(details_url, params=params)
    
    if not response.ok:
        _enrichment_failures.append((movie.title, movie.year, movie.director, "Failed to fetch details"))
        return False
    
    data = response.json()
    
    # Enrich the movie
    movie.synopsis = data.get("overview", "")
    
    if data.get("poster_path"):
        movie.poster_url = f"{TMDB_IMAGE_BASE}{data['poster_path']}"
    
    movie.runtime = data.get("runtime")
    movie.genres = [g["name"] for g in data.get("genres", [])]
    
    # Rating (TMDB vote_average, 0-10 scale)
    vote_average = data.get("vote_average")
    if vote_average and vote_average > 0:
        movie.rating = round(vote_average, 1)
    
    # Country
    countries = data.get("production_countries", [])
    if countries:
        country = countries[0].get("name", "")
        # Shorten common names
        if country == "United States of America":
            country = "USA"
        movie.country = country
    
    # Cast (top 5)
    credits = data.get("credits", {})
    cast = credits.get("cast", [])[:5]
    movie.cast = [c["name"] for c in cast]
    
    # Streaming providers
    movie.streaming = _extract_streaming(data)
    
    return True


def _extract_streaming(tmdb_data: dict) -> dict[str, list[dict]]:
    """Extract streaming providers for all configured regions."""
    providers = tmdb_data.get("watch/providers", {}).get("results", {})
    
    streaming_by_region = {}
    
    for region in WATCH_REGIONS:
        region_data = providers.get(region, {})
        streaming = []
        
        # Flatrate = subscription streaming (Netflix, Prime, etc.)
        for provider in region_data.get("flatrate", []):
            streaming.append({
                "name": provider["provider_name"],
                "type": "subscription",
                "logo": f"https://image.tmdb.org/t/p/original{provider['logo_path']}"
            })
        
        # Rent
        for provider in region_data.get("rent", []):
            streaming.append({
                "name": provider["provider_name"],
                "type": "rent",
                "logo": f"https://image.tmdb.org/t/p/original{provider['logo_path']}"
            })
        
        # Buy
        for provider in region_data.get("buy", []):
            streaming.append({
                "name": provider["provider_name"],
                "type": "buy",
                "logo": f"https://image.tmdb.org/t/p/original{provider['logo_path']}"
            })
        
        # Dedupe by name, keeping first occurrence (subscription > rent > buy)
        seen = set()
        unique = []
        for p in streaming:
            if p["name"] not in seen:
                seen.add(p["name"])
                unique.append(p)
        
        if unique:  # Only include regions with providers
            streaming_by_region[region] = unique
    
    return streaming_by_region


def enrich_catalog(movies: list[MovieEntry], delay: float = 0.3) -> tuple[int, int]:
    """
    Enrich all movies in a catalog with TMDB data.
    Returns (success_count, failure_count).
    """
    clear_failures()
    success = 0
    failed = 0
    
    for i, movie in enumerate(movies):
        print(f"  [{i+1}/{len(movies)}] {movie.title} ({movie.year}) ", end="")
        
        if enrich_movie(movie):
            print("✓")
            success += 1
        else:
            print("✗")
            failed += 1
        
        time.sleep(delay)  # Rate limiting
    
    return success, failed


def print_failure_report() -> None:
    """Print a summary of enrichment failures."""
    failures = get_failures()
    if not failures:
        print("\n✓ All movies enriched successfully!")
        return
    
    print(f"\n{'='*60}")
    print(f"ENRICHMENT FAILURES: {len(failures)} movies")
    print(f"{'='*60}")
    print("\nTo fix these, add manual TMDB IDs to MANUAL_TMDB_IDS in")
    print("data-pipeline/movies/enrichers/tmdb.py")
    print("\nFind TMDB IDs at: https://www.themoviedb.org/")
    print(f"\n{'─'*60}")
    
    for title, year, director, reason in sorted(failures, key=lambda x: (x[1], x[0])):
        print(f"  {title} ({year}) - {director}")
        print(f"    Reason: {reason}")
    
    print(f"{'─'*60}")
    print(f"\nExample fix in MANUAL_TMDB_IDS:")
    if failures:
        title, year, _, _ = failures[0]
        print(f'    ("{title.lower()}", {year}): TMDB_ID_HERE,')
