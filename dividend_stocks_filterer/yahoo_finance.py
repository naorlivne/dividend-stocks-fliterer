import yfinance as yf
from retrying import retry
from cachetools import cached, TTLCache


@cached(cache=TTLCache(maxsize=2048, ttl=600))
@retry(wait_exponential_multiplier=2500, wait_exponential_max=10000, stop_max_attempt_number=10)
def get_yahoo_finance_data_for_tickers_tuple(tickers_tuple: tuple) -> dict:
    """
    Takes a tuple of tickers and returns the relevant data for them from yahoo_finance, have to use tuple because of
    caching hating lists

    :rtype: object
    :param tickers_tuple: the tuple of tickers you want the data for

    :return filtered_radar_dict: A dict including all data for tickers requested
    """

    filtered_radar_dict = {}
    tickers = yf.Tickers(list(tickers_tuple))

    for stock_ticker in tickers_tuple:
        # TODO - I stopped here checking which of the wanted_stock_dict below is really needed, the key is what the row
        # in divifilter is named and the value is what yahoo-finance returns to said value
        # TODO - also need to check the relation between what needed from yahoo finance to the name in divifilter as
        # I didn't check all names in divifilter  yet
        wanted_stock_dict = {
            "price": "currentPrice",
            "payoutRatio": "payoutRatio",
            "trailingPE": "trailingPE",
            "forwardPE": "forwardPE",
            "low": "fiftyTwoWeekLow",
            "high": "fiftyTwoWeekHigh",
            "trailingAnnualDividendRate": "trailingAnnualDividendRate",
            "trailingAnnualDividendYield": "trailingAnnualDividendYield",
            "profitMargins": "profitMargins",
            "bookValue": "bookValue",
            "priceToBook": "priceToBook",
            "netIncomeToCommon": "netIncomeToCommon",
            "trailingEps": "trailingEps",
            "forwardEps": "forwardEps",
            "pegRatio": "pegRatio",
            "debtToEquity": "debtToEquity",
            "revenuePerShare": "revenuePerShare",
            "returnOnAssets": "returnOnAssets",
            "returnOnEquity": "returnOnEquity",
            "earningsGrowth": "earningsGrowth",
            "revenueGrowth": "revenueGrowth"
        }
        filtered_radar_dict[stock_ticker] = {}
        for wanted_stock_key, wanted_stock_value in wanted_stock_dict.items():
            filtered_radar_dict[stock_ticker][wanted_stock_key] = \
                tickers.tickers[stock_ticker.upper()].info[wanted_stock_value]
    return filtered_radar_dict


def get_yahoo_finance_data_for_tickers_list(tickers_list: list) -> dict:
    """
    A wrapper for get_yahoo_finance_data_for_tickers_tuple, only difference is it takes a list and turns it to tuple as
    an ugly but simple workaround for cache not liking lists

    :param tickers_list: the list of tickers you want the data for

    :return filtered_radar_dict: A dict including all data for tickers requested
    """

    return get_yahoo_finance_data_for_tickers_tuple(tuple(tickers_list))
