import pandas as pd
from sklearn.model_selection import train_test_split
from sklearn.compose import ColumnTransformer
from sklearn.preprocessing import OneHotEncoder

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

# Create time features
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

# Split the data
X_train, X_test, y_train, y_test = train_test_split(
    X,
    y,
    test_size=0.20,
    random_state=42,
    stratify=y
)

# Categorical columns
categorical_features = [
    "OP_UNIQUE_CARRIER",
    "ORIGIN",
    "DEST"
]

# Numerical columns
numerical_features = [
    "CRS_ARR_TIME",
    "CRS_ELAPSED_TIME",
    "DISTANCE",
    "MONTH",
    "DAY_OF_WEEK",
    "DEP_HOUR"
]

# Create encoder
preprocessor = ColumnTransformer(
    transformers=[
        (
            "categorical",
            OneHotEncoder(handle_unknown="ignore"),
            categorical_features
        )
    ],
    remainder="passthrough"
)

# Fit encoder only on training data
X_train_encoded = preprocessor.fit_transform(X_train)

# Transform testing data
X_test_encoded = preprocessor.transform(X_test)

print("========== FEATURE ENCODING ==========")

print("\nOriginal training shape:")
print(X_train.shape)

print("\nEncoded training shape:")
print(X_train_encoded.shape)

print("\nOriginal testing shape:")
print(X_test.shape)

print("\nEncoded testing shape:")
print(X_test_encoded.shape)