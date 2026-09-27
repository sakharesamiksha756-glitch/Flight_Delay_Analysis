import pandas as pd

from sklearn.model_selection import train_test_split
from sklearn.compose import ColumnTransformer
from sklearn.preprocessing import OneHotEncoder
from sklearn.linear_model import LogisticRegression
from sklearn.metrics import confusion_matrix, accuracy_score


# =========================================================
# 1. LOAD DATASET
# =========================================================

df = pd.read_csv("data/T_ONTIME_REPORTING.csv")


# =========================================================
# 2. KEEP NORMAL OPERATED FLIGHTS
# =========================================================

df = df[
    (df["CANCELLED"] == 0) &
    (df["DIVERTED"] == 0) &
    (df["ARR_DELAY"].notna())
].copy()


# =========================================================
# 3. CREATE TARGET
# =========================================================

# 1 = Arrival delay of 15 minutes or more
# 0 = Arrival delay less than 15 minutes

df["IS_DELAYED"] = (
    df["ARR_DELAY"] >= 15
).astype(int)


# =========================================================
# 4. CONVERT DATE
# =========================================================

df["FL_DATE"] = pd.to_datetime(df["FL_DATE"])


# =========================================================
# 5. CREATE TIME FEATURES
# =========================================================

df["MONTH"] = df["FL_DATE"].dt.month

df["DAY_OF_WEEK"] = df["FL_DATE"].dt.dayofweek


# Convert scheduled departure time into hour

df["DEP_HOUR"] = (
    df["CRS_DEP_TIME"]
    .astype(int)
    .astype(str)
    .str.zfill(4)
    .str[:2]
    .astype(int)
)


# =========================================================
# 6. SELECT FEATURES
# =========================================================

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


# =========================================================
# 7. TRAIN-TEST SPLIT
# =========================================================

X_train, X_test, y_train, y_test = train_test_split(
    X,
    y,
    test_size=0.20,
    random_state=42,
    stratify=y
)


# =========================================================
# 8. DEFINE CATEGORICAL FEATURES
# =========================================================

categorical_features = [
    "OP_UNIQUE_CARRIER",
    "ORIGIN",
    "DEST"
]


# =========================================================
# 9. ENCODE CATEGORICAL FEATURES
# =========================================================

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


# =========================================================
# 10. ENCODE TRAINING AND TESTING DATA
# =========================================================

X_train_encoded = preprocessor.fit_transform(X_train)

X_test_encoded = preprocessor.transform(X_test)


print("========== MODEL EVALUATION ==========")

print("\nTraining encoded data:")
print(X_train_encoded.shape)

print("\nTesting encoded data:")
print(X_test_encoded.shape)


# =========================================================
# 11. CREATE LOGISTIC REGRESSION MODEL
# =========================================================

model = LogisticRegression(
    max_iter=2000,
    class_weight="balanced"
)


# =========================================================
# 12. TRAIN MODEL
# =========================================================

print("\nTraining the model...")

model.fit(
    X_train_encoded,
    y_train
)

print("Model training completed!")


# =========================================================
# 13. MAKE PREDICTIONS
# =========================================================

y_pred = model.predict(X_test_encoded)


# =========================================================
# 14. CREATE CONFUSION MATRIX
# =========================================================

cm = confusion_matrix(
    y_test,
    y_pred
)


print("\n========== CONFUSION MATRIX ==========")

print(cm)


print("\nMatrix format:")

print(
    "[[True Negative, False Positive],"
)

print(
    " [False Negative, True Positive]]"
)


# =========================================================
# 15. CALCULATE ACCURACY
# =========================================================

accuracy = accuracy_score(
    y_test,
    y_pred
)


print("\nAccuracy:")

print(
    f"{accuracy:.4f}"
)