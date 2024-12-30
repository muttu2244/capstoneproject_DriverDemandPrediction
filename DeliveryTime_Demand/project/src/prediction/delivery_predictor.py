"""Delivery time prediction service."""
import pandas as pd
from typing import Dict, Any
from ..models.delivery_time_model import DeliveryTimeModel
from ..data.processor import DataProcessor
from ..utils.validation import validate_order_data

class DeliveryPredictor:
    def __init__(self):
        self.processor = DataProcessor()
        self.model = DeliveryTimeModel()
        
    def predict(self, order_data: Dict[str, Any]) -> Dict[str, Any]:
        """Predict delivery time for an order."""
        try:
            # Validate input data
            validate_order_data(order_data)
            
            # Process order data
            processed_order = self.processor.process_single_order(order_data)
            
            # Load and process historical data
            historical_data = self._load_historical_data()
            if historical_data is not None:
                processed_historical = self.processor.preprocess(historical_data)
                self.model.train(processed_historical)
            
            # Make prediction
            estimated_time = self.model.predict(processed_order)
            
            return {
                'estimated_time': float(estimated_time),
                'unit': 'minutes'
            }
        except Exception as e:
            return {'error': str(e)}
    
    def _load_historical_data(self) -> pd.DataFrame:
        """Load historical delivery data."""
        try:
            return pd.read_csv('data/historical_deliveries.csv')
        except Exception as e:
            raise RuntimeError(f"Could not load historical data: {str(e)}")