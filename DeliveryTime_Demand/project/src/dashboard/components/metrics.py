"""Basic metrics display component."""
import streamlit as st
import pandas as pd

def display_basic_metrics(data: pd.DataFrame) -> None:
    """Display basic delivery metrics."""
    col1, col2, col3 = st.columns(3)
    
    with col1:
        total_orders = len(data) if data is not None else 0
        st.metric("Total Orders", f"{total_orders:,}")
    
    with col2:
        avg_time = data['time_taken(min)'].mean() if data is not None else 0
        st.metric("Average Delivery Time", f"{avg_time:.1f} mins")
    
    with col3:
        ontime_rate = (data['time_taken(min)'] <= 30).mean() * 100 if data is not None else 0
        st.metric("On-time Rate", f"{ontime_rate:.1f}%")