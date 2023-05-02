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
import json

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


def sell_shares(stock_price, num_stocks):
    """Calculate the return when selling a stock. The transaction cost
    is removed

    Args:
        stock_price (float): the price of each stock
        num_stocks (int): the number of stocks to sell
    return the remaining cash, when transaction cost is deduced
    """
    conf = Configuration()
    sell_amount = stock_price*num_stocks
    transaction_cost = conf.get_transaction_cost(sell_amount)
    return sell_amount - transaction_cost


def plot_sell_buy_ma(sv, short_name, long_name, short_label, long_label, header):
    """Plot the current data, including sell and buy points

    Args:
        sv (panda): the values to use for the evaluation
        short_name (string): the name of the short strategy entry points in sv
        long_name (string): the name of the long strategy entry points in sv
        short_label (string): the graph label for the short strategy
        long_label (string): the graph label for the long strategy
        stock_name (string): the name of the stock currently being analyzed
    """
    sv.index = pd.to_datetime(sv['Date'])
    plt.figure(figsize=(12, 6))
    plt.plot(sv.index, sv['Close'], label='Close', alpha=0.5)
    if short_name is not None:
        plt.plot(sv[short_name], label=short_label, linestyle='--', alpha=0.7)
        plt.plot(sv[long_name], label=long_label, linestyle='--', alpha=0.7)

    buy_signals = sv[sv['signal'] == 1]
    sell_signals = sv[sv['signal'] == -1]

    plt.scatter(buy_signals.index, buy_signals['Close'], marker='^', color='g', label='Buy Signal', alpha=1)
    plt.scatter(sell_signals.index, sell_signals['Close'], marker='v', color='r', label='Sell Signal', alpha=1)

    plt.xlabel('Date')
    plt.ylabel('Close Price')
    plt.title(f'{header}')
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
    """Given history values including signal values, calculate the return.
    Assume that the actual buy or sell happens on the next trading day,
    since our data is available first after closing time.

    Args:
        sv (_type_): the history values to use for the evaluation
        start_cash (_type_): how much cash to start with
    """
    cash = initial_capital
    position = 0

    sv = sv.reset_index(drop=True)

    for index, row in sv.iterrows():
        signal = row['signal']
        stock_price = (row['Close'] + row['Open'])/2
        if (index + 1) < len(sv):
            frame = sv.iloc[index+1]
            stock_price = (frame['Open'] + frame['Close'])/2
        if 1 == signal:  # buy
            if cash <= 0:
                print("ERROR: buy signal but out of cash")
                return 0
            position, used_cash = buy_max_shares(cash, stock_price)
            cash -= used_cash
        elif signal == -1 and position > 0: #sell
            cash += sell_shares(stock_price, position)
            position = 0

    # undo the last buy if currently has a position
    # since strategy is based on only selling at sell-points
    if position > 0:
        cash += used_cash

    return cash


def calculate_midpoint_day_price(sv, target_date):
    """given history values, get the midpoint price for a particular day,
    this can be used as a rough estimate of the actual price that an active
    trader will pay for the stock.

    Args:
        sv (panda): history values
        date (string): which date to calculate, e.g. 1981-01-06
    """
   # Convert the 'Date' column to datetime format
    sv['Date'] = pd.to_datetime(sv['Date'])

    # Filter the daily data for the specific date
    filtered_data = sv[sv['Date'] == target_date]

    # Calculate the midpoint between the Open and Close prices
    midpoint = (filtered_data['Open'] + filtered_data['Close']) / 2

    return midpoint.iloc[0]


def update_json_file_data(json_file_path, new_data):
    """Write new data to a json file

    Args:
        json_file_path (string): path to the json file to create or update
        new_data (dict): the new data to write or update in the file
    """
    try:
        with open(json_file_path, "r") as json_file:
            data = json.load(json_file)
    except FileNotFoundError:
        data = {}

    # Update the data with new_data
    data.update(new_data)

    # Write the updated data back to the JSON file
    with open(json_file_path, "w") as json_file:
        json.dump(data, json_file, indent=4)


if __name__ == "__main__":
    #print(buy_max_shares(50, 50))

    history_values = pd.read_csv(f"./stock_data/apple.csv")
    date = "1981-01-06"
    print(calculate_midpoint_day_price(history_values, date))