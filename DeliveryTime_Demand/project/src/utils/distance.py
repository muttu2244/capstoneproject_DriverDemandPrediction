"""Distance calculation utilities."""
import numpy as np
from typing import Tuple

def calculate_haversine_distance(lat1: float, lon1: float, lat2: float, lon2: float) -> float:
    """Calculate the great circle distance between two points on Earth."""
    R = 6371  # Earth's radius in kilometers
    
    # Convert decimal degrees to radians
    lat1, lon1, lat2, lon2 = map(np.radians, [lat1, lon1, lat2, lon2])
    
    # Haversine formula
    dlat = lat2 - lat1
    dlon = lon2 - lon1
    
    a = np.sin(dlat/2)**2 + np.cos(lat1) * np.cos(lat2) * np.sin(dlon/2)**2
    c = 2 * np.arcsin(np.sqrt(a))
    
    return R * c

def calculate_manhattan_distance(lat1: float, lon1: float, lat2: float, lon2: float) -> float:
    """Calculate Manhattan (city block) distance between two points."""
    # Convert to radians
    lat1, lon1, lat2, lon2 = map(np.radians, [lat1, lon1, lat2, lon2])
    
    # Calculate distances
    R = 6371  # Earth's radius in kilometers
    x = (lon2 - lon1) * np.cos(0.5 * (lat1 + lat2))
    y = lat2 - lat1
    
    return R * (abs(x) + abs(y))

def get_bounding_box(lat: float, lon: float, radius_km: float) -> Tuple[float, float, float, float]:
    """Calculate bounding box coordinates given a center point and radius."""
    # Convert radius from kilometers to degrees
    r_earth = 6371  # Earth's radius in kilometers
    radius_deg = (radius_km / r_earth) * (180 / np.pi)
    
    # Calculate bounding box
    min_lat = lat - radius_deg
    max_lat = lat + radius_deg
    min_lon = lon - radius_deg / np.cos(lat * np.pi / 180)
    max_lon = lon + radius_deg / np.cos(lat * np.pi / 180)
    
    return min_lat, min_lon, max_lat, max_lon