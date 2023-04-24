"""
utilities.py

Utility functions data used throughout the project

Author: Björn Johansson
Date: 2023-04-16
"""

from configuration import Configuration
import pandas as pd
import matplotlib.pyplot as plt
import matplotlib.dates as mdates
import matplotlib.ticker as ticker


def buy_max_shares(cash, stock_price):
    """Given cash and a stock_price, calculate the maximum number of
    shares that we can buy, considering the transaction cost defined
    by the Configuration

    Args:
        cash (_type_): our current cash
        stock_price (_type_): the price of each stock
    return max_num_shares, total_transaction_cost
    """
    conf = Configuration()
    max_num_shares = cash // stock_price
    transaction_amount = max_num_shares * stock_price
    transaction_cost = conf.get_transaction_cost(transaction_amount)
    while transaction_amount + transaction_cost > cash:
        max_num_shares -= 1
        transaction_amount = max_num_shares * stock_price
        transaction_cost = conf.get_transaction_cost(transaction_amount)
    return max_num_shares, transaction_amount + transaction_cost


def plot_sell_buy_ma(sv, short_name, long_name, short_label, long_label, stock_name):
    """Plot the current data, including sell and buy points

    Args:
        sv (_type_): the values to use for the evaluation
    """
    sv.index = pd.to_datetime(sv['Date'])
    plt.figure(figsize=(12, 6))
    plt.plot(sv.index, sv['Close'], label='Close', alpha=0.5)
    plt.plot(sv[short_name], label=short_label, linestyle='--', alpha=0.7)
    plt.plot(sv[long_name], label=long_label, linestyle='--', alpha=0.7)

    buy_signals = sv[sv['signal'] == 1]
    sell_signals = sv[sv['signal'] == -1]

    plt.scatter(buy_signals.index, buy_signals['Close'], marker='^', color='g', label='Buy Signal', alpha=1)
    plt.scatter(sell_signals.index, sell_signals['Close'], marker='v', color='r', label='Sell Signal', alpha=1)

    plt.xlabel('Date')
    plt.ylabel('Close Price')
    plt.title(f'{stock_name} - Price with Buy and Sell Signals')
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


def calculate_return(sv, initial_capital):
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
            position, used_cash = buy_max_shares(cash, stock_price)
            cash -= used_cash
        elif signal == -1 and position > 0: #sell
            cash += position * stock_price
            position = 0

    # undo the last buy if currently has a position
    # since strategy is based on only selling at sell-points
    if position > 0:
        cash += used_cash

    return cash




if __name__ == "__main__":
    print(buy_max_shares(50, 50))

