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
from ..utils.console_logger import print_best_model, print_model_comparison

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
            try:
                model.train(X_train, y_train)
                y_pred = model.predict(X_test)
                metrics = model.calculate_metrics(y_test, y_pred)
                self.results[name] = metrics
            except Exception as e:
                print(f"Error training {name}: {str(e)}")
                continue
        
        # Print comparison results
        print_model_comparison(self.results)
       
        # Get best model and print results
        best_model_name, best_metrics = self.get_best_model()
        print_best_model(best_model_name, best_metrics)
        
        return self.results
    

    
    def get_best_model(self) -> Tuple[str, Dict[str, float]]:
        """Get the best performing model based on R² score."""
        best_model = max(self.results.items(), key=lambda x: x[1]['r2'])
        return best_model[0], best_model[1]
