"""Data filtering utilities for the dashboard."""
import pandas as pd
from typing import Tuple
from datetime import date

def filter_data(data: pd.DataFrame, date_range: Tuple[date, date], weather: str, traffic: str) -> pd.DataFrame:
    """Apply filters to the dashboard data.
    
    Args:
        data: DataFrame containing delivery data
        date_range: Tuple of (start_date, end_date)
        weather: Selected weather condition or 'All'
        traffic: Selected traffic condition or 'All'
        
    Returns:
        Filtered DataFrame
    """
    filtered = data.copy()
    
    # Apply date filter
    if len(date_range) == 2:
        filtered = filtered[
            (filtered['Order_Date'].dt.date >= date_range[0]) &
            (filtered['Order_Date'].dt.date <= date_range[1])
        ]
    
    # Apply weather filter
    if weather != 'All':
        filtered = filtered[filtered['Weatherconditions'] == weather]
    
    # Apply traffic filter
    if traffic != 'All':
        filtered = filtered[filtered['Road_traffic_density'] == traffic]
    
    return filtered