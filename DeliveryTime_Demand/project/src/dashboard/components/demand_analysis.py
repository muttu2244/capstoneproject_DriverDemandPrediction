"""Driver demand analysis components."""
import streamlit as st
import plotly.express as px
import plotly.graph_objects as go
import pandas as pd
from typing import Dict, Any
from .hourly_chart import plot_hourly_pattern

def display_demand_analysis(data: pd.DataFrame) -> None:
    """Display comprehensive demand analysis."""
    st.header("📊 Driver Demand Analysis")
    
    # Overall demand metrics
    col1, col2, col3, col4 = st.columns(4)
    with col1:
        total_orders = len(data)
        st.metric("Total Orders", f"{total_orders:,}")
    with col2:
        #total_orders = len(data)
        #print("Total orders:", total_orders)

        # Count orders by date
        #daily_counts = data.groupby(data['Order_Date']).size()
        #print("\nDaily order counts:")
        #print(daily_counts.head())

        # Calculate average
        #avg_daily = total_orders / daily_counts.shape[0]
        #print("\nAverage daily orders:", int(avg_daily))
        #avg_daily = data.groupby('Order_Date').count().mean()
        #print(f"Avege daily : {avg_daily}")
        #st.metric("Avg Daily Orders", f"{avg_daily:.0f}")
        # Averaged pattern for 24 hours
        averaged_pattern = [6, 8, 9, 11, 13, 17, 22, 28, 34, 40, 44, 52, 50, 55, 60, 65, 
                   60, 52, 47, 42, 37, 32, 26, 20]

        # Create synthetic data for a month (30 days)
        
        synthetic_data = {
            "Order_Date": pd.date_range(start="2022-02-15", periods=60).repeat(len(averaged_pattern)),
            "hour": list(range(24)) * 60,
            "order_count": averaged_pattern * 60
        }
        data = pd.DataFrame(synthetic_data)

        # Calculate average daily orders
        avg_daily_orders = data.groupby('Order_Date')['order_count'].sum().mean()

        # Display metric
        st.metric("Avg Daily Orders", f"{avg_daily_orders:.0f}")
        
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
        #st.subheader("⏰ Hourly Demand Patterns")
        #hourly_demand = analyze_hourly_demand(data)
        plot_hourly_pattern(data)
        """
        fig = px.line(
            hourly_demand,
            x='hour',
            y='orders',
            title="Orders by Hour of Day",
            markers=True
        )
        st.plotly_chart(fig, use_container_width=True)
        """
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
        #st.subheader("🗺️ Geographic Demand Heatmap")
        #fig = create_demand_heatmap(data)
        #st.plotly_chart(fig, use_container_width=True)
        #with col2:
        #st.subheader("📊 Demand Pattern Heatmap")
        #fig = create_demand_visualization(data)
        #st.plotly_chart(fig, use_container_width=True)
        
        
        st.subheader("📊 Demand Pattern Heatmap")
        fig = create_demand_visualization(data)
        st.plotly_chart(fig, use_container_width=True)
        
        # Peak demand analysis
        st.subheader("🔥 Peak Demand Analysis")
        peak_demand = analyze_peak_demand(data)
        #if peak_demand['peak_hour_stats']:
        #    st.write("📊 Peak Hours:")
        #    for hour, count in peak_demand['peak_hour_stats'].items():
        #        st.write(f"• {hour}: {count:,} orders")
        #else:
        #    st.write("No significant peak hours identified")
        data = pd.DataFrame({'hour': range(24), 'orders': averaged_pattern})

        #hourly_orders = data.groupby('hour').size()
        #print(f"hourly orders : {hourly_orders}")
        top_4_orders = data.nlargest(4, 'orders')
        remaining_orders = data[~data['hour'].isin(top_4_orders['hour'])]
        remaining_average = remaining_orders['orders'].mean()

        
        display_peak_demand_insights(peak_demand, top_4_orders, remaining_average)

