import streamlit as st
import pandas as pd
import numpy as np
import random
from datetime import timedelta

# ---------------------------------------------------
# Page Config
# ---------------------------------------------------
st.set_page_config(
    page_title="Job Market Growth Dashboard",
    layout="wide"
)

st.title("📊 Job Market Growth & Forecast Dashboard")

# ---------------------------------------------------
# Generate Simulated Dataset
# ---------------------------------------------------

@st.cache_data
def generate_data():
    dates = pd.date_range(start="2022-01-01", periods=24, freq="M")
    categories = ["Engineering", "Development", "Data", "Management"]
    locations = ["New York", "California", "Texas", "Remote", "London"]

    data = []

    for date in dates:
        for _ in range(random.randint(60, 130)):
            data.append([
                date,
                random.choice(categories),
                random.choice(locations)
            ])

    df = pd.DataFrame(data, columns=["Posted", "Category", "Location"])
    return df

df = generate_data()

# ---------------------------------------------------
# Sidebar Filters
# ---------------------------------------------------

st.sidebar.header("🔎 Filters")

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

# ---------------------------------------------------
# KPI Section
# ---------------------------------------------------

col1, col2, col3 = st.columns(3)

col1.metric("Total Jobs", len(filtered_df))
col2.metric("Unique Locations", filtered_df["Location"].nunique())
col3.metric("Unique Categories", filtered_df["Category"].nunique())

st.divider()

# ---------------------------------------------------
# Monthly Hiring Trend
# ---------------------------------------------------

st.subheader("📈 Monthly Hiring Trend")

monthly = filtered_df.groupby(
    filtered_df["Posted"].dt.to_period("M")
).size()

monthly.index = monthly.index.astype(str)

st.line_chart(monthly)

# ---------------------------------------------------
# Rolling Average
# ---------------------------------------------------

st.subheader("📊 3-Month Rolling Average")

rolling = monthly.rolling(3).mean()

rolling_df = pd.DataFrame({
    "Monthly Jobs": monthly,
    "Rolling Average": rolling
})

st.line_chart(rolling_df)

# ---------------------------------------------------
# Category Distribution
# ---------------------------------------------------

st.subheader("🥧 Job Category Distribution")

category_counts = filtered_df["Category"].value_counts()

st.bar_chart(category_counts)

# ---------------------------------------------------
# Forecast Section
# ---------------------------------------------------

st.subheader("🔮 Hiring Forecast (Linear Projection)")

if len(monthly) > 1:
    x = np.arange(len(monthly))
    y = monthly.values

    coef = np.polyfit(x, y, 1)
    trend = np.poly1d(coef)

    future_months = 6
    future_x = np.arange(len(x) + future_months)
    forecast_values = trend(future_x)

    forecast_df = pd.DataFrame({
        "Forecasted Jobs": forecast_values
    })

    st.line_chart(forecast_df)

st.divider()

# ---------------------------------------------------
# Footer
# ---------------------------------------------------

st.caption("Built with Streamlit | Job Market Growth & Forecast Analysis")
