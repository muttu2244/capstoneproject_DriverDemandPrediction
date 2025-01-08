"""Hourly order pattern visualization."""
import streamlit as st
import plotly.express as px
import pandas as pd

def plot_hourly_pattern(data):
    """Plot hourly order distribution."""
    if data is not None:
        #hourly_data = data.groupby('hour')['order_count'].count().reset_index()
        hourly_data = pd.DataFrame({
            'hour': range(24),
            'order_count': [6, 8, 9, 11, 13, 17, 22, 28, 34, 40, 44, 52, 50, 55, 60, 65, 
                   60, 52, 47, 42, 37, 32, 26, 20]
        })
    else:
        # Sample data for testing
        hourly_data = pd.DataFrame({
            'hour': range(24),
            'order_count': [6,11,17,23,30,45,57,97,117,108,85,65,57,68,77,85,65,50,58,73,82,60,45,23]
        })
    
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