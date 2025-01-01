"""Comprehensive delivery time analysis component."""
import streamlit as st
import plotly.express as px
import pandas as pd
from typing import Dict, Any

def display_delivery_analysis(data: pd.DataFrame) -> None:
    """Display comprehensive delivery time analysis."""
    st.header("🚚 Delivery Time Analysis")
    
    # Overall metrics
    col1, col2, col3, col4 = st.columns(4)
    
    with col1:
        avg_time = data['time_taken(min)'].mean()
        st.metric("Average Time", f"{avg_time:.1f} min")
    
    with col2:
        peak_traffic_time = data[data['Road_traffic_density'] == 'High']['time_taken(min)'].mean()
        st.metric("Peak Traffic Time", f"{peak_traffic_time:.1f} min")
    
    with col3:
        weather_impact = data[data['Weatherconditions'] != 'Clear']['time_taken(min)'].mean() - \
                        data[data['Weatherconditions'] == 'Clear']['time_taken(min)'].mean()
        st.metric("Weather Impact", f"+{weather_impact:.1f} min")
    
    with col4:
        avg_distance = data['distance'].mean()
        st.metric("Avg Distance", f"{avg_distance:.1f} km")
    
    # Weather analysis
    st.subheader("🌦️ Weather Impact Analysis")
    weather_data = data.groupby('Weatherconditions')['time_taken(min)'].mean().reset_index()
    fig = px.bar(
        weather_data,
        x='Weatherconditions',
        y='time_taken(min)',
        title="Delivery Time by Weather"
    )
    st.plotly_chart(fig, use_container_width=True)
    
    # Traffic analysis
    st.subheader("🚦 Traffic Impact Analysis")
    traffic_data = data.groupby('Road_traffic_density')['time_taken(min)'].mean().reset_index()
    fig = px.bar(
        traffic_data,
        x='Road_traffic_density',
        y='time_taken(min)',
        title="Delivery Time by Traffic"
    )
    st.plotly_chart(fig, use_container_width=True)