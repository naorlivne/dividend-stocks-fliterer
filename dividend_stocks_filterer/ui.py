import streamlit as st
from dividend_radar import *
from filterers import *
from configure import *
from helper_functions import *


configuration = read_configurations()

radar_file = DividendRadar(
    dividend_radar_url=configuration["dividend_radar_download_url"],
    local_file=configuration["local_file_path"]
)
if radar_file.check_if_local_is_latest() is False:
    radar_file.download_latest_version()

starting_radar_dict = radar_file.read_radar_file_to_dict()

st.set_page_config(layout="wide", page_title="divifilter - easily filter dividends stocks")
hide_streamlit_style = """
<style>
#MainMenu {visibility: hidden;}
footer {visibility: hidden;}
</style>
"""
st.markdown(hide_streamlit_style, unsafe_allow_html=True)
st.title('divifilter')
st.text("Radar file date: " + radar_file.latest_local_version)

radar_dict_filtered = starting_radar_dict

with st.sidebar:
    # exclude stocks by symbols
    excluded_symbols = st.multiselect(label='Stock symbols to exclude', key="excluded_symbols",
                                      options=list_values_of_key_in_radar_dict(starting_radar_dict, "Symbol"))
    radar_dict_filtered = filter_exclude_values_of_key(radar_dict_filtered, excluded_symbols, "Symbol")

    # filter to only stocks with a dividend streak of over selected # of years
    min_streak_years = st.slider(label="Select minimum number of years of dividend streaks to display", min_value=5,
                                 max_value=50, value=18, key="min_dividend_streak_years")
    radar_dict_filtered = filter_dividend_key_over_or_under_value(radar_dict_filtered, min_streak_years, "No Years",
                                                                  "over")

    # exclude stocks by sector
    excluded_sectors = st.multiselect(label='Sector to exclude', key="excluded_sectors",
                                      options=list_values_of_key_in_radar_dict(starting_radar_dict, "Sector"))
    radar_dict_filtered = filter_exclude_values_of_key(radar_dict_filtered, excluded_sectors, "Sector")

    # exclude stocks by industry
    excluded_sectors = st.multiselect(label='Industry to exclude', key="excluded_industries",
                                      options=list_values_of_key_in_radar_dict(starting_radar_dict, "Industry"))
    radar_dict_filtered = filter_exclude_values_of_key(radar_dict_filtered, excluded_sectors, "Industry")

    # filter based on stock prices
    max_stock_price_to_filter = min_max_value_of_any_stock_key(starting_radar_dict, "Price", "max")
    price_range_min, price_range_max = st.slider(label="Select range of stock prices to filter by", min_value=1.0,
                                                 max_value=max_stock_price_to_filter, key="stock_price_range",
                                                 value=(1.0, max_stock_price_to_filter))
    radar_dict_filtered = filter_dividend_key_in_range(radar_dict_filtered, price_range_min, price_range_max, "Price")

    # filter based on yield, both current & 5y avg
    max_stock_yield_to_filter = min_max_value_of_any_stock_key(starting_radar_dict, "Div Yield", "max")
    max_stock_yield_to_filter_5y_avg = min_max_value_of_any_stock_key(starting_radar_dict, "5Y Avg Yield", "max")
    max_stock_yield_to_filter_highest_value = max([max_stock_yield_to_filter, max_stock_yield_to_filter_5y_avg])
    yield_range_min, yield_range_max = st.slider(label="Select range of stock dividends yield to filter by",
                                                 max_value=min(max_stock_yield_to_filter_highest_value, 25.0),
                                                 key="dividend_yield_range", min_value=0.0,
                                                 value=(0.0, min(max_stock_yield_to_filter_highest_value, 25.0)),
                                                 help="this will filter both by Div Yield & by 5y Avg Yield")
    radar_dict_filtered = filter_dividend_key_in_range(radar_dict_filtered, yield_range_min, yield_range_max,
                                                       "Div Yield")
    radar_dict_filtered = filter_dividend_key_in_range(radar_dict_filtered, yield_range_min, yield_range_max,
                                                       "5Y Avg Yield")

    # filter to only stocks with a DGR over the selected percentage% for 1,3,5 & 10 years
    max_stock_yield_to_filter_1y_avg = min_max_value_of_any_stock_key(starting_radar_dict, "DGR 1Y", "max")
    max_stock_yield_to_filter_3y_avg = min_max_value_of_any_stock_key(starting_radar_dict, "DGR 3Y", "max")
    max_stock_yield_to_filter_5y_avg = min_max_value_of_any_stock_key(starting_radar_dict, "DGR 5Y", "max")
    max_stock_yield_to_filter_10y_avg = min_max_value_of_any_stock_key(starting_radar_dict, "DGR 10Y", "max")
    max_stock_yield_to_filter_highest_value = max([max_stock_yield_to_filter_1y_avg, max_stock_yield_to_filter_3y_avg,
                                                   max_stock_yield_to_filter_5y_avg, max_stock_yield_to_filter_10y_avg])
    min_stock_yield_to_filter_1y_avg = min_max_value_of_any_stock_key(starting_radar_dict, "DGR 1Y", "min")
    min_stock_yield_to_filter_3y_avg = min_max_value_of_any_stock_key(starting_radar_dict, "DGR 3Y", "min")
    min_stock_yield_to_filter_5y_avg = min_max_value_of_any_stock_key(starting_radar_dict, "DGR 5Y", "min")
    min_stock_yield_to_filter_10y_avg = min_max_value_of_any_stock_key(starting_radar_dict, "DGR 10Y", "min")
    min_stock_yield_to_filter_highest_value = min([min_stock_yield_to_filter_1y_avg, min_stock_yield_to_filter_3y_avg,
                                                   min_stock_yield_to_filter_5y_avg, min_stock_yield_to_filter_10y_avg])
    min_dgr = st.slider(min_value=max(min_stock_yield_to_filter_highest_value, -25.0),
                        max_value=min(max_stock_yield_to_filter_highest_value, 25.0),
                        key="min_dgr", value=0.0, label="Select minimum DGR % to display",
                        help="this will filter the DGR % of 1,3,5 & 10 years (where applicable)")
    radar_dict_filtered = filter_dividend_key_over_or_under_value(radar_dict_filtered, min_dgr, "DGR 1Y", "over")
    radar_dict_filtered = filter_dividend_key_over_or_under_value(radar_dict_filtered, min_dgr, "DGR 3Y", "over")
    radar_dict_filtered = filter_dividend_key_over_or_under_value(radar_dict_filtered, min_dgr, "DGR 5Y", "over")
    radar_dict_filtered = filter_dividend_key_over_or_under_value(radar_dict_filtered, min_dgr, "DGR 10Y", "over")

    # filter to only stocks with a fair value under the selected percentage
    max_fair_value_to_filter_1y_avg = min_max_value_of_any_stock_key(starting_radar_dict, "FV %", "max")
    min_fair_value_to_filter_1y_avg = min_max_value_of_any_stock_key(starting_radar_dict, "FV %", "min")
    fair_value = st.slider(min_value=int(max(min_fair_value_to_filter_1y_avg, -25.0)),
                           max_value=int(max(max_fair_value_to_filter_1y_avg, 0.0)),
                           key="max_fair_value", value=0, label="Select maximum fair value % to display")
    radar_dict_filtered = filter_dividend_key_over_or_under_value(radar_dict_filtered, fair_value, "FV %", "under")

# TODO - insert filter to with slider by chowder number

# TODO - insert filter to with slider by EPS

# TODO - insert filter to with slider by revenue 1y

# TODO - insert filter to with slider by NPM

# TODO - insert filter to with slider cf/share

# TODO - insert filter to with slider by ROE

# TODO - insert filter to with slider by p/bv

# TODO - insert filter to with slider by PEG

# TODO - insert toggles to enable/disable filters

# TODO - add payout ratio from somewhere else (yahoo finance? finviz?)

# TODO - add current data where relevant (price?) from somewhere (yahoo finance? finviz?)

# TODO - clean up table from meaningless columns

# TODO - add necessary legalese notice this is not recommendation and assume no responsibility and such

# TODO - unit tests all full coverage

# TODO - dockerize

# TODO - run publicly open copy somewhere

# TODO - full CI/CD based on github actions

# TODO - readme

# TODO - FoSS (change github of repo to public)

# TODO - github tags

# TODO - publicize & monitize somehow?

st.dataframe(radar_dict_to_table(radar_dict_filtered), use_container_width=True)
