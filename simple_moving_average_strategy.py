"""
simple_moving_average_strategy.py

Using rolling mean, or simple moving average (SMA) to calculate buy and
sell points and calculating a total return using this method.

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

class simple_moving_average_strategy:

    def __init__(self):
        """Constructor
        """
        pass

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


    def plot(self, sv):
        """Plot the current data, including sell and buy points

        Args:
            sv (_type_): the values to use for the evaluation
        """
        sv.index = pd.to_datetime(sv['Date'])
        plt.figure(figsize=(12, 6))
        plt.plot(sv.index, sv['Close'], label='Close', alpha=0.5)
        plt.plot(sv['short_sma'], label="short_sma", linestyle='--', alpha=0.7)
        plt.plot(sv['long_sma'], label='long_sma', linestyle='--', alpha=0.7)

        buy_signals = sv[sv['signal'] == 1]
        sell_signals = sv[sv['signal'] == -1]

        plt.scatter(buy_signals.index, buy_signals['Close'], marker='^', color='g', label='Buy Signal', alpha=1)
        plt.scatter(sell_signals.index, sell_signals['Close'], marker='v', color='r', label='Sell Signal', alpha=1)

        plt.xlabel('Date')
        plt.ylabel('Close Price')
        plt.title(f'- Price with Buy and Sell Signals')
        plt.legend(loc='best')

        # Not too many x-axis labels
        sv.index = pd.to_datetime(sv['Date'])
        #sv.drop('Date', axis=1, inplace=True)
        ax = plt.gca()
        ax.xaxis.set_major_locator(ticker.MultipleLocator(base=50))  # Ändra 'base' för att justera avståndet mellan tick-labels
        ax.xaxis.set_major_formatter(mdates.DateFormatter('%Y-%m-%d'))
        plt.setp(ax.get_xticklabels(), rotation=45, ha='right')

        plt.grid()
        plt.tight_layout()
        plt.show()


    def calculate_return(self, sv, initial_capital):
        """Given history values including signal values, calculate the return

        Args:
            sv (_type_): the history values to use for the evaluation
            start_cash (_type_): how much cash to start with
        """
        cash = initial_capital
        position = 0.0

        for index, row in sv.iterrows():
            signal = row['signal']
            stock_price = row['Close']

            if 1 == signal:  # buy
                if cash <= 0:
                    print("ERROR: buy signal but out of cash")
                    return 0
                position, used_cash = utilities.buy_max_shares(cash, stock_price)
                cash -= used_cash
            elif signal == -1 and position > 0: #sell
                cash += position * stock_price
                position = 0

        # undo the last buy if currently has a position
        # since strategy is based on only selling at sell-points
        if position > 0:
            cash += used_cash

        return cash


    def find_best_parameters(self, sv, initial_capital):
        """Given history values, evaluate the best parameters for this strategy

        Args:
            sv (_type_): the history values to use for the evaluation
            initial_capital (_type_): initial capital to use for the simulation
        """
        best_params = None
        best_return = None
        short_values = range(3, 50, 1)
        long_values = range(25, 200, 5)

        #short_values = range(3, 50, 5)
        #long_values = range(25, 100, 10)

        for long_sma in long_values:
            for short_sma in short_values:
                if short_sma >= long_sma:
                    continue

                self.set_signal_points(short_sma, long_sma, sv)
                profit = self.calculate_return(sv, initial_capital)

                if best_return is None or profit > best_return:
                    best_params = (short_sma, long_sma)
                    best_return = profit
                    print(f"Current best profit {best_return} at {best_params}")

        print(f"Best profit {best_return} at {best_params}")
        self.set_signal_points( best_params[0], best_params[1], sv)