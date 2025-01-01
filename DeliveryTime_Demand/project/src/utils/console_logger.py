"""Console logging utilities for model metrics and predictions."""
import sys
from typing import Dict, Any

def print_separator(char="=", length=80):
    """Print a separator line."""
    print(f"\n{char * length}\n")

def print_model_comparison(results: Dict[str, Dict[str, float]], best_model: str = None, best_score: float = None):
    """Print detailed model comparison results."""
    print_separator()
    print("MODEL COMPARISON RESULTS")
    print_separator()
    
    # Print header
    headers = ["Model", "MSE", "RMSE", "MAE", "MAPE", "R²"]
    header_format = "{:<15} {:<10} {:<10} {:<10} {:<10} {:<10}"
    print(header_format.format(*headers))
    print("-" * 65)
    
    # Print each model's results
    row_format = "{:<15} {:<10.2f} {:<10.2f} {:<10.2f} {:<10.2f} {:<10.4f}"
    for model_name, metrics in results.items():
        print(row_format.format(
            model_name,
            metrics['mse'],
            metrics['rmse'],
            metrics['mae'],
            metrics['mape'],
            metrics['r2']
        ))
    
    # Print best model if provided
    if best_model and best_score:
        print_separator("-", 65)
        print(f"🏆 Best Model: {best_model}")
        print(f"Best R² Score: {best_score:.4f}")

def print_best_model(model_name: str, metrics: Dict[str, float]):
    """Print best model results."""
    print_separator()
    print("🏆 BEST MODEL RESULTS")
    print_separator()
    print(f"Best Model: {model_name}")
    print(f"R² Score: {metrics['r2']:.4f}")
    print(f"RMSE: {metrics['rmse']:.2f}")
    print(f"MAE: {metrics['mae']:.2f}")
    print(f"MAPE: {metrics['mape']:.2f}%")

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
    
    print("\nOverall hourly predictions:")
    for hour, count in enumerate(prediction['hourly_predictions']):
        print(f"{hour:02d}:00 - {count:.1f} orders")
    
    peak_hours_str = [f"{hour:02d}:00-{(hour+1):02d}:00" for hour in prediction['peak_hours']]
    print("\nOverall peak hours:", ", ".join(peak_hours_str))
    
    if 'city_predictions' in prediction:
        print("\nCity-wise Predictions:")
        for city, city_pred in prediction['city_predictions'].items():
            print(f"\n{city}:")
            print(f"  Total orders: {city_pred['total_orders']:.0f}")
            city_peak_hours = [f"{hour:02d}:00-{(hour+1):02d}:00" for hour in city_pred['peak_hours']]
            print(f"  Peak hours: {', '.join(city_peak_hours)}")