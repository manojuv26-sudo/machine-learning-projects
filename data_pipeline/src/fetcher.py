import yfinance as yf
import pandas as pd

def fetch_stock_data(ticker: str, start_date: str = None, end_date: str = None) -> pd.DataFrame:
    """
    Fetches historical stock data from Yahoo Finance.

    Args:
        ticker (str): The stock ticker symbol (e.g., 'AAPL').
        start_date (str, optional): The start date for the data in 'YYYY-MM-DD' format. Defaults to None.
        end_date (str, optional): The end date for the data in 'YYYY-MM-DD' format. Defaults to None.

    Returns:
        pd.DataFrame: A DataFrame containing the historical stock data, or an empty DataFrame if the fetch fails.
    """
    try:
        stock = yf.Ticker(ticker)
        # Fetch historical data
        # Using '1d' interval for daily data
        data = stock.history(start=start_date, end=end_date, interval="1d")
        if data.empty:
            print(f"No data found for ticker {ticker}. It might be delisted or an invalid ticker.")
        return data
    except Exception as e:
        print(f"An error occurred while fetching data for {ticker}: {e}")
        return pd.DataFrame()

if __name__ == '__main__':
    # Example usage:
    ticker_symbol = 'AAPL'
    print(f"Fetching data for {ticker_symbol}...")
    stock_data = fetch_stock_data(ticker_symbol, start_date='2023-01-01', end_date='2023-12-31')

    if not stock_data.empty:
        print(f"Successfully fetched {len(stock_data)} rows of data for {ticker_symbol}.")
        print("First 5 rows:")
        print(stock_data.head())
    else:
        print(f"Failed to fetch data for {ticker_symbol}.")
