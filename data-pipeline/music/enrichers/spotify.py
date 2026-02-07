"""Spotify API enricher for album data."""
import os
import sys
import base64
import requests
import time
from datetime import datetime, timedelta
from typing import Optional


def format_duration(seconds: int) -> str:
    """Format seconds into human-readable duration."""
    if seconds < 60:
        return f"{seconds}s"
    elif seconds < 3600:
        mins = seconds // 60
        return f"{mins}m"
    else:
        hours = seconds // 3600
        mins = (seconds % 3600) // 60
        if mins:
            return f"{hours}h {mins}m"
        return f"{hours}h"


def format_retry_time(seconds: int) -> str:
    """Format when to retry in human-readable format."""
    retry_at = datetime.now() + timedelta(seconds=seconds)
    return retry_at.strftime("%H:%M")


class RateLimitedError(Exception):
    """Raised when Spotify rate limits us for a long time."""
    def __init__(self, retry_after: int):
        self.retry_after = retry_after
        self.retry_at = format_retry_time(retry_after)
        self.duration = format_duration(retry_after)
        super().__init__(f"Rate limited by Spotify. Try again in {self.duration} (around {self.retry_at})")

# Genre normalization mapping - maps Spotify's granular genres to broader categories
GENRE_MAPPING = {
    # Rock
    "rock": "Rock",
    "alternative rock": "Rock",
    "indie rock": "Indie",
    "art rock": "Art Rock",
    "progressive rock": "Prog Rock",
    "psychedelic rock": "Psychedelic",
    "garage rock": "Rock",
    "post-punk": "Post-Punk",
    "punk": "Punk",
    "hardcore punk": "Punk",
    "post-hardcore": "Post-Hardcore",
    "emo": "Emo",
    "screamo": "Emo",
    "grunge": "Grunge",
    "shoegaze": "Shoegaze",
    "dream pop": "Dream Pop",
    "noise rock": "Noise",
    "math rock": "Math Rock",
    "post-rock": "Post-Rock",
    "slowcore": "Slowcore",
    "sadcore": "Slowcore",
    
    # Metal
    "metal": "Metal",
    "heavy metal": "Metal",
    "alternative metal": "Metal",
    "nu metal": "Metal",
    "black metal": "Black Metal",
    "death metal": "Death Metal",
    "doom metal": "Doom Metal",
    "stoner metal": "Stoner",
    "sludge metal": "Sludge",
    "thrash metal": "Thrash",
    "progressive metal": "Prog Metal",
    "metalcore": "Metalcore",
    "deathcore": "Metalcore",
    
    # Electronic
    "electronic": "Electronic",
    "electronica": "Electronic",
    "idm": "IDM",
    "ambient": "Ambient",
    "dark ambient": "Ambient",
    "drone": "Drone",
    "techno": "Techno",
    "house": "House",
    "deep house": "House",
    "tech house": "House",
    "trance": "Trance",
    "drum and bass": "Drum & Bass",
    "dubstep": "Dubstep",
    "trip hop": "Trip Hop",
    "downtempo": "Downtempo",
    "chillwave": "Chillwave",
    "synthwave": "Synthwave",
    "industrial": "Industrial",
    "ebm": "Industrial",
    "noise": "Noise",
    "experimental": "Experimental",
    "glitch": "Glitch",
    "vaporwave": "Vaporwave",
    
    # Hip-Hop / R&B
    "hip hop": "Hip-Hop",
    "rap": "Hip-Hop",
    "alternative hip hop": "Hip-Hop",
    "underground hip hop": "Hip-Hop",
    "conscious hip hop": "Hip-Hop",
    "trap": "Trap",
    "r&b": "R&B",
    "alternative r&b": "R&B",
    "neo soul": "Neo-Soul",
    "soul": "Soul",
    "funk": "Funk",
    
    # Jazz
    "jazz": "Jazz",
    "contemporary jazz": "Jazz",
    "jazz fusion": "Jazz Fusion",
    "free jazz": "Free Jazz",
    "avant-garde jazz": "Free Jazz",
    "bebop": "Jazz",
    "cool jazz": "Jazz",
    "modal jazz": "Jazz",
    "spiritual jazz": "Jazz",
    "afro-cuban jazz": "Latin Jazz",
    
    # Folk / Country
    "folk": "Folk",
    "indie folk": "Folk",
    "freak folk": "Folk",
    "singer-songwriter": "Singer-Songwriter",
    "americana": "Americana",
    "country": "Country",
    "alt country": "Alt-Country",
    "outlaw country": "Country",
    "bluegrass": "Bluegrass",
    
    # Pop
    "pop": "Pop",
    "indie pop": "Indie Pop",
    "art pop": "Art Pop",
    "synth-pop": "Synth-Pop",
    "electropop": "Electropop",
    "chamber pop": "Chamber Pop",
    "baroque pop": "Baroque Pop",
    "dream pop": "Dream Pop",
    "hyperpop": "Hyperpop",
    
    # Classical / Minimalism
    "classical": "Classical",
    "contemporary classical": "Modern Classical",
    "minimalism": "Minimalism",
    "post-minimalism": "Minimalism",
    "neoclassical": "Neoclassical",
    "modern classical": "Modern Classical",
    "ambient": "Ambient",
    
    # World
    "world": "World",
    "afrobeat": "Afrobeat",
    "afropop": "Afropop",
    "latin": "Latin",
    "bossa nova": "Bossa Nova",
    "mpb": "MPB",
    "tropicalia": "Tropicália",
    "reggae": "Reggae",
    "dub": "Dub",
    "dancehall": "Dancehall",
    "ska": "Ska",
    
    # Blues
    "blues": "Blues",
    "blues rock": "Blues Rock",
    "delta blues": "Blues",
    "electric blues": "Blues",
    
    # Other
    "soundtrack": "Soundtrack",
    "score": "Soundtrack",
    "spoken word": "Spoken Word",
    "comedy": "Comedy",
}

