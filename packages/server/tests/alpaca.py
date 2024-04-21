import unittest

from alpaca import AlpacaService


class TestAlpaca(unittest.TestCase):
    def setUp(self):
        # Initialize SessionController object
        self.alpaca_service = AlpacaService()

    def test_invalid_latest_quote(self):
        """Test Alpaca API Latest Quotes with invalid info"""

        invalidSymbol = "invalidSym"
        self.assertIsNone(self.alpaca_service.get_latest_alpaca_quote(invalidSymbol))

    def test_valid_latest_quote(self):
        """Test Alpaca API Latest Quotes with valid info"""

        validSymbol = "AAPL"
        self.assertIsNotNone(self.alpaca_service.get_latest_alpaca_quote(validSymbol))

    def test_invalid_historical_quote(self):
        """Test Alpaca API Historical Quotes"""

        invalidSymbol = "invalidSym"
        self.assertIsNone(self.alpaca_service.get_latest_alpaca_quote(invalidSymbol))

    def test_valid_historical_quote(self):
        """Test Alpaca API Historical Quotes with valid info"""

        validSymbol = "AAPL"
        self.assertIsNotNone(
            self.alpaca_service.get_historical_alpaca_quote(validSymbol)
        )


if __name__ == "__main__":
    unittest.main()
