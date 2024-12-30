"""Model registry for saving and loading trained models."""
import pickle
from pathlib import Path
from typing import Any, Optional
from ..config.data_config import MODEL_DIR

class ModelRegistry:
    @staticmethod
    def save_model(model: Any, model_name: str) -> None:
        """Save trained model to disk."""
        try:
            model_path = MODEL_DIR / f"{model_name}.pkl"
            with open(model_path, 'wb') as f:
                pickle.dump(model, f)
        except Exception as e:
            raise RuntimeError(f"Error saving model: {str(e)}")
    
    @staticmethod
    def load_model(model_name: str) -> Optional[Any]:
        """Load trained model from disk."""
        try:
            model_path = MODEL_DIR / f"{model_name}.pkl"
            if not model_path.exists():
                return None
            with open(model_path, 'rb') as f:
                return pickle.load(f)
        except Exception as e:
            raise RuntimeError(f"Error loading model: {str(e)}")