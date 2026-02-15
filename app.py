import streamlit as st
import pandas as pd

from data_pipeline import generate_simulated_data
from features import add_time_features, add_growth_features
from analytics import calculate_growth, forecast_linear
from config import FORECAST_MONTHS

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
monthly = add_growth_features(filtered_df)

# KPIs
col1, col2, col3 = st.columns(3)

col1.metric("Total Jobs", len(filtered_df))
col2.metric("Unique Locations", filtered_df["Location"].nunique())
col3.metric("Unique Categories", filtered_df["Category"].nunique())

growth = calculate_growth(monthly)

if growth:
    st.metric("Monthly Growth %", f"{growth}%")

st.divider()

# Trend Chart
st.subheader("Monthly Hiring Trend")
st.line_chart(monthly)

# Forecast
st.subheader("Forecast")

forecast_values = forecast_linear(monthly, FORECAST_MONTHS)

forecast_df = pd.DataFrame({
    "Forecasted Jobs": forecast_values
})

st.line_chart(forecast_df)
