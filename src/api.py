from fastapi import FastAPI, HTTPException
from pydantic import BaseModel
from datetime import datetime
import joblib
import pandas as pd
import uvicorn

app = FastAPI(title="Air Quality Prediction API")

# Load the model
model = joblib.load('models/random_forest.pkl')

class AirQualityInput(BaseModel):
    date: str
    time: str
    temperature: float
    humidity: float
    nox: float
    no2: float
    o3: float

class PredictionOutput(BaseModel):
    co_prediction: float
    timestamp: str

@app.get("/")
def home():
    return {"message": "Air Quality Prediction API", 
            "status": "active"}
    from src.monitoring import record_metrics
    import time

    @app.post("/predict", response_model=PredictionOutput)
    def predict(input_data: AirQualityInput):
        start_time = time.time()
        try:
            features = create_features(input_data)
            prediction = model.predict(features)[0]
        
            # Record metrics
            latency = time.time() - start_time
            record_metrics(prediction, latency)
        
            return PredictionOutput(
                co_prediction=float(prediction),
                timestamp=datetime.now().isoformat()
            )
        except Exception as e:
            raise HTTPException(status_code=500, detail=str(e))
def create_features(input_data):
    # Convert input data to features
    date = datetime.strptime(input_data.date, '%Y-%m-%d')
    time = datetime.strptime(input_data.time, '%H:%M:%S')
    
    features = {
        'PT08.S1(CO)': [1000.0],
        'NMHC(GT)': [100.0],
        'C6H6(GT)': [10.0],
        'PT08.S2(NMHC)': [900.0],
        'NOx(GT)': [input_data.nox],
        'PT08.S3(NOx)': [1000.0],
        'NO2(GT)': [input_data.no2],
        'PT08.S4(NO2)': [1000.0],
        'PT08.S5(O3)': [input_data.o3],
        'T': [input_data.temperature],
        'RH': [input_data.humidity],
        'AH': [input_data.humidity * 0.1],
        'Hour': [time.hour],
        'Month': [date.month],
        'DayOfWeek': [date.weekday()]
    }
    
    return pd.DataFrame(features)

if __name__ == "__main__":
    uvicorn.run("api:app", host="0.0.0.0", port=8000, reload=True)

from typing import List

class BatchPredictionInput(BaseModel):
    records: List[AirQualityInput]

@app.post("/batch-predict")
def batch_predict(inputs: BatchPredictionInput):
    predictions = []
    for record in inputs.records:
        features = create_features(record)
        pred = model.predict(features)[0]
        predictions.append({
            "prediction": float(pred),
            "timestamp": datetime.now().isoformat()
        })
    return predictions
