import streamlit as st
import requests
from datetime import datetime
import os

def get_weather_data():
    api_key = os.getenv('OPENWEATHER_API_KEY')
    city = "London"  # Default city, can be changed
    base_url = "http://api.openweathermap.org/data/2.5/weather"
    params = {
        'q': city,
        'appid': api_key,
        'units': 'metric'
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

def main():
    st.title("Real-Time Weather Dashboard")
    
    # City selection in sidebar
    city = st.sidebar.selectbox(
        "Select City",
        ["London", "New York", "Tokyo", "Paris", "Mumbai"]
    )
    
    # Auto-refresh button
    if st.button("Refresh Data"):
        weather = get_weather_data()
        
        # Display metrics
        col1, col2, col3 = st.columns(3)
        col1.metric("Temperature", f"{weather['temperature']}°C")
        col2.metric("Humidity", f"{weather['humidity']}%")
        col3.metric("Wind Speed", f"{weather['wind_speed']} m/s")
        
        st.info(f"Current Conditions: {weather['description']}")
        st.success(f"Last Updated: {weather['timestamp']}")

if __name__ == "__main__":
    main()
