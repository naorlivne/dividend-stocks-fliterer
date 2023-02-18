import streamlit as st
from dividend_radar import *
from configure import  *


configuration = read_configurations()

radar_file = DividendRadar(
    dividend_radar_url = configuration["dividend_radar_download_url"],
    local_file = configuration["local_file_path"]
)
if radar_file.check_if_local_is_latest() is False:
    radar_file.download_latest_version()
    radar_dict = radar_file.read_radar_file_to_dict()

st.title('divifilter')
st.text("Radar file date: " + radar_file.latest_local_version)
