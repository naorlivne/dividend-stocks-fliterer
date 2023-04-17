from parse_it import ParseIt


def read_configurations(config_folder: str = "config") -> dict:
    """
    Will create a config dict that includes all of the configurations for terraformize by aggregating from all valid
    config sources (files, envvars, cli args, etc) & using sane defaults on config params that are not declared

    Arguments:
        :param config_folder: the folder which all configuration file will be read from recursively

    Returns:
        :return config: a dict of all configurations needed for terraformize to work
    """
    print("reading config variables")

    config = {}
    parser = ParseIt(config_location=config_folder, recurse=True)
    config["dividend_radar_download_url"] = \
        parser.read_configuration_variable("dividend_radar_download_url",
                                           default_value="https://www.portfolio-insight.com/dividend-radar")
    config["local_file_path"] = parser.read_configuration_variable("local_file_path",
                                                                   default_value="/tmp/latest_dividend_radar.xlsx")
    return config
