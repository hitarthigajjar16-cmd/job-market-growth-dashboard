# features.py

def add_time_features(df):
    df["Year"] = df["Posted"].dt.year
    df["Month"] = df["Posted"].dt.month
    df["Quarter"] = df["Posted"].dt.quarter
    return df


def compute_monthly_volume(df):
    monthly = df.groupby(
        df["Posted"].dt.to_period("M")
    ).size()

    monthly.index = monthly.index.astype(str)
    return monthly


def compute_salary_stats(df):
    return df.groupby("Category")["Salary"].mean().round(0)
