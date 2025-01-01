"""Script to test delivery time prediction."""
import pandas as pd
from src.models.delivery_time_model import DeliveryTimeModel
from src.data_processor import DataProcessor
from src.models.features.feature_preparation import prepare_prediction_features

def predict_delivery():
    # Sample order
    order = {
        'restaurant_lat': 30.327968,
        'restaurant_lng': 78.046106,
        'delivery_lat': 30.337968,
        'delivery_lng': 78.056106,
        'weather': 'Clear',
        'traffic': 'Medium',
        'vehicle_type': 'motorcycle',
        'order_time': '14:30'
    }
    
    try:
        # Load and process data
        data = pd.read_csv('data/raw/delivery_data.csv')
        processor = DataProcessor()
        processed_data = processor.preprocess(data)
        
        # Train model
        model = DeliveryTimeModel()
        X = processed_data.drop(['time_taken(min)'], axis=1)
        y = processed_data['time_taken(min)']
        model.train(X, y)
        
        # Prepare features and predict
        features = prepare_prediction_features(order)
        estimated_time = model.predict(features)
        
        print(f"\nDelivery Time Prediction:")
        print(f"Estimated time: {estimated_time[0]:.1f} minutes")
        
    except Exception as e:
        print(f"Error: {str(e)}")

if __name__ == "__main__":
    predict_delivery()