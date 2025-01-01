# run.py
"""Main entry point for the delivery prediction service."""
import argparse
from src.data_processor import DataProcessor
from src.models.delivery_time_model import DeliveryTimeModel
from src.models.peak_demand_model import PeakDemandModel
import pandas as pd

def train_main():
    """Train the models."""
    try:
        # Initialize data processor
        processor = DataProcessor()
        
        print("Loading and preprocessing data...")
        data = pd.read_csv('data/raw/delivery_data.csv')
        processed_data = processor.preprocess(data)
        
        print("\n=== Training Delivery Time Model ===")
        delivery_model = DeliveryTimeModel()
        delivery_metrics = delivery_model.train(processed_data)
        
        print("\n=== Training Peak Demand Model ===")
        peak_model = PeakDemandModel()
        peak_metrics = peak_model.train(processed_data)
        
    except Exception as e:
        print(f"Error loading/training models: {str(e)}")

def main():
    parser = argparse.ArgumentParser(description='Delivery prediction service')
    parser.add_argument('--mode', choices=['train', 'serve'], default='serve',
                      help='Run mode: train models or serve predictions')
    
    args = parser.parse_args()
    
    if args.mode == 'train':
        train_main()
    else:
        # Add API server mode here if needed
        pass

if __name__ == "__main__":
    main()
