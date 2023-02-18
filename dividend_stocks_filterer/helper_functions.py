import pandas as pd


def radar_dict_to_table(radar_dict: dict) -> pd.DataFrame:
    """
    Takes a dict of the radar file and returns it as a dataframe to display in streamlit

    :param radar_dict: The dict of the data to work with

    :return radar_df: The dict but in table/dataframe form
    """
    radar_df = pd.DataFrame.from_dict(radar_dict, orient='index')
    return radar_df


def list_values_of_key_in_radar_dict(radar_dict: dict, requested_key: str) -> list:
    """
    Takes a dict of the radar file and returns a list of the request key

    :param radar_dict: The dict of the data to work with
    :param requested_key: The key you want to list all options of

    :return values_list: The list of symbols in the radar dict
    """
    values_list = []
    for value in radar_dict.values():
        values_list.append(value[requested_key])
    return list(set(values_list))
