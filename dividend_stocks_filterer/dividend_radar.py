import requests
from bs4 import BeautifulSoup
from dividend_stocks_filterer.configure import *
from retrying import retry
from cachetools import cached, TTLCache


class DividendRader:

    def __init__(self, dividend_radar_url, local_file):
        self.dividend_radar_url = dividend_radar_url
        self.local_file = local_file
        self.latest_version_url = None
        self.latest_version = None
        self.latest_local_version = None

    @cached(cache=TTLCache(maxsize=1024, ttl=3600))
    @retry(wait_exponential_multiplier=2500, wait_exponential_max=10000, stop_max_attempt_number=10)
    def find_latest_version(self):
        page = requests.get(self.dividend_radar_url)
        soup = BeautifulSoup(page.content, "html.parser")
        self.latest_version_url = soup.find(class_="link-block w-inline-block").attrs['href']
        self.latest_version = self.latest_version_url[-15:-5]

    def check_if_local_is_latest(self):
        if self.latest_local_version == self.latest_version:
            return True
        else:
            return False

    def download_latest_version(self):
        pass
