import unittest
import datetime

from src.services.alpaca import AlpacaService


class TestAlpaca(unittest.TestCase):
    def test_invalid_quote(self):
        """Test Alpaca API Latest Quotes with invalid info"""

        invalidSymbol = "invalidSym"
        self.assertIsNone(AlpacaService.get_quote(invalidSymbol))

    def test_valid_quote(self):
        """Test Alpaca API Latest Quotes with valid info"""

        validSymbol = "AAPL"
        self.assertIsNotNone(AlpacaService.get_quote(validSymbol))

    def test_historical_interval(self):
        """ Test Historical Quote interval"""
        # Test case for a custom interval
        a1 = AlpacaService.get_historical_quote("TSLA", datetime(2023, 10, 3), datetime(2023, 10, 5), "15m", quote_limit=100)
        self.assertIsNotNone(a1)
        # Test case for an invalid custom interval (should default to 5 minutes)
        a2 = AlpacaService.get_historical_quote("AAPL", datetime(2023, 10, 3), datetime(2023, 10, 5), "22m", quote_limit=100)
        a3 = AlpacaService.get_historical_quote("AAPL", datetime(2023, 10, 3), datetime(2023, 10, 5), "5m", quote_limit=100)
        self.assertDictEqual(a2, a3)

    def test_historical_limit(self):
        """ Test Historical Quote limit """
        # Test case for a custom quote limit
        b1 = AlpacaService.get_historical_quote("TSLA", datetime(2023, 5, 3), datetime(2023, 5, 5), quote_limit=3)
        self.assertIsNotNone(b1)
        # Test case for a very high quote limit
        b2 = AlpacaService.get_historical_quote("AAPL", datetime(2023, 5, 3), datetime(2023, 5, 5), quote_limit=10000)
        self.assertIsNotNone(b2)
        # Test with negative quote limit (should raise ValueError)
        with self.assertRaises(ValueError):
            AlpacaService.get_historical_quote("TSLA", datetime(2023, 5, 3), datetime(2023, 5, 5), quote_limit=-3)
        # Test with non-integer quote limit (should raise ValueError)
        with self.assertRaises(ValueError):
            AlpacaService.get_historical_quote("TSLA", datetime(2023, 5, 3), datetime(2023, 5, 5), quote_limit="invalid")

    def test_historical_offset(self):
        """ Test Historical Quote offset"""
        # Test with valid offset
        c1 = AlpacaService.get_historical_quote("AAPL", datetime(2023, 6, 3), datetime(2023, 6, 6), quote_limit=20, offset=2)
        self.assertIsNotNone(c1)
        # Test with negative offset (should raise ValueError)
        with self.assertRaises(ValueError):
            AlpacaService.get_historical_quote("AAPL", datetime(2023, 6, 3), datetime(2023, 6, 6), quote_limit=20, offset=-2)
        # Test with non-integer offset (should raise ValueError)
        with self.assertRaises(ValueError):
            AlpacaService.get_historical_quote("AAPL", datetime(2023, 6, 3), datetime(2023, 6, 6), quote_limit=20, offset="invalid")


if __name__ == "__main__":
    unittest.main()
