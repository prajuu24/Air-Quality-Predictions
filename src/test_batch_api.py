import requests

batch_data = {
    "records": [
        {
            "date": "2024-02-21",
            "time": "14:30:00",
            "temperature": 25.0,
            "humidity": 60.0,
            "nox": 120.0,
            "no2": 80.0,
            "o3": 100.0
        },
        {
            "date": "2024-02-21",
            "time": "15:30:00",
            "temperature": 26.0,
            "humidity": 65.0,
            "nox": 125.0,
            "no2": 85.0,
            "o3": 105.0
        }
    ]
}

response = requests.post("http://localhost:8000/batch-predict", json=batch_data)
print(response.json())
