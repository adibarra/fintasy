# @author: mariptime (Akshay)
# @description: Testcases for the Quote class

import unittest
from datetime import datetime

from src.helpers.quote import Quote


class TestQuoteMethods(unittest.TestCase):
    def setUp(self):
        # Initialize any required objects or variables for testing
        self.quote_obj = Quote()

    def test_historical_graph_data_shown(self):
        """Test review_historical_prices with valid start and end dates"""
        start_date = "03/03/24"
        end_date = "03/05/24"
        expected_outcome = "Historical Graph and data shown"
        outcome = self.quote_obj.review_historical_prices(start_date, end_date)
        self.assertEqual(outcome, expected_outcome)

    def test_end_date_before_today(self):
        """Test review_historical_prices with end date after today's date"""
        start_date = "03/03/24"
        end_date = "03/26/24"
        expected_outcome = "End date must be before today's date"
        outcome = self.quote_obj.review_historical_prices(start_date, end_date)
        self.assertEqual(outcome, expected_outcome)

    def test_historical_graph_data_shown_2(self):
        """Test review_historical_prices with valid start and end dates"""
        start_date = "03/25/24"
        end_date = "03/25/24"
        expected_outcome = "Historical Graph and data shown"
        outcome = self.quote_obj.review_historical_prices(start_date, end_date)
        self.assertEqual(outcome, expected_outcome)

    def test_start_date_before_end_date(self):
        """Test review_historical_prices with start date after end date"""
        start_date = "03/10/24"
        end_date = "03/05/24"
        expected_outcome = "Start date must be before End Date"
        outcome = self.quote_obj.review_historical_prices(start_date, end_date)
        self.assertEqual(outcome, expected_outcome)

    def test_invalid_interval_get_historical_quotes(self):
        """Test get_historical_quotes with an invalid interval"""
        symbol = "AAPL"
        start_time = datetime(2024, 3, 3)
        end_time = datetime(2024, 3, 5)
        invalid_interval = "INVALID"
        with self.assertRaises(ValueError):
            self.quote_obj.get_historical_quotes(
                symbol, start_time, end_time, invalid_interval
            )

    def tearDown(self):
        # Clean up any resources used for testing
        pass


if __name__ == "__main__":
    unittest.main()
