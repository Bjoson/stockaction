"""
buy_and_hold_strategy.py

Calculate the return of simply buying at the first available date
and never selling.

Author: Björn Johansson
Date: 2023-04-24
"""
import utilities

class buy_and_hold_strategy:

    def __init__(self):
        pass


    def evaluate_strategy(self, sv, initial_capital):
        """Given history values and initial cash, evaluate the return
        of this strategy

        Args:
            sv (pandas): the values to use for the evaluation
            initial_capital (int): initial capital to use for the simulation
        """
        first_frame = sv.iloc[0]
        buy_stock_price = (first_frame['Close'] + first_frame['Open'])/2
        num_stocks, cost = utilities.buy_max_shares(initial_capital, buy_stock_price)

        last_frame = sv.iloc[-1]
        sell_stock_price = (last_frame['Close'] + last_frame['Open'])/2
        end_cash = utilities.sell_shares(sell_stock_price, num_stocks)
        print(f"Buy and hold profit {end_cash}")
        return end_cash


    def plot(self, sv, stock_name):
        """Plot the current data, including sell and buy points

        Args:
            sv (pandas): the values to use for the evaluation
            stock_name (string) : the name of the stock
        """
        sv['signal'] = 0
        utilities.plot_sell_buy_ma(sv, None, None,
                                   "",
                                   "",
                                   f"{stock_name} - Buy and hold strategy")