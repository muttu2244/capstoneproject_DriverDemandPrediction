"""Unified script to run all delivery prediction components."""
import os
import sys
import pandas as pd
import time
from multiprocessing import Process
from src.models.training import ModelTrainer
from src.models.delivery_time_model import DeliveryTimeModel
from src.models.peak_demand_model import PeakDemandModel
from src.data_processor import DataProcessor

def run_dashboard():
    """Run the Streamlit dashboard."""
    print("\nStarting the Streamlit dashboard...")
    os.system("streamlit run src/dashboard/dashboard.py")

def train_and_predict():
    """Train models and make sample predictions."""
    try:
        # 1. Train Models
        print("=== Training Models ===")
        data = pd.read_csv('data/raw/delivery_data.csv')
        trainer = ModelTrainer()
        trainer.train_models(data)

        # 2. Sample Predictions
        print("\n=== Sample Predictions ===")
        
        # Delivery Time Prediction
        print("\nDelivery Time Prediction:")
        order = {
            'restaurant_lat': 30.327968,
            'restaurant_lng': 78.046106,
            'delivery_lat': 30.337968,
            'delivery_lng': 78.056106,
            'weather': 'Clear',
            'traffic': 'Medium',
            'vehicle_type': 'motorcycle',
            'order_time': '14:30'
        }
        
        processor = DataProcessor()
        model = DeliveryTimeModel()
        processed_data = processor.preprocess(data)
        X = processed_data.drop(['time_taken(min)', 'Weatherconditions', 'Road_traffic_density',
                                 'Type_of_order', 'Type_of_vehicle', 'City', 'Festival', 'Order_Date',
                                 'Time_Orderd', 'Time_Order_picked'], axis=1)
        y = processed_data['time_taken(min)']
        model.train(X, y)
        processed_order = processor.process_single_order(order)
        estimated_time = model.predict(pd.DataFrame([processed_order]))
        print(f"Estimated delivery time: {estimated_time[0]:.1f} minutes")
        
        # Peak Demand Prediction
        print("\nPeak Demand Prediction:")
        demand_model = PeakDemandModel()
        demand_model.train(data)
        prediction = demand_model.predict_next_day()
        print(f"Total orders expected: {prediction['total_orders']}")
        print("\nPeak hours:")
        for hour in prediction['peak_hours']:
            print(f"  {hour:02d}:00 - {(hour+1):02d}:00")
    except Exception as e:
        print(f"Error during training and prediction: {str(e)}")
        sys.exit(1)

def main():
    """Main function to orchestrate the components."""
    try:
        # Train models and make predictions
        train_and_predict()

        # Start the dashboard in a separate process
        dashboard_process = Process(target=run_dashboard)
        dashboard_process.start()

        print("\n=== All components started ===")
        print("Dashboard is running at http://localhost:8501")
        print("\nPress Ctrl+C to exit")

        while True:
            time.sleep(1)

    except KeyboardInterrupt:
        print("\nShutting down...")
        sys.exit(0)
    except Exception as e:
        print(f"Unexpected error: {str(e)}")
        sys.exit(1)

if __name__ == "__main__":
    main()
