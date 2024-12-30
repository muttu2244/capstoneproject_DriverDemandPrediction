"""Time-based feature extraction."""
import pandas as pd
import numpy as np
from typing import Dict
from ...utils.date_parsers import parse_date
from ...utils.time_parsers import decimal_to_hour

def extract_time_features(data: pd.DataFrame) -> pd.DataFrame:
    """Extract time-based features from order data."""
    df = data.copy()
    
    try:
        # Convert Time_Orderd to hour (0-23)
        df['hour'] = df['Time_Orderd'].apply(decimal_to_hour)
        
        # Handle case where all hours are NaN
        if df['hour'].isna().all():
            df['hour'] = 12  # Set default hour
        else:
            # Fill missing hours with median of non-NaN values
            median_hour = int(df['hour'].dropna().median())
            df['hour'] = df['hour'].fillna(median_hour)
        
        # Extract day of week from Order_Date
        df['day_of_week'] = df['Order_Date'].apply(
            lambda x: parse_date(x).dayofweek if pd.notna(x) else 3  # Default to Wednesday
        )
        
        # Handle case where all days are NaN
        if df['day_of_week'].isna().all():
            df['day_of_week'] = 3  # Set default to Wednesday
        else:
            # Fill missing days with median of non-NaN values
            median_day = int(df['day_of_week'].dropna().median())
            df['day_of_week'] = df['day_of_week'].fillna(median_day)
        
        # Calculate weekend flag
        df['is_weekend'] = df['day_of_week'].isin([5, 6]).astype(int)
        
        return df
    except Exception as e:
        raise ValueError(f"Error extracting time features: {str(e)}")