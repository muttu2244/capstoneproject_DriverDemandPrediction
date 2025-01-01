"""Numeric feature processing."""
import pandas as pd
import numpy as np

def process_numeric_features(df: pd.DataFrame) -> pd.DataFrame:
    """Process numeric features."""
    df = df.copy()
    
    # Define numeric columns
    numeric_columns = [
        'time_taken(min)',
        'Restaurant_latitude',
        'Restaurant_longitude',
        'Delivery_location_latitude',
        'Delivery_location_longitude',
        'Delivery_person_Age',
        'Delivery_person_Ratings',
        'Vehicle_condition',
        'multiple_deliveries'
    ]
    
    # Convert to numeric and handle missing values
    for col in numeric_columns:
        if col in df.columns:
            # Convert to numeric, coerce errors to NaN
            df[col] = pd.to_numeric(df[col], errors='coerce')
            # Fill NaN with median
            median_value = df[col].median()
            df[col] = df[col].fillna(median_value)
            # Ensure float64 type
            df[col] = df[col].astype('float64')
    
    return df