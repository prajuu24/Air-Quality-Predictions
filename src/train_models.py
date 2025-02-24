import pandas as pd
import numpy as np
from sklearn.linear_model import LinearRegression, Ridge, Lasso
from sklearn.ensemble import RandomForestRegressor, GradientBoostingRegressor
from sklearn.metrics import mean_squared_error, r2_score
import matplotlib.pyplot as plt
import seaborn as sns
import joblib

def load_processed_data():
    X_train = pd.read_csv('data/X_train.csv')
    X_test = pd.read_csv('data/X_test.csv')
    y_train = pd.read_csv('data/y_train.csv')
    y_test = pd.read_csv('data/y_test.csv')
    return X_train, X_test, y_train.values.ravel(), y_test.values.ravel()

def train_models(X_train, X_test, y_train, y_test):
    models = {
        'Linear Regression': LinearRegression(),
        'Ridge Regression': Ridge(),
        'Lasso Regression': Lasso(),
        'Random Forest': RandomForestRegressor(n_estimators=100, random_state=42),
        'Gradient Boosting': GradientBoostingRegressor(random_state=42)
    }
    
    results = {}
    
    for name, model in models.items():
        print(f"\nTraining {name}...")
        model.fit(X_train, y_train)
        
        # Make predictions
        train_pred = model.predict(X_train)
        test_pred = model.predict(X_test)
        
        # Calculate metrics
        results[name] = {
            'train_rmse': np.sqrt(mean_squared_error(y_train, train_pred)),
            'test_rmse': np.sqrt(mean_squared_error(y_test, test_pred)),
            'train_r2': r2_score(y_train, train_pred),
            'test_r2': r2_score(y_test, test_pred),
            'model': model
        }
        
        # Save model
        joblib.dump(model, f'models/{name.lower().replace(" ", "_")}.pkl')
    
    return results

def plot_results(results):
    # Plot RMSE comparison
    plt.figure(figsize=(12, 6))
    
    models = list(results.keys())
    train_rmse = [results[m]['train_rmse'] for m in models]
    test_rmse = [results[m]['test_rmse'] for m in models]
    
    x = np.arange(len(models))
    width = 0.35
    
    plt.bar(x - width/2, train_rmse, width, label='Train RMSE')
    plt.bar(x + width/2, test_rmse, width, label='Test RMSE')
    
    plt.xlabel('Models')
    plt.ylabel('RMSE')
    plt.title('Model Performance Comparison')
    plt.xticks(x, models, rotation=45)
    plt.legend()
    plt.tight_layout()
    plt.savefig('results/model_comparison.png')
    plt.show()

if __name__ == "__main__":
    # Create necessary directories
    import os
    os.makedirs('models', exist_ok=True)
    os.makedirs('results', exist_ok=True)
    
    # Load data
    print("Loading processed data...")
    X_train, X_test, y_train, y_test = load_processed_data()
    
    # Train and evaluate models
    print("Training models...")
    results = train_models(X_train, X_test, y_train, y_test)
    
    # Print results
    print("\nModel Performance Summary:")
    for name, metrics in results.items():
        print(f"\n{name}:")
        print(f"Train RMSE: {metrics['train_rmse']:.4f}")
        print(f"Test RMSE: {metrics['test_rmse']:.4f}")
        print(f"Train R²: {metrics['train_r2']:.4f}")
        print(f"Test R²: {metrics['test_r2']:.4f}")
    
    # Plot results
    print("\nGenerating performance plots...")
    plot_results(results)