# Genres to skip (too generic or not useful)
SKIP_GENRES = {
    "album rock", "classic rock", "mellow gold", "soft rock",
    "adult standards", "easy listening", "background music",
    "spotify", "viral", "tiktok",
}


def get_broad_category(genre: str) -> str | None:
    """Get the broad category for a genre."""
    genre_lower = genre.lower()
    
    # Skip unwanted genres
    if genre_lower in SKIP_GENRES:
        return None
    
    # Check for exact match
    if genre_lower in GENRE_MAPPING:
        return GENRE_MAPPING[genre_lower]
    
    # Check for partial match
    for key, value in GENRE_MAPPING.items():
        if key in genre_lower:
            return value
    
    return None


def process_genres(genres: list[str]) -> tuple[list[str], list[str]]:
    """
    Process Spotify genres into broad categories and detailed genres.
    Returns (broad_categories, detailed_genres).
    
    - broad_categories: Up to 3 main categories for filtering
    - detailed_genres: All original genres (cleaned up) for detail view
    """
    broad = []
    broad_seen = set()
    detailed = []
    detailed_seen = set()
    
    for genre in genres:
        genre_lower = genre.lower()
        
        # Skip unwanted genres
        if genre_lower in SKIP_GENRES:
            continue
        
        # Get broad category
        category = get_broad_category(genre)
        if category and category not in broad_seen:
            broad.append(category)
            broad_seen.add(category)
        
        # Keep detailed genre (title case, cleaned)
        detailed_clean = genre.title()
        if detailed_clean not in detailed_seen:
            detailed.append(detailed_clean)
            detailed_seen.add(detailed_clean)
    
    # Limit broad categories to top 3
    return broad[:3], detailed