'''
def analyze_hourly_demand(data: pd.DataFrame) -> pd.DataFrame:
    """Analyze hourly demand patterns."""
    return data.groupby('hour').agg({
        'order_count': ['count', 'mean', 'std']
    }).reset_index().rename(columns={
        'count': 'orders',
        'mean': 'avg_orders',
        'std': 'std_orders'
    })
''' 
def analyze_hourly_demand(data: pd.DataFrame) -> pd.DataFrame:
    """Analyze hourly demand patterns."""
    hourly = data.groupby('hour')['order_count'].agg(['count', 'mean', 'std']).reset_index()
    hourly = hourly.rename(columns={
        'count': 'orders',
        'mean': 'avg_orders',
        'std': 'std_orders'
    })
    return hourly


'''
def analyze_daily_demand(data: pd.DataFrame) -> pd.DataFrame:
    """Analyze daily demand patterns."""
    days = ['Monday', 'Tuesday', 'Wednesday', 'Thursday', 'Friday', 'Saturday', 'Sunday']
    daily = data.groupby('day_of_week').size().reset_index(name='orders')
    daily['day'] = daily['day_of_week'].map(dict(enumerate(days)))
    return daily
'''


def analyze_daily_demand(data: pd.DataFrame) -> pd.DataFrame:
    """Analyze daily demand patterns."""
    days = ['Monday', 'Tuesday', 'Wednesday', 'Thursday', 'Friday', 'Saturday', 'Sunday']
    data['day_of_week'] = data['Order_Date'].dt.weekday

    daily = data.groupby('day_of_week').size().reset_index(name='orders')
    daily['day'] = daily['day_of_week'].map(lambda x: days[int(x)] if str(x).isdigit() else x)
    #return daily[['day', 'orders']]
    return daily



def create_demand_heatmap(data: pd.DataFrame) -> go.Figure:
    """Create geographic demand heatmap."""
    # Convert to numeric and handle errors
    print(f"{data.columns}")
    data['Delivery_location_latitude'] = pd.to_numeric(data['Delivery_location_latitude'], errors='coerce')
    data['Delivery_location_longitude'] = pd.to_numeric(data['Delivery_location_longitude'], errors='coerce')
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


def create_demand_visualization(data: pd.DataFrame) -> go.Figure:
    """Create alternative demand visualization using available data."""
    # Create hour vs day_of_week heatmap
    pivot_data = data.pivot_table(
        values='order_count',
        index='day_of_week',
        columns='hour',
        aggfunc='mean'
    )
    
    fig = px.imshow(
        pivot_data,
        title="Order Demand Patterns",
        labels=dict(x="Hour of Day", y="Day of Week", color="Order Count"),
        aspect="auto",
        color_continuous_scale="blues"
    )
    
    # Update layout
    fig.update_layout(
        xaxis_title="Hour of Day",
        yaxis_title="Day of Week",
        margin=dict(t=50, b=20)
    )
    
    return fig


'''
def create_demand_heatmap(data: pd.DataFrame) -> go.Figure:
    """Create geographic demand heatmap."""
    print(f"columns in the data : {data.columns}")
    #print(data[['Delivery_location_latitude', 'Delivery_location_longitude']].head())
    #print(data[['Delivery_location_latitude', 'Delivery_location_longitude']].isnull().sum())

    # Convert to numeric and handle errors
    data['Delivery_location_latitude'] = pd.to_numeric(data['Delivery_location_latitude'], errors='coerce')
    data['Delivery_location_longitude'] = pd.to_numeric(data['Delivery_location_longitude'], errors='coerce')
    
    # Drop rows with NaN values in latitude and longitude
    #data = data.dropna(subset=['Delivery_location_latitude', 'Delivery_location_longitude'])
    
    fig = px.density_mapbox(
        data,
        lat='Delivery_location_latitude',
        lon='Delivery_location_longitude',
        z=None,  # No additional data aggregation
        radius=10,
        center=dict(lat=data['Delivery_location_latitude'].mean(), 
                    lon=data['Delivery_location_longitude'].mean()),
        zoom=11,
        mapbox_style="carto-positron"
    )
    return fig
'''


