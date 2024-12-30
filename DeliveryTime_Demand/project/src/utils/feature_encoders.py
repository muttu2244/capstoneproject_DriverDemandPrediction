"""Utility functions for encoding categorical features."""
from typing import Dict
import pandas as pd
from sklearn.preprocessing import LabelEncoder
from ..config.column_mappings import ENCODED_COLUMNS

class CategoryEncoder:
    def __init__(self):
        self.encoders: Dict[str, LabelEncoder] = {}
        self.feature_mappings = ENCODED_COLUMNS
    
    def fit_transform(self, df: pd.DataFrame) -> pd.DataFrame:
        """Fit and transform categorical columns."""
        df = df.copy()
        
        # Convert numeric columns to appropriate types
        numeric_columns = ['Delivery_person_Age', 'Vehicle_condition', 'multiple_deliveries']
        for col in numeric_columns:
            if col in df.columns:
                df[col] = pd.to_numeric(df[col], errors='coerce')
        
        # Encode categorical columns
        for original, encoded in self.feature_mappings.items():
            if original in df.columns:
                if original not in self.encoders:
                    self.encoders[original] = LabelEncoder()
                df[encoded] = self.encoders[original].fit_transform(df[original].fillna('Unknown'))
        
        return df