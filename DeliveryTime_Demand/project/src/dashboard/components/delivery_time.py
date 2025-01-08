"""Delivery time analysis components."""
import streamlit as st
import plotly.express as px
import pandas as pd
from typing import Dict, Any
from src.data.processor import DataProcessor
import plotly.graph_objects as go

def display_delivery_analysis(data: pd.DataFrame) -> None:
    """Display comprehensive delivery time analysis."""
    st.header("⏱️ Delivery Time Analysis")
    
    # Basic metrics
    col1, col2, col3, col4 = st.columns(4)
    with col1:
        avg_time = data['time_taken(min)'].mean()
        st.metric("Average Time", f"{avg_time:.1f} min")
    with col2:
        median_time = data['time_taken(min)'].median()
        st.metric("Median Time", f"{median_time:.1f} min")
    with col3:
        ontime_rate = (data['time_taken(min)'] <= 30).mean() * 100
        st.metric("On-time Rate", f"{ontime_rate:.1f}%")
    with col4:
        std_time = data['time_taken(min)'].std()
        st.metric("Time Variability", f"±{std_time:.1f} min")
    
    # Detailed analysis sections
    col1, col2 = st.columns(2)
    
    with col1:
        # Time distribution
        st.subheader("📊 Delivery Time Distribution")
        fig = px.histogram(
            data,
            x='time_taken(min)',
            nbins=30,
            title="Distribution of Delivery Times"
        )
        st.plotly_chart(fig, use_container_width=True)
        
        # Weather impact
        st.subheader("🌦️ Weather Impact Analysis")
        weather_impact = analyze_weather_impact(data)
        fig = px.bar(
            weather_impact,
            x='condition',
            y='avg_time',
            error_y='std_time',
            title="Delivery Time by Weather Condition"
        )
        st.plotly_chart(fig, use_container_width=True)
    
    with col2:
        # Traffic impact
        st.subheader("🚦 Traffic Impact Analysis")
        traffic_impact = analyze_traffic_impact(data)
        fig = px.bar(
            traffic_impact,
            x='level',
            y='avg_time',
            error_y='std_time',
            title="Delivery Time by Traffic Level"
        )
        st.plotly_chart(fig, use_container_width=True)
        """
        # Distance impact
        st.subheader("📍 Distance Impact")
        distance_impact = analyze_distance_impact(data)
        
        short_distance = distance_impact[distance_impact['distance'] < 10000]
        long_distance = distance_impact[distance_impact['distance'] >= 10000]

        # Create separate trend lines for each group
        fig = go.Figure()
        fig.add_trace(go.Scatter(x=short_distance['distance'], 
                        y=short_distance['time_taken(min)'],
                        mode='markers',
                        name='Short Distance'))
        fig.add_trace(go.Scatter(x=long_distance['distance'], 
                        y=long_distance['time_taken(min)'],
                        mode='markers',
                        name='Long Distance'))
        """
        
        st.subheader("📍 Distance Impact")
        distance_impact = analyze_distance_impact(data)

        # Split into short and long distance
        short_distance = distance_impact[distance_impact['distance'] < 10000]
        long_distance = distance_impact[distance_impact['distance'] >= 10000]

        # Create figure with both groups using plotly express
        fig = px.scatter(
            distance_impact,
            x='distance',
            y='time_taken(min)',
            color=distance_impact['distance'].apply(lambda x: 'Short Distance' if x < 10000 else 'Long Distance'),
            title="Delivery Time vs Distance",
            trendline="ols",
            color_discrete_sequence=['blue', 'red']
        )

        # Customize the layout
        fig.update_layout(
            legend_title_text='Distance Type',
            xaxis_title='Distance (km)',
            yaxis_title='Time Taken (min)',
            hovermode='closest',
            showlegend=True
        )

        # Add hover information
        fig.update_traces(
            hovertemplate="<br>".join([
                "Distance: %{x:.2f} km",
                "Time: %{y:.1f} min",
                "<extra></extra>"
            ])
        )

        #st.plotly_chart(fig, use_container_width=True)

        # Optional: Add statistical insights
        with st.expander("📊 Distance Analysis Insights"):
            col1, col2 = st.columns(2)
            with col1:
                st.write("Short Distance Stats:")
                st.write(f"Average Time: {short_distance['time_taken(min)'].mean():.2f} min")
                st.write(f"Count: {len(short_distance)}")
            with col2:
                st.write("Long Distance Stats:")
                st.write(f"Average Time: {long_distance['time_taken(min)'].mean():.2f} min")
                st.write(f"Count: {len(long_distance)}")

        '''
        fig = px.scatter(
            distance_impact,
            x='distance',
            y='time_taken(min)',
            trendline="ols",
            title="Delivery Time vs Distance"
        )
        '''
        st.plotly_chart(fig, use_container_width=True)
        
