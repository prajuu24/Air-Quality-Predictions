import requests
import json

# Test data
test_data = {
    "date": "2024-02-21",
    "time": "14:30:00",
    "temperature": 25.0,
    "humidity": 60.0,
    "nox": 120.0,
    "no2": 80.0,
    "o3": 100.0
}

# Make prediction request
response = requests.post(
    "http://localhost:8000/predict",
    json=test_data
)

# Print results
print("Status Code:", response.status_code)
print("Prediction:", response.json())
