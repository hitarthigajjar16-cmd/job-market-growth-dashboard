import streamlit as st
import pandas as pd
import numpy as np
from data_pipeline import generate_simulated_data
from features import add_time_features, compute_monthly_volume, compute_salary_stats
#from analytics import calculate_growth, forecast_linear
from config import FORECAST_MONTHS
from analytics import (
    prepare_time_series,
    train_test_split_ts,
    train_linear_model,
    evaluate_model,
    forecast_future,
    evaluate_naive
)

st.set_page_config(
    page_title="Job Market Growth Dashboard",
    layout="wide"
)

st.title("📊 Modular Job Market Growth Dashboard")

# Load Data
df = generate_simulated_data()
df = add_time_features(df)

# Sidebar Filters
st.sidebar.header("Filters")

selected_category = st.sidebar.multiselect(
    "Select Category",
    df["Category"].unique(),
    default=df["Category"].unique()
)

selected_location = st.sidebar.multiselect(
    "Select Location",
    df["Location"].unique(),
    default=df["Location"].unique()
)

filtered_df = df[
    (df["Category"].isin(selected_category)) &
    (df["Location"].isin(selected_location))
]

# Monthly Aggregation
monthly = compute_monthly_volume(filtered_df)

# KPIs
col1, col2, col3 = st.columns(3)

col1.metric("Total Jobs", len(filtered_df))
col2.metric("Unique Locations", filtered_df["Location"].nunique())
col3.metric("Unique Categories", filtered_df["Category"].nunique())

#growth = calculate_growth(monthly)

#if growth:
 #   st.metric("Monthly Growth %", f"{growth}%")

st.divider()

# Trend Chart
st.subheader("Monthly Hiring Trend")
st.line_chart(monthly)

# Forecast
st.subheader("🔮 ML-Based Hiring Forecast")

# Prepare data
X, y = prepare_time_series(monthly)

# Train-test split
X_train, X_test, y_train, y_test = train_test_split_ts(X, y)

# Train model
model = train_linear_model(X_train, y_train)

# Evaluate
mae, rmse = evaluate_model(model, X_test, y_test)

col1, col2 = st.columns(2)
col1.metric("MAE (Error)", mae)
col2.metric("RMSE (Error)", rmse)

# Forecast(ML evalution)
future_periods = 6
forecast_values = forecast_future(
    model,
    last_index=len(monthly) - 1,
    periods=future_periods
)

forecast_df = np.concatenate([y, forecast_values])

st.line_chart(forecast_df)

st.subheader("📉 Baseline vs ML Comparison")

naive_mae, naive_rmse = evaluate_naive(y_train, y_test)

col1, col2, col3, col4 = st.columns(4)

col1.metric("ML MAE", mae)
col2.metric("Baseline MAE", naive_mae)

col3.metric("ML RMSE", rmse)
col4.metric("Baseline RMSE", naive_rmse)
st.caption(
    "Baseline model predicts future values using the last observed value. "
    "ML model performance should be evaluated relative to this baseline."
)