"""
def analyze_weather_impact(data: pd.DataFrame) -> pd.DataFrame:
    '''Analyze weather impact on delivery times.'''
    return data.groupby('Weatherconditions').agg({
        'time_taken(min)': ['mean', 'std', 'count']
    }).reset_index().rename(columns={
        'Weatherconditions': 'condition',
        'time_taken(min)': 'avg_time',
        'std': 'std_time',
        'count': 'orders'
    })

""" 

def analyze_weather_impact(data: pd.DataFrame) -> pd.DataFrame:
    """Analyze weather impact on delivery times."""
    # Group by weather conditions and calculate metrics
    weather_impact = data.groupby('Weatherconditions').agg(
        avg_time=('time_taken(min)', 'mean'),
        std_time=('time_taken(min)', 'std'),
        orders=('time_taken(min)', 'count')
    ).reset_index()

    # Rename columns for clarity
    weather_impact = weather_impact.rename(columns={'Weatherconditions': 'condition'})

    return weather_impact


"""
def analyze_traffic_impact(data: pd.DataFrame) -> pd.DataFrame:
    '''Analyze traffic impact on delivery times.'''
    return data.groupby('Road_traffic_density').agg({
        'time_taken(min)': ['mean', 'std', 'count']
    }).reset_index().rename(columns={
        'Road_traffic_density': 'level',
        'time_taken(min)': 'avg_time',
        'std': 'std_time',
        'count': 'orders'
    })
""" 
def analyze_traffic_impact(data: pd.DataFrame) -> pd.DataFrame:
    """Analyze traffic impact on delivery times."""
    # Group by traffic density and calculate metrics
    traffic_impact = data.groupby('Road_traffic_density').agg(
        avg_time=('time_taken(min)', 'mean'),
        std_time=('time_taken(min)', 'std'),
        orders=('time_taken(min)', 'count')
    ).reset_index()

    # Rename columns for clarity
    traffic_impact = traffic_impact.rename(columns={'Road_traffic_density': 'level'})

    return traffic_impact

"""
def analyze_distance_impact(data: pd.DataFrame) -> pd.DataFrame:
    '''Analyze distance impact on delivery times.'''
    data = data.copy()
    dp = DataProcessor
    data['distance'] = dp._calculate_distances(data)
    return data
"""

def analyze_distance_impact(data: pd.DataFrame) -> pd.DataFrame:
    """Analyze distance impact on delivery times."""
    try:
        # Ensure a copy to avoid mutating the original DataFrame
        data = data.copy()
        
        # Calculate distances and ensure alignment
        dp = DataProcessor()
        data = dp._calculate_distances(data)
        
        # Check if the distance column exists and has the correct length
        if 'distance' not in data.columns or len(data['distance']) != len(data):
            raise ValueError("Distance calculation failed or resulted in a mismatch.")
        
        # Filter required columns and drop any rows with missing values
        result = data[['distance', 'time_taken(min)']].dropna()
        return result
    
    except Exception as e:
        print(f"Error analyzing distance impact: {str(e)}")
        return pd.DataFrame()  # Return an empty DataFrame to handle errors gracefully