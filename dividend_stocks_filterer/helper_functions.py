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


def min_max_value_of_any_stock_key(radar_dict: dict, key: str, min_or_max: str) -> float:
    """
    Takes a dict of the radar file and returns the highest/lowest price of any stock in it, ignores None values

    :param radar_dict: The dict of the data to work with
    :param key: The key of the stock to return the max/min value of
    :param min_or_max: if to return min or max

    :return min_max_key_value: the highest/lowest value of any stock in the dict key

    :raise ValueError: if min_or_max isn't min or max which are it's only allowed values
    """
    value_list = list_values_of_key_in_radar_dict(radar_dict, key)
    if min_or_max == "max":
        min_max_key_value = max(x for x in value_list if x is not None)
    elif min_or_max == "min":
        min_max_key_value = min(x for x in value_list if x is not None)
    else:
        raise ValueError
    return float(min_max_key_value)
