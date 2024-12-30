from sklearn.ensemble import GradientBoostingRegressor
from ..base_model import BaseModel

class GradientBoostingModel(BaseModel):
    def __init__(self):
        self.model = GradientBoostingRegressor(
            n_estimators=100,
            learning_rate=0.1,
            max_depth=3,
            random_state=42
        )
        
    def train(self, X_train, y_train, X_val=None, y_val=None):
        self.model.fit(X_train, y_train)
        
    def predict(self, X):
        return self.model.predict(X)