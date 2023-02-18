def filter_dividend_paid_years_in_row(radar_dict: dict, min_years_in_row_paid: int) -> dict:
    """
    Takes a dict of the radar file and returns subset of it of only those that have paid over the given number of years

    :param radar_dict: The dict of the data to work with
    :param min_years_in_row_paid: the minimum number of years to have paid dividends in a row

    :return filtered_radar_dict: The dict but in table/dataframe form
    """
    filtered_radar_dict = {}
    for key, value in radar_dict.items():
        if value["No Years"] >= min_years_in_row_paid:
            filtered_radar_dict[key] = value
    return filtered_radar_dict


def filter_exclude_symbols(radar_dict: dict, excluded_symobls_list: list) -> dict:
    """
    Takes a dict of the radar file and returns subset of it without those on the excluded list

    :param radar_dict: The dict of the data to work with
    :param excluded_symobls_list: list of stock symbols to exclude

    :return filtered_radar_dict: The dict but in table/dataframe form
    """
    filtered_radar_dict = {}
    for key, value in radar_dict.items():
        if value["Symbol"] not in excluded_symobls_list:
            filtered_radar_dict[key] = value
    return filtered_radar_dict
