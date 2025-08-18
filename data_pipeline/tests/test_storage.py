import unittest
import os
import pandas as pd
import sqlite3
from unittest.mock import patch

import sys
sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))

from src.storage import save_data
from src.database_setup import create_database_and_table

class TestStorage(unittest.TestCase):

    def setUp(self):
        """
        Set up a temporary database and some test data.
        """
        self.test_db_path = 'test_stock_data.db'
        self.ticker = 'TEST'
        self.test_data = pd.DataFrame({
            'Date': pd.to_datetime(['2023-01-01', '2023-01-02']),
            'Ticker': [self.ticker, self.ticker],
            'Open': [100, 102],
            'High': [105, 105],
            'Low': [99, 101],
            'Close': [104, 103],
            'Volume': [10000, 12000]
        })

        # Patch get_db_path in both modules where it is used
        self.db_setup_patcher = patch('src.database_setup.get_db_path', return_value=self.test_db_path)
        self.storage_patcher = patch('src.storage.get_db_path', return_value=self.test_db_path)

        self.mock_db_setup = self.db_setup_patcher.start()
        self.mock_storage = self.storage_patcher.start()

        # Create the database and table in the test DB
        create_database_and_table()

    def tearDown(self):
        """
        Clean up the temporary database file and stop the patchers.
        """
        self.db_setup_patcher.stop()
        self.storage_patcher.stop()
        if os.path.exists(self.test_db_path):
            os.remove(self.test_db_path)

    def test_save_new_data(self):
        """
        Test that new data is correctly saved to the database.
        """
        save_data(self.test_data, self.ticker)

        # Verify the data was saved
        conn = sqlite3.connect(self.test_db_path)
        saved_df = pd.read_sql(f"SELECT * FROM stock_prices WHERE Ticker='{self.ticker}'", conn)
        conn.close()

        self.assertEqual(len(saved_df), 2)
        self.assertEqual(saved_df['Open'].iloc[0], 100)

    def test_prevent_duplicates(self):
        """
        Test that saving the same data twice does not create duplicate entries.
        """
        # Save once
        save_data(self.test_data, self.ticker)

        # Save again
        save_data(self.test_data, self.ticker)

        # Verify the data was not duplicated
        conn = sqlite3.connect(self.test_db_path)
        count = pd.read_sql(f"SELECT COUNT(*) FROM stock_prices WHERE Ticker='{self.ticker}'", conn).iloc[0,0]
        conn.close()

        self.assertEqual(count, 2)

if __name__ == '__main__':
    unittest.main()
