import sys
import os
import pandas as pd
import sqlite3

# Add the 'src' directory to the Python path (go back one folder, then into 'src')
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))
db_path = os.path.abspath(os.path.join(os.path.dirname(__file__), '..', 'data', 'revenues.db'))

from revenue_tracker.database import create_table, add_revenue

TEST_CITY = 'Romano di Lombardia'
TEST_DATE = '2025-03-01'  # Example date for testing
TEST_REVENUE = 1000.0


def test_create_table():
    # Test the weather data retrieval for a known city (e.g., "Rome")
    create_table()
 

# Call the test functions
if __name__ == "__main__":

    # Create the table
    test_create_table()

    # Add an revenue entry
    add_revenue(date=TEST_DATE, city=TEST_CITY, declared_revenue=TEST_REVENUE, notes='Test entry')


    # Read the database and print the contents
    conn = sqlite3.connect(db_path)
    df = pd.read_sql_query("SELECT * FROM revenues", conn)
    print(df)
    conn.close()

    # Eliminate the database
    os.remove(db_path)
    print(f"Database '{db_path}' has been deleted.")

