"""Dashboard layout components."""
import streamlit as st
from typing import Tuple

def create_layout() -> Tuple[st.container, st.container, st.container]:
    """Create main dashboard layout."""
    # Create main containers
    header = st.container()
    st.markdown("---")
    
    delivery_section = st.container()
    st.markdown("---")
    
    demand_section = st.container()
    
    return header, delivery_section, demand_section