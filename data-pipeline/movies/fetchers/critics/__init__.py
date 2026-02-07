"""Critics' picks and magazine top lists fetchers."""

from .sightandsound import SightAndSoundFetcher
from .filmcomment import FilmCommentFetcher
from .kinemajunpo import KinemaJunpoFetcher
from .cahiers import CahiersFetcher
from .indiewire import IndiewireFetcher
from .cinemascope import CinemaScopeFetcher
from .german import GermanCriticsFetcher
from .fotogramas import FotogramasFetcher
from .korean import KoreanCriticsFetcher

__all__ = [
    "SightAndSoundFetcher",
    "FilmCommentFetcher",
    "KinemaJunpoFetcher",
    "CahiersFetcher",
    "IndiewireFetcher",
    "CinemaScopeFetcher",
    "GermanCriticsFetcher",
    "FotogramasFetcher",
    "KoreanCriticsFetcher",
]
