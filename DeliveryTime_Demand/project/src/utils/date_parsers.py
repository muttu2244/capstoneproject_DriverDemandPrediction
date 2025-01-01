"""Date parsing utilities with support for multiple formats."""
import pandas as pd
from typing import Optional
from datetime import datetime

def parse_date(date_str: str) -> Optional[pd.Timestamp]:
    """Parse date string with multiple format support."""
    formats = [
        '%Y-%m-%d',  # 2022-02-13
        '%d-%m-%Y',  # 13-02-2022
        '%m/%d/%Y',  # 02/13/2022
        '%d/%m/%Y'   # 13/02/2022
    ]
    
    if pd.isna(date_str):
        return None
        
    # If already a timestamp, return as is
    if isinstance(date_str, (pd.Timestamp, datetime)):
        return pd.Timestamp(date_str)
    
    # Try parsing with each format
    for fmt in formats:
        try:
            return pd.to_datetime(date_str, format=fmt)
        except ValueError:
            continue
    
    # If no format works, try pandas default parser
    try:
        return pd.to_datetime(date_str)
    except ValueError as e:
        raise ValueError(f"Could not parse date {date_str}")
