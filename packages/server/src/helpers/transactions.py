# @author: Mason Clark (maclark)
# @description: Transactions class for handling buy and sell transactions in a portfolio
# The class is responsible for executing transactions and updating the portfolio accordingly


def __init__(self, portfolio, company_name, qty, unit_price, transaction_type):
    """
    Initializes a new transaction.

    Args:
        portfolio (Portfolio): The portfolio to which this transaction applies.
        company_name (str): The name of the company involved in the transaction.
        qty (int): The quantity of stocks bought or sold.
        unit_price (float): The price per stock unit at the time of the transaction.
        transaction_type (str): The type of transaction, either 'buy' or 'sell'.
    """
    self.portfolio = portfolio
    self.company_name = company_name
    self.qty = qty
    self.unit_price = unit_price
    self.transaction_type = transaction_type


def execute(self):
    """
    Executes the transaction, updating the portfolio accordingly.
    """
    if self.transaction_type == "buy":
        self._buy_stock()
    elif self.transaction_type == "sell":
        self._sell_stock()
    else:
        raise ValueError("Invalid transaction type")


def _buy_stock(self):
    """
    Handles the logic for buying stock, updating the portfolio's balance and holdings.
    """
    total_cost = self.qty * self.unit_price
    if self.portfolio.balance >= total_cost:
        self.portfolio.add_stock(self.company_name, self.qty, self.unit_price)
        # Deduct the total cost of the purchased stocks from the portfolio's balance
        self.portfolio.update_balance(-total_cost)
    else:
        raise ValueError("Insufficient funds for transaction")


def _sell_stock(self):
    """
    Handles the logic for selling stock, updating the portfolio's balance and holdings.
    """
    # Assume the Portfolio class has methods 'remove_stock' and 'update_balance'
    if self.portfolio.has_stock(self.company_name, self.qty):
        self.portfolio.remove_stock(self.company_name, self.qty)
        self.portfolio.update_balance(self.qty * self.unit_price)
    else:
        raise ValueError("Insufficient stock quantity for transaction")
