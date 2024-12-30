"""Time series feature extraction."""
import pandas as pd
import numpy as np
from typing import List

def create_lag_features(data: pd.DataFrame, target_col: str, lags: List[int]) -> pd.DataFrame:
    """Create lagged features for time series data."""
    df = data.copy()
    
    for lag in lags:
        df[f'lag_{lag}h'] = df[target_col].shift(lag)
    
    return df

def create_rolling_features(data: pd.DataFrame, target_col: str, windows: List[int]) -> pd.DataFrame:
    """Create rolling window features."""
    df = data.copy()
    
    for window in windows:
        df[f'rolling_mean_{window}h'] = df[target_col].rolling(window=window).mean()
        df[f'rolling_std_{window}h'] = df[target_col].rolling(window=window).std()
    
    return df

def add_cyclical_features(data: pd.DataFrame, time_col: str) -> pd.DataFrame:
    """Add cyclical time features."""
    df = data.copy()
    
    # Hour of day
    df['hour_sin'] = np.sin(2 * np.pi * df[time_col].dt.hour / 24)
    df['hour_cos'] = np.cos(2 * np.pi * df[time_col].dt.hour / 24)
    
    # Day of week
    df['day_sin'] = np.sin(2 * np.pi * df[time_col].dt.dayofweek / 7)
    df['day_cos'] = np.cos(2 * np.pi * df[time_col].dt.dayofweek / 7)
    
    return df