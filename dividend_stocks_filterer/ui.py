import streamlit as st
from dividend_radar import *
from filterers import *
from configure import *


configuration = read_configurations()

radar_file = DividendRadar(
    dividend_radar_url=configuration["dividend_radar_download_url"],
    local_file=configuration["local_file_path"]
)
if radar_file.check_if_local_is_latest() is False:
    radar_file.download_latest_version()

starting_radar_dict = radar_file.read_radar_file_to_dict()

st.set_page_config(layout="wide")
st.title('divifilter')
st.text("Radar file date: " + radar_file.latest_local_version)

radar_dict_filtered = starting_radar_dict

with st.sidebar:
    min_streak_years = st.slider(label="select minimum number of years of dividend streaks to display", min_value=5,
                                 max_value=50, value=18, key="min_dividend_streak_years")
    radar_dict_filtered = filter_dividend_paid_years_in_row(radar_dict_filtered, min_streak_years)

# TODO - insert filter to exclude tickers from the list

# TODO - insert filter to exclude sector

# TODO - insert filter to exclude industry

# TODO - insert filter with slider with min and max prices

# TODO - insert filter with slider with min and max div yield, note it will filter only if both div & 5y avg yield

# TODO - insert filter to filter with slider by DGR min only which will filter 1y, 3y, 5y & 10y DGR

# TODO - insert filter to filter with slider by fair value by fv%

# TODO - insert filter to with slider by chowder number

# TODO - insert filter to with slider by EPS

# TODO - insert filter to with slider by revenue 1y

# TODO - insert filter to with slider by NPM

# TODO - insert filter to with slider cf/share

# TODO - insert filter to with slider by ROE

# TODO - insert filter to with slider by p/bv

# TODO - insert filter to with slider by PEG

# TODO - insert toggles to enable/disable filters

# TODO - add payout ratio from somewhere else (yahoo finance?)

# TODO - add current data where relvent (price?) from somehwere (yahoo finance?)

st.dataframe(radar_dict_to_table(radar_dict_filtered), use_container_width=True)
