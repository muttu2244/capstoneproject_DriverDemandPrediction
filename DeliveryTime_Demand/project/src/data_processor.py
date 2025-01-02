"""Data preprocessing pipeline."""
import pandas as pd
import numpy as np
from typing import Dict, Any
from src.utils.type_conversion import to_numeric_safe, to_int_safe
from src.utils.distance import calculate_haversine_distance
from src.utils.time_parsers import parse_time_string

class DataProcessor:
    def __init__(self):
        self.numeric_columns = {
            'time_taken(min)': float,
            'Restaurant_latitude': float,
            'Restaurant_longitude': float,
            'Delivery_location_latitude': float,
            'Delivery_location_longitude': float,
            'Delivery_person_Age': int,
            'Delivery_person_Ratings': float,
            'Vehicle_condition': int,
            'multiple_deliveries': int,
            'distance': float
        }
        
        self.categorical_columns = {
            'Weatherconditions': 'Weatherconditions_encoded',
            'Road_traffic_density': 'Road_traffic_density_encoded',
            'Type_of_vehicle': 'Type_of_vehicle_encoded',
            'Type_of_order': 'Type_of_order_encoded',
            'Festival': 'Festival_encoded',
            'City': 'City_encoded'
        }
    
    def preprocess(self, data: pd.DataFrame) -> pd.DataFrame:
        """Preprocess the data for model training."""
        try:
            df = data.copy()
            
            # Drop ID columns if they exist
            id_columns = ['ID', 'Delivery_person_ID']
            #id_columns = ['ID']
            df = df.drop(columns=[col for col in id_columns if col in df.columns])
            
            # Process numeric columns
            df = self._process_numeric_columns(df)
            
            # Process categorical columns
            df = self._process_categorical_columns(df)
            
            # Calculate distance if not present
            if 'distance' not in df.columns:
                df = self._calculate_distances(df)
            
            # Extract hour from time
            df = self._extract_time_features(df)
            
            # Convert all remaining object columns to category
            for col in df.select_dtypes(['object']).columns:
                df[col] = df[col].astype('category')
            
            # Ensure all numeric columns are float64
            numeric_cols = df.select_dtypes(['int64', 'float64']).columns
            for col in numeric_cols:
                df[col] = df[col].astype('float64')
            
            return df
            
        except Exception as e:
            raise RuntimeError(f"Error preprocessing data: {str(e)}")
    
    def process_single_order(self, order_data: Dict[str, Any]) -> Dict[str, Any]:
        """Process a single order for prediction."""
        try:
            # Map categorical values to encoded values
            weather_mapping = {'Clear': 0, 'Cloudy': 1, 'Fog': 2, 'Rain': 3, 'Storm': 4}
            traffic_mapping = {'Low': 0, 'Medium': 1, 'High': 2, 'Jam': 3}
            vehicle_mapping = {'motorcycle': 0, 'scooter': 1, 'bicycle': 2}
            
            # Create DataFrame with all required features
            df = pd.DataFrame([{
                'Restaurant_latitude': float(order_data['restaurant_lat']),
                'Restaurant_longitude': float(order_data['restaurant_lng']),
                'Delivery_location_latitude': float(order_data['delivery_lat']),
                'Delivery_location_longitude': float(order_data['delivery_lng']),
                'Weatherconditions_encoded': weather_mapping.get(order_data.get('weather', 'Clear'), 0),
                'Road_traffic_density_encoded': traffic_mapping.get(order_data.get('traffic', 'Medium'), 0),
                'Type_of_vehicle_encoded': vehicle_mapping.get(order_data.get('vehicle_type', 'motorcycle').lower(), 0),
                'Type_of_order_encoded': 0,  # Default values for required features
                'Festival_encoded': 0,
                'City_encoded': 0,
                'Delivery_person_Age': 30,
                'Delivery_person_Ratings': 4.5,
                'Vehicle_condition': 2,
                'multiple_deliveries': 0,
                'hour': parse_time_string(order_data.get('order_time', '12:00'))
            }])
            
            # Calculate distance
            df['distance'] = calculate_haversine_distance(
                df['Restaurant_latitude'].iloc[0],
                df['Restaurant_longitude'].iloc[0],
                df['Delivery_location_latitude'].iloc[0],
                df['Delivery_location_longitude'].iloc[0]
            )
            
            # Ensure all numeric columns are float64
            numeric_cols = df.select_dtypes(['int64', 'float64']).columns
            for col in numeric_cols:
                df[col] = df[col].astype('float64')
            
            return df.iloc[0].to_dict()
            
        except Exception as e:
            raise RuntimeError(f"Error processing order: {str(e)}")
    
    def _process_numeric_columns(self, df: pd.DataFrame) -> pd.DataFrame:
        """Process numeric columns with type conversion."""
        for col, dtype in self.numeric_columns.items():
            if col in df.columns:
                if dtype == float:
                    df[col] = df[col].apply(to_numeric_safe).astype('float64')
                else:
                    df[col] = df[col].apply(to_int_safe).astype('float64')
                # Fill NaN with median
                df[col] = df[col].fillna(df[col].median())
        return df
    
    def _process_categorical_columns(self, df: pd.DataFrame) -> pd.DataFrame:
        """Process categorical columns with encoding."""
        for col, encoded_col in self.categorical_columns.items():
            if col in df.columns:
                df[encoded_col] = pd.Categorical(df[col]).codes
                df[encoded_col] = df[encoded_col].astype('float64')
        return df
    
    def _calculate_distances(self, df: pd.DataFrame) -> pd.DataFrame:
        """Calculate distances between restaurants and delivery locations."""
        df['distance'] = df.apply(
            lambda row: calculate_haversine_distance(
                row['Restaurant_latitude'],
                row['Restaurant_longitude'],
                row['Delivery_location_latitude'],
                row['Delivery_location_longitude']
            ),
            axis=1
        ).astype('float64')
        return df
    
    def _extract_time_features(self, df: pd.DataFrame) -> pd.DataFrame:
        """Extract time features from order time."""
        if 'Time_Orderd' in df.columns:
            df['hour'] = df['Time_Orderd'].apply(lambda x: parse_time_string(str(x)))
        elif 'hour' not in df.columns:
            df['hour'] = 12  # Default hour if no time column exists
        df['hour'] = df['hour'].astype('float64')
        return df