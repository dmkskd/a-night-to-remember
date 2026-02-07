# Story fetchers
from .awards import fetch_hugo_winners, fetch_nebula_winners, fetch_ohenry_winners
from .classics import fetch_literary_classics, fetch_scifi_classics
from .curated import fetch_curated_stories
from .online import fetch_online_stories

__all__ = [
    "fetch_hugo_winners",
    "fetch_nebula_winners",
    "fetch_ohenry_winners",
    "fetch_literary_classics",
    "fetch_scifi_classics",
    "fetch_curated_stories",
    "fetch_online_stories",
]
