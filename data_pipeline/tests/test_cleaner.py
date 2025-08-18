import unittest
import pandas as pd
import numpy as np
import sys
import os

sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))

from src.cleaner import clean_data

class TestCleaner(unittest.TestCase):

    def test_remove_na(self):
        """
        Test that rows with NaN values are removed.
        """
        data = {
            'Date': pd.to_datetime(['2023-01-01', '2023-01-02', '2023-01-03']),
            'Open': [10, 11, np.nan],
            'Close': [10.2, 11.2, 12.2]
        }
        df = pd.DataFrame(data).set_index('Date')
        cleaned_df = clean_data(df)
        self.assertEqual(len(cleaned_df), 2)
        self.assertFalse(cleaned_df.isnull().values.any())

    def test_remove_duplicates(self):
        """
        Test that duplicate rows (based on index) are removed.
        """
        data = {
            'Date': pd.to_datetime(['2023-01-01', '2023-01-02', '2023-01-02']),
            'Open': [10, 11, 11],
            'Close': [10.2, 11.2, 11.2]
        }
        df = pd.DataFrame(data).set_index('Date')
        cleaned_df = clean_data(df)
        self.assertEqual(len(cleaned_df), 2)

    def test_reset_index(self):
        """
        Test that the 'Date' index is reset to a column.
        """
        data = {'Date': pd.to_datetime(['2023-01-01']), 'Open': [10]}
        df = pd.DataFrame(data).set_index('Date')
        cleaned_df = clean_data(df)
        self.assertIn('Date', cleaned_df.columns)
        self.assertIsInstance(cleaned_df.index, pd.RangeIndex)

    def test_empty_dataframe(self):
        """
        Test that an empty DataFrame is handled gracefully.
        """
        empty_df = pd.DataFrame()
        cleaned_df = clean_data(empty_df)
        self.assertTrue(cleaned_df.empty)

if __name__ == '__main__':
    unittest.main()
