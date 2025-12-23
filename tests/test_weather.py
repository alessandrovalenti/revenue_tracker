import sys
import os

# Add the 'src' directory to the Python path (go back one folder, then into 'src')
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))

from src.weather import get_day_weather

TEST_CITY = ['Romano di Lombardia']
TEST_DATE = '2025-03-01'  # Example date for testing


def test_get_day_weather(city, date):
    # Test the weather data retrieval for a known city (e.g., "Rome")
    day_temp, day_felt_temp, wind_speed, main_weather, weather_description = get_day_weather(city, date)
    print(f"City: {city}", 'Day Temperature:', day_temp, '°C, ', 'Felt Temperature:', day_felt_temp, '°C, ',
          'Wind Speed:', wind_speed, 'm/s, ', 'Main Weather:', main_weather, ', Weather Description:', weather_description)
 

# Call the test functions
if __name__ == "__main__":

    print("-" * 40, f'\nDate: {TEST_DATE}\n')
    for city in TEST_CITY:
        test_get_day_weather(city=city, date=TEST_DATE)
        print("-" * 40)
