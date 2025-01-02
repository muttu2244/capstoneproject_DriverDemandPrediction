# src/server.py
from fastapi import FastAPI, HTTPException
from fastapi.middleware.cors import CORSMiddleware
from pydantic import BaseModel
from typing import Dict, Any
from .models.delivery_time_model import DeliveryTimeModel
from .models.peak_demand_model import PeakDemandModel
from .data_processor import DataProcessor

app = FastAPI()

# Add CORS middleware
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Models
delivery_model = DeliveryTimeModel()
peak_model = PeakDemandModel()
processor = DataProcessor()

class OrderData(BaseModel):
    restaurant_lat: float
    restaurant_lng: float
    delivery_lat: float
    delivery_lng: float
    weather: str
    traffic: str
    vehicle_type: str
    order_time: str

@app.post("/api/predict/delivery-time")
async def predict_delivery_time(order_data: OrderData):
    try:
        # Process order data
        processed_order = processor.process_single_order(order_data.dict())
        
        # Make prediction
        estimated_time = delivery_model.predict(processed_order)
        
        return {
            "estimated_time": float(estimated_time),
            "unit": "minutes"
        }
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

@app.post("/api/predict/peak-demand")
async def predict_peak_demand():
    try:
        prediction = peak_model.predict_next_day()
        return {
            "total_orders": float(prediction["total_orders"]),
            "peak_hours": prediction["peak_hours"],
            "hourly_predictions": prediction["hourly_predictions"]
        }
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))
