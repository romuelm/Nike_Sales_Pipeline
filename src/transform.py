import pandas as pd
import numpy as np


def transform_data(df):

    # Region Cleaning

    df["Region"] = (
        df["Region"]
        .astype(str)
        .str.title()
        .str.strip()
    )

    region_mapping = {
        "Hyd": "Hyderabad",
        "Hyderbad": "Hyderabad",
        "Bengaluru": "Bangalore"
    }

    df["Region"] = df["Region"].replace(region_mapping)

    # Date Cleaning

    df["Order_Date"] = pd.to_datetime(
        df["Order_Date"],
        format="mixed",
        errors="coerce"
    )

    df = df.dropna(subset=["Order_Date"])

    # Duplicate Removal

    df = df.drop_duplicates(
        subset="Order_ID",
        keep="first"
    )

    # Transaction Type

    df["Transaction_Type"] = np.where(
        df["Units_Sold"] < 0,
        "Return",
        "Sale"
    )

    df["Units_Sold"] = df["Units_Sold"].abs()

    # MRP Cleaning

    df["MRP"] = df["MRP"].abs()

    df["MRP"] = df.groupby(
        "Product_Name"
    )["MRP"].transform(
        lambda x: x.fillna(x.median())
    )

    df["MRP"] = df.groupby(
        "Product_Line"
    )["MRP"].transform(
        lambda x: x.fillna(x.median())
    )

    df["MRP"] = df["MRP"].fillna(
        df["MRP"].median()
    )

    # Discount

    df["Discount_Applied"] = (
        df["Discount_Applied"]
        .fillna(0)
        .clip(0, 1)
    )

    # Units Sold

    df["Units_Sold"] = df.groupby(
        "Product_Line"
    )["Units_Sold"].transform(
        lambda x: x.fillna(x.median())
    )

    df["Units_Sold"] = df["Units_Sold"].fillna(
        df["Units_Sold"].median()
    )

    df["Units_Sold"] = (
        df["Units_Sold"]
        .round()
        .astype(int)
    )

    # Remove Zero Sales

    df = df[df["Units_Sold"] > 0]

    # Size

    df["Size"] = (
        df["Size"]
        .astype(str)
        .str.upper()
        .str.strip()
    )

    df["Size"] = df["Size"].replace(
        ["NAN", "NONE", "ERROR", "UNKNOWN", ""],
        np.nan
    )

    # Revenue

    df["Revenue"] = (
        df["MRP"]
        * df["Units_Sold"]
        * (1 - df["Discount_Applied"])
    ).round(2)

    # Profit

    df["Profit"] = df["Profit"].fillna(
        df["Profit"].median()
    )

    df["Profit_Flag"] = np.where(
        df["Profit"] > df["Revenue"],
        "Review",
        "Valid"
    )

    # Quality Checks

    assert (df["MRP"] > 0).all()

    assert (df["Units_Sold"] > 0).all()

    assert (
        (df["Discount_Applied"] >= 0)
        &
        (df["Discount_Applied"] <= 1)
    ).all()

    print("Quality checks passed.")

    return df