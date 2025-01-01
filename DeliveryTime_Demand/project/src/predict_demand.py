"""Script to test peak demand prediction."""
import pandas as pd
from src.models.peak_demand_model import PeakDemandModel

def predict_demand():
    # Load and process data
    data = pd.read_csv('data/raw/delivery_data.csv')
    
    # Train model
    model = PeakDemandModel()
    model.train(data)
    
    # Get predictions
    prediction = model.predict_next_day()
    
    print("\nPeak Demand Prediction:")
    print(f"Total orders expected: {prediction['total_orders']}")
    print("\nPeak hours:")
    for hour in prediction['peak_hours']:
        print(f"  {hour:02d}:00 - {(hour+1):02d}:00")
    
    print("\nHourly predictions:")
    for hour, count in enumerate(prediction['hourly_predictions']):
        print(f"  {hour:02d}:00 - {count:.0f} orders")

if __name__ == "__main__":
    predict_demand()