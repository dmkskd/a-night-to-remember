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

OUTPUT_PATH = Path(__file__).parent.parent.parent / "src" / "data" / "movies.json"

# Known director name corrections (bad_name -> correct_name)
DIRECTOR_CORRECTIONS = {
    "괴물": "Bong Joon-ho",  # Korean title of "The Host" incorrectly parsed as director
    "기생충": "Bong Joon-ho",  # Korean title of "Parasite"
    "마더": "Bong Joon-ho",  # Korean title of "Mother"
    "ده": "Abbas Kiarostami",  # Persian title of "Ten"
    "站台": "Jia Zhangke",  # Chinese title of "Platform"
    "順流逆流": "Tsui Hark",  # Chinese title of "Time and Tide"
    "沙羅双樹": "Naomi Kawase",  # Japanese title of "Shara"
    "トウキョウソナタ": "Kiyoshi Kurosawa",  # Japanese title of "Tokyo Sonata"
    "風立ちぬ": "Hayao Miyazaki",  # Japanese title of "The Wind Rises"
    "우리 선희": "Hong Sang-soo",  # Korean title of "Our Sunhi"
    "밤의 해변에서 혼자": "Hong Sang-soo",  # Korean title of "On the Beach at Night Alone"
    "강변 호텔": "Hong Sang-soo",  # Korean title of "Hotel by the River"
    "인트로덕션": "Hong Sang-soo",  # Korean title of "Introduction"
    "물안에서": "Hong Sang-soo",  # Korean title of "In Water"
    "悪は存在しない": "Ryusuke Hamaguchi",  # Japanese title of "Evil Does Not Exist"
    "Лето": "Kirill Serebrennikov",  # Russian title of "Leto"
    "כן!": "Nir Bergman",  # Hebrew title of "Yes!"
    # French titles incorrectly parsed as directors
    "De l'autre côté": "Chantal Akerman",
    "La graine et le mulet": "Abdellatif Kechiche",
    "S-21, la machine de mort Khmère rouge": "Rithy Panh",
    "Un couple parfait": "Nobuhiro Suwa",
    "Juventude em Marcha": "Pedro Costa",
    "De la guerre": "Bertrand Bonello",
    "Les Herbes folles": "Alain Resnais",
    "Morrer Como Um Homem": "João Pedro Rodrigues",
    "Le Livre d'image": "Jean-Luc Godard",
    "P'tit Quinquin": "Bruno Dumont",
    "O Estranho Caso de Angélica": "Manoel de Oliveira",
    "As Mil e uma Noites": "Miguel Gomes",
    "L'Amant d'un jour": "Philippe Garrel",
    "Coincoin et les z'inhumains": "Bruno Dumont",
    "les garçons sauvages": "Bertrand Mandico",
    "L'île au trésor": "Guillaume Brac",
    "Les Choses qu'on dit, les choses qu'on fait": "Emmanuel Mouret",
    "La virgen de agosto": "Jonás Trueba",
    "Quién lo impide": "Jonás Trueba",
    "Un prince": "Pierre Creton",
    "Cerrar los ojos": "Victor Erice",
    "L'Été dernier": "Catherine Breillat",
    "Le Gang des bois du temple": "Rabah Ameur-Zaïmeche",
    "Miséricorde": "Alain Guiraudie",
    "Los delincuentes": "Rodrigo Moreno",
    "Volveréis": "Jonás Trueba",
    "สัตว์ประหลาด": "Apichatpong Weerasethakul",  # Thai title of "Tropical Malady"
    "铁西区": "Wang Bing",  # Chinese title of "Tie Xi Qu"
    "Shuga": "Darezhan Omirbayev",  # Kazakh film
}

# Known bad entries to skip (title_lower, year) - usually wrong year from scraping
SKIP_ENTRIES = {
    ("the host", 2000),  # Wrong year - actual film is 2006
    ("somebody i used to know", 2023),  # Wrong director in source data (not Hou Hsiao-hsien)
    # Wrong years from scraping (year 2000 but actually different years)
    ("a history of violence", 2000),  # Actually 2005
    ("elephant", 2000),  # Actually 2003
    ("tropical malady", 2000),  # Actually 2004
    ("the new world", 2000),  # Actually 2005
    ("war of the worlds", 2000),  # Actually 2005
    ("ten", 2000),  # Actually 2002
    ("the secret of the grain", 2000),  # Actually 2007
    ("tie xi qu: west of the tracks", 2000),  # Actually 2002
    # Duplicates with wrong data
    ("m/other", 2000),  # Nobuhiro Suwa film, bad data
    ("chouga", 2010),  # Bad data
    ("li'l quinquin", 2010),  # Wrong year, actually 2014
    ("paradise", 2014),  # Ambiguous title
    ("24", 2002),  # TV series, not film
    ("in good company", 2005),  # Wrong director
    # Films with original language titles as director
    ("platform", 2001),  # Has Chinese chars as director
    ("time and tide", 2001),  # Has Chinese chars as director
    # Duplicates
    ("cold war", 2013),  # Hong Kong film, duplicate entry
    ("happier than ever: a love letter to los angeles", 2021),  # Concert film
    ("hypnotic", 2023),  # Wrong director
    ("1/3 of the eyes", 2005),  # Obscure, bad data
    ("coincoin and the extra-humans", 2018),  # TV series
    ("exhuma", 2023),  # Wrong year, actually 2024
    ("to my nineteen year old self", 2023),  # Documentary
    ("yes!", 2025),  # Future release, bad data
}


def clean_movie_data(movie) -> bool:
    """
    Fix known data issues in movie entries.
    Returns False if the movie should be skipped entirely.
    """
    # Check if this is a known bad entry
    key = (movie.title.lower(), movie.year)
    if key in SKIP_ENTRIES:
        return False
    
    # Fix director names
    if movie.director in DIRECTOR_CORRECTIONS:
        movie.director = DIRECTOR_CORRECTIONS[movie.director]
    
    return True


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
                if not clean_movie_data(movie):  # Skip bad entries
                    continue
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
        success, failed = tmdb.enrich_catalog(list(catalog))
        
        # Print failure report
        tmdb.print_failure_report()
        print(f"\nEnrichment complete: {success} succeeded, {failed} failed")
    
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
