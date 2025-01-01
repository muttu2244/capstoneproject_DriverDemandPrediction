"""Feature preparation utilities."""
import pandas as pd
from typing import Tuple, Dict, Any
from ...utils.distance import calculate_haversine_distance
from .time_features import extract_hour
from .feature_standardization import standardize_features

def prepare_features(data: pd.DataFrame) -> Tuple[pd.DataFrame, pd.Series]:
    """Prepare features and target for model training."""
    # Separate features and target
    if 'time_taken(min)' in data.columns:
        y = data['time_taken(min)']
        X = data.drop('time_taken(min)', axis=1)
    else:
        raise ValueError("Target column 'time_taken(min)' not found in data")
    
    # Standardize features
    X = standardize_features(X)
    return X, y

def prepare_prediction_features(order_data: Dict[str, Any]) -> pd.DataFrame:
    """Prepare features for a single prediction."""
    try:
        # Required location fields
        required_fields = [
            'restaurant_lat', 'restaurant_lng',
            'delivery_lat', 'delivery_lng'
        ]
        
        # Validate required fields
        for field in required_fields:
            if field not in order_data:
                raise ValueError(f"Missing required field: {field}")
        
        # Calculate distance
        distance = calculate_haversine_distance(
            float(order_data['restaurant_lat']),
            float(order_data['restaurant_lng']),
            float(order_data['delivery_lat']),
            float(order_data['delivery_lng'])
        )
        
        # Extract hour from order time
        hour = extract_hour(order_data.get('order_time', '12:00'))
        
        # Create initial features
        features = pd.DataFrame([{
            'Restaurant_latitude': float(order_data['restaurant_lat']),
            'Restaurant_longitude': float(order_data['restaurant_lng']),
            'Delivery_location_latitude': float(order_data['delivery_lat']),
            'Delivery_location_longitude': float(order_data['delivery_lng']),
            'distance': distance,
            'hour': hour,
            'Weatherconditions_encoded': encode_weather(order_data.get('weather', 'Clear')),
            'Road_traffic_density_encoded': encode_traffic(order_data.get('traffic', 'Medium')),
            'Type_of_vehicle_encoded': encode_vehicle(order_data.get('vehicle_type', 'motorcycle'))
        }])
        
        # Standardize features
        return standardize_features(features)
        
    except Exception as e:
        raise ValueError(f"Error preparing prediction features: {str(e)}")

def encode_weather(weather: str) -> int:
    """Encode weather conditions."""
    weather_mapping = {
        'Clear': 0,
        'Cloudy': 1,
        'Fog': 2,
        'Rain': 3,
        'Storm': 4
    }
    return weather_mapping.get(weather, 0)

def encode_traffic(traffic: str) -> int:
    """Encode traffic conditions."""
    traffic_mapping = {
        'Low': 0,
        'Medium': 1,
        'High': 2,
        'Jam': 3
    }
    return traffic_mapping.get(traffic, 0)

def encode_vehicle(vehicle: str) -> int:
    """Encode vehicle type."""
    vehicle_mapping = {
        'motorcycle': 0,
        'scooter': 1,
        'bicycle': 2
    }
    return vehicle_mapping.get(vehicle.lower(), 0)