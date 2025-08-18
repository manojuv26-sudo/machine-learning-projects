# Stock Data Pipeline

This project is an automated data pipeline that fetches daily stock market data from the Yahoo Finance API, cleans it, and stores it in a local SQLite database.

## Features

- **Automated Data Fetching:** Fetches daily historical data for a list of configurable stock tickers.
- **Data Cleaning:** Handles missing values and ensures data integrity.
- **SQLite Storage:** Stores the cleaned data in a local SQLite database, preventing duplicate entries.
- **Configurable:** Easily configure the list of tickers, database name, and date ranges via a `config.ini` file.
- **Modular Structure:** The code is organized into logical modules for fetching, cleaning, storing, and configuration.
- **Tested:** Comes with a full suite of unit tests to ensure reliability.

## Project Structure

```
data_pipeline/
├── config/
│   └── config.ini        # Configuration file for tickers, DB name, etc.
├── src/
│   ├── __init__.py
│   ├── __main__.py       # Main entry point for the pipeline
│   ├── cleaner.py        # Data cleaning logic
│   ├── config_manager.py # Handles reading the config file
│   ├── database_setup.py # Sets up the database schema
│   ├── fetcher.py        # Fetches data from yfinance
│   └── storage.py        # Saves data to the database
├── tests/
│   ├── __init__.py
│   ├── test_cleaner.py
│   ├── test_fetcher.py
│   └── test_storage.py
├── .gitignore
├── requirements.txt      # Project dependencies
└── stock_data.db         # The SQLite database file (created on first run)
```

## Setup and Installation

### Prerequisites

- Python 3.10+
- `pip` for package management

### Installation Steps

1.  **Clone the repository:**
    ```bash
    git clone <repository-url>
    cd data_pipeline
    ```

2.  **Create and activate a virtual environment (recommended):**
    ```bash
    python -m venv venv
    source venv/bin/activate  # On Windows, use `venv\Scripts\activate`
    ```

3.  **Install the required dependencies:**
    ```bash
    pip install -r requirements.txt
    ```

## How to Use

### 1. Configure the Pipeline

Open the `config/config.ini` file to customize the pipeline settings:

```ini
[database]
db_file_name = stock_data.db

[pipeline]
tickers = AAPL,GOOGL,MSFT,TSLA
start_date = 2023-01-01
```

- `db_file_name`: The name of the SQLite database file that will be created.
- `tickers`: A comma-separated list of stock tickers you want to process.
- `start_date`: The start date for fetching historical data.

### 2. Run the Pipeline

To run the entire data pipeline, execute the `src` package as a module from the project's root directory (`/app`):

```bash
python -m data_pipeline.src
```

The script will:
- Set up the database and table if they don't exist.
- Fetch data for each ticker specified in the config file.
- Clean the data.
- Save any new data to the SQLite database.

## Running Tests

To run the unit tests and verify that all components are working correctly, run the following command from the project's root directory:

```bash
python -m unittest discover data_pipeline/tests
```
The test suite will run, and you should see an "OK" message indicating that all tests passed.
