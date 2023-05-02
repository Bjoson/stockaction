"""
exponential_moving_average_strategy.py

Using exponential moving average (EMA) to calculate buy and
sell points and calculating a total return using this method.

Author: Björn Johansson
Date: 2023-04-24
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

class exponential_moving_average_strategy:

    def __init__(self):
        """Constructor
        """
        self.best_short_ema = None
        self.best_long_ema = None


    def set_params(self, sv, params_to_set):
        """Given params as returned from find_best_parameters, restore the parameters

        Args:
            params_to_set (_type_): the parameters to set
        """
        self.set_signal_points( params_to_set[0], params_to_set[1], sv)


    def set_signal_points(self, short_ema, long_ema, sv):
        """Set the buy/sell signal points for the current parameters
        Args:
            short_ema (int): the short EMA timeframe, e.g. 25 days
            long_ema (int): the long EMA timeframe, e.g. 200 days
            sv (pandas): the values to use for the evaluation
        Return:
            the final cash using the given parameters
        """
        sv['short_ema'] = sv['Close'].ewm(span=short_ema, adjust=False).mean()
        sv['long_ema'] = sv['Close'].ewm(span=long_ema, adjust=False).mean()

        sv['signal'] = 0

        sv.iloc[short_ema:, sv.columns.get_loc('signal')] = np.where(sv['short_ema'][short_ema:] > sv['long_ema'][short_ema:], 1, -1)
        sv['signal'] = sv['signal'].where(sv['signal'].shift(1) != sv['signal'])


    def plot(self, sv, stock_name):
        """Plot the current data, including sell and buy points

        Args:
            sv (pandas): the values to use for the evaluation
            stock_name (string) : the name of the stock
        """
        utilities.plot_sell_buy_ma(sv, 'short_ema', 'long_ema',
                                   f"Short EMA {self.best_short_ema}",
                                   f"Long EMA {self.best_long_ema}",
                                   f"{stock_name} - exponential moving average active trading")


    def find_best_parameters(self, sv, initial_capital):
        """Given history values, evaluate the best parameters for this strategy

        Args:
            sv (panda): the history values to use for the evaluation
            initial_capital (int): initial capital to use for the simulation
        """
        ParamTuple = namedtuple('ParamTuple', ['return_amount', 'quick', 'long'])
        top_tuples = []

        best_params = None
        best_return = None

        #sort the best 10 tuples, if an 'almost as good version exists but with
        #better distance between short and long, use that one instead?!

        #for long_sma in range(10, 200, 5):
        for long_ema in range(10, 80, 5):
            for short_ema in range(3, min(long_ema-5,50)+1, 1):
                self.set_signal_points(short_ema, long_ema, sv)
                profit = utilities.calculate_return(sv, initial_capital)

                if best_return is None or profit > best_return:
                    best_params = (short_ema, long_ema)
                    best_return = profit
                    print(f"EMA Current best profit {best_return} at {best_params}")
                current_tuple = ParamTuple(profit, short_ema, long_ema)
                bisect.insort(top_tuples, current_tuple, key=lambda c:c[0])
                top_tuples = top_tuples[-10:]  #top 10

        self.best_short_ema = best_params[0]
        self.best_long_ema = best_params[1]
        print(f"EMA Best profit {best_return} at {best_params}")
        self.set_signal_points( best_params[0], best_params[1], sv)
        print(f"EMA best tuples {top_tuples}")
        return best_return, best_params
