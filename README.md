# Revenue tracker with weather data

This program allows you to record daily revenues for different cities and automatically add weather information for the selected date and location. The goal is to track revenues over time and later study possible correlations with weather conditions. Particularly useful for vendors operating in open air markets.

## Features

- Store daily revenues in a local SQLite database
- Automatically fetch weather data for a given city and date
- Prevent duplicate entries for the same date and city
- Assign default personnel automatically based on city and weekday
- Fully configurable defaults without modifying Python code

## Project structure

- main.py  
  Entry point of the program

- revenue_tracker/  
  Application package containing all business logic
  - database.py database access and data insertion
  - interface.py user interaction and menus
  - weather.py weather data retrieval
  - defaults.py loading and handling of default configuration
  - who_defaults.json user editable configuration for default personnel

- data/
  - revenues.db SQLite database file

- tests/
  Unit tests for database and weather logic

## Weather API configuration

This project uses the OpenWeather API.

Create a file called .env in the project root with the following content:

OPENWEATHER_API_KEY=your_api_key_here

You can obtain an API key by creating a free account on openweathermap.org.

The .env file is not tracked by git.

## Database configuration

By default the SQLite database is stored in data/revenues.db.

You can override the location by setting DATABASE_PATH in the .env file.

## Default personnel configuration

The file

revenue_tracker/who_defaults.json

controls the automatic assignment of the who field when inserting a revenue entry.

You can edit this file directly to change defaults. No Python knowledge is required.

### Format

Each city name must be written in lowercase.  
Weekdays must be written in English with capital first letter.

Example:

{
  "Zurich": {
    "Tuesday": "Marco, Sofia",
    "Thursday": "Liam, Mia",
    "Saturday": "Marco, Liam, Mia"
  },
  "Basel": {
    "*": "Marco, Sofia"
  }
}

- Use "*" to specify a fallback for all weekdays
- Specific weekdays override the fallback

If no rule is found for a given city and date, the who field is left empty.

## Installation

This project requires Python 3.10 or newer.

Install dependencies with:

pip install -r requirements.txt

Set up the OpenWeather API, the database path (optional) and the default personnel (optional)

## Usage

From the project root, run:

python main.py

Follow the on screen instructions to insert and manage revenue data.

## Notes

- Dates must be entered in YYYY-MM-DD format
- If a future date is entered, the program will issue a warning but still allow insertion
- Weather data availability depends on the external weather service
