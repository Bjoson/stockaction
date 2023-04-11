"""
configuration.py

Configuration data used throughout the project

Author: Björn Johansson
Date: 2023-04-10
"""
import json

class Configuration:

    """The configuration json object, read from "stock_config.json"
    """
    config_json = None


    def __init__(self):
        """Construct this class, read the config file if needed
        """
        if Configuration.config_json is None:
            with open("stock_config.json") as config_file:
                Configuration.config_json = json.load(config_file)


    def get_monitored_stocks(self):
        '''
        Get all stocks we are currently interested in
        Returns a list of dicts with keys "symbol" and "name"
        '''
        return Configuration.config_json["monitored_stocks"]


    def get_proxy(self):
        """If a http proxy is needed, this function returns the proxy string, else None

        Returns:
            string: proxy address
        """
        return Configuration.config_json["proxy"]


    def get_current_software_version(self):
        """This function keeps track of the current software version
        """
        return "0.0.1"


if __name__ == "__main__":
    b = Configuration()
    for stock in b.get_monitored_stocks():
        print(f"stock name {stock['name']} symbol {stock['symbol']}")

    print(b.get_proxy())
