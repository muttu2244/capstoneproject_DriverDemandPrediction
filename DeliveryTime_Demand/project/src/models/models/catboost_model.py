"""CatBoost model implementation."""
from catboost import CatBoostRegressor
from ..base_model import BaseModel

class CatBoostModel(BaseModel):
    def __init__(self):
        self.model = CatBoostRegressor(
            iterations=1000,
            learning_rate=0.01,
            depth=6,
            random_seed=42,
            verbose=False
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
            self.model.fit(X_train, y_train, verbose=False)
        
    def predict(self, X):
        """Make predictions."""
        return self.model.predict(X)