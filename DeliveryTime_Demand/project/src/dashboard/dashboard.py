"""Main dashboard application."""
import streamlit as st
from typing import Tuple
from src.dashboard.components.layout import create_layout
from src.dashboard.components.filters import create_filters
from src.dashboard.components.delivery_time import display_delivery_analysis
#from src.dashboard.components.delivery_analysis import display_delivery_analysis
from src.dashboard.components.demand_analysis import display_demand_analysis
from src.dashboard.data_loader import load_dashboard_data
from src.utils.filter_utils import filter_data
from src.dashboard.components.metrics import display_basic_metrics
from src.dashboard.components.city_analysis import display_city_analysis
from src.dashboard.components.chatbot_interface import display_chatbot_interface
from src.dashboard.components.city_analysis import display_city_analysis

def main():
    """Main dashboard function."""
    st.set_page_config(
        page_title="Delivery Analytics Dashboard",
        page_icon="🚚",
        layout="wide"
    )

    # Create main layout
    header, delivery_section, demand_section, city_analysis = create_layout()
    
    with header:
        st.title("🚚 Delivery Analytics Dashboard")
        st.markdown("""
        Comprehensive analysis of delivery times and driver demand patterns.
        Use the sidebar filters to explore different scenarios.
        """)
    
    try:
        # Load data
        data = load_dashboard_data()
        
        if not data.empty:
            # Create and apply filters
            #filters = create_filters(data)
            #filters = create_filters()
            #filtered_data = filters.apply_filters(data)
            #date_range, weather, traffic = create_filters()
            filtered_data = filter_data(data, date_range, weather, traffic)
            
            # Display components
            #display_basic_metrics(filtered_data)
        
            # Create two columns for analysis
            #col1, col2 = st.columns(2)
            
            
            #with col1:
            #    display_city_analysis(filtered_data)
                
            #with col2:
            #    display_delivery_analysis(filtered_data)
            
            # Display chatbot interface
            #display_chatbot_interface(filtered_data)
            
            # Display delivery time analysis
            with delivery_section:
                #display_delivery_analysis(filtered_data)
                display_delivery_analysis(data)
            
            # Display demand analysis
            with demand_section:
                #display_demand_analysis(filtered_data)
                display_demand_analysis(data)
                
            with city_analysis:
                display_city_analysis(data)
                
        else:
            st.error("No data available. Please check your data source.")
            
    except Exception as e:
        st.error(f"An error occurred: {str(e)}")

if __name__ == "__main__":
    main()