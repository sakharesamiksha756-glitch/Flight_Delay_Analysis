import pandas as pd

# Load the original dataset
df = pd.read_csv("data/T_ONTIME_REPORTING.csv")

# Keep normal operated flights
prediction_df = df[
    (df["CANCELLED"] == 0) &
    (df["DIVERTED"] == 0) &
    (df["ARR_DELAY"].notna())
].copy()

# Create the target
prediction_df["IS_DELAYED"] = (
    prediction_df["ARR_DELAY"] >= 15
).astype(int)

# Convert flight date to datetime
prediction_df["FL_DATE"] = pd.to_datetime(
    prediction_df["FL_DATE"]
)

# Extract month
prediction_df["MONTH"] = prediction_df["FL_DATE"].dt.month

# Extract day of week
prediction_df["DAY_OF_WEEK"] = (
    prediction_df["FL_DATE"].dt.dayofweek
)

# Convert scheduled departure time to 4-digit format
prediction_df["DEP_HOUR"] = (
    prediction_df["CRS_DEP_TIME"]
    .astype(int)
    .astype(str)
    .str.zfill(4)
    .str[:2]
    .astype(int)
)

# Select final prediction features
prediction_df = prediction_df[
    [
        "OP_UNIQUE_CARRIER",
        "ORIGIN",
        "DEST",
        "CRS_ARR_TIME",
        "CRS_ELAPSED_TIME",
        "DISTANCE",
        "MONTH",
        "DAY_OF_WEEK",
        "DEP_HOUR",
        "IS_DELAYED"
    ]
]

# Display first 5 rows
print("========== FEATURE ENGINEERING ==========")
print(prediction_df.head())

# Display columns
print("\nFEATURE COLUMNS:")
print(prediction_df.columns)

# Display dataset shape
print("\nDATASET SHAPE:")
print(prediction_df.shape)