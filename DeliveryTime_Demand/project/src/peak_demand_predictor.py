"""Peak demand prediction model."""
import pandas as pd
import numpy as np
from typing import Dict, Any, Optional
from .base_model import BaseModel
from ..utils.data_splitting import split_data
from ..utils.metrics import calculate_regression_metrics
from ..utils.console_logger import print_model_results

class PeakDemandModel(BaseModel):
    def __init__(self):
        self.hourly_patterns = {}
        self.city_patterns = {}
        self.metrics = {}
    
    def train(self, data: pd.DataFrame) -> Dict[str, float]:
        """Train the model with proper train-test split."""
        try:
            # Prepare time series data
            ts_data = self._prepare_time_series(data)
            
            # Split data
            X_train, X_test, y_train, y_test = split_data(
                ts_data,
                target_col='order_count',
                test_size=0.2
            )
            
            # Calculate patterns from training data
            self._calculate_patterns(X_train)
            
            # Make predictions on test set
            y_pred = self._predict_orders(X_test)
            
            # Calculate metrics
            self.metrics = calculate_regression_metrics(y_test, y_pred)
            
            # Print results
            print_model_results(
                {'PeakDemand': self.metrics},
                'PeakDemand',
                self.metrics['r2']
            )
            
            return self.metrics
            
        except Exception as e:
            raise RuntimeError(f"Error training model: {str(e)}")
    
    def _prepare_time_series(self, data: pd.DataFrame) -> pd.DataFrame:
        """Prepare time series features."""
        df = data.copy()
        
        # Convert dates to datetime if needed
        if not pd.api.types.is_datetime64_any_dtype(df['Order_Date']):
            df['Order_Date'] = pd.to_datetime(df['Order_Date'])
        
        # Add hour if not present
        if 'hour' not in df.columns:
            df['hour'] = df['Order_Date'].dt.hour
        
        # Add order count column
        df['order_count'] = 1
        
        # Group by date and hour
        hourly_data = df.groupby([
            df['Order_Date'].dt.date,
            'hour'
        ])['order_count'].sum().reset_index()
        
        # Add additional features
        hourly_data['day_of_week'] = pd.to_datetime(hourly_data['Order_Date']).dt.dayofweek
        hourly_data['is_weekend'] = hourly_data['day_of_week'].isin([5, 6]).astype(int)
        
        return hourly_data
    
    def _calculate_patterns(self, data: pd.DataFrame) -> None:
        """Calculate hourly and city-wise patterns."""
        # Calculate overall hourly patterns
        hourly_stats = data.groupby('hour')['order_count'].agg(['mean', 'std'])
        self.hourly_patterns = {
            hour: {
                'mean': stats['mean'],
                'std': stats['std']
            }
            for hour, stats in hourly_stats.iterrows()
        }
        
        # Calculate city patterns if city data available
        if 'City' in data.columns:
            for city in data['City'].unique():
                city_data = data[data['City'] == city]
                city_stats = city_data.groupby('hour')['order_count'].agg(['mean', 'std'])
                self.city_patterns[city] = {
                    hour: {
                        'mean': stats['mean'],
                        'std': stats['std']
                    }
                    for hour, stats in city_stats.iterrows()
                }
    
    def _predict_orders(self, data: pd.DataFrame) -> np.ndarray:
        """Make predictions using calculated patterns."""
        predictions = []
        
        for _, row in data.iterrows():
            hour = row['hour']
            city = row.get('City')
            
            if city and city in self.city_patterns:
                patterns = self.city_patterns[city]
            else:
                patterns = self.hourly_patterns
                
            if hour in patterns:
                predictions.append(patterns[hour]['mean'])
            else:
                predictions.append(np.mean([p['mean'] for p in patterns.values()]))
        
        return np.array(predictions)
