import streamlit as st
import requests
from datetime import datetime

def get_real_time_data():
    OPENWEATHER_API_KEY = "55dec2cdec64b62a502a8baa1042738b"  # Replace with your actual API key
    
    # Weather data endpoint
    weather_url = f"https://api.openweathermap.org/data/2.5/weather?q=Pune&appid={OPENWEATHER_API_KEY}&units=metric"
    
    # Air quality data endpoint
    lat, lon = 18.5204, 73.8567  # Pune coordinates
    aqi_url = f"http://api.openweathermap.org/data/2.5/air_pollution?lat={lat}&lon={lon}&appid={OPENWEATHER_API_KEY}"
    
    try:
        weather_response = requests.get(weather_url)
        aqi_response = requests.get(aqi_url)
        
        weather_data = weather_response.json()
        aqi_data = aqi_response.json()
        
        return {
            'temp': round(weather_data['main']['temp'], 1),
            'humidity': weather_data['main']['humidity'],
            'wind_speed': round(weather_data['wind']['speed'] * 3.6, 1),  # Convert m/s to km/h
            'pressure': weather_data['main']['pressure'],
            'aqi': aqi_data['list'][0]['main']['aqi'],
            'pm2_5': round(aqi_data['list'][0]['components']['pm2_5'], 1),
            'pm10': round(aqi_data['list'][0]['components']['pm10'], 1),
            'co': round(aqi_data['list'][0]['components']['co'], 1),
            'no2': round(aqi_data['list'][0]['components']['no2'], 1),
            'o3': round(aqi_data['list'][0]['components']['o3'], 1)
        }
    except Exception as e:
        st.error(f"Error fetching data: {str(e)}")
        return None

def get_aqi_status(aqi):
    if aqi == 1: return "Good", "#00E400"
    elif aqi == 2: return "Fair", "#FFFF00"
    elif aqi == 3: return "Moderate", "#FF7E00"
    elif aqi == 4: return "Poor", "#FF0000"
    else: return "Very Poor", "#8F3F97"

def main():
    st.set_page_config(layout="wide", page_title="Air Quality Monitor")
    
    st.title("🌍 Real-Time Air Quality Dashboard - Pune")
    
    data = get_real_time_data()
    
    if data:
        col1, col2, col3 = st.columns(3)
        col1.metric("Temperature", f"{data['temp']}°C")
        col2.metric("Humidity", f"{data['humidity']}%")
        col3.metric("Wind Speed", f"{data['wind_speed']} km/h")
        
        st.header("Air Quality Parameters")
        col4, col5, col6 = st.columns(3)
        col4.metric("PM2.5", f"{data['pm2_5']} μg/m³")
        col5.metric("PM10", f"{data['pm10']} μg/m³")
        col6.metric("CO", f"{data['co']} mg/m³")
        
        col7, col8, col9 = st.columns(3)
        col7.metric("NO₂", f"{data['no2']} μg/m³")
        col8.metric("O₃", f"{data['o3']} μg/m³")
        col9.metric("Pressure", f"{data['pressure']} hPa")
        
        status, color = get_aqi_status(data['aqi'])
        st.markdown(f"""
            <div style='padding: 20px; border-radius: 10px; background-color: {color}; 
                      color: black; text-align: center; margin: 20px 0;'>
                <h2>Air Quality Status: {status}</h2>
            </div>
        """, unsafe_allow_html=True)
        
        st.caption(f"Last Updated: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}")
    
    if st.button("🔄 Refresh Data"):
        st.rerun()

if __name__ == "__main__":
    main()