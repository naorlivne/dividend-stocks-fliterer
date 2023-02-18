import pandas as pd


def radar_dict_to_table(radar_dict: dict) -> pd.DataFrame:
    """
    Takes a dict of the radar file and returns it as a dataframe to display in streamlit

    :param radar_dict: The dict of the data to work with

    :return radar_df: The dict but in table/dataframe form
    """
    radar_df = pd.DataFrame.from_dict(radar_dict, orient='index')
    return radar_df


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
