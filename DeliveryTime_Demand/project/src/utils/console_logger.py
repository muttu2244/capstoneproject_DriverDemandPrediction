"""Console logging utilities for model metrics and predictions."""
import sys
from typing import Dict, Any

def print_separator():
    """Print a separator line."""
    print("\n" + "="*80 + "\n")

def print_model_results(results: Dict[str, Dict[str, float]], best_model: str, best_score: float):
    """Print model evaluation results to console."""
    print_separator()
    print("MODEL EVALUATION RESULTS")
    print_separator()
    
    for model_name, metrics in results.items():
        print(f"{model_name}:")
        print(f"  MSE:  {metrics['mse']:.2f}")
        print(f"  RMSE: {metrics['rmse']:.2f}")
        print(f"  MAE:  {metrics['mae']:.2f}")
        print(f"  MAPE: {metrics['mape']:.2f}%")
        print(f"  R2:   {metrics['r2']:.4f}\n")
    
    print(f"🏆 Best Model: {best_model}")
    print(f"Best R2 Score: {best_score:.4f}")

def print_delivery_prediction(estimated_time: float, features: Dict[str, Any]):
    """Print delivery time prediction to console."""
    print_separator()
    print("DELIVERY TIME PREDICTION")
    print_separator()
    
    print(f"Estimated delivery time: {estimated_time:.1f} minutes")
    print("\nOrder details:")
    print(f"  Weather: {features['weather']}")
    print(f"  Traffic: {features['traffic']}")
    print(f"  Vehicle: {features['vehicle_type']}")
    print(f"  Order time: {features['order_time']}")

def print_peak_demand_forecast(prediction: Dict[str, Any]):
    """Print peak demand predictions to console."""
    print_separator()
    print("PEAK DEMAND FORECAST")
    print_separator()
    
    print(f"Total orders expected: {prediction['total_orders']:.0f}")
    print(f"Average orders per hour: {prediction['total_orders']/24:.1f}")
    
    print("\nHourly predictions:")
    for hour, count in enumerate(prediction['hourly_predictions']):
        print(f"{hour:02d}:00 - {count:.1f} orders")
    
    peak_hours_str = [f"{hour:02d}:00-{(hour+1):02d}:00" for hour in prediction['peak_hours']]
    print("\nPeak hours:", ", ".join(peak_hours_str))