"""Interactive dashboard for delivery analytics."""
import streamlit as st
from src.dashboard.data_loader import load_dashboard_data
from src.dashboard.filters import create_sidebar_filters, apply_filters
from src.dashboard.visualizations import (
    plot_delivery_time_distribution,
    plot_weather_impact,
    plot_traffic_impact,
    plot_hourly_patterns
)
from src.dashboard.model_metrics import display_model_metrics, display_peak_demand_forecast

# Page config
st.set_page_config(
    page_title="Delivery Analytics Dashboard",
    page_icon="🚚",
    layout="wide"
)

# Title
st.title("🚚 Delivery Analytics Dashboard")

try:
    # Load data
    data = load_dashboard_data()
    
    # Create filters
    date_range, selected_weather, selected_traffic = create_sidebar_filters(data)
    
    # Apply filters
    filtered_data = apply_filters(data, date_range, selected_weather, selected_traffic)
    
    # Create visualizations
    col1, col2 = st.columns(2)
    
    with col1:
        st.subheader("📊 Delivery Time Distribution")
        plot_delivery_time_distribution(filtered_data)
        
        st.subheader("🌦️ Weather Impact on Delivery Time")
        plot_weather_impact(filtered_data)
    
    with col2:
        st.subheader("🚦 Traffic Impact Analysis")
        plot_traffic_impact(filtered_data)
        
        st.subheader("📈 Hourly Order Patterns")
        plot_hourly_patterns(filtered_data)
    
    # Display model metrics and peak demand forecast
    st.markdown("---")
    display_model_metrics(filtered_data)
    
    st.markdown("---")
    display_peak_demand_forecast(filtered_data)

except Exception as e:
    st.error(f"Error loading data: {str(e)}")
    st.info("Please ensure you have the required data file in the data directory.")