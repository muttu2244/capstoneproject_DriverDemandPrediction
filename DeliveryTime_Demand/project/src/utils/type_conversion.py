"""Type conversion utilities for data preprocessing."""
import pandas as pd
import numpy as np
from typing import Any, Optional
from datetime import datetime

def to_numeric_safe(value: Any) -> float:
    """Convert value to float, with fallback to 0.0."""
    try:
        if pd.isna(value):
            return 0.0
        if isinstance(value, str):
            # Remove any non-numeric characters except decimal point and minus
            value = ''.join(c for c in value if c.isdigit() or c in '.-')
        return float(value)
    except (ValueError, TypeError):
        return 0.0

def to_int_safe(value: Any) -> int:
    """Convert value to integer, with fallback to 0."""
    try:
        num = to_numeric_safe(value)
        return int(num)
    except (ValueError, TypeError):
        return 0

def extract_hour(time_value: Any) -> int:
    """Extract hour from time value, with fallback to 12."""
    try:
        if pd.isna(time_value):
            return 12
            
        # Handle numeric values (decimal time)
        if isinstance(time_value, (int, float)):
            hour = int((float(time_value) * 24) % 24)
            return hour if 0 <= hour < 24 else 12
            
        # Handle string time formats
        if isinstance(time_value, str):
            time_str = time_value.strip()
            
            # Try HH:MM format
            if ':' in time_str:
                hour = int(time_str.split(':')[0])
                return hour if 0 <= hour < 24 else 12
                
            # Try decimal format
            try:
                hour = int((float(time_str) * 24) % 24)
                return hour if 0 <= hour < 24 else 12
            except ValueError:
                return 12
                
        return 12
    except:
        return 12

def parse_time(time_str: str) -> Optional[datetime]:
    """Parse time string into datetime object."""
    formats = ['%H:%M', '%H:%M:%S', '%I:%M %p', '%I:%M:%S %p']
    
    for fmt in formats:
        try:
            return datetime.strptime(time_str, fmt)
        except ValueError:
            continue
            
    return None