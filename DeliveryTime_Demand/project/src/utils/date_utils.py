"""Date parsing utilities."""
import pandas as pd
from datetime import datetime
from typing import Optional

def parse_date(date_str: str) -> Optional[datetime]:
    """Parse date string with multiple format support."""
    formats = [
        '%d-%m-%Y',  # 13-02-2022
        '%Y-%m-%d',  # 2022-02-13
        '%m/%d/%Y',  # 02/13/2022
        '%d/%m/%Y'   # 13/02/2022
    ]
    
    for fmt in formats:
        try:
            return datetime.strptime(date_str, fmt)
        except ValueError:
            continue
            
    return None

def convert_dates(df: pd.DataFrame, date_col: str = 'Order_Date') -> pd.DataFrame:
    """Convert date column to datetime with proper format handling."""
    df = df.copy()
    
    # Try parsing with multiple formats
    df[date_col] = df[date_col].apply(parse_date)
    
    # Handle any remaining unparseable dates
    df[date_col] = pd.to_datetime(df[date_col], errors='coerce')
    
    return df