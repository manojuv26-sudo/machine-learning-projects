import yfinance as yf
import pandas as pd
import os

# Define the ticker symbol and the date range
TICKER = "AAPL"
START_DATE = "2020-01-01"
END_DATE = "2023-12-31"

# Define the output path
OUTPUT_DIR = "data"
OUTPUT_FILE = os.path.join(OUTPUT_DIR, f"{TICKER}_stock_data.csv")

def download_stock_data(ticker, start_date, end_date, output_file):
    """
    Downloads historical stock data from Yahoo Finance and saves it to a CSV file.
    """
    print(f"Downloading data for {ticker} from {start_date} to {end_date}...")

    # Download the data
    stock_data = yf.download(ticker, start=start_date, end=end_date)

    if stock_data.empty:
        print(f"No data found for ticker {ticker}. Exiting.")
        return

    # Create the output directory if it doesn't exist
    os.makedirs(os.path.dirname(output_file), exist_ok=True)

    # Reset index to make 'Date' a column
    stock_data.reset_index(inplace=True)

    # Save the data to a CSV file without the pandas index
    stock_data.to_csv(output_file, index=False)

    print(f"Data downloaded and saved to {output_file}")

if __name__ == "__main__":
    download_stock_data(TICKER, START_DATE, END_DATE, OUTPUT_FILE)
