import streamlit as st
import pandas as pd
import numpy as np
from datetime import datetime
import smtplib
from email.mime.text import MIMEText
import json

class AlertSystem:
    def __init__(self):
        self.thresholds = {
            'co_level': 4.0,
            'temperature': 30.0,
            'humidity': 75.0
        }
    
    def check_alerts(self, data):
        alerts = []
        if data['co_level'] > self.thresholds['co_level']:
            alerts.append(f"High CO Level: {data['co_level']:.2f}")
        if data['temperature'] > self.thresholds['temperature']:
            alerts.append(f"High Temperature: {data['temperature']:.1f}°C")
        if data['humidity'] > self.thresholds['humidity']:
            alerts.append(f"High Humidity: {data['humidity']:.1f}%")
        return alerts

def generate_report(data):
    report = {
        'timestamp': datetime.now().isoformat(),
        'metrics': {
            'avg_co_level': np.mean(data['co_level']),
            'max_co_level': np.max(data['co_level']),
            'alert_count': len(data['alerts'])
        }
    }
    return report

def save_report(report):
    with open('reports/daily_report.json', 'w') as f:
        json.dump(report, f, indent=4)

def main():
    st.title("Air Quality Monitoring with Alerts")
    
    alert_system = AlertSystem()
    
    # Sidebar for threshold settings
    st.sidebar.header("Alert Thresholds")
    for metric, value in alert_system.thresholds.items():
        alert_system.thresholds[metric] = st.sidebar.slider(
            f"{metric.replace('_', ' ').title()}", 
            0.0, 
            value * 2, 
            value
        )
    
    # Main dashboard
    col1, col2 = st.columns(2)
    
    with col1:
        st.subheader("Current Readings")
        current_data = {
            'co_level': np.random.uniform(2.0, 6.0),
            'temperature': np.random.uniform(25.0, 35.0),
            'humidity': np.random.uniform(50.0, 85.0)
        }
        
        for metric, value in current_data.items():
            st.metric(
                metric.replace('_', ' ').title(),
                f"{value:.2f}",
                f"{value - alert_system.thresholds[metric]:.2f}"
            )
    
    with col2:
        st.subheader("Active Alerts")
        alerts = alert_system.check_alerts(current_data)
        if alerts:
            for alert in alerts:
                st.error(alert)
        else:
            st.success("No active alerts")

if __name__ == "__main__":
    main()
