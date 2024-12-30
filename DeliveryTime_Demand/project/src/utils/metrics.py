"""Model evaluation metrics."""
import numpy as np
from typing import Dict

def calculate_regression_metrics(y_true: np.ndarray, y_pred: np.ndarray) -> Dict[str, float]:
    """Calculate common regression metrics."""
    mse = np.mean((y_true - y_pred) ** 2)
    rmse = np.sqrt(mse)
    mae = np.mean(np.abs(y_true - y_pred))
    mape = np.mean(np.abs((y_true - y_pred) / y_true)) * 100
    r2 = 1 - np.sum((y_true - y_pred) ** 2) / np.sum((y_true - np.mean(y_true)) ** 2)
    
    return {
        'mse': float(mse),
        'rmse': float(rmse),
        'mae': float(mae),
        'mape': float(mape),
        'r2': float(r2)
    }

def calculate_classification_metrics(y_true: np.ndarray, y_pred: np.ndarray) -> Dict[str, float]:
    """Calculate classification metrics for peak hour prediction."""
    true_peaks = set(np.where(y_true > np.mean(y_true) + np.std(y_true))[0])
    pred_peaks = set(np.where(y_pred > np.mean(y_pred) + np.std(y_pred))[0])
    
    peak_precision = len(true_peaks.intersection(pred_peaks)) / len(pred_peaks) if pred_peaks else 0
    peak_recall = len(true_peaks.intersection(pred_peaks)) / len(true_peaks) if true_peaks else 0
    peak_f1 = 2 * (peak_precision * peak_recall) / (peak_precision + peak_recall) if (peak_precision + peak_recall) > 0 else 0
    
    return {
        'peak_precision': float(peak_precision),
        'peak_recall': float(peak_recall),
        'peak_f1': float(peak_f1)
    }