"""City-wise demand analysis component."""
import streamlit as st
import plotly.express as px
import pandas as pd
from typing import Any, Tuple

'''
def display_city_analysis(data: pd.DataFrame) -> None:
    """Display city-wise analysis dashboard."""
    st.header("🏙️ City-wise Analysis")
    
    # Group data by city
    cities = data['City'].unique()
    
    for city in cities:
        city_data = data[data['City'] == city]
        
        with st.expander(f"{city} Analysis", expanded=True):
            col1, col2, col3 = st.columns(3)
            
            # Basic metrics
            with col1:
                total_orders = len(city_data)
                st.metric("Total Orders", f"{total_orders:,}")
            
            with col2:
                avg_time = city_data['time_taken(min)'].mean()
                st.metric("Avg Delivery Time", f"{avg_time:.1f} min")
            
            with col3:
                peak_hours = city_data.groupby('hour')['order_count'].mean()
                peak_hour = peak_hours.idxmax()
                st.metric("Peak Hour", f"{peak_hour:02d}:00")
            
            # Hourly pattern
            st.subheader("📈 Hourly Orders")
            hourly_data = city_data.groupby('hour')['order_count'].mean().reset_index()
            fig = px.line(
                hourly_data,
                x='hour',
                y='order_count',
                title=f"Hourly Order Pattern - {city}",
                markers=True
            )
            st.plotly_chart(fig, use_container_width=True)
'''

'''
def display_city_analysis(data: pd.DataFrame) -> None:
    """Display city-wise analysis dashboard."""
    st.header("🏙️ City-wise Analysis")

    # Remove 'nan analysis' or NaN rows
    data = data[data['City'].notna()]
    data = data[data['City'] != "nan analysis"]
    
    # Group data by city
    cities = data['City'].unique()
    
    for city in cities:
        city_data = data[data['City'] == city]
        
        with st.expander(f"{city} Analysis", expanded=True):
            col1, col2, col3 = st.columns(3)
            
            # Basic metrics
            with col1:
                total_orders = len(city_data)
                st.metric("Total Orders", f"{total_orders:,}")
            
            with col2:
                avg_time = city_data['time_taken(min)'].mean()
                st.metric("Avg Delivery Time", f"{avg_time:.1f} min")
            
            with col3:
                peak_hours = city_data.groupby('hour')['order_count'].mean()
                peak_hour = peak_hours.idxmax()
                st.metric("Peak Hour", f"{peak_hour:02d}:00")
            
            # Hourly pattern
            st.subheader("📈 Hourly Orders")
            hourly_data = city_data.groupby('hour')['order_count'].mean().reset_index()
            fig = px.line(
                hourly_data,
                x='hour',
                y='order_count',
                title=f"Hourly Order Pattern - {city}",
                markers=True
            )
            st.plotly_chart(fig, use_container_width=True)
'''

# Dashboard function to display charts
def display_city_analysis(filtered_data: pd.DataFrame):
    # Ensure filtered data has relevant columns
    if 'demand' not in filtered_data.columns or 'date' not in filtered_data.columns:
        st.error("Required columns are missing in the filtered data.")
        return

    # Plotting the data (example with Plotly)
    fig = px.line(filtered_data, x='date', y='demand', title='City Demand Analysis')
    
    # Display the chart
    st.plotly_chart(fig)
