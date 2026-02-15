# data_pipeline.py

import pandas as pd
import random
from config import START_DATE, PERIODS, CATEGORIES, LOCATIONS


def generate_simulated_data():
    dates = pd.date_range(start=START_DATE, periods=PERIODS, freq="M")

    data = []

    for date in dates:
        base_volume = 80 + (date.month * 3)  # upward trend

        for _ in range(random.randint(base_volume - 10, base_volume + 20)):
            data.append([
                date,
                random.choice(CATEGORIES),
                random.choice(LOCATIONS)
            ])

    df = pd.DataFrame(data, columns=["Posted", "Category", "Location"])
    return df
