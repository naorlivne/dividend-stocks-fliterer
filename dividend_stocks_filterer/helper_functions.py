import pandas as pd


def radar_dict_to_table(radar_dict: dict) -> pd.DataFrame:
    """
    Takes a dict of the radar file and returns it as a dataframe to display in streamlit

    :param radar_dict: The dict of the data to work with

    :return radar_df: The dict but in table/dataframe form
    """
    radar_df = pd.DataFrame.from_dict(radar_dict, orient='index')
    return radar_df


def list_symbols_in_radar_dict(radar_dict: dict) -> list:
    """
    Takes a dict of the radar file and returns it as a dataframe to display in streamlit

    :param radar_dict: The dict of the data to work with

    :return symbols_list: The list of symbols in the radar dict
    """
    symbols_list = []
    for key in radar_dict.keys():
        symbols_list.append(key)
    return symbols_list
