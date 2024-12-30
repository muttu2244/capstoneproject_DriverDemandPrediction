import pandas as pd
import numpy as np
from sklearn.ensemble import RandomForestRegressor
from sklearn.metrics import mean_absolute_error
from datetime import datetime, timedelta

class PeakDemandPredictor:
    def __init__(self):
        self.model = RandomForestRegressor(
            n_estimators=100,
            max_depth=10,
            random_state=42
        )
    
    def create_time_series_features(self, data):
        """Create time series features including lag features"""
        # Group orders by hour to get hourly order counts
        hourly_orders = data.groupby(['Order_Date', 'hour']).size().reset_index(name='order_count')
        hourly_orders['datetime'] = pd.to_datetime(hourly_orders['Order_Date']) + \
                                  pd.to_timedelta(hourly_orders['hour'], unit='h')
        hourly_orders = hourly_orders.set_index('datetime').sort_index()
        
        # Create lag features
        for i in range(1, 25):  # Last 24 hours
            hourly_orders[f'lag_{i}'] = hourly_orders['order_count'].shift(i)
        
        # Create time-based features
        hourly_orders['hour'] = hourly_orders.index.hour
        hourly_orders['day_of_week'] = hourly_orders.index.dayofweek
        hourly_orders['is_weekend'] = hourly_orders['day_of_week'].isin([5, 6]).astype(int)
        
        # Drop rows with NaN values (due to lag features)
        hourly_orders = hourly_orders.dropna()
        
        return hourly_orders
    
    def train(self, data):
        """Train the peak demand prediction model"""
        # Prepare time series data
        ts_data = self.create_time_series_features(data)
        
        # Prepare features and target
        feature_cols = ['hour', 'day_of_week', 'is_weekend'] + \
                      [f'lag_{i}' for i in range(1, 25)]
        
        X = ts_data[feature_cols]
        y = ts_data['order_count']
        
        # Split data into train and test
        train_size = int(len(ts_data) * 0.8)
        X_train, X_test = X[:train_size], X[train_size:]
        y_train, y_test = y[:train_size], y[train_size:]
        
        # Train model
        self.model.fit(X_train, y_train)
        
        # Evaluate model
        y_pred = self.model.predict(X_test)
        mae = mean_absolute_error(y_test, y_pred)
        print(f"Peak Demand Model MAE: {mae:.2f} orders")
    
    def predict_next_day(self, current_data=None):
        """Predict order demand for the next 24 hours"""
        if current_data is None:
            # Use dummy data for demonstration
            current_data = np.random.randint(10, 50, size=24)
        
        predictions = []
        next_day_hours = range(24)
        
        for hour in next_day_hours:
            features = np.array([[
                hour,  # hour
                0,     # day_of_week (dummy)
                0,     # is_weekend (dummy)
                *current_data[-24:]  # last 24 hours of data
            ]])
            
            pred = self.model.predict(features)[0]
            predictions.append(pred)
        
        # Find peak hours (hours with demand > mean + std)
        mean_demand = np.mean(predictions)
        std_demand = np.std(predictions)
        peak_hours = [h for h in next_day_hours if predictions[h] > mean_demand + std_demand]
        
        return {
            'hourly_predictions': predictions,
            'peak_hours': peak_hours,
            'total_orders': sum(predictions)
        }