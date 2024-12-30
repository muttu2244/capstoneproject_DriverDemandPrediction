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
from ..utils.console_logger import print_delivery_prediction

class DeliveryTimeModel(BaseModel):
    def __init__(self):
        self.model = lgb.LGBMRegressor(
            n_estimators=1000,
            learning_rate=0.01,
            num_leaves=31,
            subsample=0.8,
            subsample_freq=5,
            random_state=42,
            verbose=-1,
            force_row_wise=True
        )
        self.categorical_processor = CategoricalFeatureProcessor()
        self.numeric_processor = NumericFeatureProcessor()
        self.is_trained = False
    
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
        
        # Make prediction
        estimated_time = float(self.model.predict(feature_values.reshape(1, -1))[0])
        
        # Print prediction to console
        print_delivery_prediction(estimated_time, features)
        
        return estimated_time