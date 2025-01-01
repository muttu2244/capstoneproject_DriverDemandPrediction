"""Data validation utilities."""
import pandas as pd
from typing import List, Tuple

def validate_required_columns(df: pd.DataFrame) -> Tuple[bool, List[str]]:
    """Validate that all required columns are present."""
    required_columns = {
        'Order_Date',
        'time_taken(min)',
        'Weatherconditions',
        'Road_traffic_density',
        'Type_of_vehicle',
        'Restaurant_latitude',
        'Restaurant_longitude',
        'Delivery_location_latitude',
        'Delivery_location_longitude'
    }
    
    missing_columns = required_columns - set(df.columns)
    return len(missing_columns) == 0, list(missing_columns)

def validate_data_types(df: pd.DataFrame) -> Tuple[bool, List[str]]:
    """Validate data types of key columns."""
    type_errors = []
    
    # Check numeric columns
    numeric_columns = [
        'time_taken(min)',
        'Restaurant_latitude',
        'Restaurant_longitude',
        'Delivery_location_latitude',
        'Delivery_location_longitude'
    ]
    for col in numeric_columns:
        if col in df.columns and not pd.api.types.is_numeric_dtype(df[col]):
            type_errors.append(f"{col} should be numeric")
    
    # Check datetime columns
    if 'Order_Date' in df.columns and not pd.api.types.is_datetime64_any_dtype(df['Order_Date']):
        type_errors.append("Order_Date should be datetime")
    
    return len(type_errors) == 0, type_errors