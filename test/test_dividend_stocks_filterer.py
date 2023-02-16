import os
import re
from unittest import TestCase
from dividend_stocks_filterer.dividend_radar import DividendRadar


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
