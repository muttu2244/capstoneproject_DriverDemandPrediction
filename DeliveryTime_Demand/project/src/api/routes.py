"""FastAPI route definitions."""
from fastapi import APIRouter, HTTPException
from typing import Dict, Any
from ..models.delivery_time_model import DeliveryTimeModel
from ..models.peak_demand_model import PeakDemandModel
from ..data.data_loader import load_processed_data
from ..utils.validation import validate_order_data

# Create router
router = APIRouter()

# Initialize models
delivery_model = DeliveryTimeModel()
peak_model = PeakDemandModel()

# Load and preprocess data
try:
    data = load_processed_data()
    if data is not None:
        delivery_model.train(data)
        peak_model.train(data)
except Exception as e:
    print(f"Error loading/training models: {str(e)}")

@router.get("/")
async def root():
    """Root endpoint."""
    return {"message": "Delivery Analytics API"}

@router.post("/predict/delivery-time")
async def predict_delivery_time(order: Dict[str, Any]):
    """Predict delivery time for an order."""
    try:
        # Validate order data
        validate_order_data(order)
        
        # Make prediction
        estimated_time = delivery_model.predict(order)
        
        return {
            "estimated_time": float(estimated_time),
            "unit": "minutes"
        }
    except Exception as e:
        raise HTTPException(status_code=400, detail=str(e))

@router.post("/predict/peak-demand")
async def predict_peak_demand():
    """Predict peak demand patterns."""
    try:
        prediction = peak_model.predict_next_day()
        return prediction
    except Exception as e:
        raise HTTPException(status_code=400, detail=str(e))