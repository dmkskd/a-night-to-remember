"""
Movie catalog with deduplication logic.
Handles merging movies from multiple sources, combining recognitions.
"""

from dataclasses import dataclass, field


@dataclass
class Recognition:
    """An award or recognition for a movie."""
    type: str
    year: int
    details: str = "Winner"


@dataclass
class MovieEntry:
    """A movie entry in the catalog."""
    title: str
    year: int
    director: str
    recognitions: list[Recognition] = field(default_factory=list)
    
    # TMDB enriched data (optional)
    synopsis: str | None = None
    poster_url: str | None = None
    country: str | None = None
    runtime: int | None = None
    cast: list[str] = field(default_factory=list)
    genres: list[str] = field(default_factory=list)
    streaming: list[dict] = field(default_factory=list)
    rating: float | None = None  # TMDB vote_average (0-10)
    
    @property
    def key(self) -> tuple[str, int]:
        """Unique key for deduplication (normalized lowercase title, year)."""
        # Normalize: lowercase, replace non-breaking spaces, strip whitespace
        normalized = self.title.lower().replace('\u00a0', ' ').strip()
        return (normalized, self.year)
    
    @property
    def id(self) -> str:
        """Generate URL-friendly ID."""
        slug = self.title.lower()
        for char in [" ", ",", ":", "'", '"', ".", "!"]:
            slug = slug.replace(char, "-" if char == " " else "")
        # Remove double dashes
        while "--" in slug:
            slug = slug.replace("--", "-")
        return f"{slug}-{self.year}"
    
    def add_recognition(self, recognition: Recognition) -> None:
        """Add a recognition if not already present."""
        existing_types = {r.type for r in self.recognitions}
        if recognition.type not in existing_types:
            self.recognitions.append(recognition)
    
    def to_dict(self) -> dict:
        """Convert to dictionary for JSON export."""
        data = {
            "id": self.id,
            "title": self.title,
            "director": self.director,
            "year": self.year,
            "recognitions": [
                {"type": r.type, "year": r.year, "details": r.details}
                for r in self.recognitions
            ],
        }
        
        # Add optional fields if present
        if self.synopsis:
            data["synopsis"] = self.synopsis
        if self.poster_url:
            data["posterUrl"] = self.poster_url
        if self.country:
            data["country"] = self.country
        if self.runtime:
            data["runtime"] = self.runtime
        if self.cast:
            data["cast"] = self.cast
        if self.genres:
            data["genres"] = self.genres
        if self.streaming:
            data["streaming"] = self.streaming
        if self.rating is not None:
            data["rating"] = self.rating
        
        return data


class Catalog:
    """
    Movie catalog that handles deduplication.
    When the same movie is added multiple times (e.g., won multiple awards),
    recognitions are merged into a single entry.
    Uses fuzzy year matching (±1 year) to handle different release dates.
    """
    
    def __init__(self):
        self._movies: dict[tuple[str, int], MovieEntry] = {}
    
    def _find_existing(self, movie: MovieEntry) -> MovieEntry | None:
        """Find existing movie with fuzzy year match (±1 year)."""
        normalized_title = movie.title.lower().replace('\u00a0', ' ').strip()
        
        # Check exact match first
        key = (normalized_title, movie.year)
        if key in self._movies:
            return self._movies[key]
        
        # Check ±1 year for same title
        for year_offset in [-1, 1]:
            fuzzy_key = (normalized_title, movie.year + year_offset)
            if fuzzy_key in self._movies:
                return self._movies[fuzzy_key]
        
        return None
    
    def add(self, movie: MovieEntry) -> MovieEntry:
        """
        Add a movie to the catalog.
        If movie already exists (fuzzy match), merge recognitions.
        Returns the (possibly merged) movie entry.
        """
        existing = self._find_existing(movie)
        
        if existing:
            # Movie exists - merge recognitions
            for recognition in movie.recognitions:
                existing.add_recognition(recognition)
            return existing
        else:
            # New movie
            key = movie.key
            self._movies[key] = movie
            return movie
    
    def get(self, title: str, year: int) -> MovieEntry | None:
        """Get a movie by title and year."""
        return self._movies.get((title.lower(), year))
    
    def all(self) -> list[MovieEntry]:
        """Get all movies, sorted by year descending."""
        return sorted(self._movies.values(), key=lambda m: -m.year)
    
    def __len__(self) -> int:
        return len(self._movies)
    
    def __iter__(self):
        return iter(self.all())
