"""Time parsing utilities."""
import pandas as pd
from typing import Optional, Union
from datetime import time

def decimal_to_hour(decimal_time: Union[float, str]) -> Optional[int]:
    """Convert decimal time to hour.
    
    Args:
        decimal_time: Time in decimal format (e.g., 0.458333333 = 11:00)
        
    Returns:
        Hour (0-23) or None if parsing fails
    """
    try:
        if pd.isna(decimal_time):
            return None
            
        # Convert string to float if needed
        if isinstance(decimal_time, str):
            decimal_time = float(decimal_time)
            
        # Convert decimal to hours
        hours = int(decimal_time * 24)
        
        # Handle edge cases
        if hours >= 24:
            hours = hours % 24
            
        return hours
    except (ValueError, TypeError):
        return None

def combine_date_time(date: pd.Timestamp, decimal_time: Union[float, str]) -> Optional[pd.Timestamp]:
    """Combine date and decimal time into timestamp."""
    try:
        if pd.isna(date) or pd.isna(decimal_time):
            return None
            
        hour = decimal_to_hour(decimal_time)
        if hour is None:
            return None
            
        return pd.Timestamp.combine(
            date.date(),
            time(hour=hour)
        )
    except Exception:
        return None