"""Peak demand prediction model with city-wise analysis."""
import pandas as pd
import numpy as np
from typing import Dict, Any, Optional
from .base_model import BaseModel
from .features import extract_time_features
from ..utils.date_parsers import parse_date
from ..utils.time_parsers import combine_date_time
from ..utils.console_logger import print_peak_demand_forecast

class PeakDemandModel(BaseModel):
    def __init__(self):
        self.hourly_patterns = {}
        self.city_patterns = {}
    
    def _prepare_data(self, data: pd.DataFrame) -> Dict[str, pd.DataFrame]:
        """Prepare time series data for peak demand prediction."""
        df = data.copy()
        
        # Parse dates and times
        df['datetime'] = df.apply(
            lambda row: combine_date_time(
                parse_date(row['Order_Date']),
                row['Time_Orderd']
            ),
            axis=1
        )
        
        # Remove rows with NaN values
        df = df.dropna(subset=['datetime', 'City'])
        
        # Group by hour and count orders (overall)
        hourly_orders = (
            df.groupby([pd.Grouper(key='datetime', freq='H')])
            .size()
            .reset_index(name='order_count')
        )
        
        # Group by city and hour
        city_orders = {}
        for city in df['City'].unique():
            if pd.isna(city):
                continue
            city_data = df[df['City'] == city]
            city_orders[city] = (
                city_data.groupby([pd.Grouper(key='datetime', freq='H')])
                .size()
                .reset_index(name='order_count')
            )
        
        return {
            'overall': hourly_orders,
            'by_city': city_orders
        }
    
    def train(self, data: pd.DataFrame) -> Dict[str, float]:
        """Train the peak demand prediction model."""
        try:
            # Prepare hourly order data
            ts_data = self._prepare_data(data)
            
            # Calculate overall hourly patterns
            overall_patterns = (
                ts_data['overall'].groupby(ts_data['overall']['datetime'].dt.hour)['order_count']
                .agg(['mean', 'std'])
            )
            self.hourly_patterns = {
                hour: {'mean': round(row['mean']), 'std': row['std']}
                for hour, row in overall_patterns.iterrows()
            }
            
            # Calculate city-wise patterns
            self.city_patterns = {}
            for city, city_data in ts_data['by_city'].items():
                if pd.isna(city):
                    continue
                city_patterns = (
                    city_data.groupby(city_data['datetime'].dt.hour)['order_count']
                    .agg(['mean', 'std'])
                )
                self.city_patterns[city] = {
                    hour: {'mean': round(row['mean']), 'std': row['std']}
                    for hour, row in city_patterns.iterrows()
                }
            
            return {"status": "success", "message": "Model trained successfully"}
            
        except Exception as e:
            raise RuntimeError(f"Error training peak demand model: {str(e)}")
    
    def predict(self, features: Optional[Dict[str, Any]] = None) -> Dict[str, Any]:
        """Make predictions using the trained model."""
        if not self.hourly_patterns:
            raise RuntimeError("Model must be trained before making predictions")
            
        # For single prediction, return next hour's prediction
        if features and 'hour' in features:
            hour = features['hour']
            city = features.get('city')
            
            if city and city in self.city_patterns:
                stats = self.city_patterns[city].get(hour, {'mean': 0, 'std': 0})
            else:
                stats = self.hourly_patterns.get(hour, {'mean': 0, 'std': 0})
                
            return {'predicted_orders': round(stats['mean'])}
            
        # Otherwise return full day prediction
        prediction = self.predict_next_day()
        # Only print once from the main prediction call
        if not features:
            print_peak_demand_forecast(prediction)
        return prediction
    
    def predict_next_day(self, city: Optional[str] = None) -> Dict[str, Any]:
        """Predict peak demand for next day, optionally for a specific city."""
        if not self.hourly_patterns:
            raise RuntimeError("Model must be trained before making predictions")
        
        # Get patterns based on city
        patterns = self.city_patterns.get(city, self.hourly_patterns) if city else self.hourly_patterns
        
        # Get hourly predictions (rounded to integers)
        predictions = []
        for hour in range(24):
            hour_stats = patterns.get(hour, {'mean': 0, 'std': 0})
            predictions.append(round(hour_stats['mean']))
        
        # Identify peak hours (hours with demand > mean + std)
        mean_demand = np.mean(predictions)
        std_demand = np.std(predictions)
        peak_hours = [
            hour for hour, pred in enumerate(predictions)
            if pred > mean_demand + std_demand
        ]
        
        result = {
            'total_orders': sum(predictions),  # Already rounded
            'peak_hours': peak_hours,
            'hourly_predictions': predictions,  # Already rounded
        }
        
        # Add city-specific predictions if available
        if city:
            result['city'] = city
        else:
            # Add city-wise breakdown
            result['city_predictions'] = {
                city: self.predict_next_day(city)
                for city in self.city_patterns.keys()
            }
        
        return result