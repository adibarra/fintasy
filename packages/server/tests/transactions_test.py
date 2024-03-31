# @author: Mason Clark (maclark)
# @description: Test for the Transactions class

import unittest

from src.helpers.transactions import Transactions
from src.helpers.portfolio import Portfolio

class TestTransactionsMethods(unittest.TestCase):
    def setUp(self):
        self.portfolio = Portfolio()
        self.portfolio_name = self.portfolio.default_name()
        self.initial_balance = 1000

    def test_buy_transaction_execution(self):
        transaction = Transactions(self.portfolio, "Tech Co", 10, 50, "buy")
        transaction.execute()
        # Verify the balance is updated correctly and the stock is added
        self.assertEqual(self.portfolio.portfolios[self.portfolio_name]['balance'], self.initial_balance - 500)  # Adjust based on actual implementation
        self.assertTrue("Tech Co" in self.portfolio.portfolios[self.portfolio_name])  # Adjust based on actual implementation

    def test_sell_transaction_execution(self):
        self.portfolio.add_data(self.portfolio_name, "Tech Co", 10, 50, 0, 0)  # Adjust add_data method usage as necessary
        transaction = Transactions(self.portfolio, "Tech Co", 5, 60, "sell")
        transaction.execute()
        # Verify the balance is updated correctly and the stock quantity is updated
        self.assertEqual(self.portfolio.portfolios[self.portfolio_name]['balance'], self.initial_balance + 300)  # Adjust based on actual implementation
        self.assertEqual(self.portfolio.portfolios[self.portfolio_name]["Tech Co"]["qty"], 5)  # Adjust based on actual implementation

    def test_invalid_transaction_type(self):
        transaction = Transactions(self.portfolio, "Tech Co", 10, 50, "swap")
        self.assertRaises(ValueError, transaction.execute)

    def test_buy_transaction_insufficient_funds(self):
        low_initial_balance = 200 # Set a low initial balance
        self.portfolio.initialize_balance(self.portfolio_name)  # Reset or initialize the balance if  Portfolio supports it
        self.portfolio.change_balance(self.portfolio_name, low_initial_balance, 0)  # Set the low balance

        # Attempt to execute a buy transaction that exceeds available funds
        transaction = Transactions(self.portfolio, "Expensive Co", 5, 50, "buy")

        # Verify that a ValueError is raised due to insufficient funds
        self.assertRaises(ValueError, transaction.execute)

        # Additionally, verify that the balance remains unchanged after the failed transaction attempt
        self.assertEqual(self.portfolio.portfolios[self.portfolio_name]['balance'], low_initial_balance)  # Adjust based on actual implementation


    # Add more tests as needed for coverage

if __name__ == "__main__":
    unittest.main()
