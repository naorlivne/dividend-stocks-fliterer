def filter_dividend_key_over_or_under_value(radar_dict: dict, value_to_filter: int, key_to_filter: str,
                                            over_or_under: str) -> dict:
    """
    Takes a dict of the key and returns all values over or under the specific value

    :param radar_dict: The dict of the data to work with
    :param value_to_filter: the value to use as the base to work from
    :param key_to_filter: the key to use as the base to work from
    :param over_or_under: valid values are "over" for everything bigger or equal to value or "under" for everything
    equal or smaller then value

    :return filtered_radar_dict: The subset dict

    :raise ValueError: if over_or_under isn't over or under which are it's only allowed values
    """
    filtered_radar_dict = {}
    for key, value in radar_dict.items():
        if value[key_to_filter] is None:
            filtered_radar_dict[key] = value
        else:
            if over_or_under == "over":
                if value[key_to_filter] >= value_to_filter:
                    filtered_radar_dict[key] = value
            elif over_or_under == "under":
                if value[key_to_filter] <= value_to_filter:
                    filtered_radar_dict[key] = value
            else:
                raise ValueError
    return filtered_radar_dict


def filter_exclude_values_of_key(radar_dict: dict, excluded_values: list, excluded_key: str) -> dict:
    """
    Takes a dict of the radar file and returns subset of it without those on the excluded list

    :param radar_dict: The dict of the data to work with
    :param excluded_values: list of values to exclude
    :param excluded_key: the key who value should be excluded

    :return filtered_radar_dict: The subset dict
    """
    filtered_radar_dict = {}
    for key, value in radar_dict.items():
        if value[excluded_key] not in excluded_values:
            filtered_radar_dict[key] = value
    return filtered_radar_dict


def filter_dividend_key_in_range(radar_dict: dict, min_price_range: float, max_price_range: float, stocks_key: str) -> \
        dict:
    """
    Takes a dict of the radar file and returns subset of it of only those that have paid over the given number of years

    :param radar_dict: The dict of the data to work with
    :param min_price_range: the minimum value of stocks key to show
    :param max_price_range: the maximum value of stocks key to show
    :param stocks_key: the stock key to filter by

    :return filtered_radar_dict:  The subset dict
    """
    filtered_radar_dict = {}
    for key, value in radar_dict.items():
        if value[stocks_key] is not None:
            if min_price_range <= value[stocks_key] <= max_price_range:
                filtered_radar_dict[key] = value
    return filtered_radar_dict


def remove_unneeded_columns(radar_dict: dict, unneeded_column_list: list) -> dict:
    """
    Takes a dict of the radar file and returns it with the unneeded columns removed

    :param radar_dict: The dict of the data to work with
    :param unneeded_column_list: list of columns to remove

    :return radar_dict: The dict with the keys in unneeded_column_list removed from it
    """
    for key_to_remove in unneeded_column_list:
        for dict_value in radar_dict.values():
            dict_value.pop(key_to_remove, None)
    return radar_dict
