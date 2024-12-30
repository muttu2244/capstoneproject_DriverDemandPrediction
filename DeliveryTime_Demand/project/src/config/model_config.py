"""Model configuration parameters."""

DELIVERY_MODEL_CONFIG = {
    'n_estimators': 1000,
    'learning_rate': 0.01,
    'num_leaves': 31,
    'feature_fraction': 0.8,
    'bagging_fraction': 0.8,
    'bagging_freq': 5,
    'random_state': 42
}

PEAK_DEMAND_CONFIG = {
    'lstm_units': 50,
    'learning_rate': 0.001,
    'batch_size': 32,
    'epochs': 50,
    'validation_split': 0.2
}