"""LightGBM-based delivery time prediction model."""
import pandas as pd
import numpy as np
import lightgbm as lgb
from typing import Dict, Any, List, Union
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
        self.metrics = None
    
    def train(self, X_train, y_train, X_val=None, y_val=None):
        """Train the model."""
        #print(f" x train cols are: {X_train.columns}")
        #print(f" y train cols are: {y_train}")
        if X_val is not None and y_val is not None:
            eval_set = [(X_val, y_val)]
            self.model.fit(
                X_train, y_train,
                eval_set=eval_set,
                callbacks=[lgb.early_stopping(50, verbose=False)]
            )
        else:
            self.model.fit(X_train, y_train)
        
        # Calculate and store metrics
        y_pred = self.model.predict(X_train)
        self.metrics = self.calculate_metrics(y_train, y_pred)
        self.is_trained = True
    
    def predict(self, features: Union[pd.DataFrame, Dict[str, Any]]) -> np.ndarray:
        """Make predictions using the trained model.
        
        Args:
            features: DataFrame or dict containing order features
            
        Returns:
            Array of predicted delivery times in minutes
        """
        #for (index, col), value in features.stack().items():
        #    print(f"******* Features in Predict  ... Row {index}, Column {col}: {value}********")
        if not self.is_trained:
            raise RuntimeError("Model must be trained before making predictions")
            
        try:
            # Convert dict to DataFrame if needed
            if isinstance(features, dict):
                features = pd.DataFrame([features])
            
            # Prepare features
            #processed_features = self._prepare_features(features)
            #for (index, col), value in processed_features.stack().items():
            #    print(f"\n Processed Features are.... \n Row {index}, Column {col}: {value}")
            # Get feature values in correct order
            #feature_columns = self._get_feature_columns()
            
            #missing_features = [col for col in feature_columns if col not in processed_features.columns]
            #if missing_features:
            #    raise ValueError(f"Missing required features: {missing_features}")
                
            #feature_values = processed_features[feature_columns]
            
            # Make prediction
            #predictions = self.model.predict(feature_values)
            #predictions = self.model.predict(processed_features)
            predictions = self.model.predict(features)
            # Log prediction details if single order
            if len(predictions) == 1 and isinstance(features, dict):
                print_delivery_prediction(predictions[0], features)
            
            return predictions
            
        except Exception as e:
            raise RuntimeError(f"Error making prediction: {str(e)}")
    
    def _prepare_features(self, df: pd.DataFrame) -> pd.DataFrame:
        """Prepare features for prediction."""
        df = extract_time_features(df)
        df = extract_distance_features(df)
        df = self.categorical_processor.process_features(df)
        df = self.numeric_processor.process_features(df)
        return df
    
    def _get_feature_columns(self) -> List[str]:
        """Get list of feature columns in correct order."""
        return (
            self.numeric_processor.get_feature_names() +
            self.categorical_processor.get_feature_names()
        )