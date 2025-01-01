"""Data splitting utilities."""
from typing import Tuple
import pandas as pd
from sklearn.model_selection import train_test_split

def split_data(data: pd.DataFrame, target_col: str, test_size: float = 0.2) -> Tuple[pd.DataFrame, pd.DataFrame, pd.Series, pd.Series]:
    """Split data into training and testing sets.
    
    Args:
        data: Input DataFrame
        target_col: Name of target column
        test_size: Proportion of data to use for testing (default: 0.2)
        
    Returns:
        Tuple of (X_train, X_test, y_train, y_test)
    """
    # Separate features and target
    feature_cols = [col for col in data.columns if col != target_col]
    X = data[feature_cols]
    y = data[target_col]
    
    # Split data
    X_train, X_test, y_train, y_test = train_test_split(
        X, y,
        test_size=test_size,
        random_state=42
    )
    
    return X_train, X_test, y_train, y_test
