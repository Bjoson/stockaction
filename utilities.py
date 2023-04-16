"""
utilities.py

Utility functions data used throughout the project

Author: Björn Johansson
Date: 2023-04-16
"""

from configuration import Configuration


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



if __name__ == "__main__":
    print(buy_max_shares(50, 50))

