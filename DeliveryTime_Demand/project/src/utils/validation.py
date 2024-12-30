"""Input validation utilities."""
from typing import Dict, Any, List

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
    
    for field, field_type in required_fields.items():
        if field not in order_data:
            raise ValueError(f"Missing required field: {field}")
        if not isinstance(order_data[field], field_type):
            raise TypeError(f"Field {field} must be of type {field_type.__name__}")
    
    # Validate coordinates
    validate_coordinates(order_data['restaurant_lat'], order_data['restaurant_lng'])
    validate_coordinates(order_data['delivery_lat'], order_data['delivery_lng'])