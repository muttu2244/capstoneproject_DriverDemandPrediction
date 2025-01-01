"""Feature standardization and preparation."""
import pandas as pd
import numpy as np
from typing import Dict, Any
from ...utils.distance import calculate_haversine_distance
from .time_features import extract_hour

def standardize_features(features: pd.DataFrame) -> pd.DataFrame:
    """Ensure all required features are present with default values."""
    standard_features = {
        # Location features
        'Restaurant_latitude': 0.0,
        'Restaurant_longitude': 0.0,
        'Delivery_location_latitude': 0.0,
        'Delivery_location_longitude': 0.0,
        'distance': 0.0,
        
        # Time features
        'hour': 12,
        
        # Delivery person features
        'Delivery_person_Age': 30,
        'Delivery_person_Ratings': 4.5,
        'Vehicle_condition': 2,
        'multiple_deliveries': 0,
        
        # Encoded categorical features
        'Weatherconditions_encoded': 0,
        'Road_traffic_density_encoded': 0,
        'Type_of_vehicle_encoded': 0,
        'Type_of_order_encoded': 0,
        'Festival_encoded': 0,
        'City_encoded': 0
    }
    
    # Create a new DataFrame with all standard features
    df = pd.DataFrame(columns=standard_features.keys())
    
    # Fill with default values
    for col, default_value in standard_features.items():
        if col in features.columns:
            df[col] = features[col]
        else:
            df[col] = default_value
    
    # Ensure all columns are present and in the correct order
    return df[list(standard_features.keys())]