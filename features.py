# features.py

import pandas as pd


def add_time_features(df):
    df["Year"] = df["Posted"].dt.year
    df["Month"] = df["Posted"].dt.month
    df["Quarter"] = df["Posted"].dt.quarter
    return df


def add_growth_features(df):
    monthly = df.groupby(
        df["Posted"].dt.to_period("M")
    ).size()

    monthly.index = monthly.index.astype(str)
    return monthly
