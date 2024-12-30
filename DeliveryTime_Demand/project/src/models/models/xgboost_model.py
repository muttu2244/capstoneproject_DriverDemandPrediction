"""XGBoost model implementation."""
import xgboost as xgb
from typing import Dict, Any
import numpy as np
from ..base_model import BaseModel

class XGBoostModel(BaseModel):
    def __init__(self):
        self.model = xgb.XGBRegressor(
            n_estimators=1000,
            learning_rate=0.01,
            max_depth=6,
            subsample=0.8,
            colsample_bytree=0.8,
            random_state=42
        )
        
    def train(self, X_train, y_train, X_val=None, y_val=None):
        """Train the model."""
        if X_val is not None and y_val is not None:
            eval_set = [(X_val, y_val)]
            self.model.fit(
                X_train, y_train,
                eval_set=eval_set,
                early_stopping_rounds=50,
                verbose=False
            )
        else:
            self.model.fit(X_train, y_train)
        
    def predict(self, X):
        """Make predictions."""
        return self.model.predict(X)