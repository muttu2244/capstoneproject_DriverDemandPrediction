import pandas as pd
import numpy as np
from typing import List, Tuple

def create_lag_features(data: pd.DataFrame, 
                       target_col: str,
                       lag_hours: List[int] = [1, 2, 3, 6, 12, 24]) -> pd.DataFrame:
    """Create lag features for time series data."""
    df = data.copy()
    
    for lag in lag_hours:
        df[f'lag_{lag}h'] = df[target_col].shift(lag)
    
    return df

def create_rolling_features(data: pd.DataFrame, 
                          target_col: str,
                          windows: List[int] = [3, 6, 12, 24]) -> pd.DataFrame:
    """Create rolling mean and std features."""
    df = data.copy()
    
    for window in windows:
        df[f'rolling_mean_{window}h'] = df[target_col].rolling(window=window).mean()
        df[f'rolling_std_{window}h'] = df[target_col].rolling(window=window).std()
    
    return df

def prepare_time_series_data(data: pd.DataFrame,
                           target_col: str,
                           sequence_length: int = 24) -> Tuple[np.ndarray, np.ndarray]:
    """Prepare sequences for LSTM model."""
    values = data[target_col].values
    X, y = [], []
    
    for i in range(len(values) - sequence_length):
        X.append(values[i:i+sequence_length])
        y.append(values[i+1:i+sequence_length+1])
    
    return np.array(X), np.array(y)

def add_cyclical_features(data: pd.DataFrame, 
                         time_col: str) -> pd.DataFrame:
    """Add cyclical time features (hour of day, day of week)."""
    df = data.copy()
    
    # Hour of day
    df['hour_sin'] = np.sin(2 * np.pi * df[time_col].dt.hour / 24)
    df['hour_cos'] = np.cos(2 * np.pi * df[time_col].dt.hour / 24)
    
    # Day of week
    df['day_sin'] = np.sin(2 * np.pi * df[time_col].dt.dayofweek / 7)
    df['day_cos'] = np.cos(2 * np.pi * df[time_col].dt.dayofweek / 7)
    
    return df