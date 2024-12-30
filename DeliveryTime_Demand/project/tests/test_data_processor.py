"""Tests for data preprocessing pipeline."""
import pytest
import pandas as pd
import numpy as np
from src.data.processor import DataProcessor

@pytest.fixture
def sample_data():
    return pd.DataFrame({
        'Restaurant_latitude': [30.327968],
        'Restaurant_longitude': [78.046106],
        'Delivery_location_latitude': [30.337968],
        'Delivery_location_longitude': [78.056106],
        'Weatherconditions': ['Fog'],
        'Road_traffic_density': ['High'],
        'Type_of_vehicle': ['motorcycle'],
        'Order_Date': ['2024-01-01'],
        'Time_Orderd': ['21:55']
    })

def test_preprocess_calculates_distance(sample_data):
    processor = DataProcessor()
    processed = processor.preprocess(sample_data)
    assert 'distance' in processed.columns
    assert not processed['distance'].isna().any()

def test_preprocess_handles_missing_columns():
    processor = DataProcessor()
    bad_data = pd.DataFrame({'wrong_column': [1]})
    with pytest.raises(ValueError, match="Missing columns"):
        processor.preprocess(bad_data)