"""Model training and evaluation metrics display."""
import streamlit as st
import pandas as pd
import plotly.express as px
from src.models.model_evaluator import ModelEvaluator
from src.models.peak_demand_model import PeakDemandModel

def display_model_metrics(data):
    """Display model training metrics and evaluation results."""
    st.header("🎯 Model Performance Comparison")
    
    # Prepare features
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
        best_model_name, best_score = evaluator.get_best_model(metric='r2')
        
        # Create metrics table
        metrics_df = pd.DataFrame([
            {
                'Model': name,
                'R² Score': f"{metrics['r2']:.4f}",
                'Mean Absolute Error': f"{metrics['mae']:.2f}",
                'Root Mean Square Error': f"{metrics['rmse']:.2f}",
                'Mean Absolute % Error': f"{metrics['mape']:.2f}%"
            }
            for name, metrics in results.items()
        ])
        
        # Display best model banner
        st.success(f"🏆 Best Model: {best_model_name} (R² Score: {best_score:.4f})")
        
        # Display metrics table
        st.dataframe(
            metrics_df.style.highlight_max(subset=['R² Score'], axis=0)
                           .highlight_min(subset=['Mean Absolute Error', 'Root Mean Square Error', 'Mean Absolute % Error'], axis=0),
            hide_index=True,
            use_container_width=True
        )
        
        # Detailed metrics visualization
        with st.expander("📊 Detailed Model Metrics", expanded=True):
            # R² Score comparison
            fig_r2 = px.bar(
                metrics_df,
                x='Model',
                y='R² Score',
                title='Model R² Score Comparison',
                color='Model'
            )
            st.plotly_chart(fig_r2, use_container_width=True)
            
            # Error metrics comparison
            error_metrics = pd.melt(
                metrics_df,
                id_vars=['Model'],
                value_vars=['Mean Absolute Error', 'Root Mean Square Error'],
                var_name='Metric',
                value_name='Value'
            )
            fig_errors = px.bar(
                error_metrics,
                x='Model',
                y='Value',
                color='Metric',
                barmode='group',
                title='Model Error Metrics Comparison'
            )
            st.plotly_chart(fig_errors, use_container_width=True)

def display_peak_demand_forecast(data):
    """Display peak demand predictions."""
    st.header("📈 Peak Demand Forecast")
    
    with st.spinner("Generating peak demand forecast..."):
        peak_model = PeakDemandModel()
        peak_model.train(data)
        prediction = peak_model.predict_next_day()
        
        col1, col2, col3 = st.columns(3)
        with col1:
            st.metric("📦 Total Orders Expected", f"{prediction['total_orders']:.0f}")
        with col2:
            st.metric("⏰ Peak Hours", len(prediction['peak_hours']))
        with col3:
            st.metric("📊 Avg Orders/Hour", f"{prediction['total_orders']/24:.1f}")
        
        # Hourly predictions chart
        hourly_data = pd.DataFrame({
            'Hour': range(24),
            'Predicted Orders': prediction['hourly_predictions']
        })
        
        fig = px.line(
            hourly_data,
            x='Hour',
            y='Predicted Orders',
            title="Hourly Order Predictions",
            markers=True
        )
        fig.add_hline(
            y=hourly_data['Predicted Orders'].mean(),
            line_dash="dash",
            line_color="red",
            annotation_text="Average"
        )
        st.plotly_chart(fig, use_container_width=True)
        
        # Peak hours
        peak_hours_str = [f"{hour:02d}:00-{(hour+1):02d}:00" for hour in prediction['peak_hours']]
        st.info("🔥 Peak Hours: " + ", ".join(peak_hours_str))