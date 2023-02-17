import os
from unittest import TestCase
from dividend_stocks_filterer.dividend_radar import DividendRadar
from datetime import datetime


class DividendRadarTests(TestCase):
    def setUp(self):
        self.radar_url = "https://www.portfolio-insight.com/dividend-radar"
        self.local_file = "radar_test.xlsx"
        self.dividend_radar = DividendRadar(self.radar_url, self.local_file)

    def tearDown(self):
        if os.path.exists(self.local_file):
            os.remove(self.local_file)

    def test_find_latest_version(self):
        self.dividend_radar.find_latest_version()
        date_regex = r"\d{4}-\d{2}-\d{2}"
        self.assertRegex(self.dividend_radar.latest_version, date_regex)

    def test_check_if_local_is_latest(self):
        self.assertFalse(self.dividend_radar.check_if_local_is_latest())
        self.dividend_radar.download_latest_version()
        self.assertTrue(self.dividend_radar.check_if_local_is_latest())

    def test_download_latest_version(self):
        self.dividend_radar.download_latest_version()
        self.assertTrue(os.path.exists(self.local_file))

    def test_read_radar_file_to_dict(self):
        self.dividend_radar.download_latest_version()
        result = self.dividend_radar.read_radar_file_to_dict()

        # Ensure return result is a dict
        self.assertIsInstance(result, dict)

        # Ensure the dictionary has at least one entry
        self.assertGreater(len(result), 0)

        # Check that the dictionary values are of the expected types
        for key, value in result.items():
            self.assertIsInstance(key, str)
            self.assertIsInstance(value, dict)
            for inner_key, inner_value in value.items():
                self.assertIsInstance(inner_value, (datetime, str, int, float, type(None)))
