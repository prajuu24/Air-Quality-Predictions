import streamlit as st
import pandas as pd
import time
from datetime import datetime
import random

def simulate_prediction():
    return {
        'timestamp': datetime.now(),
        'co_level': random.uniform(0.5, 5.0),
        'temperature': random.uniform(20, 30),
        'humidity': random.uniform(40, 80)
    }

def update_dashboard():
    placeholder = st.empty()
    while True:
        with placeholder.container():
            # Get new prediction
            new_data = simulate_prediction()
            
            # Display metrics
            col1, col2, col3 = st.columns(3)
            col1.metric("CO Level", f"{new_data['co_level']:.2f}")
            col2.metric("Temperature", f"{new_data['temperature']:.1f}°C")
            col3.metric("Humidity", f"{new_data['humidity']:.1f}%")
            
            # Update every 5 seconds
            time.sleep(5)

if __name__ == "__main__":
    st.title("Real-Time Air Quality Monitoring")
    update_dashboard()
