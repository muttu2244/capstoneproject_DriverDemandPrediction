"""Distance-based feature extraction."""
import pandas as pd
import numpy as np

def calculate_distance(lat1: float, lon1: float, lat2: float, lon2: float) -> float:
    """Calculate distance between two points using Haversine formula."""
    R = 6371  # Earth's radius in kilometers
    
    lat1, lon1, lat2, lon2 = map(np.radians, [lat1, lon1, lat2, lon2])
    dlat = lat2 - lat1
    dlon = lon2 - lon1
    
    a = np.sin(dlat/2)**2 + np.cos(lat1) * np.cos(lat2) * np.sin(dlon/2)**2
    c = 2 * np.arcsin(np.sqrt(a))
    
    return R * c

def extract_distance_features(data: pd.DataFrame) -> pd.DataFrame:
    """Extract distance-based features from order data."""
    df = data.copy()
    
    df['distance'] = df.apply(
        lambda row: calculate_distance(
            row['Restaurant_latitude'],
            row['Restaurant_longitude'],
            row['Delivery_location_latitude'],
            row['Delivery_location_longitude']
        ),
        axis=1
    )
    
    return df