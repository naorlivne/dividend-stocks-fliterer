import streamlit as st
from dividend_radar import *
from filterers import *
from configure import *
from helper_functions import *


configuration = read_configurations()

st.set_page_config(layout="wide", page_title="Divifilter - easily filter dividends stocks")
hide_streamlit_style = """
<style>
.block-container {
                    margin-top: -60px;
                    padding-bottom: 0rem;
                }
#MainMenu {visibility: hidden;}
footer {visibility: hidden;}
</style>
"""
st.markdown(hide_streamlit_style, unsafe_allow_html=True)

radar_file = DividendRadar(
    dividend_radar_url=configuration["dividend_radar_download_url"],
    local_file=configuration["local_file_path"]
)
if radar_file.check_if_local_is_latest() is False:
    radar_file.download_latest_version()

starting_radar_dict = radar_file.read_radar_file_to_dict()

st.title('Divifilter')
st.text("Radar file date: " + radar_file.latest_local_version)

radar_dict_filtered = starting_radar_dict

unneeded_columns = ["FV", "None", None, "Current R", "New Member"]
radar_dict_filtered = remove_unneeded_columns(radar_dict_filtered, unneeded_columns)

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

    # filter to only stocks with a chowder number over the selected value
    max_chowder_number_to_filter_1y_avg = min_max_value_of_any_stock_key(starting_radar_dict, "Chowder Number", "max")
    chowder_number = st.slider(min_value=0, max_value=int(min(max_chowder_number_to_filter_1y_avg, 25.0)),
                               key="min_chowder_number", value=0, label="Select minimum chowder number to display")
    radar_dict_filtered = filter_dividend_key_over_or_under_value(radar_dict_filtered, chowder_number, "Chowder Number",
                                                                  "over")

    # filter to only stocks with a EPS over the selected value
    max_eps_to_filter_1y_avg = min_max_value_of_any_stock_key(starting_radar_dict, "EPS 1Y", "max")
    min_eps_to_filter_1y_avg = min_max_value_of_any_stock_key(starting_radar_dict, "EPS 1Y", "min")
    min_eps = st.slider(min_value=min_eps_to_filter_1y_avg, key="min_eps_number", value=0.0,
                        max_value=max_eps_to_filter_1y_avg, label="Select minimum EPS over 1 year to display")
    radar_dict_filtered = filter_dividend_key_over_or_under_value(radar_dict_filtered, min_eps, "EPS 1Y", "over")

    # filter to only stocks with a revenue over 1y over the selected value
    max_revenue_1y_avg_to_filter_1y_avg = min_max_value_of_any_stock_key(starting_radar_dict, "Revenue 1Y", "max")
    min_revenue_1y_avg_to_filter_1y_avg = min_max_value_of_any_stock_key(starting_radar_dict, "Revenue 1Y", "min")
    min_revenue = st.slider(min_value=min_revenue_1y_avg_to_filter_1y_avg, key="min_revenue_1y_avg", value=0.0,
                            max_value=max_revenue_1y_avg_to_filter_1y_avg,
                            label="Select minimum revenue over 1 year to display")
    radar_dict_filtered = filter_dividend_key_over_or_under_value(radar_dict_filtered, min_revenue, "Revenue 1Y",
                                                                  "over")

    # filter to only stocks with a NPM percentage over the selected value
    max_npm_to_filter_1y_avg = min_max_value_of_any_stock_key(starting_radar_dict, "NPM", "max")
    min_npm_to_filter_1y_avg = min_max_value_of_any_stock_key(starting_radar_dict, "NPM", "min")
    min_npm = st.slider(min_value=min_npm_to_filter_1y_avg, key="min_npm_number", value=0.0,
                        max_value=max_npm_to_filter_1y_avg, label="Select minimum NPM % to display")
    radar_dict_filtered = filter_dividend_key_over_or_under_value(radar_dict_filtered, min_npm, "NPM", "over")

    # filter to only stocks with a cf/share over the selected value
    max_cf_per_share_to_filter_1y_avg = min_max_value_of_any_stock_key(starting_radar_dict, "CF/Share", "max")
    min_cf_per_share_to_filter_1y_avg = min_max_value_of_any_stock_key(starting_radar_dict, "CF/Share", "min")
    min_cf_per_share = st.slider(min_value=min_cf_per_share_to_filter_1y_avg, key="min_cf_per_share_number", value=0.0,
                                 max_value=max_cf_per_share_to_filter_1y_avg,
                                 label="Select minimum cf/share to display")
    radar_dict_filtered = filter_dividend_key_over_or_under_value(radar_dict_filtered, min_cf_per_share, "CF/Share",
                                                                  "over")
    # filter to only stocks with a ROE over the selected value
    max_roe_to_filter_1y_avg = min_max_value_of_any_stock_key(starting_radar_dict, "ROE", "max")
    min_roe_to_filter_1y_avg = min_max_value_of_any_stock_key(starting_radar_dict, "ROE", "min")
    min_roe = st.slider(min_value=min_roe_to_filter_1y_avg, key="min_roe_number", value=0.0,
                        max_value=max_roe_to_filter_1y_avg, label="Select minimum ROE to display")
    radar_dict_filtered = filter_dividend_key_over_or_under_value(radar_dict_filtered, min_roe, "ROE", "over")

# TODO - insert filter to with slider by p/bv

# TODO - insert filter to with slider by PEG

# TODO - insert filter to with slider by Debt/Capital

# TODO - insert toggles to enable/disable filters

# TODO - add payout ratio from somewhere else (yahoo finance? finviz?)

# TODO - add current data where relevant (price?) from somewhere (yahoo finance? finviz?)

# TODO - unit tests all full coverage

# TODO - run publicly open copy somewhere

# TODO - full CI/CD based on github actions - only deploying to whatever (northflank?) remains

# TODO - readme

# TODO - github link to website

# TODO - publicize & monetize somehow?

# TODO - https://tree-nation.com/offset-website

# TODO - add help field for every slider/selector/etc which explains what it is for

st.dataframe(radar_dict_to_table(radar_dict_filtered), use_container_width=True)

st.info("""
The information provided by Divifilter is for informational purposes only and should not be considered as financial 
advice. The information provided by Divifilter is not intended to provide investment advice or recommendations. Users 
are solely responsible for their own investment decisions.

Divifilter is not affiliated with any financial institution or investment company. The accuracy of the data provided 
by Divifilter cannot be guaranteed and is subject to change without notice.

By using Divifilter you acknowledge that you have read and understand this legal notification. You agree to use the 
information provided by Divifilter at your own risk and agree to hold harmless the creators of Divifilter from any and 
all claims or damages arising from your use of Divifilter.
""", icon="ℹ️")
