"""Restaurant analytics chatbot."""
import pandas as pd
from typing import Dict, Any
from datetime import datetime, timedelta

class RestaurantBot:
    def __init__(self, data: pd.DataFrame):
        self.data = data
    
    def get_peak_hours(self) -> Dict[str, Any]:
        """Get peak hours for next 24 hours."""
        hourly_orders = self.data.groupby('hour')['order_count'].mean()
        peak_threshold = hourly_orders.mean() + hourly_orders.std()
        peak_hours = hourly_orders[hourly_orders > peak_threshold].index.tolist()
        
        return {
            'peak_hours': [f"{hour:02d}:00-{(hour+1):02d}:00" for hour in peak_hours],
            'expected_orders': hourly_orders[peak_hours].to_dict()
        }
    
    def get_monthly_forecast(self) -> Dict[str, Any]:
        """Get demand forecast for next month."""
        # Group by date and calculate daily stats
        daily_orders = self.data.groupby('Order_Date')['order_count'].agg(['sum', 'mean', 'std'])
        
        return {
            'avg_daily_orders': float(daily_orders['mean'].mean()),
            'peak_dates': daily_orders.nlargest(5, 'sum').index.strftime('%Y-%m-%d').tolist(),
            'trend': 'increasing' if daily_orders['sum'].is_monotonic_increasing else 'stable'
        }
    
    def get_historical_analysis(self) -> Dict[str, Any]:
        """Get historical performance analysis."""
        return {
            'total_orders': len(self.data),
            'avg_delivery_time': float(self.data['time_taken(min)'].mean()),
            'popular_hours': self.data.groupby('hour')['order_count'].sum().nlargest(3).index.tolist(),
            'weather_impact': self._analyze_weather_impact(),
            'traffic_impact': self._analyze_traffic_impact()
        }
    
    def _analyze_weather_impact(self) -> Dict[str, float]:
        """Analyze impact of weather on delivery times."""
        return self.data.groupby('Weatherconditions')['time_taken(min)'].mean().to_dict()
    
    def _analyze_traffic_impact(self) -> Dict[str, float]:
        """Analyze impact of traffic on delivery times."""
        return self.data.groupby('Road_traffic_density')['time_taken(min)'].mean().to_dict()
    
    def handle_query(self, query: str) -> str:
        """Handle restaurant queries."""
        query = query.lower()
        
        if 'peak' in query and 'hour' in query:
            peak_data = self.get_peak_hours()
            return f"Peak hours: {', '.join(peak_data['peak_hours'])}"
        
        if 'forecast' in query or 'next month' in query:
            forecast = self.get_monthly_forecast()
            return f"Average daily orders: {forecast['avg_daily_orders']:.0f}\nPeak dates: {', '.join(forecast['peak_dates'])}"
        
        if 'historical' in query or 'analysis' in query:
            analysis = self.get_historical_analysis()
            return f"Total orders: {analysis['total_orders']}\nAverage delivery time: {analysis['avg_delivery_time']:.1f} minutes"
        
        return "I can help with peak hours, monthly forecasts, and historical analysis. What would you like to know?"