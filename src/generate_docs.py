def generate_user_guide():
    guide = """
    # Air Quality Prediction System - User Guide
    
    ## Quick Start
    1. Launch the dashboard: `streamlit run src/advanced_dashboard.py`
    2. Access via browser: http://localhost:8502
    
    ## Available Features
    1. Overview Tab
        - Real-time CO level metrics
        - Temperature tracking
        - Humidity monitoring
        - 3D visualization
        
    2. Analysis Tab
        - Temporal heatmaps
        - Correlation analysis
        - Historical trends
        
    3. Predictions Tab
        - Forecast viewing
        - Trend analysis
        
    ## Data Interpretation
    - CO Levels: 0-4 ppm (normal range)
    - Temperature: 20-30°C (optimal)
    - Humidity: 40-60% (recommended)
    
    ## Best Practices
    1. Regular monitoring of CO levels
    2. Check correlations between metrics
    3. Review temporal patterns
    4. Track forecast accuracy
    """
    return guide

if __name__ == "__main__":
    with open("docs/user_guide.md", "w") as f:
        f.write(generate_user_guide())
