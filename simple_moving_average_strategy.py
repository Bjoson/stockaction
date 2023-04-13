"""
simple_moving_average_strategy.py

Using rolling mean, or simple moving average (SMA) to calculate buy and
sell points and calculating a total return using this method.

Author: Björn Johansson
Date: 2023-04-12
"""

import configuration
import numpy as np
#import matplotlib
#matplotlib.use('agg')
import matplotlib.pyplot as plt
from pandas.plotting import scatter_matrix

class simple_moving_average_strategy:

    def __init__(self):
        """Constructor
        """
        pass

    def evaluate_strategy(self, short_sma, long_sma, sv, start_cash):
        """Calculate the return when using this strategy
        Args:
            short_sma (_type_): the short SMA timeframe, e.g. 25 days
            long_sma (_type_): the long SMA timeframe, e.g. 200 days
            sv (_type_): the values to use for the evaluation
            start_cash (_type_): how much cash to start with
        Return:
            the final cash using the given parameters
        """
        sv['short_sma'] = sv['Close'].rolling(window=short_sma).mean()
        sv['long_sma'] = sv['Close'].rolling(window=long_sma).mean()

        sv['signal'] = 0

        sv.iloc[short_sma:, sv.columns.get_loc('signal')] = np.where(sv['short_sma'][short_sma:] > sv['long_sma'][short_sma:], 1, -1)
        sv['signal'] = sv['signal'].where(sv['signal'].shift(1) != sv['signal'])


    def plot(self, sv):
        """Plot the current data, including se

        Args:
            sv (_type_): the values to use for the evaluation
        """
        plt.figure(figsize=(12, 6))
        plt.plot(sv['Close'], label='Close', alpha=0.5)
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
        plt.grid()
        plt.show()




# ## Agera
# import numpy as np
# import pandas as pd

# # ... (Samma kod som tidigare för att beräkna SMA och hitta köp- och säljsignaler)

# initial_capital = 1000.0
# capital = initial_capital
# shares = 0

# # Iterera över DataFrame och agera på köp- och säljsignaler
# for index, row in df.iterrows():
#     if row['Cross'] == 2:  # Köpsignal
#         shares_to_buy = capital // row['Close']
#         if shares_to_buy > 0:
#             cost = shares_to_buy * row['Close']
#             shares += shares_to_buy
#             capital -= cost
#     elif row['Cross'] == -2:  # Säljsignal
#         if shares > 0:
#             revenue = shares * row['Close']
#             capital += revenue
#             shares = 0

# # Sälj alla aktier vid sista säljpositionen
# if shares > 0:
#     last_sell_position = df.loc[df['Cross'] == -2].index[-1]
#     last_sell_price = df.loc[last_sell_position, 'Close']
#     capital += shares * last_sell_price
#     shares = 0

# total_assets = capital
# print(f"Initialkapital: {initial_capital:.2f} kr")
# print(f"Totala tillgångar: {total_assets:.2f} kr")

