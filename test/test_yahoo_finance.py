import time
import unittest
from dividend_stocks_filterer.yahoo_finance import *


class TestReadConfigurations(unittest.TestCase):

    def test_get_yahoo_finance_data_for_tickers_tuple(self):
        time_reply, reply = get_yahoo_finance_data_for_tickers_tuple(("PG", "SCL"))

    def test_get_yahoo_finance_data_for_tickers_list(self):
        time_reply, reply = get_yahoo_finance_data_for_tickers_list(["PG", "SCL"])
