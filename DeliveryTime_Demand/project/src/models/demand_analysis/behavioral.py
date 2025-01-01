"""Behavioral demand pattern analysis."""
import pandas as pd
import numpy as np
from typing import Dict, Any

class BehavioralAnalyzer:
    def analyze(self, data: pd.DataFrame) -> Dict[str, Any]:
        """Analyze behavioral patterns in demand."""
        return {
            'weather_impact': self._analyze_weather_impact(data),
            'traffic_patterns': self._analyze_traffic_patterns(data),
            'order_type_analysis': self._analyze_order_types(data),
            'customer_segments': self._analyze_customer_segments(data)
        }
    
    def _analyze_weather_impact(self, data: pd.DataFrame) -> Dict[str, Any]:
        """Analyze impact of weather on demand."""
        weather_stats = data.groupby('Weatherconditions').agg({
            'order_count': ['mean', 'std', 'sum'],
            'time_taken(min)': 'mean'
        }).to_dict()
        
        # Calculate weather sensitivity
        overall_mean = data['order_count'].mean()
        weather_sensitivity = {
            weather: stats['mean']['order_count'] / overall_mean
            for weather, stats in weather_stats.items()
        }
        
        return {
            'weather_stats': weather_stats,
            'weather_sensitivity': weather_sensitivity
        }
    
    def _analyze_traffic_patterns(self, data: pd.DataFrame) -> Dict[str, Any]:
        """Analyze impact of traffic on demand and delivery times."""
        traffic_stats = data.groupby('Road_traffic_density').agg({
            'order_count': ['mean', 'std', 'sum'],
            'time_taken(min)': ['mean', 'std']
        }).to_dict()
        
        # Calculate peak traffic hours
        peak_traffic_hours = data[data['Road_traffic_density'].isin(['High', 'Jam'])]['hour'].value_counts()
        
        return {
            'traffic_stats': traffic_stats,
            'peak_traffic_hours': peak_traffic_hours.to_dict()
        }
    
    def _analyze_order_types(self, data: pd.DataFrame) -> Dict[str, Any]:
        """Analyze patterns in order types."""
        if 'Type_of_order' in data.columns:
            type_stats = data.groupby('Type_of_order').agg({
                'order_count': ['mean', 'sum'],
                'time_taken(min)': 'mean'
            }).to_dict()
            
            return {
                'type_stats': type_stats,
                'popular_types': self._identify_popular_types(data)
            }
        return {}
    
    def _analyze_customer_segments(self, data: pd.DataFrame) -> Dict[str, Any]:
        """Analyze customer segmentation patterns."""
        if 'customer_id' in data.columns:
            # Frequency analysis
            frequency = data.groupby('customer_id')['order_count'].count()
            
            # Recency analysis
            recency = data.groupby('customer_id')['Order_Date'].max()
            
            return {
                'frequency_stats': {
                    'mean': float(frequency.mean()),
                    'median': float(frequency.median()),
                    'std': float(frequency.std())
                },
                'customer_segments': self._segment_customers(frequency, recency)
            }
        return {}
    
    def _identify_popular_types(self, data: pd.DataFrame) -> Dict[str, float]:
        """Identify most popular order types."""
        type_counts = data['Type_of_order'].value_counts()
        total_orders = type_counts.sum()
        return {
            order_type: float(count/total_orders)
            for order_type, count in type_counts.items()
        }
    
    def _segment_customers(self, frequency: pd.Series, recency: pd.Series) -> Dict[str, int]:
        """Segment customers based on frequency and recency."""
        # Simple RFM segmentation
        freq_median = frequency.median()
        recency_median = recency.median()
        
        high_value = ((frequency > freq_median) & (recency > recency_median)).sum()
        at_risk = ((frequency > freq_median) & (recency <= recency_median)).sum()
        new = ((frequency <= freq_median) & (recency > recency_median)).sum()
        lost = ((frequency <= freq_median) & (recency <= recency_median)).sum()
        
        return {
            'high_value': int(high_value),
            'at_risk': int(at_risk),
            'new': int(new),
            'lost': int(lost)
        }