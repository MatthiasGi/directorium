import glob
import json
import os
import tempfile
from datetime import date
from unittest import TestCase

from platformdirs import user_data_dir

from directorium.api import Api, CacheApi, FileApi, RequestApi


class TestApi(TestCase):

    def clearCache(self) -> None:
        for f in glob.glob(f"{self.cache_dir}/*.json"):
            os.remove(f)
        if os.path.exists(self.cache_dir):
            os.removedirs(self.cache_dir)

    def setUp(self) -> None:
        self.cache_dir = user_data_dir("directorium", False)
        self.clearCache()

    def tearDown(self) -> None:
        self.clearCache()

    def test_request(self):
        with open("tests/data/2024.json", "r") as f:
            actual = RequestApi().get_year(2024)
            expected = json.load(f)
            self.assertEqual(actual, expected)


    def test_request_calendar(self):
        with open("tests/data/2025.koeln.json", "r") as f:
            api = RequestApi("koeln")
            actual = api.get_year(2025)
            expected = json.load(f)
            self.assertEqual(actual, expected)


    def test_file(self):
        with open("tests/data/2024.json", "r") as f:
            api = FileApi("tests/data/%s.json")
            actual = api.get_year(2024)
            expected = json.load(f)
            self.assertEqual(actual, expected)

    def test_cache(self):
        with (
            tempfile.TemporaryDirectory() as tempdir,
            open("tests/data/2024.json", "r") as f,
        ):
            api = CacheApi(tempdir)
            path = f"{tempdir}/2024.json"
            self.assertFalse(os.path.exists(path))
            actual = api.get_year(2024)
            self.assertTrue(os.path.exists(path))
            expected = json.load(f)
            self.assertEqual(actual, expected)
            with open(path, "r") as f:
                actual = json.load(f)
                self.assertEqual(actual, expected)
            actual = api.get_year(2024)
            self.assertEqual(actual, expected)

    def test_cache_calendar(self):
        with (
            tempfile.TemporaryDirectory() as tempdir,
            open("tests/data/2025.koeln.json", "r") as f,
        ):
            api = CacheApi(tempdir, calendar="koeln")
            path = f"{tempdir}/2025.koeln.json"
            self.assertFalse(os.path.exists(path))
            actual = api.get_year(2025)
            self.assertTrue(os.path.exists(path))
            expected = json.load(f)
            self.assertEqual(actual, expected)
            with open(path, "r") as f:
                actual = json.load(f)
                self.assertEqual(actual, expected)
            actual = api.get_year(2025)
            self.assertEqual(actual, expected)

    def test_cache_without_dir(self):
        self.assertFalse(os.path.exists(self.cache_dir))
        self.assertFalse(os.path.exists(f"{self.cache_dir}/2024.json"))
        CacheApi().get_year(2024)
        self.assertTrue(os.path.exists(self.cache_dir))
        self.assertTrue(os.path.exists(f"{self.cache_dir}/2024.json"))
        with (
            open("tests/data/2024.json", "r") as f,
            open(f"{self.cache_dir}/2024.json", "r") as g,
        ):
            actual = json.load(g)
            expected = json.load(f)
            self.assertEqual(actual, expected)

    def test_get_date(self):
        with open("tests/data/2024.json", "r") as f:
            data = json.load(f)
            expected = data["Zelebrationen"][1:3]

        class TestApi(Api):
            def get_year(self, year):
                with open("tests/data/2024.json", "r") as f:
                    return json.load(f)

        api = TestApi()
        self.assertEqual(api.get_date(2024, 1, 2), expected)
        self.assertEqual(api.get_date(date(2024, 1, 2)), expected)

    def test_request_get_date(self):
        with open("tests/data/2024.json", "r") as f:
            data = json.load(f)
            expected = data["Zelebrationen"][1:3]

        api = RequestApi()
        self.assertEqual(api.get_date(2024, 1, 2), expected)
        self.assertEqual(api.get_date(date(2024, 1, 2)), expected)

    def test_cache_get_date(self):
        with (
            tempfile.TemporaryDirectory() as tempdir,
            open("tests/data/2025.koeln.json", "r") as f,
        ):
            api = CacheApi(tempdir, calendar="koeln")
            path = f"{tempdir}/2025.koeln.json"
            self.assertFalse(os.path.exists(path))
            actual = api.get_date(2025, 1, 2)
            self.assertTrue(os.path.exists(path))
            expected = json.load(f)
            self.assertEqual(actual, expected["Zelebrationen"][1:4])
            with open(path, "r") as f:
                actual = json.load(f)
                self.assertEqual(actual, expected)
            actual = api.get_year(2025)
            self.assertEqual(actual, expected)
