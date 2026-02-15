# analytics.py

import numpy as np


def calculate_growth(monthly_series):
    if len(monthly_series) < 2:
        return None

    growth = (
        (monthly_series.iloc[-1] - monthly_series.iloc[-2])
        / monthly_series.iloc[-2]
    ) * 100

    return round(growth, 2)


def forecast_linear(monthly_series, future_months=6):
    x = np.arange(len(monthly_series))
    y = monthly_series.values

    coef = np.polyfit(x, y, 1)
    trend = np.poly1d(coef)

    future_x = np.arange(len(x) + future_months)
    forecast_values = trend(future_x)

    return forecast_values
