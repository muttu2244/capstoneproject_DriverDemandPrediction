"""FastAPI server for delivery prediction service."""
from fastapi import FastAPI, HTTPException, Request
from fastapi.middleware.cors import CORSMiddleware
from fastapi.responses import JSONResponse
from typing import Dict, Any
import logging
from pydantic import BaseModel

from .models.delivery_time_model import DeliveryTimeModel
from .models.peak_demand_model import PeakDemandModel
from .data.data_loader import load_processed_data
from .utils.validation import validate_order_data

# Configure logging
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

# Initialize FastAPI app
app = FastAPI(
    title="Delivery Prediction Service",
    description="API for delivery time and peak demand predictions",
    version="1.0.0"
)

# Add CORS middleware
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"]
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
    unit: str = "minutes"

class PeakDemandResponse(BaseModel):
    total_orders: float
    peak_hours: list
    hourly_predictions: list

# Error handler
@app.exception_handler(Exception)
async def global_exception_handler(request: Request, exc: Exception):
    logger.error(f"Error processing request: {str(exc)}")
    return JSONResponse(
        status_code=500,
        content={"error": str(exc)}
    )

# Health check endpoint
@app.get("/health")
async def health_check():
    """Health check endpoint."""
    return {"status": "healthy"}

# Prediction endpoints
@app.post("/api/predict/delivery-time", response_model=DeliveryTimeResponse)
async def predict_delivery_time(order: OrderRequest):
    """Predict delivery time for an order."""
    try:
        # Validate order data
        validate_order_data(order.dict())
        
        # Load model and make prediction
        model = DeliveryTimeModel()
        data = load_processed_data()
        
        if data is not None:
            model.train(data)
            estimated_time = model.predict(order.dict())
            
            return {
                "estimated_time": float(estimated_time),
                "unit": "minutes"
            }
        else:
            raise HTTPException(status_code=500, detail="Could not load training data")
            
    except Exception as e:
        logger.error(f"Error predicting delivery time: {str(e)}")
        raise HTTPException(status_code=400, detail=str(e))

@app.post("/api/predict/peak-demand", response_model=PeakDemandResponse)
async def predict_peak_demand():
    """Predict peak demand patterns."""
    try:
        # Load model and make prediction
        model = PeakDemandModel()
        data = load_processed_data()
        
        if data is not None:
            model.train(data)
            prediction = model.predict()
            
            return {
                "total_orders": float(prediction['total_orders']),
                "peak_hours": prediction['peak_hours'],
                "hourly_predictions": prediction['hourly_predictions']
            }
        else:
            raise HTTPException(status_code=500, detail="Could not load training data")
            
    except Exception as e:
        logger.error(f"Error predicting peak demand: {str(e)}")
        raise HTTPException(status_code=400, detail=str(e))

# Model metrics endpoint
@app.get("/api/metrics")
async def get_model_metrics():
    """Get current model performance metrics."""
    try:
        delivery_model = DeliveryTimeModel()
        peak_model = PeakDemandModel()
        data = load_processed_data()
        
        if data is not None:
            delivery_metrics = delivery_model.train(data)
            peak_metrics = peak_model.train(data)
            
            return {
                "delivery_time_model": delivery_metrics,
                "peak_demand_model": peak_metrics
            }
        else:
            raise HTTPException(status_code=500, detail="Could not load training data")
            
    except Exception as e:
        logger.error(f"Error getting model metrics: {str(e)}")
        raise HTTPException(status_code=400, detail=str(e))

if __name__ == "__main__":
    import uvicorn
    uvicorn.run(app, host="0.0.0.0", port=8000)
