"""Data preparation for model training."""
import pandas as pd
from typing import Tuple
from ...data_processor import DataProcessor
from ..features.feature_preparation import prepare_features

def prepare_training_data(data: pd.DataFrame) -> Tuple[pd.DataFrame, pd.Series]:
    """Prepare features and target for model training."""
    # Preprocess data
    processor = DataProcessor()
    processed_data = processor.preprocess(data)
    print(f"Proc_data in prepare_training_data function of modelsTrainingDataPrep.py {processed_data}")
    # Prepare features
    return prepare_features(processed_data)