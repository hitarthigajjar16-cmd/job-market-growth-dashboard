# analytics.py

import streamlit as st
import pandas as pd
import numpy as np

from sklearn.linear_model import LinearRegression
from sklearn.metrics import mean_absolute_error, mean_squared_error


def prepare_time_series(monthly_series):
    """
    Convert time series to supervised learning format
    X = time index
    y = job counts
    """
    X = np.arange(len(monthly_series)).reshape(-1, 1)
    y = monthly_series.values
    return X, y


def train_test_split_ts(X, y, test_size=0.2):
    split_index = int(len(X) * (1 - test_size))
    return (
        X[:split_index],
        X[split_index:],
        y[:split_index],
        y[split_index:]
    )


def train_linear_model(X_train, y_train):
    model = LinearRegression()
    model.fit(X_train, y_train)
    return model


def evaluate_model(model, X_test, y_test):
    predictions = model.predict(X_test)

    mae = mean_absolute_error(y_test, predictions)

    # RMSE manually (version-safe)
    mse = mean_squared_error(y_test, predictions)
    rmse = np.sqrt(mse)

    return round(mae, 2), round(rmse, 2)



def forecast_future(model, last_index, periods):
    future_X = np.arange(
        last_index + 1,
        last_index + periods + 1
    ).reshape(-1, 1)

    return model.predict(future_X)


# -----------------------------
# Naive Baseline Model
# -----------------------------

def naive_forecast(y_train, y_test):
    """
    Predict all future values as the last observed training value
    """
    last_value = y_train[-1]
    predictions = [last_value] * len(y_test)
    return predictions


def evaluate_naive(y_train, y_test):
    predictions = naive_forecast(y_train, y_test)

    mae = mean_absolute_error(y_test, predictions)

    mse = mean_squared_error(y_test, predictions)
    rmse = np.sqrt(mse)

    return round(mae, 2), round(rmse, 2)
