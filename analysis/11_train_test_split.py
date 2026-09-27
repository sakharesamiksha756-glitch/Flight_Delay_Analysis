import pandas as pd
from sklearn.model_selection import train_test_split

# Load the original dataset
df = pd.read_csv("data/T_ONTIME_REPORTING.csv")

# Keep normal operated flights
df = df[
    (df["CANCELLED"] == 0) &
    (df["DIVERTED"] == 0) &
    (df["ARR_DELAY"].notna())
].copy()

# Create target
df["IS_DELAYED"] = (
    df["ARR_DELAY"] >= 15
).astype(int)

# Convert date
df["FL_DATE"] = pd.to_datetime(df["FL_DATE"])

# Create features
df["MONTH"] = df["FL_DATE"].dt.month
df["DAY_OF_WEEK"] = df["FL_DATE"].dt.dayofweek

df["DEP_HOUR"] = (
    df["CRS_DEP_TIME"]
    .astype(int)
    .astype(str)
    .str.zfill(4)
    .str[:2]
    .astype(int)
)

# Select features
features = [
    "OP_UNIQUE_CARRIER",
    "ORIGIN",
    "DEST",
    "CRS_ARR_TIME",
    "CRS_ELAPSED_TIME",
    "DISTANCE",
    "MONTH",
    "DAY_OF_WEEK",
    "DEP_HOUR"
]

X = df[features]
y = df["IS_DELAYED"]

# Split into training and testing data
X_train, X_test, y_train, y_test = train_test_split(
    X,
    y,
    test_size=0.20,
    random_state=42,
    stratify=y
)

print("========== TRAIN TEST SPLIT ==========")

print("\nTraining data:")
print(X_train.shape)

print("\nTesting data:")
print(X_test.shape)

print("\nTraining target distribution:")
print(y_train.value_counts())

print("\nTesting target distribution:")
print(y_test.value_counts())