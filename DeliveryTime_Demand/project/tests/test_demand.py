"""Test peak demand predictions."""
import pandas as pd
from src.models.peak_demand_model import PeakDemandModel

def test_demand_prediction():
    """Test peak demand predictions."""
    try:
        # Load data
        data = pd.read_csv('data/raw/delivery_data.csv')
        
        # Train model
        model = PeakDemandModel()
        model.train(data)
        
        # Get predictions
        prediction = model.predict_next_day()
        
        print("\nPeak Demand Predictions:")
        print("-" * 50)
        print(f"\nTotal orders expected: {prediction['total_orders']:.0f}")
        
        print("\nPeak Hours:")
        for hour in prediction['peak_hours']:
            print(f"  {hour:02d}:00 - {(hour+1):02d}:00")
        
        print("\nHourly Breakdown:")
        for hour, count in enumerate(prediction['hourly_predictions']):
            print(f"  {hour:02d}:00: {count:.0f} orders")
            
    except Exception as e:
        print(f"Error: {str(e)}")

if __name__ == "__main__":
    test_demand_prediction()