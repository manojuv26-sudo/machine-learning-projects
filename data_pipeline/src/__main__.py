from datetime import datetime

from .database_setup import create_database_and_table
from .fetcher import fetch_stock_data
from .cleaner import clean_data
from .storage import save_data
from .config_manager import get_tickers, get_start_date

def run_pipeline():
    """
    Runs the full data pipeline:
    1. Ensures database is created.
    2. Fetches data for each ticker.
    3. Cleans the data.
    4. Saves the data to the database.
    """
    print("--- Starting Data Pipeline ---")

    # 1. Setup Database
    print("Step 1: Ensuring database and table exist...")
    create_database_and_table()
    print("Database setup complete.")

    # 2. Process each ticker
    tickers = get_tickers()
    start_date = get_start_date()
    end_date = datetime.today().strftime('%Y-%m-%d')

    for ticker in tickers:
        print(f"\n--- Processing Ticker: {ticker} ---")

        # Fetch
        print(f"Fetching data for {ticker} from {start_date} to {end_date}...")
        raw_data = fetch_stock_data(ticker, start_date=start_date, end_date=end_date)

        if raw_data.empty:
            print(f"No data fetched for {ticker}. Skipping.")
            continue

        print(f"Fetched {len(raw_data)} rows.")

        # Clean
        print("Cleaning data...")
        cleaned_data = clean_data(raw_data)
        print(f"Cleaned data has {len(cleaned_data)} rows.")

        # Save
        print("Saving data to database...")
        save_data(cleaned_data, ticker)

    print("\n--- Data Pipeline Finished ---")

if __name__ == '__main__':
    run_pipeline()
