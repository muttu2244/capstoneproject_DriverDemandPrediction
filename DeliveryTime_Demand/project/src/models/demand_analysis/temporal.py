"""Temporal demand pattern analysis."""
import pandas as pd
import numpy as np
from typing import Dict, Any

class TemporalAnalyzer:
    def analyze(self, data: pd.DataFrame) -> Dict[str, Any]:
        """Analyze temporal patterns in demand."""
        results = {
            'hourly_patterns': self._analyze_hourly_patterns(data),
            'daily_patterns': self._analyze_daily_patterns(data),
            'weekly_patterns': self._analyze_weekly_patterns(data),
            'seasonal_patterns': self._analyze_seasonal_patterns(data)
        }
        return results
    
    def _analyze_hourly_patterns(self, data: pd.DataFrame) -> Dict[str, Any]:
        """Analyze hourly demand patterns."""
        hourly_stats = data.groupby('hour')['order_count'].agg(['mean', 'std', 'sum']).to_dict('index')
        peak_hours = self._identify_peak_hours(hourly_stats)
        
        return {
            'hourly_stats': hourly_stats,
            'peak_hours': peak_hours,
            'rush_hour_demand': self._calculate_rush_hour_demand(data)
        }
    
    def _analyze_daily_patterns(self, data: pd.DataFrame) -> Dict[str, Any]:
        """Analyze daily demand patterns."""
        daily_stats = data.groupby('day_of_week')['order_count'].agg(['mean', 'std', 'sum']).to_dict('index')
        weekend_impact = self._analyze_weekend_impact(data)
        
        return {
            'daily_stats': daily_stats,
            'weekend_impact': weekend_impact
        }
    
    def _analyze_weekly_patterns(self, data: pd.DataFrame) -> Dict[str, Any]:
        """Analyze weekly demand patterns."""
        weekly_stats = data.groupby(['year', 'week'])['order_count'].agg(['mean', 'std', 'sum']).to_dict('index')
        
        return {
            'weekly_stats': weekly_stats,
            'weekly_trends': self._calculate_weekly_trends(data)
        }
    
    def _analyze_seasonal_patterns(self, data: pd.DataFrame) -> Dict[str, Any]:
        """Analyze seasonal demand patterns."""
        monthly_stats = data.groupby('month')['order_count'].agg(['mean', 'std', 'sum']).to_dict('index')
        
        return {
            'monthly_stats': monthly_stats,
            'seasonal_factors': self._calculate_seasonal_factors(data)
        }
    
    def _identify_peak_hours(self, hourly_stats: Dict) -> list:
        """Identify peak demand hours."""
        means = [stats['mean'] for stats in hourly_stats.values()]
        threshold = np.mean(means) + np.std(means)
        return [hour for hour, stats in hourly_stats.items() if stats['mean'] > threshold]
    
    def _calculate_rush_hour_demand(self, data: pd.DataFrame) -> Dict[str, float]:
        """Calculate demand during rush hours."""
        morning_rush = data[data['hour'].between(7, 9)]['order_count'].mean()
        evening_rush = data[data['hour'].between(17, 19)]['order_count'].mean()
        return {'morning_rush': morning_rush, 'evening_rush': evening_rush}
    
    def _analyze_weekend_impact(self, data: pd.DataFrame) -> Dict[str, float]:
        """Analyze weekend vs weekday demand patterns."""
        weekend_avg = data[data['is_weekend'] == 1]['order_count'].mean()
        weekday_avg = data[data['is_weekend'] == 0]['order_count'].mean()
        return {'weekend_avg': weekend_avg, 'weekday_avg': weekday_avg}
    
    def _calculate_weekly_trends(self, data: pd.DataFrame) -> Dict[str, float]:
        """Calculate weekly demand trends."""
        weekly_totals = data.groupby(['year', 'week'])['order_count'].sum()
        trend = np.polyfit(range(len(weekly_totals)), weekly_totals, 1)
        return {'slope': float(trend[0]), 'intercept': float(trend[1])}
    
    def _calculate_seasonal_factors(self, data: pd.DataFrame) -> Dict[str, float]:
        """Calculate seasonal demand factors."""
        monthly_avg = data.groupby('month')['order_count'].mean()
        overall_avg = monthly_avg.mean()
        return {month: float(avg/overall_avg) for month, avg in monthly_avg.items()}