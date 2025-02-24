import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns
from datetime import datetime, timedelta
import numpy as np

class ReportGenerator:
    def __init__(self):
        self.timestamp = datetime.now().strftime("%Y%m%d_%H%M")
        self.report_path = f"reports/air_quality_report_{self.timestamp}.png"
        
    def generate_sample_data(self):
        # Generate 24 hours of sample data
        dates = pd.date_range(
            start=datetime.now() - timedelta(days=1),
            end=datetime.now(),
            freq='H'
        )
        
        data = pd.DataFrame({
            'timestamp': dates,
            'co_level': np.random.normal(2.5, 0.5, len(dates)),
            'temperature': np.random.normal(25, 3, len(dates)),
            'humidity': np.random.normal(60, 10, len(dates))
        })
        return data
    
    def create_report(self):
        # Generate sample data
        data = self.generate_sample_data()
        
        # Create report visualizations
        plt.figure(figsize=(15, 10))
        
        # CO Level Trends
        plt.subplot(2, 2, 1)
        plt.plot(data['timestamp'], data['co_level'], 'b-')
        plt.title('CO Level Trends (Last 24 Hours)')
        plt.xticks(rotation=45)
        
        # Temperature vs CO Level
        plt.subplot(2, 2, 2)
        plt.scatter(data['temperature'], data['co_level'])
        plt.title('Temperature vs CO Level')
        plt.xlabel('Temperature (°C)')
        plt.ylabel('CO Level')
        
        # CO Level Distribution
        plt.subplot(2, 2, 3)
        sns.histplot(data['co_level'], bins=20)
        plt.title('CO Level Distribution')
        
        # Correlation Heatmap
        plt.subplot(2, 2, 4)
        sns.heatmap(data[['co_level', 'temperature', 'humidity']].corr(), 
                   annot=True, cmap='coolwarm')
        plt.title('Correlation Matrix')
        
        # Save the report
        plt.tight_layout()
        plt.savefig(self.report_path)
        
        return f"Report generated successfully at: {self.report_path}"

if __name__ == "__main__":
    # Create reports directory if it doesn't exist
    import os
    os.makedirs('reports', exist_ok=True)
    
    # Generate report
    generator = ReportGenerator()
    result = generator.create_report()
    print(result)
