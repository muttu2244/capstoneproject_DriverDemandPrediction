"""Model evaluation and comparison."""
from typing import Dict, List, Tuple
import pandas as pd
import numpy as np
from sklearn.model_selection import train_test_split
from .models import (
    LightGBMModel,
    XGBoostModel,
    RandomForestModel,
    CatBoostModel,
    GradientBoostingModel
)
from ..utils.console_logger import print_model_results

class ModelEvaluator:
    def __init__(self):
        self.models = {
            'LightGBM': LightGBMModel(),
            'XGBoost': XGBoostModel(),
            'RandomForest': RandomForestModel(),
            'CatBoost': CatBoostModel(),
            'GradientBoosting': GradientBoostingModel()
        }
        self.results = {}
    
    def evaluate_models(self, X: pd.DataFrame, y: pd.Series) -> Dict[str, Dict[str, float]]:
        """Evaluate all models and return their metrics."""
        X_train, X_test, y_train, y_test = train_test_split(
            X, y, test_size=0.2, random_state=42
        )
        
        for name, model in self.models.items():
            print(f"\nTraining {name}...")
            model.train(X_train, y_train)
            y_pred = model.predict(X_test)
            metrics = model.calculate_metrics(y_test, y_pred)
            self.results[name] = metrics
        
        # Get best model and print results
        best_model_name, best_score = self.get_best_model(metric='r2')
        print_model_results(self.results, best_model_name, best_score)
        
        return self.results
    
    def get_best_model(self, metric: str = 'r2') -> Tuple[str, float]:
        """Get the best performing model based on specified metric."""
        scores = {name: results[metric] for name, results in self.results.items()}
        best_model = max(scores.items(), key=lambda x: x[1])
        return best_model