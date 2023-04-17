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


    def get_num_days_to_analyze(self):
        """Get the configured number of days to analyze
        """
        return Configuration.config_json["prior_days_to_analyze"]


    def get_num_days_to_plot(self):
        """Get the number of days to plot when plotting a stock
        """
        return Configuration.config_json["days_to_plot"]


    def get_initial_cash_for_simulation(self):
        """Get the initial cash to use for the validation of the sell/buy points
        """
        return Configuration.config_json["initial_cash_for_simulation"]


    def get_transaction_cost(self, transaction_amount):
        """Given a transaction amount, calculate the transaction cost

        Args:
            transaction_amount (float): how much to sell/buy for
        Return
            the cost for this transaction
        """
        if 0 == transaction_amount:
            return 0
        percentage_cost = transaction_amount * Configuration.config_json["transaction_percent_cost"]
        minimum_fixed_cost = Configuration.config_json["transaction_min_cost"]
        return max(percentage_cost, minimum_fixed_cost)


if __name__ == "__main__":
    b = Configuration()
    for stock in b.get_monitored_stocks():
        print(f"stock name {stock['name']} symbol {stock['symbol']}")

    print(b.get_proxy())
    print(b.get_num_days_to_analyze(), type(b.get_num_days_to_analyze()))
    print(b.get_num_days_to_plot())
    print(b.get_transaction_cost(12455))
