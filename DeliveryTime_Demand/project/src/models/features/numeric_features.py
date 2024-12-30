"""Numeric feature processing."""
import pandas as pd
from typing import List

class NumericFeatureProcessor:
    def __init__(self):
        self.numeric_columns = [
            'Delivery_person_Age',
            'Vehicle_condition',
            'multiple_deliveries',
            'Delivery_person_Ratings'
        ]
    
    def process_features(self, data: pd.DataFrame) -> pd.DataFrame:
        """Process numeric features."""
        df = data.copy()
        
        for col in self.numeric_columns:
            if col in df.columns:
                df[col] = pd.to_numeric(df[col], errors='coerce')
                df[col] = df[col].fillna(df[col].median())
        
        return df
    
    def get_feature_names(self) -> List[str]:
        """Get list of numeric feature names."""
        return self.numeric_columns