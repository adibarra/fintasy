from datetime import datetime
from enum import Enum


class Quote:
    """
    Represents a quote for a symbol at a specific timestamp.
    """

    INTERVALS = Enum("INTERVALS", ["MINUTE", "HOUR", "DAY", "WEEK", "MONTH", "YEAR"])

    def __init__(self, symbol: str, price: int, timestamp: datetime):
        """
        Initializes a Quote object.

        Args:
            symbol (str): The symbol of the quote.
            price (float): The price of the symbol.
            timestamp (datetime): The timestamp of the quote.
        """
        self.symbol = symbol
        self.price = price
        self.timestamp = timestamp

    def get_quote(self):
        """
        Returns the quote information.

        Returns:
            dict: A dictionary containing the quote information.
        """
        return {
            "symbol": self.symbol,
            "price": self.price,
            "timestamp": self.timestamp.isoformat(),
        }

    @staticmethod
    def get_historical_quotes(
        symbol: str, start_time: datetime, end_time: datetime, interval: str
    ):
        """
        Gets historical quotes for a symbol within a specified time range and interval.

        Args:
            symbol (str): The symbol for which historical quotes are requested.
            start_time (datetime): The start time of the historical data range.
            end_time (datetime): The end time of the historical data range.
            interval (str): The interval for grouping price points (e.g., "MINUTE", "HOUR", "DAY", etc.).

        Returns:
            list: A list of historical quotes grouped by the specified interval.
        """
        if interval not in Quote.INTERVALS.__members__:
            raise ValueError("Invalid interval specified.")

        interval_seconds = {
            "MINUTE": 60,
            "HOUR": 3600,
            "DAY": 86400,
            "WEEK": 604800,
            "MONTH": 2628000,
            "YEAR": 31536000,
        }

        interval_seconds = interval_seconds[interval]

        # Simulate getting historical data (replace with actual data retrieval logic)
        historical_data = [
            {"timestamp": start_time + i * interval_seconds, "price": i * 10.0}
            for i in range(
                int((end_time - start_time).total_seconds() // interval_seconds)
            )
        ]

        return historical_data
