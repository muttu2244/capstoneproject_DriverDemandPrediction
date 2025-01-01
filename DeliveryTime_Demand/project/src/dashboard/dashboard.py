"""Main dashboard application."""
import streamlit as st
from typing import Tuple
from .components.layout import create_layout
from .components.filters import create_filters
from .components.delivery_time import display_delivery_analysis
from .components.demand_analysis import display_demand_analysis
from .data_loader import load_dashboard_data

def main():
    """Main dashboard function."""
    st.set_page_config(
        page_title="Delivery Analytics Dashboard",
        page_icon="🚚",
        layout="wide"
    )

    # Create main layout
    header, delivery_section, demand_section = create_layout()
    
    with header:
        st.title("🚚 Delivery Analytics Dashboard")
        st.markdown("""
        Comprehensive analysis of delivery times and driver demand patterns.
        Use the sidebar filters to explore different scenarios.
        """)
    
    try:
        # Load data
        data = load_dashboard_data()
        
        if data is not None:
            # Create and apply filters
            filters = create_filters(data)
            filtered_data = filters.apply_filters(data)
            
            # Display delivery time analysis
            with delivery_section:
                display_delivery_analysis(filtered_data)
            
            # Display demand analysis
            with demand_section:
                display_demand_analysis(filtered_data)
                
        else:
            st.error("No data available. Please check your data source.")
            
    except Exception as e:
        st.error(f"An error occurred: {str(e)}")

if __name__ == "__main__":
    main()