"""Model persistence utilities."""
import pickle
from typing import Any
from ..config.data_paths import MODELS_DIR

def save_model(model: Any, model_name: str) -> None:
    """Save trained model to disk."""
    try:
        model_path = MODELS_DIR / f"{model_name}.pkl"
        with open(model_path, 'wb') as f:
            pickle.dump(model, f)
    except Exception as e:
        raise RuntimeError(f"Error saving model: {str(e)}")

def load_model(model_name: str) -> Any:
    """Load trained model from disk."""
    try:
        model_path = MODELS_DIR / f"{model_name}.pkl"
        if not model_path.exists():
            return None
        with open(model_path, 'rb') as f:
            return pickle.load(f)
    except Exception as e:
        raise RuntimeError(f"Error loading model: {str(e)}")