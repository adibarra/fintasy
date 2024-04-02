import unittest

from src.helpers.quote import Quote


class TestQuoteMethods(unittest.TestCase):
    def setUp(self):
        # Initialize any required objects or variables for testing
        self.quote_obj = Quote()

    def test_validate_quote_symbol(self):
        # Test valid symbol
        valid_symbol = "AAPL"
        self.assertTrue(self.quote_obj.validate_quote_symbol(valid_symbol))

        # Test invalid symbol
        invalid_symbol = "invalid_symbol"
        self.assertFalse(self.quote_obj.validate_quote_symbol(invalid_symbol))

    def test_get_quote(self):
        # Test getting a quote for a valid symbol
        valid_symbol = "AAPL"
        self.assertIsNotNone(self.quote_obj.get_quote(valid_symbol))

        # Test getting a quote for an invalid symbol
        invalid_symbol = "invalid_symbol"
        self.assertIsNone(self.quote_obj.get_quote(invalid_symbol))

    def test_get_historical_quotes(self):
        # Test getting historical quotes with a valid symbol and interval
        valid_symbol = "AAPL"
        valid_interval = "1d"
        self.assertIsNotNone(
            self.quote_obj.get_historical_quotes(valid_symbol, valid_interval)
        )

        # Test getting historical quotes with an invalid symbol
        invalid_symbol = "invalid_symbol"
        valid_interval = "1d"
        self.assertIsNone(
            self.quote_obj.get_historical_quotes(invalid_symbol, valid_interval)
        )

        # Test getting historical quotes with an invalid interval
        valid_symbol = "AAPL"
        invalid_interval = "invalid_interval"
        self.assertIsNone(
            self.quote_obj.get_historical_quotes(valid_symbol, invalid_interval)
        )

    def tearDown(self):
        # Clean up any resources used for testing
        pass


if __name__ == "__main__":
    unittest.main()
