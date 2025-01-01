"""Hourly order pattern visualization."""
import streamlit as st
import plotly.express as px
import pandas as pd

def plot_hourly_pattern(data):
    """Plot hourly order distribution."""
    if data is not None:
        hourly_data = data.groupby('hour')['order_count'].mean().reset_index()
    else:
        # Sample data for testing
        hourly_data = pd.DataFrame({
            'hour': range(24),
            'order_count': [10, 8, 5, 3, 2, 5, 15, 25, 30, 28, 35, 45,
                          50, 40, 35, 30, 35, 45, 50, 40, 30, 25, 20, 15]
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