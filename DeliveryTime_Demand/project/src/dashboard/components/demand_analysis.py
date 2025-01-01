"""Driver demand analysis components."""
import streamlit as st
import plotly.express as px
import plotly.graph_objects as go
import pandas as pd
from typing import Dict, Any

def display_demand_analysis(data: pd.DataFrame) -> None:
    """Display comprehensive demand analysis."""
    st.header("📊 Driver Demand Analysis")
    
    # Overall demand metrics
    col1, col2, col3, col4 = st.columns(4)
    with col1:
        total_orders = len(data)
        st.metric("Total Orders", f"{total_orders:,}")
    with col2:
        avg_daily = data.groupby('Order_Date').size().mean()
        st.metric("Avg Daily Orders", f"{avg_daily:.0f}")
    with col3:
        peak_hour_orders = data.groupby('hour').size().max()
        st.metric("Peak Hour Orders", f"{peak_hour_orders:.0f}")
    with col4:
        drivers_needed = calculate_drivers_needed(data)
        st.metric("Estimated Drivers", f"{drivers_needed:.0f}")
    
    # Detailed analysis sections
    col1, col2 = st.columns(2)
    
    with col1:
        # Hourly patterns
        st.subheader("⏰ Hourly Demand Patterns")
        hourly_demand = analyze_hourly_demand(data)
        fig = px.line(
            hourly_demand,
            x='hour',
            y='orders',
            title="Orders by Hour of Day",
            markers=True
        )
        st.plotly_chart(fig, use_container_width=True)
        
        # Daily patterns
        st.subheader("📅 Daily Demand Patterns")
        daily_demand = analyze_daily_demand(data)
        fig = px.bar(
            daily_demand,
            x='day',
            y='orders',
            title="Orders by Day of Week"
        )
        st.plotly_chart(fig, use_container_width=True)
    
    with col2:
        # Geographic demand
        st.subheader("🗺️ Geographic Demand Heatmap")
        fig = create_demand_heatmap(data)
        st.plotly_chart(fig, use_container_width=True)
        
        # Peak demand analysis
        st.subheader("🔥 Peak Demand Analysis")
        peak_demand = analyze_peak_demand(data)
        display_peak_demand_insights(peak_demand)

def analyze_hourly_demand(data: pd.DataFrame) -> pd.DataFrame:
    """Analyze hourly demand patterns."""
    return data.groupby('hour').agg({
        'order_count': ['count', 'mean', 'std']
    }).reset_index().rename(columns={
        'count': 'orders',
        'mean': 'avg_orders',
        'std': 'std_orders'
    })

def analyze_daily_demand(data: pd.DataFrame) -> pd.DataFrame:
    """Analyze daily demand patterns."""
    days = ['Monday', 'Tuesday', 'Wednesday', 'Thursday', 'Friday', 'Saturday', 'Sunday']
    daily = data.groupby('day_of_week').size().reset_index(name='orders')
    daily['day'] = daily['day_of_week'].map(dict(enumerate(days)))
    return daily

def create_demand_heatmap(data: pd.DataFrame) -> go.Figure:
    """Create geographic demand heatmap."""
    return px.density_mapbox(
        data,
        lat='Delivery_location_latitude',
        lon='Delivery_location_longitude',
        radius=10,
        center=dict(lat=data['Delivery_location_latitude'].mean(), 
                   lon=data['Delivery_location_longitude'].mean()),
        zoom=11,
        mapbox_style="carto-positron"
    )

def analyze_peak_demand(data: pd.DataFrame) -> Dict[str, Any]:
    """Analyze peak demand patterns."""
    hourly_orders = data.groupby('hour').size()
    mean_orders = hourly_orders.mean()
    std_orders = hourly_orders.std()
    peak_hours = hourly_orders[hourly_orders > (mean_orders + std_orders)].index.tolist()
    
    return {
        'peak_hours': peak_hours,
        'mean_orders': mean_orders,
        'max_orders': hourly_orders.max(),
        'peak_hour_stats': hourly_orders[peak_hours].to_dict()
    }

def display_peak_demand_insights(peak_data: Dict[str, Any]) -> None:
    """Display peak demand insights."""
    st.markdown("#### Peak Hours")
    peak_hours = [f"{hour:02d}:00-{(hour+1):02d}:00" for hour in peak_data['peak_hours']]
    st.write(", ".join(peak_hours))
    
    st.markdown("#### Peak Hour Statistics")
    for hour, orders in peak_data['peak_hour_stats'].items():
        st.write(f"- {hour:02d}:00: {orders:.0f} orders")
    
    st.markdown("#### Recommendations")
    st.write(f"- Maintain {(peak_data['max_orders']/30):.0f} drivers during peak hours")
    st.write(f"- Keep {(peak_data['mean_orders']/30):.0f} drivers during normal hours")

def calculate_drivers_needed(data: pd.DataFrame) -> int:
    """Calculate estimated number of drivers needed."""
    hourly_orders = data.groupby('hour').size()
    peak_orders = hourly_orders.max()
    return int(peak_orders / 30)  # Assuming 30 orders per driver during peak