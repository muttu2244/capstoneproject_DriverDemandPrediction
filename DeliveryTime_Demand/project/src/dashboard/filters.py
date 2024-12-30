"""Dashboard filter components."""
import streamlit as st
import pandas as pd

def create_sidebar_filters(data: pd.DataFrame):
    """Create sidebar filters for the dashboard."""
    st.sidebar.header("Filters")
    
    # Date range filter
    date_range = st.sidebar.date_input(
        "Select Date Range",
        value=(data['Order_Date'].min(), data['Order_Date'].max())
    )
    
    # Weather filter
    weather_options = ['All'] + list(data['Weatherconditions'].unique())
    selected_weather = st.sidebar.selectbox("Weather Condition", weather_options)
    
    # Traffic filter
    traffic_options = ['All'] + list(data['Road_traffic_density'].unique())
    selected_traffic = st.sidebar.selectbox("Traffic Condition", traffic_options)
    
    return date_range, selected_weather, selected_traffic

def apply_filters(data: pd.DataFrame, date_range, weather, traffic):
    """Apply selected filters to the data."""
    filtered_data = data.copy()
    
    if weather != 'All':
        filtered_data = filtered_data[filtered_data['Weatherconditions'] == weather]
    if traffic != 'All':
        filtered_data = filtered_data[filtered_data['Road_traffic_density'] == traffic]
        
    return filtered_data