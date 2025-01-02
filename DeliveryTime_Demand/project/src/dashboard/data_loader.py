"""Data loading and caching module for dashboard."""
import streamlit as st
import pandas as pd
from src.data_processor import DataProcessor
from src.utils.data_preprocessing import preprocess_delivery_data

@st.cache_data
def load_dashboard_data():
    """Load and preprocess data with caching."""
    data = pd.read_csv('data/raw/delivery_data.csv')
    data = preprocess_delivery_data(data)
    processor = DataProcessor()
    return processor.preprocess(data)