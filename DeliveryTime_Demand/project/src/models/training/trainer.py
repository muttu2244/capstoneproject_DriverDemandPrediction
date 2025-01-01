"""Model training orchestration."""
import pandas as pd
from typing import Dict, Any
from ..model_evaluator import ModelEvaluator
from .data_preparation import prepare_training_data

class ModelTrainer:
    def __init__(self):
        self.evaluator = ModelEvaluator()
    
    def train_models(self, data: pd.DataFrame) -> Dict[str, Any]:
        """Train and evaluate all models."""
        print("Preparing training data...")
        X, y = prepare_training_data(data)
        
        print("\nTraining and evaluating models...")
        results = self.evaluator.evaluate_models(X, y)
        
        return results