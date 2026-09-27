import pandas as pd

# Load the dataset
df = pd.read_csv("data/T_ONTIME_REPORTING.csv")

# Keep only flights that actually operated normally
prediction_df = df[
    (df["CANCELLED"] == 0) &
    (df["DIVERTED"] == 0) &
    (df["ARR_DELAY"].notna())
].copy()

# Create the prediction target
# 1 = delayed by 15 minutes or more
# 0 = less than 15 minutes late
prediction_df["IS_DELAYED"] = (
    prediction_df["ARR_DELAY"] >= 15
).astype(int)

# Select information available before the flight
prediction_df = prediction_df[
    [
        "FL_DATE",
        "OP_UNIQUE_CARRIER",
        "ORIGIN",
        "DEST",
        "CRS_DEP_TIME",
        "CRS_ARR_TIME",
        "CRS_ELAPSED_TIME",
        "DISTANCE",
        "IS_DELAYED"
    ]
]

# Display the first 5 rows
print("========== PREDICTION DATA ==========")
print(prediction_df.head())

# Display shape
print("\nPREDICTION DATA SHAPE:")
print(prediction_df.shape)

# Display columns
print("\nPREDICTION COLUMNS:")
print(prediction_df.columns)

# Display target distribution
print("\nTARGET DISTRIBUTION:")
print(prediction_df["IS_DELAYED"].value_counts())