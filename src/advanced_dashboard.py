import streamlit as st
import pandas as pd
import numpy as np
import plotly.express as px
import plotly.graph_objects as go
from sklearn.preprocessing import StandardScaler
from sklearn.decomposition import PCA
from datetime import datetime, timedelta

def create_mock_data():
    dates = pd.date_range(start='2024-01-01', end='2024-02-21', freq='H')
    data = pd.DataFrame({
        'timestamp': dates,
        'co_level': np.random.normal(2.5, 0.5, len(dates)),
        'temperature': np.random.normal(25, 3, len(dates)),
        'humidity': np.random.normal(60, 10, len(dates)),
        'wind_speed': np.random.normal(15, 5, len(dates))
    })
    return data

def plot_3d_scatter(data):
    fig = px.scatter_3d(
        data, 
        x='temperature', 
        y='humidity', 
        z='co_level',
        color='wind_speed',
        title='3D Air Quality Analysis'
    )
    return fig

def plot_heatmap(data):
    pivot = data.pivot_table(
        index=data['timestamp'].dt.hour,
        columns=data['timestamp'].dt.dayofweek,
        values='co_level',
        aggfunc='mean'
    )
    fig = px.imshow(
        pivot,
        title='CO Levels Heatmap (Hour vs Day)',
        labels={'x': 'Day of Week', 'y': 'Hour of Day'}
    )
    return fig

def main():
    st.title("Advanced Air Quality Analytics Dashboard")
    
    # Load data
    data = create_mock_data()
    
    # Sidebar filters
    st.sidebar.header("Filters")
    date_range = st.sidebar.date_input(
        "Select Date Range",
        [data['timestamp'].min(), data['timestamp'].max()]
    )
    
    # Main dashboard
    tab1, tab2, tab3 = st.tabs(["Overview", "Analysis", "Predictions"])
    
    with tab1:
        st.subheader("Key Metrics")
        col1, col2, col3, col4 = st.columns(4)
        col1.metric("Average CO Level", f"{data['co_level'].mean():.2f}")
        col2.metric("Max Temperature", f"{data['temperature'].max():.1f}°C")
        col3.metric("Avg Humidity", f"{data['humidity'].mean():.1f}%")
        col4.metric("Wind Speed", f"{data['wind_speed'].mean():.1f} km/h")
        
        st.plotly_chart(plot_3d_scatter(data))
    
    with tab2:
        st.subheader("Temporal Analysis")
        st.plotly_chart(plot_heatmap(data))
        
        # Correlation analysis
        st.subheader("Feature Correlations")
        corr = data.drop('timestamp', axis=1).corr()
        st.plotly_chart(px.imshow(corr, text_auto=True))
    
    with tab3:
        st.subheader("Predictive Analytics")
        # Add simple forecasting
        forecast = data['co_level'].rolling(24).mean()
        fig = go.Figure()
        fig.add_trace(go.Scatter(x=data['timestamp'], y=data['co_level'], name='Actual'))
        fig.add_trace(go.Scatter(x=data['timestamp'], y=forecast, name='Forecast'))
        st.plotly_chart(fig)

if __name__ == "__main__":
    main()
