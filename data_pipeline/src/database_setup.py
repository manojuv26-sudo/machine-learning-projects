import sqlite3
from .config_manager import get_db_path

def create_database_and_table():
    """
    Creates the SQLite database and the stock_prices table if they don't exist.
    """
    db_path = get_db_path()
    try:
        # The connect function will create the file if it doesn't exist
        conn = sqlite3.connect(db_path)
        cursor = conn.cursor()

        # SQL statement to create the table
        create_table_query = """
        CREATE TABLE IF NOT EXISTS stock_prices (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            Ticker TEXT NOT NULL,
            Date TEXT NOT NULL,
            Open REAL NOT NULL,
            High REAL NOT NULL,
            Low REAL NOT NULL,
            Close REAL NOT NULL,
            Volume INTEGER NOT NULL,
            UNIQUE (Ticker, Date)
        );
        """

        cursor.execute(create_table_query)
        conn.commit()
        print(f"Database and table created successfully at '{db_path}'.")

    except sqlite3.Error as e:
        print(f"Database error: {e}")
    finally:
        if 'conn' in locals() and conn:
            conn.close()

if __name__ == '__main__':
    create_database_and_table()
