"""Data preprocessing utilities."""
import pandas as pd

def preprocess_delivery_data(df: pd.DataFrame) -> pd.DataFrame:
    """Preprocess delivery data with proper type conversions."""
    df = df.copy()
    
    # Convert date column
    df['Order_Date'] = pd.to_datetime(df['Order_Date'], format='%d-%m-%Y')
    
    # Convert numeric columns
    numeric_columns = [
        'time_taken(min)',
        'Delivery_person_Age',
        'Delivery_person_Ratings',
        'Vehicle_condition',
        'multiple_deliveries'
    ]
    
    for col in numeric_columns:
        if col in df.columns:
            df[col] = pd.to_numeric(df[col], errors='coerce')
            # Fill NaN values with column median
            df[col] = df[col].fillna(df[col].median())
    
    return df