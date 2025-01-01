"""Delivery time analysis components."""
import streamlit as st
import plotly.express as px
import pandas as pd
from typing import Dict, Any

def display_delivery_analysis(data: pd.DataFrame) -> None:
    """Display comprehensive delivery time analysis."""
    st.header("⏱️ Delivery Time Analysis")
    
    # Basic metrics
    col1, col2, col3, col4 = st.columns(4)
    with col1:
        avg_time = data['time_taken(min)'].mean()
        st.metric("Average Time", f"{avg_time:.1f} min")
    with col2:
        median_time = data['time_taken(min)'].median()
        st.metric("Median Time", f"{median_time:.1f} min")
    with col3:
        ontime_rate = (data['time_taken(min)'] <= 30).mean() * 100
        st.metric("On-time Rate", f"{ontime_rate:.1f}%")
    with col4:
        std_time = data['time_taken(min)'].std()
        st.metric("Time Variability", f"±{std_time:.1f} min")
    
    # Detailed analysis sections
    col1, col2 = st.columns(2)
    
    with col1:
        # Time distribution
        st.subheader("📊 Delivery Time Distribution")
        fig = px.histogram(
            data,
            x='time_taken(min)',
            nbins=30,
            title="Distribution of Delivery Times"
        )
        st.plotly_chart(fig, use_container_width=True)
        
        # Weather impact
        st.subheader("🌦️ Weather Impact Analysis")
        weather_impact = analyze_weather_impact(data)
        fig = px.bar(
            weather_impact,
            x='condition',
            y='avg_time',
            error_y='std_time',
            title="Delivery Time by Weather Condition"
        )
        st.plotly_chart(fig, use_container_width=True)
    
    with col2:
        # Traffic impact
        st.subheader("🚦 Traffic Impact Analysis")
        traffic_impact = analyze_traffic_impact(data)
        fig = px.bar(
            traffic_impact,
            x='level',
            y='avg_time',
            error_y='std_time',
            title="Delivery Time by Traffic Level"
        )
        st.plotly_chart(fig, use_container_width=True)
        
        # Distance impact
        st.subheader("📍 Distance Impact")
        distance_impact = analyze_distance_impact(data)
        fig = px.scatter(
            distance_impact,
            x='distance',
            y='time_taken(min)',
            trendline="ols",
            title="Delivery Time vs Distance"
        )
        st.plotly_chart(fig, use_container_width=True)

def analyze_weather_impact(data: pd.DataFrame) -> pd.DataFrame:
    """Analyze weather impact on delivery times."""
    return data.groupby('Weatherconditions').agg({
        'time_taken(min)': ['mean', 'std', 'count']
    }).reset_index().rename(columns={
        'Weatherconditions': 'condition',
        'time_taken(min)': 'avg_time',
        'std': 'std_time',
        'count': 'orders'
    })

def analyze_traffic_impact(data: pd.DataFrame) -> pd.DataFrame:
    """Analyze traffic impact on delivery times."""
    return data.groupby('Road_traffic_density').agg({
        'time_taken(min)': ['mean', 'std', 'count']
    }).reset_index().rename(columns={
        'Road_traffic_density': 'level',
        'time_taken(min)': 'avg_time',
        'std': 'std_time',
        'count': 'orders'
    })

def analyze_distance_impact(data: pd.DataFrame) -> pd.DataFrame:
    """Analyze distance impact on delivery times."""
    data = data.copy()
    data['distance'] = calculate_distances(data)
    return data