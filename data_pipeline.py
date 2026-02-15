# data_pipeline.py

import pandas as pd
import numpy as np
import random
from config import START_DATE, PERIODS, CATEGORIES, LOCATIONS


def generate_simulated_data():
    dates = pd.date_range(start=START_DATE, periods=PERIODS, freq="M")

    data = []

    for i, date in enumerate(dates):

        # -----------------------------
        # 1. Controlled upward trend
        # -----------------------------
        base_volume = 80 + (i * 5)

        # -----------------------------
        # 2. Seasonality (more hiring in Q1 & Q4)
        # -----------------------------
        if date.month in [1, 2, 3, 10, 11]:
            seasonal_boost = 20
        else:
            seasonal_boost = -5

        total_jobs = base_volume + seasonal_boost

        for _ in range(total_jobs):

            category = weighted_category()
            experience = weighted_experience()
            location = weighted_location()
            salary = generate_salary(category, experience)
            remote = generate_remote_flag()

            data.append([
                date,
                category,
                experience,
                location,
                salary,
                remote
            ])

    df = pd.DataFrame(data, columns=[
        "Posted",
        "Category",
        "Experience",
        "Location",
        "Salary",
        "Remote"
    ])

    return df


# ---------------------------------------------------
# Weighted Category Distribution
# ---------------------------------------------------

def weighted_category():
    weights = {
        "Engineering": 0.35,
        "Development": 0.30,
        "Data": 0.20,
        "Management": 0.15
    }
    return random.choices(
        list(weights.keys()),
        weights=list(weights.values())
    )[0]


# ---------------------------------------------------
# Experience Level Bias
# ---------------------------------------------------

def weighted_experience():
    levels = ["Junior", "Mid", "Senior"]
    weights = [0.4, 0.35, 0.25]
    return random.choices(levels, weights=weights)[0]


# ---------------------------------------------------
# Location Bias (Remote heavy in Data roles)
# ---------------------------------------------------

def weighted_location():
    weights = {
        "New York": 0.20,
        "California": 0.20,
        "Texas": 0.15,
        "London": 0.15,
        "Remote": 0.30
    }
    return random.choices(
        list(weights.keys()),
        weights=list(weights.values())
    )[0]


# ---------------------------------------------------
# Salary Modeling by Category + Experience
# ---------------------------------------------------

def generate_salary(category, experience):

    base_salary = {
        "Engineering": 90000,
        "Development": 85000,
        "Data": 95000,
        "Management": 105000
    }

    experience_multiplier = {
        "Junior": 0.8,
        "Mid": 1.0,
        "Senior": 1.3
    }

    salary = base_salary[category] * experience_multiplier[experience]

    # Add controlled noise
    noise = random.randint(-8000, 8000)

    return int(salary + noise)


# ---------------------------------------------------
# Remote Probability
# ---------------------------------------------------

def generate_remote_flag():
    return random.random() < 0.4
