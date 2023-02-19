import unittest
from dividend_stocks_filterer.helper_functions import *
import datetime
import pandas as pd

# Not real data - changing it based on need for tests
test_radar_dict = {
    'A': {
        'Symbol': 'A',
        'Company': 'Agilent Technologies, Inc.',
        'FV': None,
        'Sector': 'Health Care',
        'No Years': 13,
        'Price': 148.28,
        'Div Yield': 0.61,
        '5Y Avg Yield': 0.68,
        'Current Div': 0.225,
        'Payouts/ Year': 4,
        'Annualized': 0.9,
        'Previous Div': 0.21,
        'Ex-Date': datetime.datetime(2022, 12, 30, 0, 0),
        'Pay-Date': datetime.datetime(2023, 1, 25, 0, 0),
        'Low': 112.52,
        'High': 160.27,
        'DGR 1Y': 37.25,
        'DGR 3Y': 16.59,
        'DGR 5Y': 14.34,
        'DGR 10Y': 14.05,
        'TTR 1Y': -5.53,
        'TTR 3Y': 21.41,
        'Fair Value': 'At Fair Value',
        'FV %': 0,
        None: 'Blended',
        'Streak Basis': 'Declaration date',
        'Chowder Number': 15,
        'EPS 1Y': 80.25,
        'Revenue 1Y': 28.27,
        'NPM': 18.32,
        'CF/Share': 4.39,
        'ROE': 23.46,
        'Current R': 2.04,
        'Debt/Capital': 0.36,
        'ROTC': 12.69,
        'P/E': 32.99,
        'P/BV': 7.71,
        'PEG': 1.37,
        'New Member': None,
        'Industry': 'Life Sciences Tools and Services'
    },
    'AAPL': {
        'Symbol': 'AAPL',
        'Company': 'Apple Inc.',
        'FV': None,
        'Sector': 'Information Technology',
        'No Years': 11,
        'Price': 153.71,
        'Div Yield': 0.6,
        '5Y Avg Yield': 0.93,
        'Current Div': 0.23,
        'Payouts/ Year': 4,
        'Annualized': 0.92,
        'Previous Div': 0.22,
        'Ex-Date': datetime.datetime(2022, 5, 6, 0, 0),
        'Pay-Date': datetime.datetime(2022, 5, 12, 0, 0),
        'Low': 124.17,
        'High': 179.61,
        'DGR 1Y': 5.21,
        'DGR 3Y': 6.19,
        'DGR 5Y': 8.16,
        'DGR 10Y': 17.01,
        'TTR 1Y': -26.41,
        'TTR 3Y': 21.8,
        'Fair Value': 'At Fair Value',
        'FV %': 0,
        None: 'Blended',
        'Streak Basis': 'Ex-date',
        'Chowder Number': 9,
        'EPS 1Y': -2.57,
        'Revenue 1Y': 2.44,
        'NPM': 24.56,
        'CF/Share': 6.79,
        'ROE': 147.95,
        'Current R': 0.94,
        'Debt/Capital': 0.67,
        'ROTC': 39.3,
        'P/E': 21.97,
        'P/BV': 36.29,
        'PEG': 1.14,
        'New Member': None,
        'Industry': 'Technology Hardware, Storage and Peripherals'
    }
}


class TestReadConfigurations(unittest.TestCase):

    def test_radar_dict_to_table_conversion(self):
        test_data_frame = radar_dict_to_table(test_radar_dict)
        self.assertIsInstance(test_data_frame, pd.DataFrame)

    def test_radar_list_values_of_key_in_radar_dict(self):
        test_symbols_list = list_values_of_key_in_radar_dict(test_radar_dict, "Symbol")
        self.assertIsInstance(test_symbols_list, list)
        self.assertIn("A", test_symbols_list)
        self.assertIn("AAPL", test_symbols_list)
