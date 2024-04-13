# @authors: caleb-j-kim (Caleb Kim), OsiddiquiProjects (Tinatsei Chingaya)
# @description: Test class for portfolio class

import unittest

from src.helpers.portfolio import Portfolio


class TestPortfolioMethods(unittest.TestCase):
    def setUp(self):
        # Initialize any required objects or variables for testing
        self.portfolio = Portfolio()
        self.portfolio_name = self.portfolio.default_name()
        self.initial_balance = 1000

    def test_default_name(self):
        # Test that the default name is returned
        self.assertEqual(self.portfolio.default_name(), "default")

    def test_validate_portfolio_name(self):
        self.assertRaisesRegex(
            ValueError,
            Portfolio.ERROR_MESSAGES[Portfolio.ERROR_TYPES.PORTFOLIO_SHORT],
            Portfolio.validate_portfolio_name,
            "",
        )
        self.assertTrue(Portfolio.validate_portfolio_name("P1"))
        self.assertTrue(Portfolio.validate_portfolio_name("Portfolio1"))
        self.assertRaisesRegex(
            ValueError,
            Portfolio.ERROR_MESSAGES[Portfolio.ERROR_TYPES.PORTFOLIO_LONG],
            Portfolio.validate_portfolio_name,
            "Portfolio1",
        )
        self.assertFalse(Portfolio.validate_portfolio_name("Portfolio-1"))
        self.assertRaisesRegex(
            ValueError,
            Portfolio.ERROR_MESSAGES[Portfolio.ERROR_TYPES.PORTFOLIO_INVALID],
            Portfolio.validate_portfolio_name,
            "Portfolio-1",
        )
        # checks to see if portfolio name is unique
        self.assertFalse(Portfolio.validate_portfolio_name("Portfolio1"))
        self.assertRaisesRegex(
            ValueError,
            Portfolio.ERROR_MESSAGES[Portfolio.ERROR_TYPES.PORTFOLIO_NAME_EXISTS],
            Portfolio.validate_portfolio_name,
            "Portfolio1",
        )

    def test_initialize_balance(self):
        # Test that the balance is initialized correctly
        self.portfolio.initialize_balance(self.portfolio_name)
        self.assertEqual(
            self.portfolio.portfolios[self.portfolio_name]["balance"],
            self.initial_balance,
        )

    def test_change_balance(self):
        # Test that the balance is updated correctly
        self.portfolio.change_balance(self.portfolio_name, 5, 0)
        self.assertEqual(
            self.portfolio.portfolios[self.portfolio_name]["balance"],
            self.initial_balance + 500,
        )

    def test_add_data(self):
        # Test that data is added correctly
        self.portfolio.add_data(self.portfolio_name, "Tech_Co", 10, 50, 0, 0)
        self.assertTrue("Tech_Co" in self.portfolio.portfolios[self.portfolio_name])
        self.portfolio.add_data("DNE", "Tech_Co", 10, 50, 0, 0)
        self.assertFalse(KeyError, "Portfolio does not exist.")
        self.portfolio.add_data(self.portfolio_name, "", 10, 50, 0, 0)
        self.assertFalse(
            ValueError,
            "Company name must contain one or more characters inside of its name.",
        )
        self.portfolio.add_data(self.portfolio_name, "Tech-Co", -10, 50, 0, 0)
        self.assertFalse(ValueError, "Company name must contain only valid characters")
        self.portfolio.add_data(self.portfolio_name, "Tech Co", 0, 50, 0, 0)
        self.assertFalse(ValueError, "Quantity must be greater than 0.")
        self.portfolio.add_data(self.portfolio_name, "Tech Co", 10, 0, 0, 0)
        self.assertFalse(ValueError, "Price must be greater than 0.")

    def test_update_data(self):
        # Test that data is updated correctly
        self.portfolio.add_data(self.portfolio_name, "Tech Co", 10, 50, 0, 0)
        self.portfolio.update_data(self.portfolio_name, "Tech Co", 5, 60, 0, 0)
        self.assertEqual(
            self.portfolio.portfolios[self.portfolio_name]["Tech Co"]["qty"], 5
        )

    def test_get_portfolio(self):
        # Test that the portfolio is returned correctly
        self.portfolio.add_data(self.portfolio_name, "Tech Co", 10, 50, 0, 0)
        self.assertIsNotNone(self.portfolio.get_portfolio(self.portfolio_name))

    def test_get_portfolio_data(self):
        # Test that the portfolio data is returned correctly
        self.portfolio.add_data
