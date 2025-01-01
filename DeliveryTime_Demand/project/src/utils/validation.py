"""Input validation utilities."""
from typing import Dict, Any

def validate_coordinates(lat: float, lng: float) -> None:
    """Validate latitude and longitude values."""
    if not -90 <= lat <= 90:
        raise ValueError(f"Invalid latitude: {lat}")
    if not -180 <= lng <= 180:
        raise ValueError(f"Invalid longitude: {lng}")

def validate_order_data(order_data: Dict[str, Any]) -> None:
    """Validate order data contains required fields with correct types."""
    required_fields = {
        'restaurant_lat': float,
        'restaurant_lng': float,
        'delivery_lat': float,
        'delivery_lng': float,
        'weather': str,
        'traffic': str,
        'vehicle_type': str,
        'order_time': str
    }
    
    # Check required fields
    for field, field_type in required_fields.items():
        if field not in order_data:
            raise ValueError(f"Missing required field: {field}")
        if not isinstance(order_data[field], field_type):
            raise TypeError(f"Field {field} must be of type {field_type.__name__}")
    
    # Validate coordinates
    validate_coordinates(order_data['restaurant_lat'], order_data['restaurant_lng'])
    validate_coordinates(order_data['delivery_lat'], order_data['delivery_lng'])
    
    # Validate weather conditions
    valid_weather = {'Clear', 'Cloudy', 'Fog', 'Rain', 'Storm'}
    if order_data['weather'] not in valid_weather:
        raise ValueError(f"Invalid weather condition. Must be one of: {', '.join(valid_weather)}")
    
    # Validate traffic conditions
    valid_traffic = {'Low', 'Medium', 'High', 'Jam'}
    if order_data['traffic'] not in valid_traffic:
        raise ValueError(f"Invalid traffic condition. Must be one of: {', '.join(valid_traffic)}")
    
    # Validate vehicle type
    valid_vehicles = {'motorcycle', 'scooter', 'bicycle'}
    if order_data['vehicle_type'].lower() not in valid_vehicles:
        raise ValueError(f"Invalid vehicle type. Must be one of: {', '.join(valid_vehicles)}")