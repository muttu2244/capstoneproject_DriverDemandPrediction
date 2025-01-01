"""Setup script for the delivery analytics package."""
from setuptools import setup, find_packages

setup(
    name="delivery_analytics",
    version="1.0.0",
    packages=find_packages(),
    install_requires=[
        'streamlit==1.28.1',
        'pandas==2.1.0',
        'numpy==1.24.3',
        'plotly==5.18.0',
        'scikit-learn==1.3.0',
        'python-dateutil==2.8.2'
    ]
)