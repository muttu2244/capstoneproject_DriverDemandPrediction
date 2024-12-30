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
    GradientBoostingModel,
    SARIMAModel
)

class ModelEvaluator:
    def __init__(self):
        self.models = {
            'LightGBM': LightGBMModel(),
            'XGBoost': XGBoostModel(),
            'RandomForest': RandomForestModel(),
            'CatBoost': CatBoostModel(),
            'GradientBoosting': GradientBoostingModel()
        }
        self.time_series_models = {
            'SARIMA': SARIMAModel()
        }
        self.results = {}
    
    def evaluate_models(self, X: pd.DataFrame, y: pd.Series, 
                       time_series_data: pd.Series = None) -> Dict[str, Dict[str, float]]:
        """Evaluate all models and return their metrics."""
        # Evaluate regression models
        X_train, X_test, y_train, y_test = train_test_split(
            X, y, test_size=0.2, random_state=42
        )
        
        for name, model in self.models.items():
            print(f"\nTraining {name}...")
            model.train(X_train, y_train)
            y_pred = model.predict(X_test)
            metrics = model.calculate_metrics(y_test, y_pred)
            self.results[name] = metrics
            
            print(f"{name} Metrics:")
            print(f"MSE: {metrics['mse']:.2f}")
            print(f"RMSE: {metrics['rmse']:.2f}")
            print(f"MAE: {metrics['mae']:.2f}")
            print(f"MAPE: {metrics['mape']:.2f}%")
            print(f"R2 Score: {metrics['r2']:.4f}")
        
        # Evaluate time series models if data provided
        if time_series_data is not None:
            train_size = int(len(time_series_data) * 0.8)
            train_data = time_series_data[:train_size]
            test_data = time_series_data[train_size:]
            
            for name, model in self.time_series_models.items():
                print(f"\nTraining {name}...")
                model.train(train_data)
                y_pred = model.predict({'steps': len(test_data)})
                metrics = model.calculate_metrics(test_data, y_pred)
                self.results[name] = metrics
                
                print(f"{name} Metrics:")
                print(f"MSE: {metrics['mse']:.2f}")
                print(f"RMSE: {metrics['rmse']:.2f}")
                print(f"MAE: {metrics['mae']:.2f}")
                print(f"MAPE: {metrics['mape']:.2f}%")
        
        return self.results
    
    def get_best_model(self, metric: str = 'r2') -> Tuple[str, float]:
        """Get the best performing model based on specified metric."""
        scores = {name: results[metric] for name, results in self.results.items()}
        best_model = max(scores.items(), key=lambda x: x[1])
        return best_model