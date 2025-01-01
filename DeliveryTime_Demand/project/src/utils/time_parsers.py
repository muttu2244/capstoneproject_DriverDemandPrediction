"""Time parsing utilities."""
from typing import Optional, Union
from datetime import time
import pandas as pd

def decimal_to_time(decimal_time: Union[float, str]) -> Optional[str]:
    """Convert decimal time to HH:MM format.
    
    Args:
        decimal_time: Time in decimal format (e.g., 0.458333333 = 11:00)
        
    Returns:
        Time string in HH:MM format or None if parsing fails
    """
    try:
        if pd.isna(decimal_time):
            return None
            
        # Convert string to float if needed
        if isinstance(decimal_time, str):
            decimal_time = float(decimal_time)
            
        # Convert decimal to hours and minutes
        total_minutes = int(decimal_time * 24 * 60)
        hours = total_minutes // 60
        minutes = total_minutes % 60
        
        # Handle edge cases
        if hours >= 24:
            hours = hours % 24
            
        return f"{hours:02d}:{minutes:02d}"
    except (ValueError, TypeError):
        return None

def parse_standard_time(time_str: str) -> Optional[pd.Timestamp]:
    """Parse time string in standard formats.
    
    Args:
        time_str: Time string (e.g., "14:30", "2:30 PM")
        
    Returns:
        Parsed timestamp or None if parsing fails
    """
    formats = [
        '%H:%M',     # 14:30
        '%I:%M %p',  # 2:30 PM
        '%H:%M:%S',  # 14:30:00
        '%I:%M:%S %p'  # 2:30:00 PM
    ]
    
    for fmt in formats:
        try:
            return pd.to_datetime(time_str, format=fmt)
        except ValueError:
            continue
    
    return None

def decimal_to_hour(decimal_time: Union[float, str]) -> Optional[int]:
    """Convert decimal time to hour.
    
    Args:
        decimal_time: Time in decimal format (e.g., 0.458333333 = 11:00)
        
    Returns:
        Hour (0-23) or None if parsing fails
    """
    time_str = decimal_to_time(decimal_time)
    if time_str:
        return int(time_str.split(':')[0])
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

def parse_time_string(time_str: str) -> int:
    """Parse time string to hour (0-23).
    
    Handles formats:
    - HH:MM
    - HH:MM:SS
    - HH.MM
    - Decimal time (e.g., 14.5 = 14:30)
    """
    try:
        # Clean the string
        time_str = time_str.strip()
        
        # Try HH:MM or HH:MM:SS format
        if ':' in time_str:
            return int(time_str.split(':')[0])
        
        # Try decimal format (both . and , as separators)
        if '.' in time_str or ',' in time_str:
            time_str = time_str.replace(',', '.')
            hour = int(float(time_str))
            return hour if 0 <= hour < 24 else 12
        
        # Try plain hour
        hour = int(time_str)
        return hour if 0 <= hour < 24 else 12
        
    except (ValueError, IndexError):
        return 12  # Default to noon on error