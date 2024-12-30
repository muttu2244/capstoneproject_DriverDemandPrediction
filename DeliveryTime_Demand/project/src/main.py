"""Main script for delivery time prediction with model comparison."""
import pandas as pd
from data_processor import DataProcessor
from models.model_evaluator import ModelEvaluator
from models.peak_demand_model import PeakDemandModel
from utils.console_logger import print_separator

def main():
    # Load and preprocess data
    print("Loading and preprocessing data...")
    data = pd.read_csv('data/delivery_data.csv')
    processor = DataProcessor()
    processed_data = processor.preprocess(data)
    
    # Prepare features for model training
    print("\n=== Delivery Time Prediction ===")
    
    # Select only numeric columns and encoded categorical columns
    feature_columns = [col for col in processed_data.columns 
                      if (col.endswith('_encoded') or  # Encoded categorical features
                          pd.api.types.is_numeric_dtype(processed_data[col])) and  # Numeric features
                          col not in ['time_taken(min)', 'Order_Date', 'Time_Orderd']]
    
    X = processed_data[feature_columns]
    y = processed_data['time_taken(min)']
    
    # Compare models
    print("\nComparing different models...")
    evaluator = ModelEvaluator()
    evaluator.evaluate_models(X, y)
    
    print_separator()
    print("\n=== Peak Demand Prediction ===")
    
    # Initialize and train peak demand model
    peak_model = PeakDemandModel()
    peak_model.train(processed_data)
    
    # Get and display predictions
    prediction = peak_model.predict()  # This will automatically print the forecast

if __name__ == "__main__":
    main()