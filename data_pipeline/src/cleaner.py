import pandas as pd
from .fetcher import fetch_stock_data

def clean_data(df: pd.DataFrame) -> pd.DataFrame:
    """
    Cleans the stock data DataFrame.

    Args:
        df (pd.DataFrame): The input DataFrame with stock data.

    Returns:
        pd.DataFrame: The cleaned DataFrame.
    """
    if df.empty:
        return df

    # Make a copy to avoid SettingWithCopyWarning
    df_cleaned = df.copy()

    # 1. Handle missing values - for simplicity, we'll drop rows with any NaNs
    # A more advanced approach could be forward-fill or interpolation.
    df_cleaned.dropna(inplace=True)

    # 2. Ensure correct data types (yfinance is usually good, but this is good practice)
    # Convert all columns to numeric, coercing errors
    for col in ['Open', 'High', 'Low', 'Close', 'Volume']:
        if col in df_cleaned.columns:
            df_cleaned[col] = pd.to_numeric(df_cleaned[col], errors='coerce')

    # Drop rows that might have become NaN after coercion
    df_cleaned.dropna(inplace=True)

    # 3. Remove duplicate rows (based on index - Date)
    if not df_cleaned.index.is_unique:
        df_cleaned = df_cleaned[~df_cleaned.index.duplicated(keep='first')]

    # 4. Reset index if it's a DatetimeIndex
    if isinstance(df_cleaned.index, pd.DatetimeIndex):
        df_cleaned.reset_index(inplace=True)

    # Ensure 'Date' is in datetime format if the column exists
    if 'Date' in df_cleaned.columns:
        df_cleaned['Date'] = pd.to_datetime(df_cleaned['Date'])

    return df_cleaned

if __name__ == '__main__':
    # Example usage:
    ticker_symbol = 'TSLA'
    print(f"Fetching data for {ticker_symbol} to test cleaning...")
    # Fetch a slightly longer period to increase chance of finding issues
    raw_data = fetch_stock_data(ticker_symbol, start_date='2020-01-01', end_date='2023-12-31')

    if not raw_data.empty:
        print("\n--- Before Cleaning ---")
        print(f"Number of rows: {len(raw_data)}")
        print(f"Missing values:\n{raw_data.isnull().sum()}")

        cleaned_df = clean_data(raw_data)

        print("\n--- After Cleaning ---")
        print(f"Number of rows: {len(cleaned_df)}")
        print(f"Missing values:\n{cleaned_df.isnull().sum()}")
        print("\nCleaned DataFrame head:")
        print(cleaned_df.head())
        print("\nCleaned DataFrame info:")
        cleaned_df.info()
    else:
        print(f"Could not fetch data for {ticker_symbol}, cleaning step skipped.")
