"""Chart components for the dashboard."""
import streamlit as st
import plotly.express as px
import pandas as pd
from typing import Optional

def plot_hourly_pattern(data: pd.DataFrame) -> None:
    """Plot hourly order distribution."""
    hourly_data = data.groupby('hour')['order_count'].mean().reset_index()
    
    st.subheader("📈 Hourly Order Pattern")
    fig = px.line(
        hourly_data,
        x='hour',
        y='order_count',
        title="Orders by Hour",
        markers=True
    )
    fig.update_layout(
        xaxis_title="Hour of Day",
        yaxis_title="Average Orders"
    )
    st.plotly_chart(fig, use_container_width=True)

def plot_weather_impact(data: pd.DataFrame) -> None:
    """Plot weather impact on delivery times."""
    weather_impact = data.groupby('Weatherconditions')['time_taken(min)'].agg(['mean', 'count']).reset_index()
    
    st.subheader("🌦️ Weather Impact")
    fig = px.bar(
        weather_impact,
        x='Weatherconditions',
        y='mean',
        title="Average Delivery Time by Weather",
        labels={'mean': 'Average Time (minutes)'},
        text='count'
    )
    st.plotly_chart(fig, use_container_width=True)

def plot_traffic_impact(data: pd.DataFrame) -> None:
    """Plot traffic impact on delivery times."""
    traffic_impact = data.groupby('Road_traffic_density')['time_taken(min)'].mean().reset_index()
    
    st.subheader("🚦 Traffic Impact")
    fig = px.bar(
        traffic_impact,
        x='Road_traffic_density',
        y='time_taken(min)',
        title="Average Delivery Time by Traffic",
        labels={'time_taken(min)': 'Average Time (minutes)'}
    )
    st.plotly_chart(fig, use_container_width=True)