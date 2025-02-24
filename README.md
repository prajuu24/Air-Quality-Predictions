# Air Quality Prediction  

## 📌 Project Description  
Air Quality Prediction is an advanced monitoring system that analyzes and forecasts air pollutant levels using Machine Learning (ML) techniques. It integrates real-time weather data using OpenWeather API and provides interactive dashboards for visualization. The system helps users monitor air pollution trends and make data-driven decisions.  

---

## 🚀 Key Features  
- 📡 **Real-time air quality monitoring**  
- 📊 **Interactive data visualization dashboard**  
- 📋 **Automated report generation**  
- 📈 **Predictive analytics for pollutant levels**  
- ⏳ **Historical trend analysis**  
- 🌤 **Integration with OpenWeather API for real-time data**  

---

## 📊 Data Preprocessing Steps  

### 🔍 Data Collection  
- **Source**: Sensor data from multiple locations & OpenWeather API  
- **Format**: Time-series data  
- **Handling Missing Values**: Forward-fill & Interpolation techniques  

### 🔬 Feature Engineering  
- **Extracted Features**:  
  - Temporal features (day, month, season)  
  - Environmental parameters (temperature, wind speed, humidity)  
  - Correlation analysis with air pollutants  
- **Standardization**: MinMaxScaler & StandardScaler  
- **Outlier Detection**: IQR (Interquartile Range) method  

### 🧹 Data Cleaning  
- Removal of corrupted or inconsistent records  
- Handling missing values via interpolation  
- Normalization of pollutant levels  
- Validation of data consistency  

---

## 🔬 Machine Learning Models Used  
- **Linear Regression**: Baseline prediction  
- **Random Forest Regressor**: Improved accuracy with non-linearity  
- **Gradient Boosting (XGBoost)**: High-performance ensemble model  
- **LSTM (Deep Learning)**: Captures temporal dependencies  

🔹 **Best Performing Models**: XGBoost & LSTM for high accuracy  

---

## 🌤 Weather API Integration  

We use **OpenWeatherMap API** to fetch real-time weather data, including:  
- Temperature  
- Humidity  
- Wind Speed  
- Air Quality Index (AQI)  

### 🔑 How to Use the API  

1. **Get an API Key** from [OpenWeather](https://home.openweathermap.org/api_keys)  
2. **Set up the API Key in your environment**  

```bash
export WEATHER_API_KEY=your_api_key_here

🛠 Dependencies
pip install -r requirements.txt

🔧 Required Libraries
Python 3.9+
Streamlit
Pandas
NumPy
Plotly
Scikit-learn
Matplotlib
Seaborn
XGBoost
TensorFlow/Keras (For LSTM)
Requests (For API calls)

