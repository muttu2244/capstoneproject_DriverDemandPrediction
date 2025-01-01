"""Categorical feature processing."""
import pandas as pd
from sklearn.preprocessing import LabelEncoder

def process_categorical_features(df: pd.DataFrame) -> pd.DataFrame:
    """Process categorical features."""
    df = df.copy()
    
    # Drop unnecessary ID columns
    id_columns = ['ID', 'Delivery_person_ID']
    df = df.drop(columns=[col for col in id_columns if col in df.columns])
    
    # Define categorical columns to encode
    categorical_columns = [
        'Weatherconditions',
        'Road_traffic_density',
        'Type_of_vehicle',
        'Type_of_order',
        'Festival',
        'City'
    ]
    
    # Create encoded features
    encoders = {}
    for col in categorical_columns:
        if col in df.columns:
            encoders[col] = LabelEncoder()
            # Fill NaN values with 'Unknown'
            df[col] = df[col].fillna('Unknown')
            # Create encoded column
            df[f'{col}_encoded'] = encoders[col].fit_transform(df[col])
            # Convert to int64 to ensure proper type
            df[f'{col}_encoded'] = df[f'{col}_encoded'].astype('int64')
            # Drop original column to avoid type issues
            df = df.drop(columns=[col])
    
    return df