#!/usr/bin/env python3
"""Music data pipeline - fetches and enriches album data."""
import argparse
import json
import os
import sys
from pathlib import Path

# Add parent directory to path for imports
sys.path.insert(0, str(Path(__file__).parent.parent))

from dotenv import load_dotenv
load_dotenv()

from music.fetchers.pitchfork import fetch_pitchfork_albums
from music.fetchers.classics import (
    fetch_jazz_classics,
    fetch_metal_essentials,
    fetch_electronic_classics,
    fetch_hiphop_classics,
    fetch_folk_classics,
)
from music.fetchers.critics import (
    fetch_mercury_prize,
    fetch_polaris_prize,
    fetch_experimental,
    fetch_underground,
    fetch_world_music,
)
from music.fetchers.expanded import fetch_rym_top_albums
from music.fetchers.genres import fetch_genre_essentials
from music.fetchers.curated import fetch_curated_albums
from music.enrichers.spotify import SpotifyEnricher


# Cache file for Spotify enrichment data
CACHE_PATH = Path(__file__).parent / ".spotify_cache.json"


# Track enrichment failures
_enrichment_failures: list[dict] = []


def add_failure(album: dict, reason: str) -> None:
    """Track an enrichment failure."""
    _enrichment_failures.append({
        "artist": album["artist"],
        "title": album["title"],
        "year": album["year"],
        "reason": reason,
    })


def get_failures() -> list[dict]:
    """Get all enrichment failures."""
    return _enrichment_failures


def clear_failures() -> None:
    """Clear all tracked failures."""
    _enrichment_failures.clear()


def print_failure_report() -> None:
    """Print a summary of enrichment failures."""
    failures = get_failures()
    if not failures:
        return
    
    print("\n" + "=" * 60)
    print(f"ENRICHMENT FAILURES: {len(failures)} albums")
    print("=" * 60)
    print("To fix these, check Spotify for correct album/artist names")
    print("-" * 60)
    
    for f in failures:
        print(f"{f['artist']} - {f['title']} ({f['year']})")
        print(f"  Reason: {f['reason']}")
    
    print("-" * 60)


def load_cache() -> dict:
    """Load the Spotify enrichment cache."""
    if CACHE_PATH.exists():
        try:
            with open(CACHE_PATH, "r", encoding="utf-8") as f:
                return json.load(f)
        except (json.JSONDecodeError, IOError):
            return {}
    return {}


def save_cache(cache: dict) -> None:
    """Save the Spotify enrichment cache."""
    with open(CACHE_PATH, "w", encoding="utf-8") as f:
        json.dump(cache, f, indent=2, ensure_ascii=False)


def get_cache_key(artist: str, title: str) -> str:
    """Create a cache key from artist and title."""
    return f"{artist.lower()}|{title.lower()}"


def merge_albums(albums: list[dict]) -> list[dict]:
    """Merge duplicate albums, combining their recognitions."""
    merged = {}
    
    for album in albums:
        # Create a key from artist + title (normalized)
        # Normalize title by removing spaces and special chars for comparison
        title_normalized = album['title'].lower().replace(' ', '').replace('(', '').replace(')', '')
        key = f"{album['artist'].lower()}|{title_normalized}"
        
        if key in merged:
            # Merge recognitions
            existing = merged[key]
            existing_types = {r["type"] for r in existing.get("recognitions", [])}
            for rec in album.get("recognitions", []):
                if rec["type"] not in existing_types:
                    existing.setdefault("recognitions", []).append(rec)
            # Keep higher rating
            if album.get("rating") and (not existing.get("rating") or album["rating"] > existing["rating"]):
                existing["rating"] = album["rating"]
        else:
            merged[key] = album.copy()
    
    return list(merged.values())


def create_album_id(artist: str, title: str, year: int) -> str:
    """Create a URL-friendly ID for an album."""
    import re
    combined = f"{title}-{artist}-{year}"
    # Remove special characters, replace spaces with hyphens
    slug = re.sub(r'[^\w\s-]', '', combined.lower())
    slug = re.sub(r'[-\s]+', '-', slug).strip('-')
    return slug


