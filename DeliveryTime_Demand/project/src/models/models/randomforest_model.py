from sklearn.ensemble import RandomForestRegressor
from ..base_model import BaseModel

class RandomForestModel(BaseModel):
    def __init__(self):
        self.model = RandomForestRegressor(
            n_estimators=100,
            max_depth=10,
            min_samples_split=5,
            min_samples_leaf=2,
            random_state=42
        )
        
    def train(self, X_train, y_train, X_val=None, y_val=None):
        self.model.fit(X_train, y_train)
        
    def predict(self, X):
        return self.model.predict(X)