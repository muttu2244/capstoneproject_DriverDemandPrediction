"""LightGBM-based delivery time prediction model."""
import pandas as pd
import numpy as np
import lightgbm as lgb
from typing import Dict, Any, List
from .base_model import BaseModel
from .features import (
    extract_time_features,
    extract_distance_features,
    CategoricalFeatureProcessor,
    NumericFeatureProcessor
)

class DeliveryTimeModel(BaseModel):
    def __init__(self):
        self.model = lgb.LGBMRegressor(
            n_estimators=1000,
            learning_rate=0.01,
            num_leaves=31,
            feature_fraction=0.8,
            bagging_fraction=0.8,
            bagging_freq=5,
            random_state=42
        )
        self.categorical_processor = CategoricalFeatureProcessor()
        self.numeric_processor = NumericFeatureProcessor()
        self.is_trained = False
    
    def _prepare_features(self, data: pd.DataFrame) -> pd.DataFrame:
        """Prepare features for model training/prediction."""
        df = data.copy()
        
        # Extract features
        df = extract_time_features(df)
        df = extract_distance_features(df)
        df = self.categorical_processor.process_features(df)
        df = self.numeric_processor.process_features(df)
        
        return df
    
    def _get_feature_columns(self) -> List[str]:
        """Get list of features used by the model."""
        return (
            ['distance', 'hour', 'day_of_week', 'is_weekend'] +
            self.categorical_processor.get_feature_names() +
            self.numeric_processor.get_feature_names()
        )
    
    def train(self, data: pd.DataFrame) -> Dict[str, float]:
        """Train the model with the provided data."""
        # Prepare features
        processed_data = self._prepare_features(data)
        feature_columns = self._get_feature_columns()
        
        # Train model
        X = processed_data[feature_columns]
        y = processed_data['time_taken(min)']
        
        self.model.fit(X, y)
        self.is_trained = True
        
        # Calculate metrics
        y_pred = self.model.predict(X)
        metrics = self.calculate_metrics(y, y_pred)
        
        return metrics
    
    def predict(self, features: Dict[str, Any]) -> float:
        """Make a prediction for a single order."""
        if not self.is_trained:
            raise RuntimeError("Model must be trained before making predictions")
        
        # Convert to DataFrame for processing
        df = pd.DataFrame([features])
        processed_features = self._prepare_features(df)
        
        # Get feature values in correct order
        feature_columns = self._get_feature_columns()
        feature_values = processed_features[feature_columns].iloc[0].values
        
        return float(self.model.predict(feature_values.reshape(1, -1))[0])