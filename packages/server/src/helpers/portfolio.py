# @author: Caleb Kim (caleb-j-kim)
# @description: Portfolio class for handling portfolios
# Hello World! This is a test for the Fintasy project.

from enum import Enum


class Portfolio:
    """
    Create objects that will be sent to portfolio dashboard in the front end.
    *Portfolio Name: (Allow users to create new portfolios as long as the name of a portfolio doesn't already exist when the user requests to name their new portfolio it & allow for default portfolio name [Portfolio #])
    *Column Names: (Company Name, QTY / Quantity, Unit Price, Daily P/L, Total P/L)
    *Row Attributes: (Company Name, QTY / Quantity, Unit Price, Daily P/L, Total P/L) #replace with API
    """

    PORTFOLIO_VALID_CHARACTERS = (
        "abcdefghijklmnopqrstuvwxyzABCDEFGHIJKLMNOPQRSTUVWXYZ0123456789_"
    )
    PORTFOLIO_LENGTH_MIN = 1
    PORTFOLIO_LENGTH_MAX = 20

    ERROR_TYPES = Enum(
        "ERROR_TYPES",
        [
            "PORTFOLIO_SHORT",
            "PORTFOLIO_LONG",
            "PORTFOLIO_INVALID_CHARACTERS",
            "PORTFOLIO_NAME_EXISTS",
        ],
    )

    ERROR_MESSAGES = {
        ERROR_TYPES.PORTFOLIO_SHORT: "Portfolio name must be at least 1 character long",
        ERROR_TYPES.PORTFOLIO_LONG: "Portfolio name must be less than or equal to 20 characters long",
        ERROR_TYPES.PORTFOLIO_INVALID_CHARACTERS: "Portfolio name must contain only valid characters",
        ERROR_TYPES.PORTFOLIO_NAME_EXISTS: "Portfolio name must be unique",
        # TODO: move error messages from the code to here
    }

    def __init__(self):
        """
        Create a dictionary of portfolios that house the portfolio name and its attributes
        """
        self.portfolios = {}

    def default_name(self):
        """
        Returns:
            Default portfolio name that's unique & it's stored inside of the self dictionary.
        """
        i = 0
        while True:
            portfolio_name = f"Portfolio #{i}"
            if portfolio_name in self.portfolios:
                i = i + 1
            else:
                self.portfolios[portfolio_name] = portfolio_name
                return self.portfolios[portfolio_name]

    def validate_portfolio_name(self, portfolio_name: str):
        """
        Validates the given portfolio name.

        Args:
            portfolio_name (str): The portfolio to be validated.

        Returns:
            bool: True if the portfolio name is valid, False otherwise.

        Raises:
            ValueError: If the portfolio name is too short, too long, or contains invalid characters.
            ValueError: If the portfolio name is not unique.

        Updates:
            self.portfolios: Dictionary is updated with a new portfolio & it's name.
        """

        if len(portfolio_name) < Portfolio.PORTFOLIO_LENGTH_MIN:
            raise ValueError(
                Portfolio.ERROR_MESSAGES[Portfolio.ERROR_TYPES.PORTFOLIO_SHORT]
            )

        if len(portfolio_name) > Portfolio.PORTFOLIO_LENGTH_MAX:
            raise ValueError(
                Portfolio.ERROR_MESSAGES[Portfolio.ERROR_TYPES.PORTFOLIO_LONG]
            )

        for char in portfolio_name:
            if char not in Portfolio.PORTFOLIO_VALID_CHARACTERS:
                raise ValueError(
                    Portfolio.ERROR_MESSAGES[
                        Portfolio.ERROR_TYPES.PORTFOLIO_INVALID_CHARACTERS
                    ]
                )

        if portfolio_name in self.portfolios:
            raise ValueError("Portfolio name must be unique.")
        self.portfolios[portfolio_name] = portfolio_name
        return True

    def remove_portfolio(self, portfolio_name: str):
        """
        Args:
            portfolio_name (str): The portfolio name must exist inside of the dictionary.

        Raises:
            KeyError: If the portfolio name doesn't exist inside of the dictionary.

        Removes:
            portfolio_name: portfolio_name is removed from self.portfolios dictionary if it exists inside of the dictionary.
        """

        if portfolio_name not in self.portfolios:
            raise KeyError(
                "Portfolio does not exist.\nPlease try again and input a portfolio name that exists inside of the Fintasy Databases."
            )
        del self.portfolios[portfolio_name]
        return True

    def add_data(
        self,
        portfolio_name: str,
        company_name: str,
        qty: int,
        unit_price: float,
        daily_PL: float,
        total_PL: float,
    ):  # unit_price, dailyPL, and totalPL will be received through API later
        """
        Args:
            portfolio_name (str): The portfolio name must exist inside of the dictionary.
            company_name (str): The company name must contain only valid characters and is greater than one character.
            qty (int): The stock quantity must contain only valid integers.
            unit_price (float): The unit price must contain only valid float values.
            daily_PL (float): The daily PL must contain only valid float values.
            total_PL (float): The total PL must contain only valid float values.

        Raises:
            KeyError: If the portfolio name or company name doesn't exist inside of the dictionary.
            ValueError: If the company name contains invalid characters.
            ValueError: If the qty, unit price, dailyPL, or totalPL contains invalid values.

        Returns:
            Updated self.portfolios[portfolio_name] dictionary with updated values for key data.
        """
        if portfolio_name not in self.portfolios:
            raise KeyError(
                "Portfolio does not exist.\nPlease try again and input a portfolio name that exists inside of the Fintasy Databases."
            )

        if len(company_name) < Portfolio.PORTFOLIO_LENGTH_MIN:
            raise ValueError(
                "Company name must contain one or more characters inside of its name."
            )

        for char in company_name:
            if char not in Portfolio.PORTFOLIO_VALID_CHARACTERS:
                raise ValueError("Company name must contain only valid characters.")

        if qty < 0:
            raise ValueError(
                f"The quantity of {company_name}'s stock(s) must be greater than zero inside of this portfolio."
            )

        if unit_price < 0:
            raise ValueError(
                f"The unit price of {company_name}'s stock(s) must be greater than zero inside of this portfolio."
            )

        if daily_PL < 0:
            raise ValueError(
                f"The daily PL of {company_name}'s stock(s) must be greater than zero inside of this portfolio."
            )

        if total_PL < 0:
            raise ValueError(
                f"The daily PL of {company_name}'s stock(s) must be greater than zero inside of this portfolio."
            )

        self.portfolios[portfolio_name][company_name] = {
            "qty": qty,
            "unit_price": unit_price,
            "daily_PL": daily_PL,
            "total_PL": total_PL,
        }
        return True

    def initialize_balance(self, portfolio_name: str):
        """
        Args:
            portfolio_name (str): The portfolio must exist inside of the dictionary

        Raises:
            KeyError: If the portfolio name doesn't exist inside of the dictionary

        Creates:
            Initial balance of $500 USD inside of the portfolio.
        """

        if portfolio_name not in self.portfolios:
            raise KeyError(
                "Portfolio does not exist. \nPlease try again and input a portfolio name that exists inside of the Fintasy Databases."
            )
        self.portfolios[portfolio_name] = {"balance": 500}
        return True

    def change_balance(self, portfolio_name: str, balance: float, transaction: float):
        """
        Args:
            portfolio_name (str): The portfolio must exist inside of the dictionary
            transaction (float): The new must contain only valid float values or if it's greater than the portfolio's current balance.

        Raises:
            KeyError: If the portfolio name doesn't exist inside of the dictionary.
            ValueError: If the transaction contains invalid values.

        Returns:
            Updated balance amount for this portfolio.
        """

        if portfolio_name not in self.portfolios:
            raise KeyError(
                "Portfolio does not exist.\nPlease try again and input a portfolio name that exists inside of the Fintasy Databases."
            )

        if transaction < 0:
            raise ValueError("The transaction amount must be greater than $0.00.")

        updated_balance = balance - transaction

        if updated_balance < 0:
            raise ValueError(
                f"The transaction amount exceeds the {portfolio_name}'s balance. \nPlease try again"
            )

        self.portfolios[portfolio_name] = {"balance": updated_balance}
        return self.portfolios[portfolio_name][balance]

    def get_portfolio(self, portfolio_name: str):
        """
        Args:
            portfolio_name (str): The portfolio must exist inside of the dictionary.

        Raises:
            KeyError: If the portfolio name doesn't exist inside of the dictionary.

        Returns:
            Portfolio name that exists inside of the self.portfolios dictionary.
        """

        if portfolio_name not in self.portfolios:
            raise KeyError(
                "Portfolio does not exist.\nPlease try again and input a portfolio name that exists inside of the Fintasy Databases."
            )
        return self.portfolios[portfolio_name]

    def list_portfolios(self):
        """
        Returns:
            A list of portfolio names along with its other attributes.
        """
        print(list(self.portfolios.keys()))
        return list(self.portfolios.keys())
