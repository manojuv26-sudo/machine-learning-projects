import sqlite3
import pandas as pd
from .fetcher import fetch_stock_data
from .cleaner import clean_data
from .config_manager import get_db_path

def save_data(df: pd.DataFrame, ticker: str):
    """
    Saves the cleaned stock data DataFrame to the SQLite database.

    Args:
        df (pd.DataFrame): The cleaned DataFrame.
        ticker (str): The stock ticker symbol.
    """
    if df.empty:
        print("DataFrame is empty. Nothing to save.")
        return

    db_path = get_db_path()
    try:
        conn = sqlite3.connect(db_path)
        cursor = conn.cursor()

        # Prepare data for insertion
        df_to_save = df.copy()
        df_to_save['Ticker'] = ticker

        # Ensure Date is in 'YYYY-MM-DD' string format for SQLite TEXT column
        if pd.api.types.is_datetime64_any_dtype(df_to_save['Date']):
            df_to_save['Date'] = df_to_save['Date'].dt.strftime('%Y-%m-%d')

        # Select and order columns to match the table schema
        df_to_save = df_to_save[['Ticker', 'Date', 'Open', 'High', 'Low', 'Close', 'Volume']]

        # Create a list of tuples from the DataFrame records
        records = [tuple(x) for x in df_to_save.to_numpy()]

        # Use INSERT OR IGNORE to prevent duplicate entries
        insert_query = """
        INSERT OR IGNORE INTO stock_prices (Ticker, Date, Open, High, Low, Close, Volume)
        VALUES (?, ?, ?, ?, ?, ?, ?);
        """

        cursor.executemany(insert_query, records)
        conn.commit()

        print(f"Successfully saved {cursor.rowcount} new rows for ticker {ticker}.")

    except sqlite3.Error as e:
        print(f"Database error during save: {e}")
    finally:
        if 'conn' in locals() and conn:
            conn.close()

if __name__ == '__main__':
    # Example usage:
    ticker_symbol = 'GOOGL'
    print(f"--- Data Storage Test for {ticker_symbol} ---")

    # 1. Fetch
    print(f"1. Fetching data for {ticker_symbol}...")
    raw_data = fetch_stock_data(ticker_symbol, start_date='2023-01-01', end_date='2023-12-31')

    if not raw_data.empty:
        # 2. Clean
        print("2. Cleaning data...")
        cleaned_data = clean_data(raw_data)

        # 3. Save
        print("3. Saving data to database...")
        save_data(cleaned_data, ticker_symbol)

        # 4. Verify by checking the number of rows for the ticker
        try:
            db_path = get_db_path()
            conn = sqlite3.connect(db_path)
            count = pd.read_sql(f"SELECT COUNT(*) FROM stock_prices WHERE Ticker='{ticker_symbol}'", conn).iloc[0,0]
            print(f"4. Verification: Found {count} rows for {ticker_symbol} in the database.")
        except Exception as e:
            print(f"Verification failed: {e}")
        finally:
            if 'conn' in locals() and conn:
                conn.close()
    else:
        print(f"Could not fetch data for {ticker_symbol}, storage step skipped.")
