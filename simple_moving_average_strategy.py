"""
moving_average_strategy.py

Using rolling or exponential mean, to calculate buy and
sell points and calculating a total return using the method.

Author: Björn Johansson
Date: 2023-04-12
"""

import configuration
import numpy as np
import matplotlib.pyplot as plt
import matplotlib.dates as mdates
import matplotlib.ticker as ticker
import pandas as pd
import utilities
from collections import namedtuple
import bisect

class simple_moving_average_strategy:

    def __init__(self):
        """Constructor
        """
        self.best_sma = None
        self.best_lma = None


    def set_params(self, sv, params_to_set):
        """Given params as returned from find_best_parameters, restore the parameters

        Args:
            params_to_set (_type_): the parameters to set
        """
        self.set_signal_points( params_to_set[0], params_to_set[1], sv)


    def set_signal_points(self, short_sma, long_sma, sv):
        """Set the buy/sell signal points for the current parameters
        Args:
            short_sma (_type_): the short SMA timeframe, e.g. 25 days
            long_sma (_type_): the long SMA timeframe, e.g. 200 days
            sv (_type_): the values to use for the evaluation
        Return:
            the final cash using the given parameters
        """
        sv['short_sma'] = sv['Close'].rolling(window=short_sma).mean()
        sv['long_sma'] = sv['Close'].rolling(window=long_sma).mean()

        sv['signal'] = 0

        sv.iloc[short_sma:, sv.columns.get_loc('signal')] = np.where(sv['short_sma'][short_sma:] > sv['long_sma'][short_sma:], 1, -1)
        sv['signal'] = sv['signal'].where(sv['signal'].shift(1) != sv['signal'])


    def plot(self, sv, stock_name):
        """Plot the current data, including sell and buy points

        Args:
            sv (_type_): the values to use for the evaluation
            stock_name (string) : the name of the stock
        """
        utilities.plot_sell_buy_ma(sv, 'short_sma', 'long_sma',
                                   f"Short SMA {self.best_sma}",
                                   f"Long SMA {self.best_lma}",
                                   f"{stock_name} - simple moving average active trading")


    def find_best_parameters(self, sv, initial_capital):
        """Given history values, evaluate the best parameters for this strategy

        Args:
            sv (_type_): the history values to use for the evaluation
            initial_capital (_type_): initial capital to use for the simulation
        """
        ParamTuple = namedtuple('ParamTuple', ['return_amount', 'quick', 'long'])
        top_tuples = []

        best_params = None
        best_return = None

        #sort the best 10 tuples, if an 'almost as good version exists but with
        #better distance between short and long, use that one instead?!

        #for long_sma in range(10, 200, 5):
        #for long_sma in range(10, 80, 5):
        for long_sma in range(10, 20, 5):
            for short_sma in range(3, min(long_sma-5,50), 1):
                self.set_signal_points(short_sma, long_sma, sv)
                profit = utilities.calculate_return(sv, initial_capital)

                if best_return is None or profit > best_return:
                    best_params = (short_sma, long_sma)
                    best_return = profit
                    print(f"SMA Current best profit {best_return} at {best_params}")
                current_tuple = ParamTuple(profit, short_sma, long_sma)
                bisect.insort(top_tuples, current_tuple, key=lambda c:c[0])
                top_tuples = top_tuples[-10:]  #top 10

        self.best_sma = best_params[0]
        self.best_lma = best_params[1]
        print(f"SMA Best profit {best_return} at {best_params}")
        self.set_signal_points( best_params[0], best_params[1], sv)
        print(f"SMA best tuples {top_tuples}")
        return best_return, best_params


    def store_current_params(self, json_file_path):
        """store the current parameters in the given json file path
        Args:
            json_file_path (string) : path to where to store the data
        """
        sma_params = {}
        sma_params["short_moving_average"] = self.best_sma
        sma_params["long_moving_average"] = self.best_lma
        params = {}
        params["SMA_Parameters"] = sma_params
        utilities.update_json_file_data(json_file_path, params)


    def restore_params(self, json_file_path):
        """Restore parameters from the supplied json file path

        Args:
            json_file_path (string): the filepath to the json file
        Return:
            True if successful
        """
        try:
            sma_params = utilities.get_params_from_json_file(json_file_path, "SMA_Parameters")
            self.best_sma = sma_params["short_moving_average"]
            self.best_lma = sma_params["long_moving_average"]
            return True
        except:
            return False


