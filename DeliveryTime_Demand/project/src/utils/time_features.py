"""Time-based feature extraction and processing."""
import pandas as pd
from typing import Dict, Any, Optional
from datetime import datetime
from .time_parsers import decimal_to_time, parse_standard_time, decimal_to_hour
from .date_parsers import parse_date


def extract_time_features(df: pd.DataFrame) -> pd.DataFrame:
    """Extract time-based features from datetime columns."""
    df = df.copy()
    
    try:
        # Convert Order_Date to datetime if not already
        if 'Order_Date' in df.columns:
            df['Order_Date'] = pd.to_datetime(df['Order_Date'])
            
            # Extract hour from Time_Orderd if available
            if 'Time_Orderd' in df.columns:
                df['hour'] = df['Time_Orderd'].apply(decimal_to_hour)
            else:
                df['hour'] = df['Order_Date'].dt.hour
            
            # Fill missing hours with median
            median_hour = int(df['hour'].dropna().median())
            df['hour'] = df['hour'].fillna(median_hour)
            
            # Extract day of week
            df['day_of_week'] = df['Order_Date'].dt.dayofweek
            df['is_weekend'] = df['day_of_week'].isin([5, 6]).astype(int)
            
            # Add order count column for aggregations
            df['order_count'] = 1
            
        return df
        
    except Exception as e:
        raise ValueError(f"Error extracting time features: {str(e)}")

