"""Data directory configuration."""
from pathlib import Path

# Base paths
PROJECT_ROOT = Path(__file__).parent.parent.parent
DATA_DIR = PROJECT_ROOT / "data"

# Data subdirectories
RAW_DATA_DIR = DATA_DIR / "raw"
PROCESSED_DATA_DIR = DATA_DIR / "processed"
MODEL_DIR = DATA_DIR / "models"

# Create directories
for directory in [RAW_DATA_DIR, PROCESSED_DATA_DIR, MODEL_DIR]:
    directory.mkdir(parents=True, exist_ok=True)

# File paths
HISTORICAL_DATA_PATH = RAW_DATA_DIR / "historical_deliveries.csv"
PROCESSED_DATA_PATH = PROCESSED_DATA_DIR / "processed_deliveries.csv"
MODEL_PATH = MODEL_DIR / "delivery_model.pkl"