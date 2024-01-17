import unittest
from dividend_stocks_filterer.finviz_data import *


#class TestYahooFinance(unittest.TestCase):

#    def test_get_finviz_data_for_tickers_tuple(self):
#        # Test with valid tickers
#        time_reply, reply = get_finviz_data_for_tickers_tuple(("PG", "SCL"))
#        self.assertIsInstance(time_reply, datetime)
#        self.assertIsInstance(reply, dict)
#        self.assertIn("PG", reply)
#        self.assertIn("SCL", reply)

#    def test_get_finviz_data_for_tickers_list(self):
#        # Test with valid tickers
#        time_reply, reply = get_finviz_data_for_tickers_list(["PG", "SCL"])
#        self.assertIsInstance(time_reply, datetime)
#        self.assertIsInstance(reply, dict)
#        self.assertIn("PG", reply)
#       self.assertIn("SCL", reply)
