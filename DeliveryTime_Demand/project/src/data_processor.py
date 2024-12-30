"""Main data processing pipeline."""
from typing import Dict, Any
import pandas as pd
from .models.features import (
    extract_time_features,
    extract_distance_features,
    CategoricalFeatureProcessor,
    NumericFeatureProcessor
)

class DataProcessor:
    def __init__(self):
        self.categorical_processor = CategoricalFeatureProcessor()
        self.numeric_processor = NumericFeatureProcessor()
        
    def preprocess(self, df: pd.DataFrame) -> pd.DataFrame:
        """Main preprocessing pipeline."""
        try:
            df = df.copy()
            
            # Extract features
            df = extract_time_features(df)
            df = extract_distance_features(df)
            df = self.categorical_processor.process_features(df)
            df = self.numeric_processor.process_features(df)
            
            return df
            
        except Exception as e:
            raise Exception(f"Error in preprocessing pipeline: {str(e)}")
    
    def process_single_order(self, order_data: Dict[str, Any]) -> Dict[str, Any]:
        """Process a single order for prediction."""
        try:
            # Create single-row DataFrame with all required fields
            df = pd.DataFrame([{
                'Restaurant_latitude': order_data['restaurant_lat'],
                'Restaurant_longitude': order_data['restaurant_lng'],
                'Delivery_location_latitude': order_data['delivery_lat'],
                'Delivery_location_longitude': order_data['delivery_lng'],
                'Weatherconditions': order_data['weather'],
                'Road_traffic_density': order_data['traffic'],
                'Type_of_vehicle': order_data['vehicle_type'],
                'Order_Date': pd.Timestamp.now().strftime('%d-%m-%Y'),
                'Time_Orderd': order_data['order_time'],
                # Add default values for required fields
                'Type_of_order': 'Snack',  # Default order type
                'Festival': 'No',  # Default no festival
                'City': 'Urban',  # Default urban area
                'Delivery_person_Age': 30,  # Default age
                'Vehicle_condition': 2,  # Default condition (1-3)
                'multiple_deliveries': 0,  # Default single delivery
                'Delivery_person_Ratings': 4.5  # Default rating
            }])
            
            # Apply preprocessing
            processed_df = self.preprocess(df)
            
            return processed_df.iloc[0].to_dict()
            
        except Exception as e:
            raise Exception(f"Error processing order: {str(e)}")