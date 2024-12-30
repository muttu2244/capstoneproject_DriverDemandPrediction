"""SARIMA model for time series prediction."""
import pandas as pd
import numpy as np
from typing import Dict, Any
from statsmodels.tsa.statespace.sarimax import SARIMAX
from ..base_model import BaseModel

class SARIMAModel(BaseModel):
    def __init__(self):
        self.model = None
        self.order = (1, 1, 1)
        self.seasonal_order = (1, 1, 1, 24)  # 24 for hourly data
    
    def train(self, data: pd.DataFrame) -> Dict[str, float]:
        """Train SARIMA model on time series data."""
        try:
            # Fit SARIMA model
            self.model = SARIMAX(
                data,
                order=self.order,
                seasonal_order=self.seasonal_order
            )
            self.results = self.model.fit(disp=False)
            
            # Calculate metrics
            y_pred = self.results.get_prediction().predicted_mean
            metrics = self.calculate_metrics(data, y_pred)
            
            return metrics
        except Exception as e:
            raise RuntimeError(f"Error training SARIMA model: {str(e)}")
    
    def predict(self, features: Dict[str, Any]) -> np.ndarray:
        """Make predictions using trained SARIMA model."""
        if self.results is None:
            raise RuntimeError("Model must be trained before making predictions")
        
        steps = features.get('steps', 24)  # Default to 24 hours
        forecast = self.results.get_forecast(steps=steps)
        return forecast.predicted_mean