class SpotifyEnricher:
    """Enriches album data with Spotify API."""
    
    def __init__(self):
        self.client_id = os.getenv("SPOTIFY_CLIENT_ID")
        self.client_secret = os.getenv("SPOTIFY_CLIENT_SECRET")
        self.access_token: Optional[str] = None
        self.base_url = "https://api.spotify.com/v1"
    
    def _get_access_token(self) -> str:
        """Get access token using client credentials flow."""
        if self.access_token:
            return self.access_token
        
        auth_string = f"{self.client_id}:{self.client_secret}"
        auth_bytes = auth_string.encode("utf-8")
        auth_base64 = base64.b64encode(auth_bytes).decode("utf-8")
        
        response = requests.post(
            "https://accounts.spotify.com/api/token",
            headers={
                "Authorization": f"Basic {auth_base64}",
                "Content-Type": "application/x-www-form-urlencoded"
            },
            data={"grant_type": "client_credentials"}
        )
        response.raise_for_status()
        self.access_token = response.json()["access_token"]
        return self.access_token
    
    def _get_headers(self) -> dict:
        """Get headers with authorization."""
        return {"Authorization": f"Bearer {self._get_access_token()}"}
    
    def search_album(self, artist: str, album: str) -> Optional[dict]:
        """Search for an album and return Spotify data."""
        # Small delay to avoid rate limiting
        time.sleep(0.1)
        
        query = f"album:{album} artist:{artist}"
        try:
            response = requests.get(
                f"{self.base_url}/search",
                headers=self._get_headers(),
                params={"q": query, "type": "album", "limit": 1}
            )
            
            if response.status_code == 429:
                vendor_retry = int(response.headers.get("Retry-After", 5))
                
                # If vendor says wait more than 5 minutes, abort entirely
                if vendor_retry > 300:
                    raise RateLimitedError(vendor_retry)
                
                print(f"    ⚠ Rate limited, waiting {format_duration(vendor_retry)}...", file=sys.stderr)
                time.sleep(vendor_retry + 1)
                response = requests.get(
                    f"{self.base_url}/search",
                    headers=self._get_headers(),
                    params={"q": query, "type": "album", "limit": 1}
                )
            
            if response.status_code != 200:
                print(f"    ✗ Search failed: HTTP {response.status_code}", file=sys.stderr)
                return None
        except requests.RequestException as e:
            print(f"    ✗ Search error: {e}", file=sys.stderr)
            return None
        
        data = response.json()
        albums = data.get("albums", {}).get("items", [])
        
        if not albums:
            # Try a simpler search
            query = f"{album} {artist}"
            response = requests.get(
                f"{self.base_url}/search",
                headers=self._get_headers(),
                params={"q": query, "type": "album", "limit": 1}
            )
            if response.status_code != 200:
                return None
            data = response.json()
            albums = data.get("albums", {}).get("items", [])
        
        if not albums:
            return None
        
        album_data = albums[0]
        
        # Get the largest image
        images = album_data.get("images", [])
        cover_url = images[0]["url"] if images else None
        
        return {
            "spotify_id": album_data["id"],
            "spotify_url": album_data["external_urls"].get("spotify"),
            "cover_url": cover_url,
            "release_date": album_data.get("release_date"),
            "total_tracks": album_data.get("total_tracks"),
            "artists": [a["name"] for a in album_data.get("artists", [])],
        }
    
    def get_album_details(self, spotify_id: str) -> Optional[dict]:
        """Get detailed album info including tracks."""
        # Retry with backoff for rate limiting
        for attempt in range(3):
            try:
                response = requests.get(
                    f"{self.base_url}/albums/{spotify_id}",
                    headers=self._get_headers()
                )
                
                if response.status_code == 429:
                    vendor_retry = int(response.headers.get("Retry-After", 5))
                    
                    # If vendor says wait more than 5 minutes, abort entirely
                    if vendor_retry > 300:
                        raise RateLimitedError(vendor_retry)
                    
                    print(f"    ⚠ Rate limited (attempt {attempt+1}/3), waiting {format_duration(vendor_retry)}...", file=sys.stderr)
                    time.sleep(vendor_retry + 1)
                    continue
                
                if response.status_code != 200:
                    print(f"    ✗ Album details failed: HTTP {response.status_code}", file=sys.stderr)
                    return None
                
                break
            except requests.RequestException as e:
                print(f"    ✗ Album details error: {e}", file=sys.stderr)
                if attempt < 2:
                    time.sleep(2)
                    continue
                return None
        else:
            print(f"    ✗ Album details failed after 3 retries", file=sys.stderr)
            return None
        
        data = response.json()
        
        tracks = [
            {
                "number": t["track_number"],
                "name": t["name"],
                "duration_ms": t["duration_ms"],
            }
            for t in data.get("tracks", {}).get("items", [])
        ]
        
        # Get genres from the first artist
        genres = data.get("genres", [])
        if not genres and data.get("artists"):
            artist_id = data["artists"][0]["id"]
            artist_genres = self._get_artist_genres(artist_id)
            if artist_genres:
                genres = artist_genres
        
        # Process genres into broad categories and detailed list
        broad_genres, detailed_genres = process_genres(genres)
        
        return {
            "genres": broad_genres,  # Broad categories for filtering
            "detailed_genres": detailed_genres,  # All genres for detail view
            "label": data.get("label"),
            "popularity": data.get("popularity"),
            "tracks": tracks,
        }
    
    def _get_artist_genres(self, artist_id: str) -> list[str]:
        """Get genres from an artist."""
        try:
            response = requests.get(
                f"{self.base_url}/artists/{artist_id}",
                headers=self._get_headers()
            )
            if response.status_code == 429:
                vendor_retry = int(response.headers.get("Retry-After", 5))
                
                if vendor_retry > 300:
                    raise RateLimitedError(vendor_retry)
                
                print(f"    ⚠ Rate limited on artist genres, waiting {format_duration(vendor_retry)}...", file=sys.stderr)
                time.sleep(vendor_retry + 1)
                response = requests.get(
                    f"{self.base_url}/artists/{artist_id}",
                    headers=self._get_headers()
                )
            if response.status_code != 200:
                return []
            return response.json().get("genres", [])
        except requests.RequestException as e:
            print(f"    ✗ Artist genres error: {e}", file=sys.stderr)
            return []
