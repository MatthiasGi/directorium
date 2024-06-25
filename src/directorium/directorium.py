"""Actual implementation of the Directorium class.

This module contains the Directorium class which is the main entry point for
the liturgical calendar. It provides methods to get the liturgical events for
a specific date and to determine the season of the liturgical year.
"""

import enum
from datetime import date, timedelta
from typing import List

from . import utils
from .api import Api
from .event import Event


class Season(enum.Enum):
    """The season of the liturgical year."""

    ORDINARY = enum.auto()
    """
    The ordinary season of the liturgical year - if no other season is currently
    active.
    """

    CHRISTMAS = enum.auto()
    """
    The christmas season starts with the first advent sunday and ends with the
    baptism of the lord (i.e. the sunday after epiphany).
    """

    LENT = enum.auto()
    """The lent season starts with ash wednesday and ends before easter sunday."""

    EASTER = enum.auto()
    """Easter season starts with easter sunday and ends with pentecost."""


class Directorium:
    """The main class to access the liturgical calendar.

    The API-backend is exchangeable to allow for different sources of the
    liturgical calendar data.

    Attributes:
        api (Api): The API to get the liturgical events from.
    """

    def __init__(self, api: Api):
        """Creates the Directorium with the given API.

        Args:
            api (Api): The api to get the liturgical events from.
        """
        self.api = api

    def get(self, d: date) -> List[Event]:
        """Retrieves a list of liturgical events for a specific date.

        Args:
            d (date): The date for which to get the liturgical events.

        Returns:
            List[Event]: List of liturgical events for the given date.
        """
        return [Event.parse(e) for e in self.api.get_date(d)]

    def season(self, d: date) -> Season:
        """Determines the season of the liturgical year for a specific date.

        Args:
            d (date): The date for which to determine the season.

        Returns:
            Season: The season of the liturgical year for the given date.
        """
        christmas = date(d.year, 12, 25)
        advent = christmas - timedelta(days=21 + christmas.isoweekday())
        if d >= advent:
            return Season.CHRISTMAS

        epiphany = date(d.year, 1, 6)
        baptism = epiphany + timedelta(days=7 - epiphany.isoweekday() % 7)
        if d <= baptism:
            return Season.CHRISTMAS

        easter = utils.easter(d.year)
        ashwednesday = easter - timedelta(days=46)
        if d >= ashwednesday and d < easter:
            return Season.LENT

        pentecoste = easter + timedelta(days=49)
        if d >= easter and d < pentecoste:
            return Season.EASTER

        return Season.ORDINARY

    @staticmethod
    def from_request(calendar: str | None = None) -> "Directorium":
        """Creates a Directorium instance with a `RequestApi` backend.

        Args:
            calendar (str | None, optional): The name of the calendar to use.

        Returns:
            Directorium: The Directorium instance with a RequestApi backend.
        """
        from .api import RequestApi
        return Directorium(RequestApi(calendar))

    @staticmethod
    def from_file(format_path: str) -> "Directorium":
        """Creates a Directorium instance with a `FileApi` backend.

        Args:
            format_path (str): The format string for the file path.

        Returns:
            Directorium: The Directorium instance with a FileApi backend.
        """
        from .api import FileApi
        return Directorium(FileApi(format_path))

    @staticmethod
    def from_cache(base_path: str, calendar: str | None = None) -> "Directorium":
        """Creates a Directorium instance with a `CacheApi` backend.

        Args:
            base_path (str): The base path for the cache files.
            calendar (str | None, optional): The name of the calendar to use.

        Returns:
            Directorium: The Directorium instance with a CacheApi backend.
        """
        from .api import CacheApi
        return Directorium(CacheApi(base_path, calendar))
