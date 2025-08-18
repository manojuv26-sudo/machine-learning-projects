import configparser
import os

# Build the path to the config file relative to this file's location
# This file is in 'data_pipeline/src', config is in 'data_pipeline/config'
CONFIG_FILE_PATH = os.path.join(os.path.dirname(__file__), '..', 'config', 'config.ini')
PROJECT_ROOT = os.path.abspath(os.path.join(os.path.dirname(__file__), '..', '..'))

config = configparser.ConfigParser()
config.read(CONFIG_FILE_PATH)

def get_db_path() -> str:
    """
    Returns the absolute path to the database file.
    """
    db_name = config.get('database', 'db_file_name', fallback='stock_data.db')
    return os.path.join(PROJECT_ROOT, db_name)

def get_tickers() -> list[str]:
    """
    Returns a list of stock tickers from the config file.
    """
    tickers_str = config.get('pipeline', 'tickers', fallback='AAPL,GOOGL')
    return [ticker.strip() for ticker in tickers_str.split(',')]

def get_start_date() -> str:
    """
    Returns the start date for fetching data.
    """
    return config.get('pipeline', 'start_date', fallback='2023-01-01')

if __name__ == '__main__':
    # Example usage and verification
    print(f"Config file path: {CONFIG_FILE_PATH}")
    print(f"Project root: {PROJECT_ROOT}")
    print("\n--- Reading Configuration ---")
    db_path = get_db_path()
    tickers = get_tickers()
    start_date = get_start_date()

    print(f"Database Path: {db_path}")
    print(f"Tickers: {tickers}")
    print(f"Start Date: {start_date}")

    # Verification
    assert os.path.exists(CONFIG_FILE_PATH), "Config file not found!"
    assert 'stock_data.db' in db_path
    assert 'AAPL' in tickers
    print("\nConfiguration seems to be loading correctly.")
