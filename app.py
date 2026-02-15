
import streamlit as st
import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
import random
from datetime import timedelta

st.set_page_config(page_title="Job Market Dashboard", layout="wide")

st.title("📊 Job Market Growth & Forecast Dashboard")

# Generate simulated data
dates = pd.date_range(start="2021-01-01", periods=24, freq="M")
categories = ["Engineering", "Development", "Data", "Management"]
locations = ["New York", "California", "Texas", "Remote", "London"]

data = []

for date in dates:
    for _ in range(random.randint(50, 120)):
        data.append([
            date,
            random.choice(categories),
            random.choice(locations)
        ])

df = pd.DataFrame(data, columns=["Posted", "Category", "Location"])

# KPIs
col1, col2, col3 = st.columns(3)
col1.metric("Total Jobs", len(df))
col2.metric("Unique Locations", df["Location"].nunique())
col3.metric("Unique Categories", df["Category"].nunique())

# Monthly Trend
st.subheader("📈 Monthly Hiring Trend")
monthly = df.groupby(df["Posted"].dt.to_period("M")).size()

fig = plt.figure()
plt.plot(monthly.index.astype(str), monthly.values)
plt.xticks(rotation=45)
plt.tight_layout()
st.pyplot(fig)
