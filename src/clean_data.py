import pandas as pd
from pathlib import Path

RAW_PATH = Path("data/raw/Motor_Vehicle_Collisions.csv")
OUT_PATH = Path("data/processed/collisions_cleaned.csv")
SAMPLE_PATH = Path("data/sample/collisions_sample.csv")

KEEP_COLS = [
    "CRASH DATE",
    "CRASH TIME",
    "BOROUGH",
    "LATITUDE",
    "LONGITUDE",
    "NUMBER OF PERSONS INJURED",
    "NUMBER OF PERSONS KILLED",
    "CONTRIBUTING FACTOR VEHICLE 1",
    "VEHICLE TYPE CODE 1",
]


def main():
    print("Reading raw CSV...")
    df = pd.read_csv(RAW_PATH, usecols=KEEP_COLS, low_memory=False)

    print("Cleaning data...")
    df["CRASH DATE"] = pd.to_datetime(df["CRASH DATE"], errors="coerce")

    df = df.dropna(subset=["CRASH DATE", "LATITUDE", "LONGITUDE"])

    # Keep NYC-like coordinates only
    df = df[
        (df["LATITUDE"].between(40.45, 40.95))
        & (df["LONGITUDE"].between(-74.30, -73.65))
    ]

    # Keep recent years for performance
    df = df[df["CRASH DATE"].dt.year >= 2022]

    df["YEAR"] = df["CRASH DATE"].dt.year
    df["MONTH"] = df["CRASH DATE"].dt.month
    df["MONTH_NAME"] = df["CRASH DATE"].dt.month_name()
    df["HOUR"] = pd.to_datetime(
        df["CRASH TIME"], format="%H:%M", errors="coerce"
    ).dt.hour

    df["BOROUGH"] = df["BOROUGH"].fillna("UNKNOWN")
    df["CONTRIBUTING FACTOR VEHICLE 1"] = df["CONTRIBUTING FACTOR VEHICLE 1"].fillna(
        "Unspecified"
    )
    df["VEHICLE TYPE CODE 1"] = df["VEHICLE TYPE CODE 1"].fillna("Unknown")

    OUT_PATH.parent.mkdir(parents=True, exist_ok=True)
    SAMPLE_PATH.parent.mkdir(parents=True, exist_ok=True)

    print(f"Saving cleaned data to {OUT_PATH}...")
    df.to_csv(OUT_PATH, index=False)

    print(f"Saving sample data to {SAMPLE_PATH}...")
    df.sample(min(5000, len(df)), random_state=42).to_csv(SAMPLE_PATH, index=False)

    print("Done.")
    print("Rows after cleaning:", len(df))
    print("Years:", sorted(df["YEAR"].dropna().unique()))


if __name__ == "__main__":
    main()
