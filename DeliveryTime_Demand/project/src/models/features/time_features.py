"""Time-based feature extraction."""
import pandas as pd
import numpy as np
from typing import Dict, Any, Optional
from ...utils.time_parsers import parse_time_string

def extract_time_features(df: pd.DataFrame) -> pd.DataFrame:
    """Extract time-based features from datetime columns."""
    df = df.copy()
    
    try:
        # Extract hour from available time columns
        time_columns = ['Time_Orderd', 'Time_Order', 'order_time']
        hour_extracted = False
        
        for col in time_columns:
            if col in df.columns:
                try:
                    df['hour'] = df[col].apply(lambda x: extract_hour(x) if pd.notna(x) else 12)
                    hour_extracted = True
                    break
                except Exception:
                    continue
        
        # If no time column was successfully processed, set default hour
        if not hour_extracted:
            df['hour'] = 12
        
        # Ensure hour is integer
        df['hour'] = df['hour'].astype('Int64')
        
        return df
        
    except Exception as e:
        raise ValueError(f"Error extracting time features: {str(e)}")

def extract_hour(time_value: Any) -> int:
    """Extract hour from time value with robust error handling."""
    try:
        # Handle NaN/None
        if pd.isna(time_value):
            return 12
            
        # Convert to string
        time_str = str(time_value).strip()
        
        # Parse time string
        hour = parse_time_string(time_str)
        
        # Validate hour
        if 0 <= hour < 24:
            return hour
        return 12
        
    except Exception:
        return 12  # Default to noon on any error