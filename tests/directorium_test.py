import json
from datetime import date
from unittest import TestCase

from directorium import Directorium
from directorium.api import FileApi
from directorium.directorium import Season
from directorium.event import Event


class TestDirectorium(TestCase):

    def setUp(self):
        with open("tests/data/2024.json", "r") as f:
            self.data = json.load(f)["Zelebrationen"]
        self.api = FileApi("tests/data/%s.json")

    def test_get(self):
        directorium = Directorium(self.api)
        expected = [Event.parse(self.data[0])]
        actual = directorium.get(date(2024, 1, 1))
        self.assertEqual(expected, actual)

    def test_get_multiple(self):
        directorium = Directorium(self.api)
        expected = [Event.parse(d) for d in self.data[1:3]]
        actual = directorium.get(date(2024, 1, 2))
        self.assertEqual(expected, actual)

    def test_season(self):
        directorium = Directorium(self.api)
        self.assertEqual(directorium.season(date(2024, 1, 1)), Season.CHRISTMAS)
        self.assertEqual(directorium.season(date(2024, 2, 5)), Season.ORDINARY)
        self.assertEqual(directorium.season(date(2024, 3, 21)), Season.LENT)
        self.assertEqual(directorium.season(date(2024, 4, 1)), Season.EASTER)
