"""Setup script for the delivery prediction service."""
from setuptools import setup, find_packages

setup(
    name="delivery-prediction-service",
    version="1.0.0",
    packages=find_packages(),
    install_requires=[
        'pandas==2.1.0',
        'numpy==1.24.3',
        'scikit-learn==1.3.0',
        'python-dateutil==2.8.2',
        'lightgbm==4.1.0',
        'xgboost==2.0.3',
        'catboost==1.2.2',
        'tensorflow==2.15.0',
        'statsmodels==0.14.0',
        'pytest==7.4.0'
    ]
)