"""Date parsing utilities with support for multiple formats."""
import pandas as pd
from typing import Optional

def parse_date(date_str: str) -> Optional[pd.Timestamp]:
    """Parse date string with DD-MM-YYYY format."""
    try:
        return pd.to_datetime(date_str, format='%d-%m-%Y')
    except ValueError as e:
        raise ValueError(f"Error parsing date {date_str}: {str(e)}")