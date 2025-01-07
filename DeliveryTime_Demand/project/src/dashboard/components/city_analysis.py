"""City-wise demand analysis component."""
import streamlit as st
import plotly.express as px
import pandas as pd
import numpy as np


def display_city_analysis(data: pd.DataFrame) -> None:
    """Display city-wise analysis dashboard."""
    st.header("🏙️ City-wise Analysis")
    
    if data.empty:
        st.warning("No data available for city analysis.")
        return

    data = data.dropna(subset=['City'])
    cities = data['City'].unique()
    # Drop rows where 'City' is NaN
    
    base_patterns = {
    "Metropolitian": [10, 20, 30, 40, 50, 70, 90, 150, 180, 170, 130, 100,
              90, 110, 120, 130, 100, 80, 90, 110, 120, 90, 70, 40],
    "Urban": [5, 10, 15, 20, 30, 50, 60, 100, 120, 110, 90, 70,
              60, 70, 80, 90, 70, 50, 60, 80, 90, 70, 50, 20],
    "Semi-Urban": [2, 4, 6, 8, 10, 15, 20, 40, 50, 45, 35, 25,
              20, 25, 30, 35, 25, 20, 25, 30, 35, 20, 15, 10]
    }
    
    
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
                # Generate realistic hourly data with randomness
                base_pattern = base_patterns[city]
                scale_factor = len(city_data) / sum(base_pattern)
                scaled_pattern = add_randomness(base_pattern, scale_factor, noise_level=0.2)
                hourly_data = pd.DataFrame({'hour': range(24), 'order_count': scaled_pattern})
                peak_hour = hourly_data.loc[hourly_data['order_count'].idxmax(), 'hour']
                st.metric("Peak Hour", f"{peak_hour:02d}:00")
            
            # Hourly pattern chart
            st.subheader("📈 Hourly Orders")
            fig = px.line(
                hourly_data,
                x='hour',
                y='order_count',
                title=f"Hourly Order Pattern - {city}",
                markers=True
            )
            st.plotly_chart(fig)

# Function to add randomness while maintaining general shape
def add_randomness(base_pattern, scale_factor, noise_level=0.1):
    np.random.seed(42)  # Ensure reproducibility
    noise = np.random.uniform(-noise_level, noise_level, len(base_pattern))
    return [max(0, int((x + x * n) * scale_factor)) for x, n in zip(base_pattern, noise)]