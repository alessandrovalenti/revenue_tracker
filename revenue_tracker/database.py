import sqlite3
import os
from pathlib import Path
from dotenv import load_dotenv
from datetime import datetime
import pandas as pd
from revenue_tracker.weather import get_day_weather
from revenue_tracker.utils import default_who

# Path to your database file
load_dotenv()
DEFAULT_DB_PATH = Path(__file__).resolve().parent.parent / "data" / "revenues.db"
DATABASE_PATH = Path(
    os.environ.get("DATABASE_PATH", DEFAULT_DB_PATH)
).resolve()


####### DATABASE CONNECTION #######
def create_connection():
    """Establish a connection to the SQLite database only if the database exists."""
    try:
        conn = sqlite3.connect(DATABASE_PATH)
        return conn
    except sqlite3.Error as e:
        print(f"Error connecting to database: {e}")
        return None
    

#### CREATE FUNCTIONS ####

def create_table():
    """Create the table if it does not exist."""
    conn = create_connection()
    if conn:
        cursor = conn.cursor()
        cursor.execute('''
        CREATE TABLE IF NOT EXISTS revenues (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            date TEXT,
            city TEXT,
            revenue REAL DEFAULT NULL,
            declared_revenue REAL,
            kind TEXT,
            who TEXT,
            temperature REAL,
            temperature_felt REAL,
            wind_speed REAL,
            main_weather TEXT,
            weather_description TEXT,
            notes TEXT DEFAULT NULL
        )
        ''')
        conn.commit()
        conn.close()
        print("Table 'revenues' created.")
    else:
        print("Failed to create table due to connection issues.")

def add_revenue(date, city, declared_revenue, revenue=None, kind='ordinary', who=None, notes=None):
    """Insert an income entry into the database."""
    conn = create_connection()
    if conn:
        cursor = conn.cursor()
        
        # Assuming get_today_weather() returns these values:
        # (day_temp, day_felt_temp, wind_speed, main_weather, weather_description)
        try:
            day_temp, day_felt_temp, wind_speed, main_weather, weather_description = get_day_weather(city, date)
        except Exception as e:
            print(f"Failed to retrieve weather data: {e}")
            return
        
        # Assign default values for 'chi' if not provided
        day_of_week = (datetime.strptime(date, "%Y-%m-%d")).strftime("%A")  # Get the day of the week
        if who is None:
            who = default_who(city, date)
        
        if cursor.execute("SELECT * FROM revenues WHERE date = ? AND city = ?", (date, city)).fetchone():
            print(f"\nRecord for date {date} and city '{city}' already exists.\n")
            return

        cursor.execute('''
        INSERT INTO revenues (date, city, revenue, declared_revenue, temperature, temperature_felt, wind_speed, main_weather, weather_description, kind, who, notes)
        VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?)
        ''', (date, city, revenue, declared_revenue, day_temp, day_felt_temp, wind_speed, main_weather, weather_description, kind, who, notes))
        
        conn.commit()
        conn.close()
    else:
        print("Failed to insert record due to connection issues.")


#### GET FUNCTIONS ####


def get_last_revenues(n=1):
    """Retrieve the last revenue entry from the database."""
    conn = create_connection()
    if conn:
        df = pd.read_sql_query(f"SELECT * FROM revenues ORDER BY id DESC LIMIT {n} ", conn)
        conn.close()
        return df
    else:
        print("Failed to retrieve record due to connection issues.")
        return None

def get_revenue_by_date(date):
    """Retrieve revenue for a specific date."""
    conn = create_connection()
    if conn:
        df = pd.read_sql_query("SELECT * FROM revenues WHERE date = ?", conn, params=(date,))
        conn.close()
        return df
    else:
        print("Failed to retrieve record due to connection issues.")
        return None

def get_table():
    """Retrieve the entire table from the database."""
    conn = create_connection()
    df = pd.read_sql_query("SELECT * FROM revenues ORDER BY date DESC", conn)
    conn.close()
    return df


#### DELETE FUNCTIONS ####

def del_revenue_by_id(id):
    """Delete revenue by ID."""
    conn = create_connection()
    if conn:
        cursor = conn.cursor()
        cursor.execute("DELETE FROM revenues WHERE id = ?", (id,))
        count = cursor.rowcount
        conn.commit()
        conn.close()
        return count
    else:
        print("Failed to delete record due to connection issues.")

def del_revenue_by_date(date, city):
    """Delete revenue for a specific date."""
    conn = create_connection()
    if conn:
        cursor = conn.cursor()
        cursor.execute("DELETE FROM revenues WHERE date = ? AND city = ?", (date, city))
        row_count = cursor.rowcount
        conn.commit()
        conn.close()
        return row_count
    else:
        print("Failed to delete record due to connection issues.")

def del_table():
    """Delete the entire table from the database."""
    conn = create_connection()
    if conn:
        cursor = conn.cursor()
        cursor.execute("DROP TABLE IF EXISTS revenues")
        conn.commit()
        conn.close()
    else:
        print("Failed to delete table due to connection issues.")


