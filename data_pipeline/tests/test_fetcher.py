import unittest
import pandas as pd
import sys
import os

# This is a bit of a hack to make sure the src module is on the path
# for the test runner. A better solution might involve a setup.py file.
sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))

from src.fetcher import fetch_stock_data

class TestFetcher(unittest.TestCase):

    def test_fetch_valid_ticker(self):
        """
        Test that fetching data for a valid ticker returns a non-empty DataFrame.
        """
        df = fetch_stock_data('AAPL', start_date='2023-01-01', end_date='2023-01-31')
        self.assertIsInstance(df, pd.DataFrame)
        self.assertFalse(df.empty)

    def test_fetch_invalid_ticker(self):
        """
        Test that fetching data for an invalid ticker returns an empty DataFrame.
        """
        # Using a clearly invalid ticker name
        df = fetch_stock_data('INVALIDTICKERXYZ', start_date='2023-01-01', end_date='2023-01-31')
        self.assertIsInstance(df, pd.DataFrame)
        self.assertTrue(df.empty)

    def test_data_columns(self):
        """
        Test that the returned DataFrame has the expected columns.
        """
        df = fetch_stock_data('MSFT', start_date='2023-01-01', end_date='2023-01-31')
        expected_columns = ['Open', 'High', 'Low', 'Close', 'Volume']
        for col in expected_columns:
            self.assertIn(col, df.columns)

if __name__ == '__main__':
    unittest.main()
