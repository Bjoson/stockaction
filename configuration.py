"""
configuration.py

Configuration data used throughout the project

Author: Björn Johansson
Date: 2023-04-10
Version: 0.0.1
"""
import json

class Configuration:

    """The configuration json object, read from "stock_config.json"
    """
    stock_config_json = None


    def __init__(self):
        """Construct this class, read the config file if needed
        """
        if Configuration.stock_config_json is None:
            with open("stock_config.json") as config_file:
                Configuration.stock_config_json = json.load(config_file)


    def get_monitored_stocks(self):
        '''
        Get all stocks we are currently interested in
        Returns a list of dicts with keys "symbol" and "name"
        '''
        return Configuration.stock_config_json["monitored_stocks"]



if __name__ == "__main__":
    b = Configuration()
    for stock in b.get_monitored_stocks():
        print(f"stock name {stock['name']} symbol {stock['symbol']}")
