from typing import Dict, Type
from .base_model import BaseModel
from .models import (
    LightGBMModel,
    XGBoostModel,
    RandomForestModel,
    CatBoostModel,
    GradientBoostingModel,
    DecisionTreeModel
)

class ModelFactory:
    _models: Dict[str, Type[BaseModel]] = {
        'lightgbm': LightGBMModel,
        'xgboost': XGBoostModel,
        'randomforest': RandomForestModel,
        'catboost': CatBoostModel,
        'gradientboosting': GradientBoostingModel,
        'decisiontree': DecisionTreeModel
    }
    
    @classmethod
    def get_model(cls, model_name: str) -> BaseModel:
        """Get model instance by name."""
        if model_name.lower() not in cls._models:
            raise ValueError(f"Model {model_name} not found. Available models: {list(cls._models.keys())}")
        return cls._models[model_name.lower()]()
    
    @classmethod
    def get_available_models(cls) -> list:
        """Get list of available models."""
        return list(cls._models.keys())