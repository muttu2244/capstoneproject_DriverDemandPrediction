"""Main script for delivery time prediction with model comparison."""
import os
import sys

# Add the project root directory to Python path
project_root = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
sys.path.append(project_root)

import pandas as pd
from src.data_processor import DataProcessor
from src.models.training import ModelTrainer

def main():
    try:
        # Load and preprocess data
        print("Loading and preprocessing data...")
        data = pd.read_csv('data/raw/delivery_data.csv')
        
        # Train models
        print("\n=== Training Delivery Time Models ===")
        trainer = ModelTrainer()
        trainer.train_models(data)
        
    except Exception as e:
        print(f"Error loading/training models: {str(e)}")

if __name__ == "__main__":
    main()