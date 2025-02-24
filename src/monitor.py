import sqlite3
import pandas as pd
import streamlit as st
import plotly.express as px
from datetime import datetime, timedelta

def create_monitoring_db():
    conn = sqlite3.connect('data/monitoring.db')
    c = conn.cursor()
    c.execute('''CREATE TABLE IF NOT EXISTS predictions
                 (timestamp TEXT, prediction FLOAT, latency FLOAT, 
                  temperature FLOAT, humidity FLOAT, nox FLOAT)''')
    conn.commit()
    conn.close()

def log_prediction(prediction, latency, temp, humidity, nox):
    conn = sqlite3.connect('data/monitoring.db')
    c = conn.cursor()
    c.execute('''INSERT INTO predictions VALUES 
                 (?, ?, ?, ?, ?, ?)''', 
                 (datetime.now().isoformat(), prediction, 
                  latency, temp, humidity, nox))
    conn.commit()
    conn.close()

def show_dashboard():
    st.title("Air Quality Prediction Monitoring")
    
    # Load data
    conn = sqlite3.connect('data/monitoring.db')
    df = pd.read_sql_query("SELECT * FROM predictions", conn)
    df['timestamp'] = pd.to_datetime(df['timestamp'])
    
    # Key metrics
    col1, col2, col3 = st.columns(3)
    col1.metric("Total Predictions", len(df))
    col2.metric("Avg Prediction", f"{df['prediction'].mean():.2f}")
    col3.metric("Avg Latency", f"{df['latency'].mean():.3f}s")
    
    # Time series plot
    st.subheader("Predictions Over Time")
    fig = px.line(df, x='timestamp', y='prediction')
    st.plotly_chart(fig)
    
    # Distribution plot
    st.subheader("Prediction Distribution")
    fig = px.histogram(df, x='prediction')
    st.plotly_chart(fig)
    
    # Correlation heatmap
    st.subheader("Feature Correlations")
    corr = df[['prediction', 'temperature', 'humidity', 'nox']].corr()
    fig = px.imshow(corr, text_auto=True)
    st.plotly_chart(fig)

if __name__ == "__main__":
    create_monitoring_db()
    show_dashboard()
