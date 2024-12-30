"""LightGBM model implementation."""
import lightgbm as lgb
from typing import Dict, Any
import numpy as np
from ..base_model import BaseModel

class LightGBMModel(BaseModel):
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
        
    def train(self, X_train, y_train, X_val=None, y_val=None):
        """Train the model."""
        if X_val is not None and y_val is not None:
            eval_set = [(X_val, y_val)]
            self.model.fit(
                X_train, y_train,
                eval_set=eval_set,
                callbacks=[lgb.early_stopping(50)]
            )
        else:
            self.model.fit(X_train, y_train)
        
    def predict(self, X):
        """Make predictions."""
        return self.model.predict(X)