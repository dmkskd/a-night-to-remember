#!/usr/bin/env python3
"""
Pipeline orchestrator - runs fetchers, deduplicates, enriches, and exports.

Usage:
    uv run python pipeline.py
    uv run python pipeline.py --skip-enrich  # Skip TMDB enrichment
    uv run python pipeline.py --dry-run      # Don't write output
"""

import argparse
import json
from pathlib import Path

from catalog import Catalog
from fetchers import (
    Fetcher,
    # Festivals
    CannesWikidataFetcher,
    CannesGrandPrixFetcher,
    CannesBestDirectorFetcher,
    CannesJuryPrizeFetcher,
    BerlinWikidataFetcher,
    VeniceWikidataFetcher,
    HongKongWikidataFetcher,
    TorontoFetcher,
    SundanceFetcher,
    TokyoFetcher,
    BusanFetcher,
    AnnecyFetcher,
    # Critics
    SightAndSoundFetcher,
    FilmCommentFetcher,
    KinemaJunpoFetcher,
    CahiersFetcher,
    IndiewireFetcher,
    CinemaScopeFetcher,
    GermanCriticsFetcher,
    FotogramasFetcher,
    KoreanCriticsFetcher,
    # Other
    DirectorsFetcher,
)
from enrichers import tmdb

OUTPUT_PATH = Path(__file__).parent.parent / "src" / "data" / "movies.json"


def get_recognition_types(fetchers: list[Fetcher]) -> list[str]:
    """Collect recognition types from all fetchers."""
    types = []
    for fetcher in fetchers:
        # Check for multiple types first
        if hasattr(fetcher, 'recognition_types') and fetcher.recognition_types:
            for t in fetcher.recognition_types:
                if t not in types:
                    types.append(t)
        # Then single type
        elif hasattr(fetcher, 'recognition_type') and fetcher.recognition_type:
            if fetcher.recognition_type not in types:
                types.append(fetcher.recognition_type)
    return types

# All available fetchers
FETCHERS: list[Fetcher] = [
    # === FESTIVALS ===
    # Cannes (multiple awards)
    CannesWikidataFetcher(),
    CannesGrandPrixFetcher(),
    CannesBestDirectorFetcher(),
    CannesJuryPrizeFetcher(),
    # Other Big 5 festivals
    BerlinWikidataFetcher(),
    VeniceWikidataFetcher(),
    TorontoFetcher(),
    SundanceFetcher(),
    # Far East festivals
    HongKongWikidataFetcher(),
    TokyoFetcher(),
    BusanFetcher(),
    # Animation
    AnnecyFetcher(),
    
    # === CRITICS ===
    # UK
    SightAndSoundFetcher(),
    # US
    FilmCommentFetcher(),
    IndiewireFetcher(),
    # Canada
    CinemaScopeFetcher(),
    # France
    CahiersFetcher(),
    # Japan
    KinemaJunpoFetcher(),
    # Germany
    GermanCriticsFetcher(),
    # Spain
    FotogramasFetcher(),
    # Korea
    KoreanCriticsFetcher(),
    
    # === OTHER ===
    DirectorsFetcher(),
]


def run_fetchers(catalog: Catalog, fetchers: list[Fetcher], min_year: int = 2005) -> None:
    """Run all fetchers and add movies to catalog."""
    
    for fetcher in fetchers:
        print(f"\nFetching {fetcher.name}...")
        try:
            movies = fetcher.fetch(min_year=min_year)
            added = 0
            merged = 0
            for movie in movies:
                existing = catalog.get(movie.title, movie.year)
                catalog.add(movie)
                if existing:
                    merged += 1
                else:
                    added += 1
            print(f"  Added {added} new, merged {merged} existing")
        except Exception as e:
            print(f"  Error: {e}")


def export_catalog(catalog: Catalog, path: Path, recognition_types: list[str]) -> None:
    """Export catalog to JSON file with normalized streaming providers."""
    
    # Build provider lookup table
    providers: dict[str, dict] = {}
    provider_id_map: dict[str, str] = {}  # name -> id
    
    for movie in catalog:
        if movie.streaming:
            for region, region_providers in movie.streaming.items():
                for provider in region_providers:
                    name = provider["name"]
                    if name not in provider_id_map:
                        # Create short ID from name
                        pid = name.lower().replace(" ", "-").replace("'", "")
                        # Handle duplicates
                        base_pid = pid
                        counter = 1
                        while pid in providers:
                            pid = f"{base_pid}-{counter}"
                            counter += 1
                        provider_id_map[name] = pid
                        providers[pid] = {
                            "name": name,
                            "logo": provider["logo"]
                        }
    
    # Convert movies with normalized streaming
    movies_data = []
    for movie in catalog:
        data = movie.to_dict()
        
        # Normalize streaming to use provider IDs
        if movie.streaming:
            normalized_streaming = {}
            for region, region_providers in movie.streaming.items():
                normalized_streaming[region] = [
                    {
                        "id": provider_id_map[p["name"]],
                        "type": p["type"]
                    }
                    for p in region_providers
                ]
            data["streaming"] = normalized_streaming
        
        movies_data.append(data)
    
    output = {
        "movies": movies_data,
        "recognitionTypes": recognition_types,
        "providers": providers,
    }
    
    with open(path, "w") as f:
        json.dump(output, f, indent=2)


def main():
    parser = argparse.ArgumentParser(description="Build movie catalog")
    parser.add_argument("--min-year", type=int, default=2000, help="Minimum year")
    parser.add_argument("--skip-enrich", action="store_true", help="Skip TMDB enrichment")
    parser.add_argument("--dry-run", action="store_true", help="Don't write output")
    parser.add_argument("--limit", type=int, default=0, help="Limit number of movies (0 = no limit)")
    args = parser.parse_args()
    
    catalog = Catalog()
    
    # Step 1: Fetch from all sources
    print("=" * 50)
    print("STEP 1: Fetching from sources")
    print("=" * 50)
    run_fetchers(catalog, FETCHERS, min_year=args.min_year)
    
    print(f"\nTotal unique movies: {len(catalog)}")
    
    # Apply limit if specified
    if args.limit > 0:
        movies_list = catalog.all()[:args.limit]
        catalog = Catalog()
        for movie in movies_list:
            catalog.add(movie)
        print(f"Limited to {len(catalog)} movies")
    
    # Step 2: Enrich with TMDB
    if not args.skip_enrich:
        print("\n" + "=" * 50)
        print("STEP 2: Enriching with TMDB")
        print("=" * 50)
        tmdb.enrich_catalog(list(catalog))
    
    # Step 3: Export
    if not args.dry_run:
        print("\n" + "=" * 50)
        print("STEP 3: Exporting")
        print("=" * 50)
        recognition_types = get_recognition_types(FETCHERS)
        export_catalog(catalog, OUTPUT_PATH, recognition_types)
        print(f"Wrote {len(catalog)} movies to {OUTPUT_PATH}")
        print(f"Recognition types: {len(recognition_types)}")
    else:
        print(f"\n[Dry run] Would write {len(catalog)} movies")


if __name__ == "__main__":
    main()
