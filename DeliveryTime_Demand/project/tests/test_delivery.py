"""Test delivery time predictions."""
import pandas as pd
from src.data_processor import DataProcessor
from src.models.delivery_time_model import DeliveryTimeModel
from src.models.features.feature_preparation import prepare_prediction_features

def test_delivery_prediction():
    """Test delivery time prediction with sample orders."""
    # Sample orders
    orders = [
        {
            'restaurant_lat': 30.327968,
            'restaurant_lng': 78.046106,
            'delivery_lat': 30.337968,
            'delivery_lng': 78.056106,
            'weather': 'Clear',
            'traffic': 'Low',
            'vehicle_type': 'motorcycle',
            'order_time': '14:30'
        },
        {
            'restaurant_lat': 30.327968,
            'restaurant_lng': 78.046106,
            'delivery_lat': 30.357968,
            'delivery_lng': 78.086106,
            'weather': 'Rain',
            'traffic': 'High',
            'vehicle_type': 'motorcycle',
            'order_time': '18:30'
        }
    ]
    
    try:
        # Load and process training data
        data = pd.read_csv('data/raw/delivery_data.csv')
        processor = DataProcessor()
        processed_data = processor.preprocess(data)
        #print(f"*********dataframe in test_delivery_prediction {processed_data.columns}***********")
        # Train model
        
        #X, y = processed_data.drop(['time_taken(min)'], axis=1), processed_data['time_taken(min)']
        X, y = processed_data.drop(['time_taken(min)','Weatherconditions','Road_traffic_density','Type_of_order','Type_of_vehicle','City','Festival', 'Order_Date', 'Time_Orderd',
       'Time_Order_picked'], axis=1), processed_data['time_taken(min)']
        #X, y = processed_data
        model = DeliveryTimeModel()
        model.train(X, y)
        
        print("\nDelivery Time Predictions:")
        print("-" * 50)
        
        # Test predictions
        for i, order in enumerate(orders, 1):
            features = prepare_prediction_features(order)
            #print(f"*********features being sent to predict {features.columns}***********")
            time = model.predict(features)[0]
            
            print(f"\nOrder {i}:")
            print(f"From: ({order['restaurant_lat']}, {order['restaurant_lng']})")
            print(f"To: ({order['delivery_lat']}, {order['delivery_lng']})")
            print(f"Weather: {order['weather']}")
            print(f"Traffic: {order['traffic']}")
            print(f"Time: {order['order_time']}")
            print(f"Estimated delivery time: {time:.1f} minutes")
            
    except Exception as e:
        print(f"Error: {str(e)}")

if __name__ == "__main__":
    test_delivery_prediction()