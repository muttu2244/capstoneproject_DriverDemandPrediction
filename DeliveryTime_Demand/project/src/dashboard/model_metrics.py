"""Model training and evaluation metrics display."""
import streamlit as st
import pandas as pd
import plotly.express as px
from src.models.model_evaluator import ModelEvaluator
from src.models.peak_demand_model import PeakDemandModel
from src.utils.console_logger import print_model_results, print_peak_demand_forecast

def display_model_metrics(data):
    """Display model training metrics and evaluation results."""
    st.header("🎯 Model Performance Metrics")
    
    # Prepare features for model training
    feature_columns = [col for col in data.columns 
                      if (col.endswith('_encoded') or 
                          pd.api.types.is_numeric_dtype(data[col])) and 
                          col not in ['time_taken(min)', 'Order_Date', 'Time_Orderd']]
    
    X = data[feature_columns]
    y = data['time_taken(min)']
    
    # Compare models
    with st.spinner("Training and evaluating models..."):
        evaluator = ModelEvaluator()
        results = evaluator.evaluate_models(X, y)
        
        # Get best model
        best_model_name, best_score = evaluator.get_best_model(metric='r2')
        
        # Print results to console
        print_model_results(results, best_model_name, best_score)
        
        # Display results in expandable section
        with st.expander("📊 Model Comparison Results", expanded=True):
            st.subheader("Model Performance Comparison")
            
            # Create a table for all metrics
            metrics_data = []
            for model_name, metrics in results.items():
                metrics_data.append({
                    'Model': model_name,
                    'R²': f"{metrics['r2']:.4f}",
                    'MSE': f"{metrics['mse']:.2f}",
                    'RMSE': f"{metrics['rmse']:.2f}",
                    'MAE': f"{metrics['mae']:.2f}",
                    'MAPE': f"{metrics['mape']:.2f}%"
                })
            
            metrics_df = pd.DataFrame(metrics_data)
            st.dataframe(
                metrics_df.style.highlight_max(subset=['R²'], axis=0)
                                 .highlight_min(subset=['MSE', 'RMSE', 'MAE', 'MAPE'], axis=0),
                hide_index=True,
                use_container_width=True
            )
            
            # Display best model banner
            st.success(f"🏆 Best Model: {best_model_name} (R² Score: {best_score:.4f})")
            
            # Add metric explanations
            with st.expander("ℹ️ Metric Explanations"):
                st.markdown("""
                - **R²** (R-squared): Indicates how well the model fits the data (higher is better, max 1.0)
                - **MSE** (Mean Squared Error): Average squared difference between predictions and actual values (lower is better)
                - **RMSE** (Root Mean Square Error): Square root of MSE, in same units as target variable (lower is better)
                - **MAE** (Mean Absolute Error): Average absolute difference between predictions and actual values (lower is better)
                - **MAPE** (Mean Absolute Percentage Error): Average percentage difference between predictions and actual values (lower is better)
                """)

def display_peak_demand_forecast(data):
    """Display peak demand predictions."""
    st.header("📈 Peak Demand Forecast")
    
    with st.spinner("Generating peak demand forecast..."):
        peak_model = PeakDemandModel()
        peak_model.train(data)
        prediction = peak_model.predict_next_day()
        
        # Print predictions to console
        print_peak_demand_forecast(prediction)
        
        # Display predictions in dashboard
        col1, col2, col3 = st.columns(3)
        
        with col1:
            st.metric("Total Orders Expected", f"{prediction['total_orders']:.0f}")
        
        with col2:
            st.metric("Peak Hours Count", len(prediction['peak_hours']))
        
        with col3:
            st.metric("Avg Orders per Hour", f"{prediction['total_orders']/24:.1f}")
        
        # Plot hourly predictions
        fig = px.line(
            x=list(range(24)),
            y=prediction['hourly_predictions'],
            title="Hourly Order Predictions for Next Day",
            labels={'x': 'Hour of Day', 'y': 'Predicted Orders'}
        )
        st.plotly_chart(fig, use_container_width=True)
        
        # Display peak hours
        peak_hours_str = [f"{hour:02d}:00-{(hour+1):02d}:00" for hour in prediction['peak_hours']]
        st.info("🔥 Expected peak hours: " + ", ".join(peak_hours_str))