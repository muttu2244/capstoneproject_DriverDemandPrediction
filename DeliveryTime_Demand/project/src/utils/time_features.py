"""Time-based feature extraction and processing."""
import pandas as pd
from typing import Dict, Any, Optional
from datetime import datetime
from .time_parsers import decimal_to_time, parse_standard_time
from .date_parsers import parse_date

def parse_time(time_value: Any) -> Optional[pd.Timestamp]:
    """Parse time value to pandas Timestamp with proper error handling."""
    try:
        # Handle NaN values
        if pd.isna(time_value):
            return None
            
        # Convert to string if numeric
        if isinstance(time_value, (float, int)):
            time_str = decimal_to_time(float(time_value))
            if time_str is None:
                return None
        else:
            time_str = str(time_value)
            
        # Try standard time formats
        result = parse_standard_time(time_str)
        if result is not None:
            return result
            
        # Last resort: try dateutil parser
        return pd.to_datetime(time_str)
    except Exception:
        return None

def extract_time_features(df: pd.DataFrame) -> pd.DataFrame:
    """Extract time-based features from datetime columns with error handling."""
    df = df.copy()
    
    try:
        # Handle Time_Order column
        if 'Time_Order' in df.columns:
            time_col = 'Time_Order'
        elif 'Time_Orderd' in df.columns:
            time_col = 'Time_Orderd'
        else:
            raise KeyError("Neither 'Time_Order' nor 'Time_Orderd' column found in dataframe")
        
        # Convert time strings to datetime and handle NaN values
        parsed_times = df[time_col].apply(parse_time)
        df['hour'] = parsed_times.apply(lambda x: x.hour if x is not None else None)
        
        # Fill NaN hours with median
        median_hour = df['hour'].median()
        df['hour'] = df['hour'].fillna(median_hour)
        
        # Handle Order_Date column with multiple format support
        if 'Order_Date' in df.columns:
            parsed_dates = df['Order_Date'].apply(parse_date)
            df['day_of_week'] = parsed_dates.apply(lambda x: x.dayofweek if x is not None else None)
            df['is_weekend'] = df['day_of_week'].isin([5, 6]).astype(int)
            
            # Handle any unparseable dates
            median_day = df['day_of_week'].median()
            df['day_of_week'] = df['day_of_week'].fillna(median_day)
        else:
            raise KeyError("'Order_Date' column not found in dataframe")
        
        return df
        
    except Exception as e:
        raise ValueError(f"Error extracting time features: {str(e)}")

def parse_order_time(time_str: str) -> Dict[str, Any]:
    """Parse order time string into hour and check if weekend."""
    try:
        dt = parse_time(time_str)
        if dt is None:
            raise ValueError(f"Could not parse time string: {time_str}")
        return {
            'hour': dt.hour,
            'is_weekend': 0  # Default to weekday for single predictions
        }
    except Exception as e:
        raise ValueError(f"Error parsing order time: {str(e)}")