def enrich_with_spotify(albums: list[dict], skip_enrich: bool = False, force_refresh: bool = False) -> list[dict]:
    """Enrich albums with Spotify data. Uses cache to avoid redundant API calls."""
    if skip_enrich:
        print("Skipping Spotify enrichment...")
        return albums
    
    print("Enriching with Spotify data...")
    clear_failures()
    
    # Load existing cache
    cache = {} if force_refresh else load_cache()
    cache_hits = 0
    api_calls = 0
    
    enricher = SpotifyEnricher()
    enriched = []
    
    for i, album in enumerate(albums):
        cache_key = get_cache_key(album["artist"], album["title"])
        
        # Check cache first
        if cache_key in cache:
            cached = cache[cache_key]
            album["cover_url"] = cached.get("cover_url")
            album["spotify_url"] = cached.get("spotify_url")
            album["spotify_id"] = cached.get("spotify_id")
            album["genres"] = cached.get("genres", [])
            album["detailed_genres"] = cached.get("detailed_genres", [])
            album["label"] = cached.get("label")
            album["tracks"] = cached.get("tracks", [])
            cache_hits += 1
            enriched.append(album)
            continue
        
        # Not in cache - call API
        print(f"  [{i+1}/{len(albums)}] {album['artist']} - {album['title']}")
        api_calls += 1
        
        spotify_data = enricher.search_album(album["artist"], album["title"])
        
        if not spotify_data:
            add_failure(album, "Not found on Spotify")
            # Cache the miss too (with empty data) to avoid re-querying
            cache[cache_key] = {"not_found": True}
            enriched.append(album)
            continue
        
        album["cover_url"] = spotify_data.get("cover_url")
        album["spotify_url"] = spotify_data.get("spotify_url")
        album["spotify_id"] = spotify_data.get("spotify_id")
        
        # Get additional details
        if spotify_data.get("spotify_id"):
            details = enricher.get_album_details(spotify_data["spotify_id"])
            if details:
                album["genres"] = details.get("genres", [])
                album["detailed_genres"] = details.get("detailed_genres", [])
                album["label"] = details.get("label")
                album["tracks"] = details.get("tracks", [])
            else:
                add_failure(album, "Failed to get album details (rate limited?)")
        
        # Save to cache
        cache[cache_key] = {
            "cover_url": album.get("cover_url"),
            "spotify_url": album.get("spotify_url"),
            "spotify_id": album.get("spotify_id"),
            "genres": album.get("genres", []),
            "detailed_genres": album.get("detailed_genres", []),
            "label": album.get("label"),
            "tracks": album.get("tracks", []),
        }
        
        enriched.append(album)
    
    # Save updated cache
    save_cache(cache)
    print(f"  Cache: {cache_hits} hits, {api_calls} API calls")
    
    return enriched


def run_pipeline(skip_enrich: bool = False, limit: int = None, force_refresh: bool = False):
    """Run the full music pipeline."""
    print("=" * 50)
    print("Music Data Pipeline")
    print("=" * 50)
    
    # Fetch from all sources
    all_albums = []
    
    all_albums.extend(fetch_pitchfork_albums())
    
    # Genre-specific classics
    all_albums.extend(fetch_jazz_classics())
    all_albums.extend(fetch_metal_essentials())
    all_albums.extend(fetch_electronic_classics())
    all_albums.extend(fetch_hiphop_classics())
    all_albums.extend(fetch_folk_classics())
    
    # Quality critic sources
    all_albums.extend(fetch_mercury_prize())
    all_albums.extend(fetch_polaris_prize())
    all_albums.extend(fetch_experimental())
    all_albums.extend(fetch_underground())
    all_albums.extend(fetch_world_music())
    
    # RYM community picks (large collection)
    all_albums.extend(fetch_rym_top_albums())
    
    # Genre essentials across all styles
    all_albums.extend(fetch_genre_essentials())
    
    # Curated world albums (geographic quality picks)
    all_albums.extend(fetch_curated_albums())
    
    print(f"\nTotal albums fetched: {len(all_albums)}")
    
    # Merge duplicates
    albums = merge_albums(all_albums)
    print(f"After merging duplicates: {len(albums)}")
    
    # Apply limit if specified
    if limit:
        albums = albums[:limit]
        print(f"Limited to: {len(albums)} albums")
    
    # Add IDs
    for album in albums:
        album["id"] = create_album_id(album["artist"], album["title"], album["year"])
    
    # Enrich with Spotify
    albums = enrich_with_spotify(albums, skip_enrich, force_refresh)
    
    # Sort by year (newest first), then by rating
    albums.sort(key=lambda x: (-x.get("year", 0), -(x.get("rating") or 0)))
    
    # Get unique recognition types
    recognition_types = set()
    for album in albums:
        for rec in album.get("recognitions", []):
            recognition_types.add(rec["type"])
    
    # Count albums with genres
    albums_with_genres = sum(1 for a in albums if a.get("genres"))
    albums_with_covers = sum(1 for a in albums if a.get("cover_url"))
    
    # Build output
    output = {
        "albums": albums,
        "recognitionTypes": sorted(recognition_types),
    }
    
    # Write to file
    output_path = Path(__file__).parent.parent.parent / "src" / "data" / "albums.json"
    output_path.parent.mkdir(parents=True, exist_ok=True)
    
    with open(output_path, "w", encoding="utf-8") as f:
        json.dump(output, f, indent=2, ensure_ascii=False)
    
    print(f"\n✓ Wrote {len(albums)} albums to {output_path}")
    print(f"✓ Recognition types: {len(recognition_types)}")
    print(f"✓ Albums with covers: {albums_with_covers}/{len(albums)}")
    print(f"✓ Albums with genres: {albums_with_genres}/{len(albums)}")
    
    if albums_with_genres < len(albums) * 0.5:
        print(f"\n⚠ Warning: Less than 50% of albums have genres. Spotify API may have been rate limited.", file=sys.stderr)


if __name__ == "__main__":
    parser = argparse.ArgumentParser(description="Music data pipeline")
    parser.add_argument("--skip-enrich", action="store_true", help="Skip Spotify enrichment")
    parser.add_argument("--force-refresh", action="store_true", help="Ignore cache, re-fetch all from Spotify")
    parser.add_argument("--limit", type=int, help="Limit number of albums to process")
    args = parser.parse_args()
    
    run_pipeline(skip_enrich=args.skip_enrich, limit=args.limit, force_refresh=args.force_refresh)
