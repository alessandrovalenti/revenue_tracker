import requests
from timezonefinder import TimezoneFinder
from datetime import datetime, timedelta
from zoneinfo import ZoneInfo
from dotenv import load_dotenv
import os

# WEATHER API CONFIGURATION
BASE_URL_TIMEMACHINE = "https://api.openweathermap.org/data/3.0/onecall/timemachine"

load_dotenv()

API_KEY = os.environ.get("OPENWEATHER_API_KEY")
if not API_KEY:
    raise RuntimeError(
        "Missing OPENWEATHER_API_KEY. "
        "Create a .env file in the project root."
    )

# Functions
def get_city_coordinates(city):
    geo_url = "http://api.openweathermap.org/geo/1.0/direct"
    geo_params = {"q": city, "appid": API_KEY}
    response = requests.get(geo_url, params=geo_params)
    if response.status_code == 200:
        data = response.json()
        if data:
            return data[0]["lat"], data[0]["lon"]
        else:
            print(f"Error: No city found for '{city}'")
    else:
        print(f"Error in geocoding request: {response.status_code}")
    return None, None

def local_to_utc_timestamp(date_str: str, lat: float, lon: float, hour: int = 10, minute: int = 0) -> int:
    tz_name = TimezoneFinder().timezone_at(lat=lat, lng=lon)
    if not tz_name:
        tz_name = "UTC"  # fallback (e.g., ocean / not found)

    local_tz = ZoneInfo(tz_name)
    local_dt = datetime.strptime(date_str, "%Y-%m-%d").replace(hour=hour, minute=minute, tzinfo=local_tz)
    return int(local_dt.astimezone(ZoneInfo("UTC")).timestamp())

def get_day_weather(city, date=None):
    """
    Retrieves daily weather data for a given city and date using the OpenWeather API.

    Parameters:
    -----------
    city : str
        The name of the city for which to retrieve weather data.
    date : str or datetime, optional
        The date for which to retrieve weather data. Can be a string in the format "YYYY-MM-DD"
        or a `datetime` object. If not provided, defaults to the current day.

    Returns:
    --------
    tuple
        A tuple containing the following:
        - day_temp (float): The average temperature for the day in Celsius.
        - day_felt_temp (float): The "feels like" temperature for the day in Celsius.
        - wind_speed (float): Wind speed in meters per second.
        - main_weather (str): Main weather condition (e.g., "Clear", "Rain").
        - weather_description (str): More detailed description of the weather.

    Raises:
    -------
    ValueError
        If the city is not found, the date is invalid, or expected weather data is missing.
    ConnectionError
        If the API request fails (e.g., wrong endpoint or rate limits).
    Exception
        For any other unexpected errors.

    Example:
    --------
    >>> get_day_weather("Rome", "2024-04-01")
    (15.2, 13.9, 3.4, 'Clouds', 'scattered clouds')
    """

    try:
        # Get city coordinates; raise exception if not found.
        lat, lon = get_city_coordinates(city)
        if lat is None or lon is None:
            raise ValueError(f"Impossible to find coordinates for city '{city}'.")

        # Determine the target date.
        if date is None:
            date = datetime.now().strftime("%Y-%m-%d")

        date = local_to_utc_timestamp(date_str=date, lat=lat, lon=lon, hour=10, minute=0)
        
        params = {
            "lat": lat, 
            "lon": lon,
            "dt": date,
            "appid": API_KEY,
            "units": "metric"
        }

        response = requests.get(BASE_URL_TIMEMACHINE, params=params)
        if response.status_code != 200:
            raise ConnectionError(f"Error in weather request: {response.status_code}")

        data= response.json()
        # Check that the expected data exists; otherwise, raise an exception.
        if not data.get('data') or len(data['data']) == 0:
            raise ValueError("Weather data not available for the requested date.")

        # Extract the weather details from timemachine
        day_data = data['data'][0]
        day_temp = day_data.get('temp')
        day_felt_temp = day_data.get('feels_like')
        wind_speed = day_data.get('wind_speed')

        weather_info = day_data.get('weather')
        if not weather_info or len(weather_info) == 0:
            raise ValueError("Weather information not available.")
        main_weather = weather_info[0].get('main')
        weather_description = weather_info[0].get('description')

        # Validate that the necessary values are not None.
        for value, name in [(day_temp, "temperature"), (day_felt_temp, "felt temperature"), 
                            (wind_speed, "wind speed"), (main_weather, "main weather"), 
                            (weather_description, "weather description")]:
            if value is None:
                raise ValueError(f"Missing value for {name}.")

        return day_temp, day_felt_temp, wind_speed, main_weather, weather_description

    except ValueError as ve:
        # Reraise ValueErrors with a clear message.
        raise ValueError(f"Validation error: {ve}")
    except Exception as e:
        # Reraise any other exceptions as a generic error.
        raise Exception(f"Unexpected error in get_day_weather: {e}")