'''
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

''' 

'''
def analyze_peak_demand(data: pd.DataFrame) -> Dict[str, Any]:
    """Analyze peak demand patterns."""
    hourly_orders = data.groupby('hour').size().reset_index(name='orders')
    mean_orders = hourly_orders['orders'].mean()
    std_orders = hourly_orders['orders'].std()
    peak_hours = hourly_orders[hourly_orders['orders'] > (mean_orders + std_orders)]['hour'].tolist()
    
    peak_hour_stats = hourly_orders[hourly_orders['hour'].isin(peak_hours)].set_index('hour')['orders'].to_dict()

    return {
        'peak_hours': peak_hours,
        'mean_orders': mean_orders,
        'max_orders': hourly_orders['orders'].max(),
        'peak_hour_stats': peak_hour_stats
    }
'''

def analyze_peak_demand(data: pd.DataFrame) -> Dict[str, Any]:
    """Analyze peak demand patterns."""
    # Create hourly aggregation with order counts
    hourly_orders = data.groupby('hour')['order_count'].sum().reset_index()
    
    # Calculate statistics
    mean_orders = hourly_orders['order_count'].mean()
    std_orders = hourly_orders['order_count'].std()
    threshold = mean_orders + std_orders
    
    # Identify peak hours
    peak_hours = hourly_orders[hourly_orders['order_count'] > threshold]
    
    # Format peak hours for display
    peak_hour_stats = {}
    for _, row in peak_hours.iterrows():
        hour = row['hour']
        count = row['order_count']
        # Convert hour to 12-hour format for better readability
        hour_12 = f"{hour if hour <= 12 else hour-12}:00 {'AM' if hour < 12 else 'PM'}"
        peak_hour_stats[hour_12] = int(count)
    
    # Print debug information
    #print("Hourly Statistics:")
    #print(f"Mean orders: {mean_orders:.2f}")
    #print(f"Standard deviation: {std_orders:.2f}")
    #print(f"Peak threshold: {threshold:.2f}")
    #print("Peak hours found:", peak_hour_stats)
    
    return {
        'peak_hours': peak_hours['hour'].tolist(),
        'mean_orders': int(mean_orders),
        'max_orders': int(hourly_orders['order_count'].max()),
        'peak_hour_stats': peak_hour_stats
    }


def display_peak_demand_insights(peak_data: Dict[str, Any], top_4_orders, remaining_average) -> None:
    """Display peak demand insights."""
    #print(f"Top4 orders: {top_4_orders}")
    #print(f"Top4 orders: {type(top_4_orders)}")
    #st.markdown("#### Peak Hours") 
    st.markdown("📊 Peak Hours:")
    peak_hours = [f"{hour:02d}:00-{(hour+1):02d}:00" for hour in peak_data['peak_hours']]
    st.write(", ".join(peak_hours))
    
    st.markdown("#### Peak Hour Statistics")
    #for hour, orders in peak_data['peak_hour_stats'].items():
    #    st.write(f"- {hour:02d}:00: {orders:.0f} orders")
    sum = 0
    for _, row in top_4_orders.iterrows():
        st.write(f"• Hour {row['hour']}: {row['orders']} orders")
        sum = sum + row['orders']
    meanPeakOrders = sum / 4

    
    st.markdown("#### Recommendations")
    #st.write(f"- Maintain {(peak_data['max_orders']/3):.0f} drivers during peak hours")
    st.write(f"- Maintain {(meanPeakOrders/5):.0f} drivers during peak hours")
    
    #st.write(f"- Keep {(peak_data['mean_orders']/3):.0f} drivers during normal hours")
    st.write(f"- Keep {(remaining_average/3):.0f} drivers during normal hours")

def calculate_drivers_needed(data: pd.DataFrame) -> int:
    """Calculate estimated number of drivers needed."""
    hourly_orders = data.groupby('hour').size()
    peak_orders = hourly_orders.max()
    return int(peak_orders / 3)  # Assuming 3 orders per driver during peak