"""Configuration for data directory paths."""
from pathlib import Path

# Base paths
PROJECT_ROOT = Path(__file__).parent.parent.parent
DATA_DIR = PROJECT_ROOT / "data"

# Data subdirectories
RAW_DIR = DATA_DIR / "raw"
PROCESSED_DIR = DATA_DIR / "processed"
MODELS_DIR = DATA_DIR / "models"

# Create directories if they don't exist
for directory in [RAW_DIR, PROCESSED_DIR, MODELS_DIR]:
    directory.mkdir(parents=True, exist_ok=True)

# File paths
RAW_DATA_PATH = RAW_DIR / "delivery_data.csv"
PROCESSED_DATA_PATH = PROCESSED_DIR / "processed_delivery_data.csv"
DELIVERY_MODEL_PATH = MODELS_DIR / "delivery_time_model.pkl"
DEMAND_MODEL_PATH = MODELS_DIR / "peak_demand_model.pkl"