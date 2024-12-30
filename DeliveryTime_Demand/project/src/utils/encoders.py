from typing import Dict, List
from sklearn.preprocessing import LabelEncoder
import pandas as pd

class FeatureEncoder:
    def __init__(self):
        self.encoders: Dict[str, LabelEncoder] = {}
        
    def fit_transform(self, df: pd.DataFrame, columns: List[str]) -> pd.DataFrame:
        """Fit and transform categorical columns using label encoding."""
        df = df.copy()
        
        for col in columns:
            if col not in self.encoders:
                self.encoders[col] = LabelEncoder()
            df[f'{col}_encoded'] = self.encoders[col].fit_transform(df[col])
        
        return df
    
    def transform_single(self, feature_dict: Dict[str, str]) -> Dict[str, int]:
        """Transform a single sample's categorical features."""
        encoded = {}
        
        for feature_name, value in feature_dict.items():
            if feature_name in self.encoders:
                encoded[f'{feature_name}_encoded'] = self.encoders[feature_name].transform([value])[0]
                
        return encoded