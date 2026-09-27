import pandas as pd

from sklearn.model_selection import train_test_split
from sklearn.compose import ColumnTransformer
from sklearn.preprocessing import OneHotEncoder
from sklearn.linear_model import LogisticRegression
from sklearn.metrics import accuracy_score, classification_report


# Load dataset
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


# Features
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


# Split data
X_train, X_test, y_train, y_test = train_test_split(
    X,
    y,
    test_size=0.20,
    random_state=42,
    stratify=y
)


# Categorical features
categorical_features = [
    "OP_UNIQUE_CARRIER",
    "ORIGIN",
    "DEST"
]


# Numerical features
numerical_features = [
    "CRS_ARR_TIME",
    "CRS_ELAPSED_TIME",
    "DISTANCE",
    "MONTH",
    "DAY_OF_WEEK",
    "DEP_HOUR"
]


# Encoding
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


# Encode training and testing data
X_train_encoded = preprocessor.fit_transform(X_train)
X_test_encoded = preprocessor.transform(X_test)


print("========== MODEL TRAINING ==========")

print("\nTraining encoded data:")
print(X_train_encoded.shape)

print("\nTesting encoded data:")
print(X_test_encoded.shape)


# Create model
model = LogisticRegression(
    max_iter=1000,
    class_weight="balanced"
)


# Train model
print("\nTraining the model...")

model.fit(X_train_encoded, y_train)

print("Model training completed!")


# Make predictions
y_pred = model.predict(X_test_encoded)


# Accuracy
accuracy = accuracy_score(y_test, y_pred)

print("\n========== MODEL RESULTS ==========")

print("\nAccuracy:")
print(f"{accuracy:.4f}")


# Detailed results
print("\nClassification Report:")
print(classification_report(y_test, y_pred))