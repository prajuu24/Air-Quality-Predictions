import pandas as pd
import numpy as np
import joblib
import matplotlib.pyplot as plt

def load_best_model():
    model = joblib.load('models/random_forest.pkl')
    return model

def make_predictions(model, input_data):
    return model.predict(input_data)

def plot_predictions(actual, predicted, title='Actual vs Predicted CO Levels'):
    plt.figure(figsize=(12, 6))
    plt.plot(actual, label='Actual', marker='o', alpha=0.6)
    plt.plot(predicted, label='Predicted', marker='x', alpha=0.6)
    plt.title(title)
    plt.xlabel('Sample Index')
    plt.ylabel('CO Level')
    plt.legend()
    plt.grid(True)
    plt.savefig('results/predictions.png')
    plt.show()

def calculate_metrics(actual, predicted):
    mse = np.mean((actual - predicted) ** 2)
    rmse = np.sqrt(mse)
    mae = np.mean(np.abs(actual - predicted))
    r2 = 1 - (np.sum((actual - predicted) ** 2) / np.sum((actual - np.mean(actual)) ** 2))
    return {'RMSE': rmse, 'MAE': mae, 'R2': r2}

if __name__ == "__main__":
    # Load test data
    print("Loading test data...")
    X_test = pd.read_csv('data/X_test.csv')
    y_test = pd.read_csv('data/y_test.csv').values.ravel()  # Convert to 1D array
    
    # Load model
    print("Loading model...")
    model = load_best_model()
    
    # Make predictions
    print("Making predictions...")
    predictions = make_predictions(model, X_test)
    
    # Calculate metrics
    print("\nCalculating performance metrics...")
    metrics = calculate_metrics(y_test, predictions)
    
    print("\nPrediction Results:")
    for metric_name, value in metrics.items():
        print(f"{metric_name}: {value:.4f}")
    
    # Plot results
    print("\nGenerating prediction plot...")
    plot_predictions(y_test, predictions)
    
    # Save predictions
    results_df = pd.DataFrame({
        'Actual': y_test,
        'Predicted': predictions,
        'Difference': y_test - predictions
    })
    results_df.to_csv('results/prediction_results.csv', index=False)
    print("\nPrediction results saved to 'results/prediction_results.csv'")
