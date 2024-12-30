"""Categorical feature processing."""
import pandas as pd
from typing import Dict, List
from sklearn.preprocessing import LabelEncoder

class CategoricalFeatureProcessor:
    def __init__(self):
        self.encoders: Dict[str, LabelEncoder] = {}
        self.categorical_columns = [
            'Weatherconditions',
            'Road_traffic_density',
            'Type_of_vehicle',
            'Type_of_order',
            'Festival',
            'City'
        ]
    
    def process_features(self, data: pd.DataFrame) -> pd.DataFrame:
        """Process and encode categorical features."""
        df = data.copy()
        
        for col in self.categorical_columns:
            if col in df.columns:
                if col not in self.encoders:
                    self.encoders[col] = LabelEncoder()
                df[f'{col}_encoded'] = self.encoders[col].fit_transform(df[col].fillna('Unknown'))
        
        return df
    
    def get_feature_names(self) -> List[str]:
        """Get list of encoded feature names."""
        return [f'{col}_encoded' for col in self.categorical_columns]