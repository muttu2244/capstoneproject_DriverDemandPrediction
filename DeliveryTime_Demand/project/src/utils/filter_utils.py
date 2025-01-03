"""Data filtering utilities for the dashboard."""
import pandas as pd
from typing import Tuple
from datetime import date
from typing import Any, Tuple

'''
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



# Function to filter the data based on the provided filters
def filter_data(data: pd.DataFrame, date_range: Tuple[str, str], weather: str, traffic: str) -> pd.DataFrame:
    """Filter data based on the given date range, weather, and traffic."""
    
    # Convert 'Order_Date' column to datetime format if it's not already
    data['Order_Date'] = pd.to_datetime(data['Order_Date'], errors='coerce')
    
    # Convert the date_range strings to datetime objects for comparison
    start_date = pd.to_datetime(date_range[0], errors='coerce')
    end_date = pd.to_datetime(date_range[1], errors='coerce')
    
    # Filter by date range
    data = data[(data['Order_Date'] >= start_date) & (data['Order_Date'] <= end_date)]
    
    # Filter by weather
    if weather:
        data = data[data['weather'] == weather]
    
    # Filter by traffic
    if traffic:
        data = data[data['traffic'] == traffic]
    
    return data
'''


#from typing import Tuple
from datetime import datetime

def filter_data(
    data: pd.DataFrame, 
    date_range: Tuple[datetime, datetime], 
    weather: int,  # Use encoded value instead of raw string
    traffic: int   # Use encoded value instead of raw string
) -> pd.DataFrame:
    """Apply filters to the dashboard data.
    
    Args:
        data: DataFrame containing delivery data.
        date_range: Tuple of (start_date, end_date) as datetime objects.
        weather: Encoded weather condition or -1 for 'All'.
        traffic: Encoded traffic condition or -1 for 'All'.
        
    Returns:
        Filtered DataFrame.
    """
    filtered = data.copy()
    
    # Apply date filter
    if len(date_range) == 2 and 'hour' in filtered.columns:
        filtered = filtered[
            (filtered['hour'] >= date_range[0].hour) &
            (filtered['hour'] <= date_range[1].hour)
        ]
    
    # Apply weather filter
    if weather != -1 and 'Weatherconditions_encoded' in filtered.columns:
        filtered = filtered[filtered['Weatherconditions_encoded'] == weather]
    
    # Apply traffic filter
    if traffic != -1 and 'Road_traffic_density_encoded' in filtered.columns:
        filtered = filtered[filtered['Road_traffic_density_encoded'] == traffic]
    
    return filtered
