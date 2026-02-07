"""
TMDB enricher - fetches movie details, posters, and streaming availability.
"""

import os
import time
import requests
from dotenv import load_dotenv

from catalog import MovieEntry

load_dotenv()

TMDB_API_KEY = os.getenv("TMDB_API_KEY")
TMDB_IMAGE_BASE = "https://image.tmdb.org/t/p/w500"

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


def enrich_movie(movie: MovieEntry) -> bool:
    """
    Enrich a movie with TMDB data.
    Returns True if enrichment was successful.
    """
    if not TMDB_API_KEY:
        print("Warning: TMDB_API_KEY not set")
        return False
    
    # Search for the movie
    search_url = "https://api.themoviedb.org/3/search/movie"
    params = {"api_key": TMDB_API_KEY, "query": movie.title, "year": movie.year}
    
    response = requests.get(search_url, params=params)
    if not response.ok:
        return False
    
    results = response.json().get("results", [])
    if not results:
        return False
    
    movie_id = results[0]["id"]
    
    # Fetch full details with credits and watch providers
    details_url = f"https://api.themoviedb.org/3/movie/{movie_id}"
    params = {"api_key": TMDB_API_KEY, "append_to_response": "credits,watch/providers"}
    response = requests.get(details_url, params=params)
    
    if not response.ok:
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


def enrich_catalog(movies: list[MovieEntry], delay: float = 0.3) -> None:
    """Enrich all movies in a catalog with TMDB data."""
    for i, movie in enumerate(movies):
        print(f"  [{i+1}/{len(movies)}] {movie.title} ({movie.year})", end=" ")
        
        if enrich_movie(movie):
            print("✓")
        else:
            print("✗")
        
        time.sleep(delay)  # Rate limiting
