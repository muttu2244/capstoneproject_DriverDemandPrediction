"""Data loading utilities for dashboard."""
import streamlit as st
import pandas as pd
from pathlib import Path
from typing import Optional

@st.cache_data
def load_dashboard_data() -> Optional[pd.DataFrame]:
    """Load and cache dashboard data."""
    try:
        # Get the absolute path to the data directory
        data_path = Path(__file__).parent.parent.parent / "data" / "raw" / "delivery_data.csv"
        
        if not data_path.exists():
            st.error(f"Data file not found at {data_path}")
            return None
            
        # Load raw data
        data = pd.read_csv(
            data_path,
            parse_dates=['Order_Date'],
            date_format='%d-%m-%Y'
        )
        
        # Add derived columns
        data = add_derived_columns(data)
            
        return data
        
    except Exception as e:
        st.error(f"Error loading data: {str(e)}")
        return None

def add_derived_columns(df: pd.DataFrame) -> pd.DataFrame:
    """Add derived columns for analysis."""
    df = df.copy()
    
    # Add hour column from Order_Date
    df['hour'] = df['Order_Date'].dt.hour
    
    # Add day of week
    df['day_of_week'] = df['Order_Date'].dt.dayofweek
    
    # Add is_weekend flag
    df['is_weekend'] = df['day_of_week'].isin([5, 6]).astype(int)
    
    # Add order count column for aggregations
    df['order_count'] = 1
    
    return df