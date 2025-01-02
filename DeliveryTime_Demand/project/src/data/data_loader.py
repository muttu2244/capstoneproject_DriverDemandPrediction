"""Data loading utilities."""
import pandas as pd
from typing import Optional
from ..config.data_paths import RAW_DATA_PATH, PROCESSED_DATA_PATH
from ..utils.data_preprocessing import preprocess_delivery_data
from .processor import DataProcessor

def load_raw_data() -> Optional[pd.DataFrame]:
    """Load raw delivery data."""
    try:
        if not RAW_DATA_PATH.exists():
            raise FileNotFoundError(f"Raw data file not found at {RAW_DATA_PATH}")
        return pd.read_csv(RAW_DATA_PATH)
    except Exception as e:
        raise RuntimeError(f"Error loading raw data: {str(e)}")

def load_processed_data() -> Optional[pd.DataFrame]:
    """Load and preprocess delivery data."""
    try:
        # Load raw data
        data = pd.read_csv('data/raw/delivery_data.csv')
        
        # Preprocess data silently
        processor = DataProcessor()
        processed_data = processor.preprocess(data)
        
        return processed_data
        
    except Exception as e:
        print(f"Error loading data: {str(e)}")
        return None


def save_processed_data(data: pd.DataFrame) -> None:
    """Save processed data to CSV."""
    try:
        data.to_csv(PROCESSED_DATA_PATH, index=False)
    except Exception as e:
        raise RuntimeError(f"Error saving processed data: {str(e)}")