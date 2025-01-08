"""Dashboard filter components."""
import streamlit as st
from datetime import datetime, timedelta
from typing import Tuple, Any

def create_filters() -> Tuple[Any, str, str]:
    """Create and return dashboard filters.
    
    Returns:
        Tuple containing:
        - date_range: Selected date range
        - weather: Selected weather condition
        - traffic: Selected traffic condition
    """
    st.sidebar.header("📊 Filters")
    
    # Date range filter
    #default_start = datetime.now() - timedelta(days=30)
    #default_end = datetime.now()
    default_start = datetime(2022, 2, 15)  # Date format: year, month, day
    default_end = datetime(2022, 4, 15)
    date_range = st.sidebar.date_input(
        "Date Range",
        value=(default_start, default_end),
        key="date_range"
    )
    
    # Weather filter
    weather_options = ['All', 'Clear', 'Cloudy', 'Fog', 'Rain', 'Storm']
    weather = st.sidebar.selectbox(
        "Weather Condition",
        options=weather_options,
        key="weather"
    )
    
    # Traffic filter
    traffic_options = ['All', 'Low', 'Medium', 'High', 'Jam']
    traffic = st.sidebar.selectbox(
        "Traffic Condition",
        options=traffic_options,
        key="traffic"
    )
    
    return date_range, weather, traffic