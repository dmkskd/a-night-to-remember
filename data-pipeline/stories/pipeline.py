#!/usr/bin/env python3
"""Stories data pipeline - fetches and exports short story data."""
import argparse
import json
import re
import sys
from pathlib import Path

# Add parent directory to path for imports
sys.path.insert(0, str(Path(__file__).parent.parent))

from stories.fetchers import (
    fetch_hugo_winners,
    fetch_nebula_winners,
    fetch_ohenry_winners,
    fetch_literary_classics,
    fetch_scifi_classics,
    fetch_curated_stories,
    fetch_online_stories,
)


def merge_stories(stories: list[dict]) -> list[dict]:
    """Merge duplicate stories, combining their recognitions."""
    merged = {}
    
    for story in stories:
        # Create a key from author + title (normalized)
        key = f"{story['author'].lower()}|{story['title'].lower()}"
        
        if key in merged:
            # Merge recognitions
            existing = merged[key]
            existing_types = {r["type"] for r in existing.get("recognitions", [])}
            for rec in story.get("recognitions", []):
                if rec["type"] not in existing_types:
                    existing.setdefault("recognitions", []).append(rec)
            # Merge themes
            existing_themes = set(existing.get("themes", []))
            for theme in story.get("themes", []):
                existing_themes.add(theme)
            existing["themes"] = list(existing_themes)
            # Keep read_url if we find one
            if story.get("read_url") and not existing.get("read_url"):
                existing["read_url"] = story["read_url"]
                existing["source"] = story.get("source")
        else:
            merged[key] = story.copy()
    
    return list(merged.values())


def create_story_id(author: str, title: str, year: int) -> str:
    """Create a URL-friendly ID for a story."""
    combined = f"{title}-{author}-{year}"
    # Remove special characters, replace spaces with hyphens
    slug = re.sub(r'[^\w\s-]', '', combined.lower())
    slug = re.sub(r'[-\s]+', '-', slug).strip('-')
    return slug


def run_pipeline(limit: int = None):
    """Run the full stories pipeline."""
    print("=" * 50)
    print("Stories Data Pipeline")
    print("=" * 50)
    
    # Fetch from all sources
    all_stories = []
    
    # Award winners
    all_stories.extend(fetch_hugo_winners())
    all_stories.extend(fetch_nebula_winners())
    all_stories.extend(fetch_ohenry_winners())
    
    # Classics
    all_stories.extend(fetch_literary_classics())
    all_stories.extend(fetch_scifi_classics())
    
    # Curated world stories
    all_stories.extend(fetch_curated_stories())
    
    # Online stories (with read links)
    all_stories.extend(fetch_online_stories())
    
    print(f"\nTotal stories fetched: {len(all_stories)}")
    
    # Merge duplicates
    stories = merge_stories(all_stories)
    print(f"After merging duplicates: {len(stories)}")
    
    # Apply limit if specified
    if limit:
        stories = stories[:limit]
        print(f"Limited to: {len(stories)} stories")
    
    # Add IDs
    for story in stories:
        story["id"] = create_story_id(story["author"], story["title"], story["year"])
    
    # Sort by year (newest first)
    stories.sort(key=lambda x: -x.get("year", 0))
    
    # Get unique recognition types
    recognition_types = set()
    for story in stories:
        for rec in story.get("recognitions", []):
            recognition_types.add(rec["type"])
    
    # Get unique genres
    all_genres = set()
    for story in stories:
        for genre in story.get("genres", []):
            all_genres.add(genre)
    
    # Get unique themes
    all_themes = set()
    for story in stories:
        for theme in story.get("themes", []):
            all_themes.add(theme)
    
    # Build output
    output = {
        "stories": stories,
        "recognitionTypes": sorted(recognition_types),
        "genres": sorted(all_genres),
        "themes": sorted(all_themes),
    }
    
    # Write to file
    output_path = Path(__file__).parent.parent.parent / "src" / "data" / "stories.json"
    output_path.parent.mkdir(parents=True, exist_ok=True)
    
    with open(output_path, "w", encoding="utf-8") as f:
        json.dump(output, f, indent=2, ensure_ascii=False)
    
    print(f"\n✓ Wrote {len(stories)} stories to {output_path}")
    print(f"✓ Recognition types: {len(recognition_types)}")
    print(f"✓ Genres: {len(all_genres)}")
    print(f"✓ Themes: {len(all_themes)}")


if __name__ == "__main__":
    parser = argparse.ArgumentParser(description="Stories data pipeline")
    parser.add_argument("--limit", type=int, help="Limit number of stories to process")
    args = parser.parse_args()
    
    run_pipeline(limit=args.limit)
