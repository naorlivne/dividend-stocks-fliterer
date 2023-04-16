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

unneeded_columns = ["FV", "None", None, "Current R", "New Member", "Previous Div", "Streak Basis"]
radar_dict_filtered = remove_unneeded_columns(radar_dict_filtered, unneeded_columns)

with st.sidebar:

    # filter to only stocks with a dividend streak of over selected # of years
    min_streak_years = st.slider(label="Select minimum number of years of dividend streaks to display", min_value=5,
                                 max_value=50, value=18, key="min_dividend_streak_years",
                                 help="Choose the minimum number of consecutive years a stock has paid dividends to be "
                                      "displayed")
    radar_dict_filtered = filter_dividend_key_over_or_under_value(radar_dict_filtered, min_streak_years, "No Years",
                                                                  "over")

    # filter based on stock prices
    max_stock_price_to_filter = min_max_value_of_any_stock_key(starting_radar_dict, "Price", "max")
    price_range_min, price_range_max = st.slider(label="Select range of stock prices to filter by", min_value=1.0,
                                                 max_value=max_stock_price_to_filter, key="stock_price_range",
                                                 value=(1.0, max_stock_price_to_filter),
                                                 help="Select the minimum and maximum prices of stocks to display")
    radar_dict_filtered = filter_dividend_key_in_range(radar_dict_filtered, price_range_min, price_range_max, "Price")

    # filter based on yield, both current & 5y avg
    max_stock_yield_to_filter = min_max_value_of_any_stock_key(starting_radar_dict, "Div Yield", "max")
    max_stock_yield_to_filter_5y_avg = min_max_value_of_any_stock_key(starting_radar_dict, "5Y Avg Yield", "max")
    max_stock_yield_to_filter_highest_value = max([max_stock_yield_to_filter, max_stock_yield_to_filter_5y_avg])
    yield_range_min, yield_range_max = st.slider(label="Select range of stock dividends yield to filter by",
                                                 max_value=min(max_stock_yield_to_filter_highest_value, 25.0),
                                                 key="dividend_yield_range", min_value=0.0,
                                                 value=(0.0, min(max_stock_yield_to_filter_highest_value, 25.0)),
                                                 help="Use this slider to filter stocks by dividend yield, which is "
                                                      "the percentage of the stock's current value paid back as "
                                                      "dividends. This slider will also filter by 5-year average yield")
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
                        help="this will filter the DGR % (dividend growth rate - the percentage dividend increased) "
                             "of 1,3,5 & 10 years (where applicable)")
    radar_dict_filtered = filter_dividend_key_over_or_under_value(radar_dict_filtered, min_dgr, "DGR 1Y", "over")
    radar_dict_filtered = filter_dividend_key_over_or_under_value(radar_dict_filtered, min_dgr, "DGR 3Y", "over")
    radar_dict_filtered = filter_dividend_key_over_or_under_value(radar_dict_filtered, min_dgr, "DGR 5Y", "over")
    radar_dict_filtered = filter_dividend_key_over_or_under_value(radar_dict_filtered, min_dgr, "DGR 10Y", "over")

    # filter to only stocks with a fair value under the selected percentage
    max_fair_value_to_filter_1y_avg = min_max_value_of_any_stock_key(starting_radar_dict, "FV %", "max")
    min_fair_value_to_filter_1y_avg = min_max_value_of_any_stock_key(starting_radar_dict, "FV %", "min")
    fair_value = st.slider(min_value=int(max(min_fair_value_to_filter_1y_avg, -25.0)),
                           max_value=int(max(max_fair_value_to_filter_1y_avg, 0.0)),
                           key="max_fair_value", value=0, label="Select maximum fair value % to display",
                           help="This filter will only display stocks with a Fair Value Percentage (FV%) below the set "
                                "FV% indicates how much the company stock is judged to cost compared to its actual "
                                "worth")
    radar_dict_filtered = filter_dividend_key_over_or_under_value(radar_dict_filtered, fair_value, "FV %", "under")

    # filter to only stocks with a chowder number over the selected value
    max_chowder_number_to_filter_1y_avg = min_max_value_of_any_stock_key(starting_radar_dict, "Chowder Number", "max")
    chowder_number = st.slider(min_value=0, max_value=int(min(max_chowder_number_to_filter_1y_avg, 25.0)),
                               key="min_chowder_number", value=0, label="Select minimum chowder number to display",
                               help="Filters for stocks with a Chowder number of the given value or higher. Chowder "
                                    "number is a rule-based system used to identify dividend growth stocks with strong "
                                    "total return potential by combining dividend yield and dividend growth. A Chowder "
                                    "number of 12 or higher is generally considered a good value")
    radar_dict_filtered = filter_dividend_key_over_or_under_value(radar_dict_filtered, chowder_number, "Chowder Number",
                                                                  "over")

    # filter to only stocks with a EPS over the selected value
    max_eps_to_filter_1y_avg = min_max_value_of_any_stock_key(starting_radar_dict, "EPS 1Y", "max")
    min_eps_to_filter_1y_avg = min_max_value_of_any_stock_key(starting_radar_dict, "EPS 1Y", "min")
    min_eps = st.slider(min_value=min_eps_to_filter_1y_avg, key="min_eps_number", value=0.0,
                        max_value=max_eps_to_filter_1y_avg, label="Select minimum EPS growth over 1 year to display",
                        help="EPS stands for earning per share, how much a company earned for each share at the time"
                             "frame, this will filter to only companies with the given value has grown over the past "
                             "year or higher")
    radar_dict_filtered = filter_dividend_key_over_or_under_value(radar_dict_filtered, min_eps, "EPS 1Y", "over")

    # filter to only stocks with a revenue over 1y over the selected value
    max_revenue_1y_avg_to_filter_1y_avg = min_max_value_of_any_stock_key(starting_radar_dict, "Revenue 1Y", "max")
    min_revenue_1y_avg_to_filter_1y_avg = min_max_value_of_any_stock_key(starting_radar_dict, "Revenue 1Y", "min")
    min_revenue = st.slider(min_value=min_revenue_1y_avg_to_filter_1y_avg, key="min_revenue_1y_avg", value=0.0,
                            max_value=max_revenue_1y_avg_to_filter_1y_avg,
                            label="Select minimum revenue growth over 1 year to display",
                            help="this will filter to only companies who's revenues have grown at or over the given "
                                 "value")
    radar_dict_filtered = filter_dividend_key_over_or_under_value(radar_dict_filtered, min_revenue, "Revenue 1Y",
                                                                  "over")

    # filter to only stocks with a NPM percentage over the selected value
    max_npm_to_filter = min_max_value_of_any_stock_key(starting_radar_dict, "NPM", "max")
    min_npm_to_filter = min_max_value_of_any_stock_key(starting_radar_dict, "NPM", "min")
    min_npm = st.slider(min_value=min_npm_to_filter, key="min_npm_number", value=0.0,
                        max_value=max_npm_to_filter, label="Select minimum NPM % to display",
                        help="NPM stands for net profit margin, calculated by dividing earnings after taxes by net "
                             "revenue, and multiplying the total by 100%. The higher the ratio, the more cash the "
                             "company has available to distribute to shareholders or invest in new opportunities")
    radar_dict_filtered = filter_dividend_key_over_or_under_value(radar_dict_filtered, min_npm, "NPM", "over")

    # filter to only stocks with a cf/share over the selected value
    max_cf_per_share_to_filter = min_max_value_of_any_stock_key(starting_radar_dict, "CF/Share", "max")
    min_cf_per_share_to_filter = min_max_value_of_any_stock_key(starting_radar_dict, "CF/Share", "min")
    min_cf_per_share = st.slider(min_value=min_cf_per_share_to_filter, key="min_cf_per_share_number", value=0.0,
                                 max_value=max_cf_per_share_to_filter, label="Select minimum cf/share to display",
                                 help="cf/share stands for cash flow per share,  the after-tax earnings plus "
                                      "depreciation on a per-share basis that functions as a measure of a firm's "
                                      "financial strength. Many financial analysts place more emphasis on cash flow "
                                      "per share than on earnings per share")
    radar_dict_filtered = filter_dividend_key_over_or_under_value(radar_dict_filtered, min_cf_per_share, "CF/Share",
                                                                  "over")
    # filter to only stocks with a ROE over the selected value
    max_roe_to_filter = min_max_value_of_any_stock_key(starting_radar_dict, "ROE", "max")
    min_roe_to_filter = min_max_value_of_any_stock_key(starting_radar_dict, "ROE", "min")
    min_roe = st.slider(min_value=min_roe_to_filter, key="min_roe_number", value=0.0,
                        max_value=max_roe_to_filter, label="Select minimum ROE to display",
                        help="ROE (return on equity) is equal to a fiscal year net income, divided by total equity, "
                             "expressed as a percentage, this will filter to only companies who have an ROE over the "
                             "given value")
    radar_dict_filtered = filter_dividend_key_over_or_under_value(radar_dict_filtered, min_roe, "ROE", "over")

    # filter to only stocks with a p/bv under the selected value
    max_price_per_book_value_to_filter = min_max_value_of_any_stock_key(starting_radar_dict, "P/BV", "max")
    min_price_per_book_value_to_filter = min_max_value_of_any_stock_key(starting_radar_dict, "P/BV", "min")
    max_price_per_book_value = st.slider(min_value=min_price_per_book_value_to_filter,
                                         key="max_price_per_book_value_number",
                                         value=max_price_per_book_value_to_filter,
                                         max_value=max_price_per_book_value_to_filter,
                                         label="Select maximum P/BV to display",
                                         help="P/BV stands for price to book value, the ratio of the market value of a "
                                              "company's shares (share price) over its book value of equity. The book "
                                              "value of equity, in turn, is the value of a company's assets expressed "
                                              "on the balance sheet,  Traditionally, any value under 1.0 is considered "
                                              "desirable for value investors, indicating an undervalued stock may have "
                                              "been identified. However, some value investors may often consider "
                                              "stocks with a less stringent P/B value of less than 3.0 as their "
                                              "benchmark.")
    radar_dict_filtered = filter_dividend_key_over_or_under_value(radar_dict_filtered, max_price_per_book_value, "P/BV",
                                                                  "under")

    # filter to only stocks with a Debt/Capital under the selected value
    max_debt_per_capital_to_filter = min_max_value_of_any_stock_key(starting_radar_dict, "Debt/Capital", "max")
    max_debt_per_capital_value = st.slider(min_value=0.0, key="max_debt_per_capital_value",
                                           value=0.5, max_value=min(5.0, max_debt_per_capital_to_filter),
                                           label="Select maximum Debt/Capital to display",
                                           help="the debt to capital ratio, how much the company barrowed devided to "
                                                "how much it has, the lower the value to less the company owes compared"
                                                "to the assets is has, investors tend to like it to stay under 0.6 "
                                                "(6o%) but some go up to 0.8 (80%) or higher as debt can mean also a"
                                                "growing company which uses the debt to increase it's size")
    radar_dict_filtered = filter_dividend_key_over_or_under_value(radar_dict_filtered, max_debt_per_capital_value,
                                                                  "Debt/Capital", "under")

    # exclude stocks by symbols
    excluded_symbols = st.multiselect(label='Stock symbols to exclude', key="excluded_symbols",
                                      options=list_values_of_key_in_radar_dict(starting_radar_dict, "Symbol"),
                                      help="exclude specific stocks from your search")
    radar_dict_filtered = filter_exclude_values_of_key(radar_dict_filtered, excluded_symbols, "Symbol")

    # exclude stocks by sector
    excluded_sectors = st.multiselect(label='Sector to exclude', key="excluded_sectors",
                                      options=list_values_of_key_in_radar_dict(starting_radar_dict, "Sector"),
                                      help="exclude whole sectors from your search")
    radar_dict_filtered = filter_exclude_values_of_key(radar_dict_filtered, excluded_sectors, "Sector")

    # exclude stocks by industry
    excluded_sectors = st.multiselect(label='Industry to exclude', key="excluded_industries",
                                      options=list_values_of_key_in_radar_dict(starting_radar_dict, "Industry"),
                                      help="exclude whole industries from your search")
    radar_dict_filtered = filter_exclude_values_of_key(radar_dict_filtered, excluded_sectors, "Industry")

# TODO - add payout ratio, P/E, P/BV and PEG from yahoo finance (function is WIP, need to finish and use it in the code)

# TODO - add current data where relevant from yahoo finance (function is WIP, need to finish and use it in the code)

# TODO - add line of when was the last data pull from yahoo finance (datetime is created when function runs, just
# need to print it on the ui remains

# TODO - unit tests all full coverage and readme badge

# TODO - real DNS domain - current test domain is https://divifilter.naor.eu.org/

# TODO - readme

# TODO - github link to website

# TODO - publicize & monetize somehow?

# TODO - https://tree-nation.com/offset-website

# TODO - catragorize with header text titles the sidebar params and group them for easier finding

# TODO - some user analytics - google analytics in streamlit is too hacky right now

st.divider()

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
