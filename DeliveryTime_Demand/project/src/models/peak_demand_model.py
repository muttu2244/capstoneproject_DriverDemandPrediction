"""Peak demand prediction model."""
import pandas as pd
import numpy as np
from typing import Dict, Any, Optional, List
from .base_model import BaseModel
from ..utils.type_conversion import extract_hour

class PeakDemandModel(BaseModel):
    def __init__(self):
        self.hourly_patterns = {}
        self.city_patterns = {}
    
    def train(self, data: pd.DataFrame) -> Dict[str, float]:
        """Train the peak demand prediction model."""
        try:
            # Preprocess data
            df = self._prepare_time_series(data)
            
            # Calculate patterns
            self._calculate_patterns(df)
            
            return {
                "status": "success",
                "message": "Model trained successfully",
                "hourly_patterns": len(self.hourly_patterns),
                "city_patterns": len(self.city_patterns)
            }
            
        except Exception as e:
            raise RuntimeError(f"Error training model: {str(e)}")
    
    def _prepare_time_series(self, data: pd.DataFrame) -> pd.DataFrame:
        """Prepare time series data for analysis."""
        df = data.copy()
        
        # Extract hour from Time_Orderd
        if 'Time_Orderd' in df.columns:
            df['hour'] = df['Time_Orderd'].apply(extract_hour)
        elif 'hour' not in df.columns:
            raise ValueError("No time column found in data")
            
        # Add order count if not present
        if 'order_count' not in df.columns:
            df['order_count'] = 1
            
        return df
    
    def _calculate_patterns(self, df: pd.DataFrame) -> None:
        """Calculate hourly and city-wise patterns."""
        # Calculate overall hourly patterns
        hourly_stats = df.groupby('hour')['order_count'].agg(['mean', 'std'])
        self.hourly_patterns = {
            int(hour): {
                'mean': float(row['mean']),
                'std': float(row['std'])
            }
            for hour, row in hourly_stats.iterrows()
        }
        
        # Calculate city-wise patterns if available
        if 'City_encoded' in df.columns:
            for city_code in df['City_encoded'].unique():
                city_data = df[df['City_encoded'] == city_code]
                city_stats = city_data.groupby('hour')['order_count'].agg(['mean', 'std'])
                self.city_patterns[int(city_code)] = {
                    int(hour): {
                        'mean': float(row['mean']),
                        'std': float(row['std'])
                    }
                    for hour, row in city_stats.iterrows()
                }
    
    def _predict_orders(self, patterns: Dict[int, Dict[str, float]]) -> List[float]:
        """Predict hourly orders using patterns."""
        predictions = []
        for hour in range(24):
            hour_stats = patterns.get(hour, {'mean': 0.0, 'std': 0.0})
            predictions.append(round(float(hour_stats['mean'])))
        return predictions
    
    def predict_next_day(self, city_code: Optional[int] = None) -> Dict[str, Any]:
        """Predict peak demand for next day."""
        if not self.hourly_patterns:
            raise RuntimeError("Model must be trained before making predictions")
        
        # Get patterns based on city
        patterns = (
            self.city_patterns.get(city_code, self.hourly_patterns)
            if city_code is not None
            else self.hourly_patterns
        )
        
        # Generate predictions
        predictions = self._predict_orders(patterns)
        
        # Identify peak hours (hours with demand > mean + std)
        mean_demand = np.mean(predictions)
        std_demand = np.std(predictions)
        peak_hours = [
            hour for hour, pred in enumerate(predictions)
            if pred > mean_demand + std_demand
        ]
        
        result = {
            'total_orders': int(sum(predictions)),
            'peak_hours': peak_hours,
            'hourly_predictions': predictions
        }
        
        # Add city-wise predictions if available
        if city_code is None and self.city_patterns:
            result['city_predictions'] = {
                city: self.predict_next_day(city)
                for city in self.city_patterns.keys()
            }
        
        return result
    
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
        return self.predict_next_day()