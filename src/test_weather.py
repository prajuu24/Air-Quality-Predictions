import os
from weather_fetcher import get_weather_data

# Your API key from environment variable
api_key = os.getenv('OPENWEATHER_API_KEY')
city = "Worldwide"  # Replace with your city

# Get weather data
weather = get_weather_data(api_key, city)
print("Current Weather:")
for key, value in weather.items():
    print(f"{key}: {value}")
