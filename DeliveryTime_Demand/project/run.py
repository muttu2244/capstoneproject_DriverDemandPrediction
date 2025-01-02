"""Main entry point for the delivery prediction service."""
import os
from typing import Dict, Any
from fastapi import FastAPI, HTTPException
from fastapi.middleware.cors import CORSMiddleware
from pydantic import BaseModel
import uvicorn

from src.main import main
from src.data_processor import DataProcessor
from src.models.delivery_time_model import DeliveryTimeModel
from src.models.peak_demand_model import PeakDemandModel
from src.utils.validation import validate_order_data

# Create FastAPI app
app = FastAPI(title="Delivery Prediction Service")

# Add CORS middleware
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Request/Response models
class OrderRequest(BaseModel):
    restaurant_lat: float
    restaurant_lng: float
    delivery_lat: float
    delivery_lng: float
    weather: str
    traffic: str
    vehicle_type: str
    order_time: str

class DeliveryTimeResponse(BaseModel):
    estimated_time: float
    unit: str

class PeakDemandResponse(BaseModel):
    total_orders: float
    peak_hours: list
    hourly_predictions: list

# Initialize models
delivery_model = DeliveryTimeModel()
peak_model = PeakDemandModel()
processor = DataProcessor()

@app.get("/")
async def root():
    return {"message": "Delivery Prediction Service API"}

@app.post("/api/predict/delivery-time", response_model=DeliveryTimeResponse)
async def predict_delivery_time(order: OrderRequest):
    try:
        # Validate order data
        order_dict = order.dict()
        validate_order_data(order_dict)
        
        # Process order data
        processed_order = processor.process_single_order(order_dict)
        
        # Make prediction
        estimated_time = delivery_model.predict(processed_order)
        
        return {
            "estimated_time": float(estimated_time),
            "unit": "minutes"
        }
    except Exception as e:
        raise HTTPException(status_code=400, detail=str(e))

@app.post("/api/predict/peak-demand", response_model=PeakDemandResponse)
async def predict_peak_demand():
    try:
        prediction = peak_model.predict_next_day()
        return {
            "total_orders": float(prediction['total_orders']),
            "peak_hours": prediction['peak_hours'],
            "hourly_predictions": prediction['hourly_predictions']
        }
    except Exception as e:
        raise HTTPException(status_code=400, detail=str(e))

if __name__ == "__main__":
    if os.environ.get("API_MODE"):
        # Run as API server
        uvicorn.run(app, host="0.0.0.0", port=8000)
    else:
        # Run model training and evaluation
        main()