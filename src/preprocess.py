import pandas as pd
import numpy as np
from sklearn.preprocessing import StandardScaler
from sklearn.model_selection import train_test_split

def load_and_clean_data():
    # Load the data
    df = pd.read_csv("data/AirQuality.csv", sep=';', decimal=',')
    
    # Drop unnamed columns and rows with missing values
    df = df.drop([col for col in df.columns if 'Unnamed' in col], axis=1)
    df = df.dropna()
    
    # Convert datetime properly
    df['Date'] = pd.to_datetime(df['Date'], format='%d/%m/%Y')
    df['Hour'] = pd.to_datetime(df['Time'], format='%H.%M.%S').dt.hour
    df['Month'] = df['Date'].dt.month
    df['DayOfWeek'] = df['Date'].dt.dayofweek
    
    return df

def prepare_features(df):
    # Select features for modeling
    feature_columns = ['PT08.S1(CO)', 'NMHC(GT)', 'C6H6(GT)', 'PT08.S2(NMHC)', 
                      'NOx(GT)', 'PT08.S3(NOx)', 'NO2(GT)', 'PT08.S4(NO2)', 
                      'PT08.S5(O3)', 'T', 'RH', 'AH', 'Hour', 'Month', 'DayOfWeek']
    
    # Target variable
    target = 'CO(GT)'
    
    # Remove any remaining invalid values
    df = df.replace(-200, np.nan)
    
    # Split features and target
    X = df[feature_columns]
    y = df[target]
    
    # Handle missing values
    X = X.fillna(X.mean())
    y = y.fillna(y.mean())
    
    # Scale the features
    scaler = StandardScaler()
    X_scaled = scaler.fit_transform(X)
    X_scaled = pd.DataFrame(X_scaled, columns=X.columns)
    
    return X_scaled, y, scaler

def split_data(X, y):
    # Split into train and test sets
    X_train, X_test, y_train, y_test = train_test_split(
        X, y, test_size=0.2, random_state=42
    )
    return X_train, X_test, y_train, y_test

if __name__ == "__main__":
    # Load and preprocess data
    print("Loading and cleaning data...")
    df = load_and_clean_data()
    
    print("Preparing features...")
    X_scaled, y, scaler = prepare_features(df)
    
    print("Splitting data...")
    X_train, X_test, y_train, y_test = split_data(X_scaled, y)
    
    # Save processed data
    print("Saving processed data...")
    X_train.to_csv('data/X_train.csv', index=False)
    X_test.to_csv('data/X_test.csv', index=False)
    y_train.to_csv('data/y_train.csv', index=False)
    y_test.to_csv('data/y_test.csv', index=False)
    
    print("\nData preprocessing completed successfully!")
    print(f"Training set shape: {X_train.shape}")
    print(f"Testing set shape: {X_test.shape}")
