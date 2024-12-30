"""Peak demand prediction model."""
import pandas as pd
import numpy as np
from typing import Dict, Any, Optional
from .base_model import BaseModel
from .features import extract_time_features
from ..utils.date_parsers import parse_date
from ..utils.time_parsers import combine_date_time

class PeakDemandModel(BaseModel):
    def __init__(self):
        self.hourly_patterns = None
        
    def _prepare_data(self, data: pd.DataFrame) -> pd.DataFrame:
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
        
        # Group by hour and count orders
        hourly_orders = (
            df.groupby([pd.Grouper(key='datetime', freq='H')])
            .size()
            .reset_index(name='order_count')
        )
        
        return hourly_orders
    
    def train(self, data: pd.DataFrame) -> Dict[str, float]:
        """Train the peak demand prediction model."""
        try:
            # Prepare hourly order data
            ts_data = self._prepare_data(data)
            
            # Calculate typical hourly patterns
            self.hourly_patterns = (
                ts_data.groupby(ts_data['datetime'].dt.hour)['order_count']
                .agg(['mean', 'std'])
                .to_dict('index')
            )
            
            return {"status": "Model trained successfully"}
            
        except Exception as e:
            raise RuntimeError(f"Error training peak demand model: {str(e)}")
    
    def predict(self, features: Optional[Dict[str, Any]] = None) -> Dict[str, Any]:
        """Make predictions using the trained model."""
        if self.hourly_patterns is None:
            raise RuntimeError("Model must be trained before making predictions")
            
        # For single prediction, return next hour's prediction
        if features and 'hour' in features:
            hour = features['hour']
            stats = self.hourly_patterns.get(hour, {'mean': 0, 'std': 0})
            return {'predicted_orders': float(stats['mean'])}
            
        # Otherwise return full day prediction
        return self.predict_next_day()
    
    def predict_next_day(self) -> Dict[str, Any]:
        """Predict peak demand for next day."""
        if self.hourly_patterns is None:
            raise RuntimeError("Model must be trained before making predictions")
        
        # Get hourly predictions
        predictions = []
        for hour in range(24):
            hour_stats = self.hourly_patterns.get(hour, {'mean': 0, 'std': 0})
            predictions.append(hour_stats['mean'])
        
        # Identify peak hours (hours with demand > mean + std)
        mean_demand = np.mean(predictions)
        std_demand = np.std(predictions)
        peak_hours = [
            hour for hour, pred in enumerate(predictions)
            if pred > mean_demand + std_demand
        ]
        
        return {
            'total_orders': float(sum(predictions)),
            'peak_hours': peak_hours,
            'hourly_predictions': predictions
        }