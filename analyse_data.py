"""
analayse_data.py

This script analyses the stock data and creates buy/sell recommendations in
the form of image graphs.

Author: Björn Johansson
Date: 2023-04-11
"""
from datetime import datetime
import os
from configuration import Configuration
import yfinance as yf

class StockAnalyser:

    def __init__(self):
        """Constructor
        """
        self.output_folder = None
        self.configuration = Configuration()
        self.data_path = "./stock_data"
        if not os.path.exists(self.data_path):
            os.makedirs(self.data_path)


    def download_all_data(self, data_path):
        """Download the stock data for all monitored stocks

        Args:
            data_path (string): absolute or relative path to where to save the data
        """
        proxy = self.configuration.get_proxy()
        for stock in self.configuration.get_monitored_stocks():
            stock_data = yf.download(stock["symbol"] ,period="max", proxy=proxy)
            temp_data = stock_data.copy(deep=True)
            temp_data.to_csv(f"{data_path}{stock['name']}.csv")

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





if __name__ == "__main__":
    sa = StockAnalyser()
    sa.analyze_all()