"""Data preprocessing pipeline."""
import pandas as pd
import numpy as np
from typing import List
from .type_conversion import to_numeric_safe, to_int_safe, extract_hour

def preprocess_delivery_data(df: pd.DataFrame) -> pd.DataFrame:
    """Preprocess delivery data with strict type enforcement."""
    df = df.copy()
    
    # Drop unnecessary ID columns
    id_columns = ['ID', 'Delivery_person_ID']
    df = df.drop(columns=[col for col in id_columns if col in df.columns])
    
    # Convert numeric columns
    numeric_columns = {
        'time_taken(min)': float,
        'Restaurant_latitude': float,
        'Restaurant_longitude': float,
        'Delivery_location_latitude': float,
        'Delivery_location_longitude': float,
        'Delivery_person_Age': int,
        'Delivery_person_Ratings': float,
        'Vehicle_condition': int,
        'multiple_deliveries': int
    }
    
    for col, dtype in numeric_columns.items():
        if col in df.columns:
            if dtype == float:
                df[col] = df[col].apply(to_numeric_safe)
            else:
                df[col] = df[col].apply(to_int_safe)
            # Fill NaN with median
            df[col] = df[col].fillna(df[col].median())
    
    # Extract hour from Time_Orderd
    if 'Time_Orderd' in df.columns:
        df['hour'] = df['Time_Orderd'].apply(extract_hour)
    
    # Add order count column
    df['order_count'] = 1
    
    # Convert categorical columns to numeric codes
    categorical_columns = [
        'Weatherconditions',
        'Road_traffic_density',
        'Type_of_vehicle',
        'Type_of_order',
        'Festival',
        'City'
    ]
    
    for col in categorical_columns:
        if col in df.columns:
            # Create encoded column
            df[f'{col}_encoded'] = pd.Categorical(df[col]).codes
            # Drop original categorical column
            df = df.drop(columns=[col])
    
    # Ensure all remaining columns are numeric
    for col in df.columns:
        if not pd.api.types.is_numeric_dtype(df[col]):
            print(f"Warning: Dropping non-numeric column {col}")
            df = df.drop(columns=[col])
    
    return df