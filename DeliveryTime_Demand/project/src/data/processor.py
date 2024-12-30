"""Data preprocessing pipeline."""
from typing import Dict, Any
import pandas as pd
from ..utils.distance import calculate_haversine_distance
from ..utils.time_features import extract_time_features
from ..utils.feature_encoders import CategoryEncoder
from ..config.column_mappings import COLUMNS

class DataProcessor:
    def __init__(self):
        self.category_encoder = CategoryEncoder()
        
    def preprocess(self, df: pd.DataFrame) -> pd.DataFrame:
        """Main preprocessing pipeline."""
        try:
            df = df.copy()
            df = self._validate_and_rename_columns(df)
            df = self._calculate_distances(df)
            df = extract_time_features(df)
            df = self.category_encoder.fit_transform(df)
            return df
        except Exception as e:
            raise Exception(f"Preprocessing error: {str(e)}")
    
    def _validate_and_rename_columns(self, df: pd.DataFrame) -> pd.DataFrame:
        """Validate required columns and standardize column names."""
        required_cols = [
            COLUMNS['RESTAURANT_LAT'], 
            COLUMNS['RESTAURANT_LNG'],
            COLUMNS['DELIVERY_LAT'], 
            COLUMNS['DELIVERY_LNG']
        ]
        missing = [col for col in required_cols if col not in df.columns]
        if missing:
            raise ValueError(f"Missing columns: {', '.join(missing)}")
        return df
    
    def _calculate_distances(self, df: pd.DataFrame) -> pd.DataFrame:
        """Calculate delivery distances."""
        df['distance'] = df.apply(
            lambda row: calculate_haversine_distance(
                row[COLUMNS['RESTAURANT_LAT']],
                row[COLUMNS['RESTAURANT_LNG']],
                row[COLUMNS['DELIVERY_LAT']],
                row[COLUMNS['DELIVERY_LNG']]
            ),
            axis=1
        )
        return df