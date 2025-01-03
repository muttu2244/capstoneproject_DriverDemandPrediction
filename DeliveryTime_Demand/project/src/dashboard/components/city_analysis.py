"""City-wise demand analysis component."""
import streamlit as st
import plotly.express as px
import pandas as pd

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

def display_city_analysis(data: pd.DataFrame) -> None:
    """Display city-wise analysis dashboard."""
    st.header("🏙️ City-wise Analysis")
    
    if data.empty:
        st.warning("No data available for city analysis.")
        return

    cities = data['City'].unique()
    
    for city in cities:
        city_data = data[data['City'] == city]
        
        with st.expander(f"{city} Analysis", expanded=False):
            col1, col2, col3 = st.columns(3)
            
            with col1:
                total_orders = len(city_data)
                st.metric("Total Orders", f"{total_orders:,}")
            
            with col2:
                avg_time = city_data['time_taken(min)'].mean()
                st.metric("Avg Delivery Time", f"{avg_time:.1f} min")
            
            with col3:
                peak_hours = city_data.groupby('hour')['order_count'].mean()
                peak_hours_sorted = peak_hours[peak_hours == peak_hours.max()]
                peak_hour = ", ".join(f"{hour:02d}:00" for hour in peak_hours_sorted.index)
                st.metric("Peak Hour(s)", peak_hour)
            
            st.subheader("📈 Hourly Orders")
            hourly_data = (
                city_data.groupby('hour')['order_count'].mean()
                .reindex(range(24), fill_value=0)
                .reset_index()
            )
            fig = px.line(
                hourly_data,
                x='hour',
                y='order_count',
                title=f"Hourly Order Pattern - {city}",
                markers=True
            )
            fig.update_layout(
                xaxis_title="Hour of Day",
                yaxis_title="Average Order Count"
            )
            st.plotly_chart(fig, use_container_width=True)
