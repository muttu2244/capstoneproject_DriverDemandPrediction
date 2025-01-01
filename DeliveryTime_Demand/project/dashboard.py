"""Entry point for the Streamlit dashboard."""
import streamlit as st
from src.data.data_loader import load_processed_data
from src.dashboard.components.city_analysis import display_city_analysis
from src.dashboard.components.delivery_analysis import display_delivery_analysis
from src.dashboard.components.chatbot_interface import display_chatbot_interface
from src.dashboard.components.metrics import display_basic_metrics
from src.dashboard.components.filters import create_filters
from src.dashboard.utils.filter_utils import filter_data

def main():
    """Main dashboard function."""
    st.set_page_config(
        page_title="Delivery Analytics",
        page_icon="🚚",
        layout="wide"
    )

    st.title("🚚 Delivery Analytics Dashboard")
    
    # Load processed data
    data = load_processed_data()
    
    if data is not None:
        # Create and apply filters
        date_range, weather, traffic = create_filters()
        filtered_data = filter_data(data, date_range, weather, traffic)
        
        # Display components
        display_basic_metrics(filtered_data)
        
        # Create two columns for analysis
        col1, col2 = st.columns(2)
        
        with col1:
            display_city_analysis(filtered_data)
            
        with col2:
            display_delivery_analysis(filtered_data)
        
        # Display chatbot interface
        display_chatbot_interface(filtered_data)
    else:
        st.error("No data available. Please check your data source.")

if __name__ == "__main__":
    main()