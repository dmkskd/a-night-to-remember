"""Festival award fetchers."""

from .wikidata import (
    WikidataFetcher,
    CannesWikidataFetcher,
    CannesGrandPrixFetcher,
    CannesBestDirectorFetcher,
    CannesJuryPrizeFetcher,
    BerlinWikidataFetcher,
    VeniceWikidataFetcher,
    HongKongWikidataFetcher,
)
from .toronto import TorontoFetcher
from .sundance import SundanceFetcher
from .tokyo import TokyoFetcher
from .busan import BusanFetcher
from .annecy import AnnecyFetcher

# Legacy scrapers (kept for reference)
from .cannes import CannesFetcher
from .berlin import BerlinFetcher
from .venice import VeniceFetcher
from .hongkong import HongKongFetcher

__all__ = [
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
]
