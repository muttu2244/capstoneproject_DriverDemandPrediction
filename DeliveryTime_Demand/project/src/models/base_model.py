"""Base model class with common functionality."""
from abc import ABC, abstractmethod
from typing import Any, Dict
import numpy as np
from ..utils.metrics import calculate_regression_metrics

class BaseModel(ABC):
    @abstractmethod
    def train(self, data: Any) -> None:
        """Train the model."""
        pass
    
    @abstractmethod
    def predict(self, features: Dict[str, Any]) -> Any:
        """Make predictions using the trained model."""
        pass
    
    def calculate_metrics(self, y_true: np.ndarray, y_pred: np.ndarray) -> Dict[str, float]:
        """Calculate common regression metrics."""
        return calculate_regression_metrics(y_true, y_pred)