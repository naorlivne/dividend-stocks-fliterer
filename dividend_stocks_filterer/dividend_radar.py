import requests
from bs4 import BeautifulSoup
from dividend_stocks_filterer.configure import *
from retrying import retry
from cachetools import cached, TTLCache


class DividendRader:

    def __init__(self, dividend_radar_url, local_file):
        """
        This class handles everything to do with the dividend radar file, finding, downloading and version checking

        Arguments:
            :param dividend_radar_url: the url of the page with the dividend radar download button
            :param local_file: where to save the local dividend radar xlsx file
        """
        self.dividend_radar_url = dividend_radar_url
        self.local_file = local_file
        self.latest_version_url = None
        self.latest_version = None
        self.latest_local_version = None

    @cached(cache=TTLCache(maxsize=1024, ttl=3600))
    @retry(wait_exponential_multiplier=2500, wait_exponential_max=10000, stop_max_attempt_number=10)
    def find_latest_version(self):
        """
        Finds the latest version of the dividend radar xlsx file, note I'm wrapping this with retries to avoid network
        glitches and then caching the result as a quick way to avoid spamming the site
        """
        page = requests.get(self.dividend_radar_url)
        soup = BeautifulSoup(page.content, "html.parser")
        self.latest_version_url = soup.find(class_="link-block w-inline-block").attrs['href']
        self.latest_version = self.latest_version_url[-15:-5]

    def check_if_local_is_latest(self):
        """
        Checks if the local dividend radar file version is the latest one

        Returns:
            :return auth_required: True if latest, False otherwise (not latest or does not exist locally)
        """
        try:
            self.find_latest_version()
            if self.latest_local_version == self.latest_version:
                return True
            else:
                return False
        except FileNotFoundError:
            return False

    def download_latest_version(self):
        """
        Gets the latest version of the dividend radar file and puts it in the local path declared in the function
        """
        self.find_latest_version()
        latest_rader_file = requests.get(self.latest_version_url)
        open(self.local_file, 'wb').write(latest_rader_file.content)
        self.latest_local_version = self.latest_version
