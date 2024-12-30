import numpy as np
from sklearn.ensemble import RandomForestRegressor
from sklearn.model_selection import train_test_split
from sklearn.metrics import mean_absolute_error, mean_squared_error

class DeliveryTimePredictor:
    def __init__(self):
        self.model = RandomForestRegressor(
            n_estimators=100,
            max_depth=10,
            random_state=42
        )
        
    def prepare_features(self, data):
        """Prepare features for the delivery time prediction model"""
        features = [
            'distance',
            'hour',
            'day_of_week',
            'is_weekend',
            'Weather_encoded',
            'Road_traffic_encoded',
            'Type_of_veh_encoded'
        ]
        
        return data[features]
    
    def train(self, data):
        """Train the delivery time prediction model"""
        X = self.prepare_features(data)
        y = data['time_taken']
        
        X_train, X_test, y_train, y_test = train_test_split(
            X, y, test_size=0.2, random_state=42
        )
        
        self.model.fit(X_train, y_train)
        
        # Evaluate model
        y_pred = self.model.predict(X_test)
        mae = mean_absolute_error(y_test, y_pred)
        rmse = np.sqrt(mean_squared_error(y_test, y_pred))
        
        print(f"Model Performance:")
        print(f"MAE: {mae:.2f} minutes")
        print(f"RMSE: {rmse:.2f} minutes")
    
    def predict(self, order_data):
        """Predict delivery time for a new order"""
        # Transform input data to match training features
        features = np.array([[
            order_data['distance'],
            int(order_data['order_time'].split(':')[0]),  # hour
            0,  # day_of_week (dummy value)
            0,  # is_weekend (dummy value)
            self.label_encoders['Weather'].transform([order_data['weather']])[0],
            self.label_encoders['Road_traffic'].transform([order_data['traffic']])[0],
            self.label_encoders['Type_of_veh'].transform([order_data['vehicle_type']])[0]
        ]])
        
        return self.model.predict(features)[0]