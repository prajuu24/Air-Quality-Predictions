from prometheus_client import start_http_server, Counter, Gauge, Histogram
import time

# Metrics
PREDICTIONS = Counter('air_quality_predictions_total', 'Total number of predictions made')
PREDICTION_VALUE = Gauge('air_quality_co_level', 'Predicted CO level')
PREDICTION_LATENCY = Histogram('prediction_latency_seconds', 'Time taken for prediction')

def record_metrics(prediction, latency):
    PREDICTIONS.inc()
    PREDICTION_VALUE.set(prediction)
    PREDICTION_LATENCY.observe(latency)
