"""Data loading utilities for dashboard."""
import streamlit as st
import pandas as pd
from pathlib import Path
from typing import Optional
import joblib
from src.models.delivery_time_model import DeliveryTimeModel
from src.data_processor import DataProcessor

@st.cache_data
def load_dashboard_data() -> Optional[pd.DataFrame]:
    """Load and cache dashboard data."""
    try:
        # Get the absolute path to the data directory
        data_path = Path(__file__).parent.parent.parent / "data" / "raw" / "delivery_data.csv"
        print(f"+++++++++++data_path is: {data_path}+++++++++")
        if not data_path.exists():
            st.error(f"Data file not found at {data_path}")
            return None
            
        # Load raw data
        data = pd.read_csv(
            data_path,
            parse_dates=['Order_Date'],
            date_format='%d-%m-%Y'
        )
        
        # Add derived columns
        #data = add_derived_columns(data)
        #print(f"&&&&&&&&data after derived cols: {data}&&&&&&&&&")
        ###################################################
        
        # Load the trained model
        model_path = Path(__file__).parent.parent.parent /"data" / "models" / "delivery_time_model.pkl"
        #print(f"+++++++++++model path is: {model_path}+++++++++")
        if not model_path.exists():
            st.error(f"Trained model file not found at {model_path}")
            return None
        
        # Load the trained model
        model = joblib.load(model_path)
        
        #print(f"+++++++++++model b4 predicting is: {model}+++++++++")
        processor = DataProcessor()
        processed_data = processor.preprocess(data)
        processed_data = processed_data.drop(['time_taken(min)', 'Weatherconditions', 'Road_traffic_density',
                                    'Type_of_order', 'Type_of_vehicle', 'City', 'Festival', 'Order_Date',
                                    'Time_Orderd', 'Time_Order_picked'], axis=1)
        #y = processed_data['time_taken(min)']
        print(f"+++++++++++processed_data cols is: {processed_data.columns}+++++++++")
        # Make predictions on the data
        # Assuming the model expects certain columns, preprocess the data as necessary
        predictions = model.predict(processed_data)  # Example features
        
        print(f"+++++++++++predictions  is: {predictions}+++++++++")

        # Add the predictions to the dataframe
        processed_data['predicted_demand'] = predictions
        print(f"+++++++++++predicted_demand is: {processed_data.columns}+++++++++")
        
        return processed_data
        
    except Exception as e:
        st.error(f"Error loading data: {str(e)}")
        return None
        
        ###################################################
            
            


'''
def load_dashboard_data() -> Optional[pd.DataFrame]:
    """Load and cache dashboard data."""
    try:
        # Get the absolute path to the data directory
        data_path = Path(__file__).parent.parent.parent / "data" / "raw" / "delivery_data.csv"
        
        if not data_path.exists():
            st.error(f"Data file not found at {data_path}")
            return None
            
        # Load raw data
        data = pd.read_csv(
            data_path,
            parse_dates=['Order_Date'],
            date_format='%d-%m-%Y'
        )
        
        # Add derived columns
        data = add_derived_columns(data)
            
        return data
        
    except Exception as e:
        st.error(f"Error loading data: {str(e)}")
        return None
'''

def add_derived_columns(df: pd.DataFrame) -> pd.DataFrame:
    """Add derived columns for analysis."""
    df = df.copy()
    
    # Add hour column from Order_Date
    df['hour'] = df['Order_Date'].dt.hour
    
    # Add day of week
    df['day_of_week'] = df['Order_Date'].dt.dayofweek
    
    # Add is_weekend flag
    df['is_weekend'] = df['day_of_week'].isin([5, 6]).astype(int)
    
    # Add order count column for aggregations
    df['order_count'] = 1
    #df['order_count'] = df.groupby('city')['Order_Date'].transform('count')
    
    
    return df