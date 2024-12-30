"""Data loading and validation utilities."""
import pandas as pd
from typing import Optional
from pathlib import Path
from ..config.data_config import DATA_DIR

class DataLoader:
    @staticmethod
    def load_historical_data() -> Optional[pd.DataFrame]:
        """Load historical delivery data."""
        data_path = DATA_DIR / 'historical_deliveries.csv'
        try:
            if not data_path.exists():
                return None
            return pd.read_csv(data_path)
        except Exception as e:
            raise RuntimeError(f"Error loading historical data: {str(e)}")
    
    @staticmethod
    def save_processed_data(df: pd.DataFrame, filename: str) -> None:
        """Save processed data to CSV."""
        try:
            output_path = DATA_DIR / 'processed' / filename
            output_path.parent.mkdir(parents=True, exist_ok=True)
            df.to_csv(output_path, index=False)
        except Exception as e:
            raise RuntimeError(f"Error saving processed data: {str(e)}")