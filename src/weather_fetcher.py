import requests
import json
from datetime import datetime

def get_weather_data(api_key, city="London"):
    base_url = "http://api.openweathermap.org/data/2.5/weather"
    params = {
        'q': city,
        'appid': api_key,
        'units': 'metric'  # For Celsius
    }
    
    response = requests.get(base_url, params=params)
    weather_data = response.json()
    
    return {
        'temperature': weather_data['main']['temp'],
        'humidity': weather_data['main']['humidity'],
        'wind_speed': weather_data['wind']['speed'],
        'description': weather_data['weather'][0]['description'],
        'timestamp': datetime.now().strftime("%Y-%m-%d %H:%M:%S")
    }
