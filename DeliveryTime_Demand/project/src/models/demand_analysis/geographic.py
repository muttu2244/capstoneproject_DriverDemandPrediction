"""Geographic demand pattern analysis."""
import pandas as pd
import numpy as np
from typing import Dict, Any
from sklearn.cluster import DBSCAN
from ...utils.distance import calculate_haversine_distance

class GeographicAnalyzer:
    def analyze(self, data: pd.DataFrame) -> Dict[str, Any]:
        """Analyze geographic demand patterns."""
        return {
            'hotspots': self._identify_hotspots(data),
            'zone_analysis': self._analyze_zones(data),
            'distance_patterns': self._analyze_distance_patterns(data),
            'coverage_analysis': self._analyze_coverage(data)
        }
    
    def _identify_hotspots(self, data: pd.DataFrame) -> Dict[str, Any]:
        """Identify order hotspots using DBSCAN clustering."""
        coords = data[['Delivery_location_latitude', 'Delivery_location_longitude']].values
        
        # Perform clustering
        clustering = DBSCAN(eps=0.01, min_samples=5).fit(coords)
        
        # Analyze clusters
        clusters = pd.DataFrame({
            'latitude': coords[:, 0],
            'longitude': coords[:, 1],
            'cluster': clustering.labels_
        })
        
        # Calculate cluster statistics
        cluster_stats = clusters[clusters['cluster'] != -1].groupby('cluster').agg({
            'latitude': ['mean', 'count'],
            'longitude': 'mean'
        }).reset_index()
        
        return {
            'cluster_centers': cluster_stats.to_dict('records'),
            'noise_points': int((clustering.labels_ == -1).sum())
        }
    
    def _analyze_zones(self, data: pd.DataFrame) -> Dict[str, Any]:
        """Analyze demand patterns by delivery zones."""
        # Create delivery zones based on lat/long grid
        data['zone'] = data.apply(
            lambda row: f"{int(row['Delivery_location_latitude']*100)}_{int(row['Delivery_location_longitude']*100)}",
            axis=1
        )
        
        zone_stats = data.groupby('zone').agg({
            'order_count': ['count', 'mean'],
            'time_taken(min)': 'mean'
        }).reset_index()
        
        return {
            'zone_stats': zone_stats.to_dict('records'),
            'high_demand_zones': self._identify_high_demand_zones(zone_stats)
        }
    
    def _analyze_distance_patterns(self, data: pd.DataFrame) -> Dict[str, Any]:
        """Analyze demand patterns based on delivery distance."""
        data['distance'] = data.apply(
            lambda row: calculate_haversine_distance(
                row['Restaurant_latitude'],
                row['Restaurant_longitude'],
                row['Delivery_location_latitude'],
                row['Delivery_location_longitude']
            ),
            axis=1
        )
        
        distance_stats = data.groupby(pd.qcut(data['distance'], q=5))['order_count'].agg([
            'count',
            'mean',
            'std'
        ]).reset_index()
        
        return {
            'distance_stats': distance_stats.to_dict('records'),
            'avg_distance': float(data['distance'].mean()),
            'max_distance': float(data['distance'].max())
        }
    
    def _analyze_coverage(self, data: pd.DataFrame) -> Dict[str, Any]:
        """Analyze delivery coverage area."""
        lat_range = data['Delivery_location_latitude'].max() - data['Delivery_location_latitude'].min()
        lng_range = data['Delivery_location_longitude'].max() - data['Delivery_location_longitude'].min()
        
        return {
            'coverage_area': float(lat_range * lng_range),
            'center_point': {
                'latitude': float(data['Delivery_location_latitude'].mean()),
                'longitude': float(data['Delivery_location_longitude'].mean())
            },
            'radius': float(max(lat_range, lng_range) / 2)
        }
    
    def _identify_high_demand_zones(self, zone_stats: pd.DataFrame) -> list:
        """Identify zones with significantly high demand."""
        threshold = zone_stats['order_count']['mean'].mean() + zone_stats['order_count']['mean'].std()
        high_demand = zone_stats[zone_stats['order_count']['mean'] > threshold]
        return high_demand['zone'].tolist()