"""Main script for delivery time prediction with model comparison."""
import pandas as pd
from .data_processor import DataProcessor
from .models.model_evaluator import ModelEvaluator
from .models.peak_demand_model import PeakDemandModel

def main():
    # Load and preprocess data
    print("Loading and preprocessing data...")
    data = pd.read_csv('data/raw/delivery_data.csv')
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
    results = evaluator.evaluate_models(X, y)
    
    # Get best model
    best_model_name, best_score = evaluator.get_best_model(metric='r2')
    print(f"\nBest Model: {best_model_name}")
    print(f"Best R2 Score: {best_score:.4f}")
    
    # Peak Demand Prediction
    print("\n=== Peak Demand Prediction ===")
    peak_model = PeakDemandModel()
    peak_model.train(processed_data)
    peak_prediction = peak_model.predict_next_day()
    
    print("\nPeak Demand Forecast:")
    print(f"Total orders expected: {peak_prediction['total_orders']:.0f}")
    print(f"Peak hours: {', '.join(map(str, peak_prediction['peak_hours']))}")
    print("\nHourly predictions:")
    for hour, count in enumerate(peak_prediction['hourly_predictions']):
        print(f"{hour:02d}:00 - {count:.1f} orders")

if __name__ == "__main__":
    main()