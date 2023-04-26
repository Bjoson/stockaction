"""
analayze_data.py

This script analyses the stock data and creates buy/sell recommendations in
the form of image graphs.

Author: Björn Johansson
Date: 2023-04-11
"""
from datetime import datetime
import os
from configuration import Configuration
import yfinance as yf
import pandas as pd
from simple_moving_average_strategy import simple_moving_average_strategy as sma
from exponential_moving_average_strategy import exponential_moving_average_strategy as ema
from buy_and_hold_strategy import buy_and_hold_strategy as bhs
class StockAnalyzer:

    def __init__(self):
        """Constructor
        """
        self.output_folder = None
        self.configuration = Configuration()
        self.data_path = "./stock_data"
        if not os.path.exists(self.data_path):
            os.makedirs(self.data_path)


    def get_csv_path(self, stock):
        """Get the csv data path for the given stock

        Args:
            stock (dictionary): the stock to get the data path for
        """
        return f"{self.data_path}/{stock['name']}.csv"


    def download_all_data(self):
        """Download the stock data for all monitored stocks

        Args:
            data_path (string): absolute or relative path to where to save the data
        """
        proxy = self.configuration.get_proxy()
        for stock in self.configuration.get_monitored_stocks():
            stock_data = yf.download(stock["symbol"] ,period="max", proxy=proxy)
            temp_data = stock_data.copy(deep=True)
            temp_data.to_csv(self.get_csv_path(stock))


    def create_output_folder(self):
        """Create an output folder where to place the generated graphs
        """
        self.output_folder = "./" + datetime.now().strftime("%Y_%m_%d")
        if not os.path.exists(self.output_folder):
            os.makedirs(self.output_folder)


    def analyze_all(self):
        """Analyze all monitored stocks.
        """
        self.create_output_folder()
        for stock in self.configuration.get_monitored_stocks():
            print(f"Analyzing {stock['name']}")
            history_values = pd.read_csv(self.get_csv_path(stock))
            history_values = history_values[-self.configuration.get_num_days_to_analyze():]
            history_values.reset_index(inplace=True)
            history_values.set_index('Date')
            c = bhs()
            bh_return = c.evaluate_strategy(history_values, self.configuration.get_initial_cash_for_simulation())
            a = sma()
            sma_return, sma_params = a.find_best_parameters(history_values, self.configuration.get_initial_cash_for_simulation())
            b = ema()
            ema_return, ema_params = b.find_best_parameters(history_values, self.configuration.get_initial_cash_for_simulation())

            plot_values = history_values.tail(self.configuration.get_num_days_to_plot()).copy()
            max_active = max(sma_return, ema_return)
            if bh_return > max_active:
                c.plot(history_values, stock['name'])
            else:
                if sma_return > ema_return:
                    a.set_params(plot_values, sma_params)
                    a.plot(plot_values, stock['name'])
                else:
                    b.set_params(plot_values, ema_params)
                    b.plot(plot_values, stock['name'])
            break


    def find_best_strategy(self, history_values):
        """Try all known strategies, keep the one returning the most

        Args:
            history_values (panda stock data): the values to analyze
        """
        pass


if __name__ == "__main__":
    sa = StockAnalyzer()
    #sa.download_all_data()
    sa.analyze_all()