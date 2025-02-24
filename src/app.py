import streamlit as st
import pandas as pd
import numpy as np
import joblib
import matplotlib.pyplot as plt
import seaborn as sns
from datetime import datetime, time

def load_model():
    return joblib.load('models/random_forest.pkl')

def create_features(date, time, nox, no2, o3, temp, humidity):
    # Create feature dictionary
    features = {
        'PT08.S1(CO)': [1000.0],  # default value
        'NMHC(GT)': [100.0],      # default value
        'C6H6(GT)': [10.0],       # default value
        'PT08.S2(NMHC)': [900.0], # default value
        'NOx(GT)': [nox],
        'PT08.S3(NOx)': [1000.0], # default value
        'NO2(GT)': [no2],
        'PT08.S4(NO2)': [1000.0], # default value
        'PT08.S5(O3)': [o3],
        'T': [temp],
        'RH': [humidity],
        'AH': [humidity * 0.1],    # approximate absolute humidity
        'Hour': [time.hour],
        'Month': [date.month],
        'DayOfWeek': [date.weekday()]
    }
    return pd.DataFrame(features)

def main():
    st.title('Air Quality Prediction System')
    
    try:
        model = load_model()
    except:
        st.error("Error: Model file not found. Please ensure the model is trained first.")
        return

    # Sidebar for navigation
    page = st.sidebar.selectbox('Select Page', ['Make Prediction', 'View Historical Data', 'Model Performance'])
    
    if page == 'Make Prediction':
        st.header('Make New Prediction')
        
        col1, col2 = st.columns(2)
        
        with col1:
            date = st.date_input('Date', datetime.now())
            time_input = st.time_input('Time', datetime.now().time())
            temp = st.number_input('Temperature (°C)', -10.0, 50.0, 20.0)
            humidity = st.number_input('Relative Humidity (%)', 0.0, 100.0, 50.0)
            
        with col2:
            nox = st.number_input('NOx Level', 0.0, 1000.0, 100.0)
            no2 = st.number_input('NO2 Level', 0.0, 1000.0, 100.0)
            o3 = st.number_input('O3 Level', 0.0, 1000.0, 100.0)
        
        if st.button('Predict CO Level'):
            # Create features and make prediction
            input_features = create_features(date, time_input, nox, no2, o3, temp, humidity)
            prediction = model.predict(input_features)
            
            st.success(f'Predicted CO Level: {prediction[0]:.2f} ppm')
            
            # Display feature importance
            if hasattr(model, 'feature_importances_'):
                st.subheader('Feature Importance')
                importance_df = pd.DataFrame({
                    'Feature': input_features.columns,
                    'Importance': model.feature_importances_
                }).sort_values('Importance', ascending=False)
                
                st.bar_chart(importance_df.set_index('Feature'))
    
    elif page == 'View Historical Data':
        st.header('Historical Data Analysis')
        
        try:
            data = pd.read_csv('data/AirQuality.csv', sep=';')
            
            fig, ax = plt.subplots(figsize=(10, 6))
            sns.lineplot(data=data, y='CO(GT)', x=data.index)
            plt.title('Historical CO Levels')
            plt.xlabel('Time')
            plt.ylabel('CO Level (ppm)')
            st.pyplot(fig)
            
            st.subheader('Statistical Summary')
            st.write(data['CO(GT)'].describe())
            
        except Exception as e:
            st.error(f"Error loading historical data: {str(e)}")
    
    else:
        st.header('Model Performance Metrics')
        
        try:
            results = pd.read_csv('results/prediction_results.csv')
            
            fig, ax = plt.subplots(figsize=(10, 6))
            plt.scatter(results['Actual'], results['Predicted'], alpha=0.5)
            plt.plot([results['Actual'].min(), results['Actual'].max()], 
                    [results['Actual'].min(), results['Actual'].max()], 
                    'r--', lw=2)
            plt.xlabel('Actual CO Levels (ppm)')
            plt.ylabel('Predicted CO Levels (ppm)')
            plt.title('Actual vs Predicted CO Levels')
            st.pyplot(fig)
            
            # Calculate and display metrics
            mse = np.mean((results['Actual'] - results['Predicted']) ** 2)
            rmse = np.sqrt(mse)
            r2 = 1 - (np.sum((results['Actual'] - results['Predicted']) ** 2) / 
                     np.sum((results['Actual'] - results['Actual'].mean()) ** 2))
            
            st.subheader('Performance Metrics')
            col1, col2 = st.columns(2)
            col1.metric('RMSE', f'{rmse:.3f}')
            col2.metric('R² Score', f'{r2:.3f}')
            
        except Exception as e:
            st.error(f"Error loading results: {str(e)}")

if __name__ == '__main__':
    main()