"""
Fetchers package - retrieves movie data from external sources.
Organized into subfolders:
- festivals/ - Film festival awards
- critics/ - Critics' picks and magazine lists
- other/ - Directors, etc.
"""

from typing import Protocol, runtime_checkable
import sys
sys.path.insert(0, str(__file__).rsplit("/", 2)[0])

from catalog import MovieEntry


@runtime_checkable
class Fetcher(Protocol):
    """
    Protocol for movie fetchers.
    
    Any class with a fetch() method matching this signature
    is considered a Fetcher (structural typing).
    """
    
    name: str  # Human-readable name for logging
    recognition_type: str | None  # Recognition type this fetcher provides (None for directors etc.)
    
    def fetch(self, min_year: int = 2005) -> list[MovieEntry]:
        """
        Fetch movies from the data source.
        
        Args:
            min_year: Only return movies from this year onwards
            
        Returns:
            List of MovieEntry objects with recognitions
        """
        ...


# Festival fetchers
from .festivals import (
    WikidataFetcher,
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
    # Legacy
    CannesFetcher,
    BerlinFetcher,
    VeniceFetcher,
    HongKongFetcher,
)

# Critics
from .critics import (
    SightAndSoundFetcher,
    FilmCommentFetcher,
    KinemaJunpoFetcher,
    CahiersFetcher,
    IndiewireFetcher,
    CinemaScopeFetcher,
    GermanCriticsFetcher,
    FotogramasFetcher,
    KoreanCriticsFetcher,
)

# Other
from .other import DirectorsFetcher


__all__ = [
    "Fetcher",
    # Festivals
    "WikidataFetcher",
    "CannesWikidataFetcher",
    "CannesGrandPrixFetcher",
    "CannesBestDirectorFetcher",
    "CannesJuryPrizeFetcher",
    "BerlinWikidataFetcher",
    "VeniceWikidataFetcher",
    "HongKongWikidataFetcher",
    "TorontoFetcher",
    "SundanceFetcher",
    "TokyoFetcher",
    "BusanFetcher",
    "AnnecyFetcher",
    "CannesFetcher",
    "BerlinFetcher",
    "VeniceFetcher",
    "HongKongFetcher",
    # Critics
    "SightAndSoundFetcher",
    "FilmCommentFetcher",
    "KinemaJunpoFetcher",
    "CahiersFetcher",
    "IndiewireFetcher",
    "CinemaScopeFetcher",
    "GermanCriticsFetcher",
    "FotogramasFetcher",
    "KoreanCriticsFetcher",
    # Other
    "DirectorsFetcher",
]
