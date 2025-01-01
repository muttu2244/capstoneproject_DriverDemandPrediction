"""Time feature processing module.

This module handles all time-related feature processing including:
- Date parsing and feature extraction
- Time parsing and normalization
- Cyclical time feature creation
- Time period indicators
"""
import pandas as pd
import numpy as np
from datetime import datetime
from typing import Optional

def process_time_features(df: pd.DataFrame) -> pd.DataFrame:
    """Process time-related features from delivery data.
    
    Args:
        df: Input DataFrame containing time-related columns
        
    Returns:
        DataFrame with processed time features
    """
    df = df.copy()
    
    # Process Order_Date
    df = _process_order_date(df)
    
    # Process Time_Orderd and Time_Order_picked
    df = _process_time_columns(df)
    
    # Add derived time features
    df = _add_time_features(df)
    
    # Drop original time columns to ensure only numeric features remain
    time_columns = ['Time_Orderd', 'Time_Order_picked']
    df = df.drop(columns=[col for col in time_columns if col in df.columns])
    
    return df

def _process_order_date(df: pd.DataFrame) -> pd.DataFrame:
    """Process Order_Date column with robust error handling."""
    if 'Order_Date' in df.columns:
        try:
            # Convert to datetime with multiple format support
            df['Order_Date'] = pd.to_datetime(
                df['Order_Date'],
                format='%d-%m-%Y',
                errors='coerce'
            )
            
            # Fill missing dates with median date
            median_date = df['Order_Date'].median()
            df['Order_Date'] = df['Order_Date'].fillna(median_date)
            
            # Extract temporal components
            df['hour'] = df['Order_Date'].dt.hour.astype('int64')
            df['day'] = df['Order_Date'].dt.day.astype('int64')
            df['month'] = df['Order_Date'].dt.month.astype('int64')
            df['year'] = df['Order_Date'].dt.year.astype('int64')
            df['day_of_week'] = df['Order_Date'].dt.dayofweek.astype('int64')
            df['week_of_year'] = df['Order_Date'].dt.isocalendar().week.astype('int64')
            df['is_weekend'] = df['day_of_week'].isin([5, 6]).astype('int64')
            df['is_month_end'] = df['Order_Date'].dt.is_month_end.astype('int64')
            
            # Drop original date column
            df = df.drop(columns=['Order_Date'])
            
        except Exception as e:
            print(f"Warning: Error processing Order_Date: {str(e)}")
            # Provide default values if date processing fails
            for col in ['hour', 'day', 'month', 'year', 'day_of_week', 'week_of_year']:
                if col not in df.columns:
                    df[col] = 0
            df['is_weekend'] = 0
            df['is_month_end'] = 0
    
    return df

def _process_time_columns(df: pd.DataFrame) -> pd.DataFrame:
    """Process Time_Orderd and Time_Order_picked columns with robust parsing."""
    time_columns = {
        'Time_Orderd': 'order_hour',
        'Time_Order_picked': 'pickup_hour'
    }
    
    for col, new_col in time_columns.items():
        if col in df.columns:
            # Convert times to hours
            df[new_col] = df[col].apply(_parse_time_to_hour)
            
            # Fill missing values with median
            median_hour = df[new_col].median()
            df[new_col] = df[new_col].fillna(median_hour)
            
            # Ensure int64 type
            df[new_col] = df[new_col].astype('int64')
            
            # Calculate time differences if both columns exist
            if 'order_hour' in df.columns and 'pickup_hour' in df.columns:
                df['preparation_time'] = (
                    (df['pickup_hour'] - df['order_hour']) % 24
                ).astype('int64')
    
    return df

def _add_time_features(df: pd.DataFrame) -> pd.DataFrame:
    """Add derived time features including cyclical encoding."""
    if 'hour' in df.columns:
        # Time period indicators
        df['is_morning'] = df['hour'].between(6, 11).astype('int64')
        df['is_afternoon'] = df['hour'].between(12, 17).astype('int64')
        df['is_evening'] = df['hour'].between(18, 22).astype('int64')
        df['is_night'] = ((df['hour'] >= 23) | (df['hour'] <= 5)).astype('int64')
        df['is_rush_hour'] = (
            df['hour'].isin([8, 9, 17, 18, 19])
        ).astype('int64')
        
        # Cyclical encoding for hour of day
        df['hour_sin'] = np.sin(2 * np.pi * df['hour'] / 24).astype('float64')
        df['hour_cos'] = np.cos(2 * np.pi * df['hour'] / 24).astype('float64')
        
        # Cyclical encoding for day of week
        if 'day_of_week' in df.columns:
            df['day_sin'] = np.sin(2 * np.pi * df['day_of_week'] / 7).astype('float64')
            df['day_cos'] = np.cos(2 * np.pi * df['day_of_week'] / 7).astype('float64')
        
        # Cyclical encoding for month
        if 'month' in df.columns:
            df['month_sin'] = np.sin(2 * np.pi * df['month'] / 12).astype('float64')
            df['month_cos'] = np.cos(2 * np.pi * df['month'] / 12).astype('float64')
    
    return df

def _parse_time_to_hour(time_str: str) -> Optional[int]:
    """Parse time string to hour (0-23) with comprehensive format support.
    
    Args:
        time_str: Time string in various formats
        
    Returns:
        Hour as integer or None if parsing fails
    """
    try:
        if pd.isna(time_str):
            return None
        
        # Handle decimal format (e.g., "0.541666667" for 13:00)
        if isinstance(time_str, (int, float)):
            hour = int(float(time_str) * 24)
            return hour % 24 if hour >= 0 else None
        
        # Handle string format
        time_str = str(time_str).strip()
        
        # Try common time formats
        formats = [
            '%H:%M',
            '%H:%M:%S',
            '%I:%M %p',
            '%I:%M:%S %p',
            '%H.%M',
            '%I.%M %p'
        ]
        
        for fmt in formats:
            try:
                dt = datetime.strptime(time_str, fmt)
                return dt.hour
            except ValueError:
                continue
        
        # Try extracting hour from decimal time
        try:
            decimal_time = float(time_str)
            hour = int(decimal_time * 24)
            return hour % 24 if 0 <= hour < 24 else None
        except ValueError:
            pass
        
        return None
        
    except Exception:
        return None