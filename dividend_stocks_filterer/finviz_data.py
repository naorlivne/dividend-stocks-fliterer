from datetime import datetime, timezone
import finviz
from cachetools import cached, TTLCache
from retrying import retry
import requests


@cached(cache=TTLCache(maxsize=2048, ttl=600))
@retry(wait_exponential_multiplier=2500, wait_exponential_max=10000, stop_max_attempt_number=10)
def get_finviz_data_for_tickers_tuple(tickers_list: tuple) -> tuple[datetime, dict]:
    """
    Takes a tuple of tickers and returns the relevant data for them from finvizfinance.

    :param tickers_list: the tuple of tickers you want the data for

    :return finvizfinance_query_date_time: the date and time in UTC finvizfinance was queried at
    :return filtered_radar_dict: A dict including all data for tickers requested
    """

    filtered_radar_dict = {}

    for stock_ticker in tickers_list:
        try:
            stock = finviz.get_stock(stock_ticker)

            wanted_stock_dict = {
                "Price": "Price",
                "Payout Ratio": "Payout",
                "Low": "52W Low",
                "High": "52W High",
                "P/BV": "P/B",
                "Debt/Equity": "Debt/Eq",
                "ROE": "ROE",
                "P/E": "P/E"
            }

            filtered_radar_dict[stock_ticker] = {}
            for wanted_stock_key, wanted_stock_value in wanted_stock_dict.items():
                try:
                    filtered_radar_dict[stock_ticker][wanted_stock_key] = stock[wanted_stock_value]
                except KeyError:
                    pass
        except requests.exceptions.HTTPError:
            pass

    finvizfinance_query_date_time = datetime.now(timezone.utc)
    return finvizfinance_query_date_time, filtered_radar_dict


def get_finviz_data_for_tickers_list(tickers_list: list) -> tuple[datetime, dict]:
    """
    A wrapper for get_yahoo_finance_data_for_tickers_tuple, only difference is it takes a list and turns it to tuple as
    an ugly but simple workaround for cache not liking lists

    :param tickers_list: the list of tickers you want the data for

    :return yahoo_finance_query_date_time: the date and time in UTC yahoo finance was queried at
    :return filtered_radar_dict: A dict including all data for tickers requested
    """

    return get_finviz_data_for_tickers_tuple(tuple(tickers_list))
