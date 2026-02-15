import streamlit as st
import pandas as pd
import numpy as np
import random
import requests
from bs4 import BeautifulSoup
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
# Data Mode Toggle
# ---------------------------------------------------

mode = st.sidebar.radio(
    "Select Data Mode",
    ["Simulated Data", "Real Scraped Data"]
)

# ---------------------------------------------------
# Real Scraping Function
# ---------------------------------------------------

@st.cache_data
def scrape_real_jobs():
    URL = "https://realpython.github.io/fake-jobs/"
    headers = {"User-Agent": "Mozilla/5.0"}

    response = requests.get(URL, headers=headers)
    soup = BeautifulSoup(response.text, "lxml")

    jobs = soup.find_all("div", class_="card-content")

    job_data = []

    for job in jobs:
        title = job.find("h2", class_="title").text.strip()
        company = job.find("h3", class_="company").text.strip()
        location = job.find("p", class_="location").text.strip()
        posted = job.find("time")["datetime"]

        job_data.append([posted, title, company, location])

    df = pd.DataFrame(
        job_data,
        columns=["Posted", "Title", "Company", "Location"]
    )

    df["Posted"] = pd.to_datetime(df["Posted"])

    # Add category classification
    def categorize(title):
        title = title.lower()
        if "engineer" in title:
            return "Engineering"
        elif "developer" in title:
            return "Development"
        elif "data" in title:
            return "Data"
        elif "manager" in title:
            return "Management"
        else:
            return "Other"

    df["Category"] = df["Title"].apply(categorize)

    return df

# ---------------------------------------------------
# Simulated Data Function
# ---------------------------------------------------

@st.cache_data
def generate_simulated_data():
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

# ---------------------------------------------------
# Load Data Based on Mode
# ---------------------------------------------------

if mode == "Real Scraped Data":
    df = scrape_real_jobs()
else:
    df = generate_simulated_data()

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
# Monthly Trend (if time exists)
# ---------------------------------------------------

if "Posted" in filtered_df.columns:
    monthly = filtered_df.groupby(
        filtered_df["Posted"].dt.to_period("M")
    ).size()

    monthly.index = monthly.index.astype(str)

    st.subheader("📈 Monthly Hiring Trend")
    st.line_chart(monthly)

# ---------------------------------------------------
# Category Distribution
# ---------------------------------------------------

st.subheader("📊 Job Category Distribution")
category_counts = filtered_df["Category"].value_counts()
st.bar_chart(category_counts)

# ---------------------------------------------------
# Download Button
# ---------------------------------------------------

st.subheader("⬇ Download Data")

csv = filtered_df.to_csv(index=False)

st.download_button(
    label="Download CSV",
    data=csv,
    file_name="job_data.csv",
    mime="text/csv",
)

st.caption("Built with Streamlit | Real + Simulated Hiring Analytics")
