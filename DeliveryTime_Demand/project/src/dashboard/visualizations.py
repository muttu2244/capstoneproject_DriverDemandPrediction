"""Dashboard visualization components."""
import streamlit as st
import plotly.express as px
import plotly.graph_objects as go
import pandas as pd

def plot_delivery_time_distribution(data: pd.DataFrame):
    """Plot delivery time distribution."""
    fig = px.histogram(
        data,
        x='time_taken(min)',
        nbins=30,
        title="Distribution of Delivery Times",
        labels={'time_taken(min)': 'Delivery Time (minutes)'}
    )
    st.plotly_chart(fig, use_container_width=True)

def plot_weather_impact(data: pd.DataFrame):
    """Plot weather impact on delivery time."""
    weather_impact = data.groupby('Weatherconditions')['time_taken(min)'].agg(['mean', 'count']).reset_index()
    fig = px.bar(
        weather_impact,
        x='Weatherconditions',
        y='mean',
        title="Average Delivery Time by Weather",
        labels={'mean': 'Average Time (minutes)'},
        text='count'
    )
    st.plotly_chart(fig, use_container_width=True)

def plot_traffic_impact(data: pd.DataFrame):
    """Plot traffic impact on delivery time."""
    traffic_impact = data.groupby('Road_traffic_density')['time_taken(min)'].mean().reset_index()
    fig = px.bar(
        traffic_impact,
        x='Road_traffic_density',
        y='time_taken(min)',
        title="Average Delivery Time by Traffic Condition",
        labels={'time_taken(min)': 'Average Time (minutes)'}
    )
    st.plotly_chart(fig, use_container_width=True)

def plot_hourly_patterns(data: pd.DataFrame):
    """Plot hourly order patterns."""
    hourly_orders = data.groupby('hour').size().reset_index(name='count')
    fig = px.line(
        hourly_orders,
        x='hour',
        y='count',
        title="Order Volume by Hour",
        labels={'count': 'Number of Orders', 'hour': 'Hour of Day'}
    )
    st.plotly_chart(fig, use_container_width=True)