import pandas as pd
import numpy as np


def clean_data(df):
    # Create a copy to avoid modifying the original DataFrame
    df_clean = df.copy()
    
    # Standardize column names
    df_clean.columns = (
        df_clean.columns.str.strip()
        .str.lower()
        .str.replace(" ", "_")
    )

    # Remove duplicate rows
    df_clean = df_clean.drop_duplicates()

    # Handle missing values
    for col in df_clean.columns:
        if df_clean[col].dtype == "object":
            df_clean[col] = df_clean[col].fillna("Unknown")
        else:
            df_clean[col] = df_clean[col].fillna(df_clean[col].median())

    # Remove outliers using IQR
    numeric_cols = df_clean.select_dtypes(include=np.number).columns

    for col in numeric_cols:
        q1 = df_clean[col].quantile(0.25)
        q3 = df_clean[col].quantile(0.75)
        iqr = q3 - q1
        df_clean = df_clean[(df_clean[col] >= q1 - 1.5 * iqr) &
                (df_clean[col] <= q3 + 1.5 * iqr)]

    return df_clean
