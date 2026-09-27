import pandas as pd
import joblib

from sklearn.model_selection import train_test_split
from sklearn.compose import ColumnTransformer
from sklearn.preprocessing import OneHotEncoder
from sklearn.pipeline import Pipeline
from sklearn.ensemble import RandomForestClassifier


# ============================================================
# 1. LOAD DATA
# ============================================================

file_path = "data/T_ONTIME_REPORTING.csv"

df = pd.read_csv(file_path)

print("Original dataset shape:", df.shape)


# ============================================================
# 2. KEEP NORMAL OPERATED FLIGHTS
# ============================================================

df = df[
    (df["CANCELLED"] == 0) &
    (df["DIVERTED"] == 0) &
    (df["ARR_DELAY"].notna())
].copy()

print("Operated flights:", len(df))


# ============================================================
# 3. CREATE TARGET VARIABLE
# ============================================================

df["IS_DELAYED"] = (df["ARR_DELAY"] >= 15).astype(int)


# ============================================================
# 4. CONVERT DATE
# ============================================================

df["FL_DATE"] = pd.to_datetime(
    df["FL_DATE"],
    format="mixed"
)

df["DAY_OF_WEEK"] = df["FL_DATE"].dt.dayofweek


# ============================================================
# 5. CREATE DEPARTURE HOUR
# ============================================================

df["DEP_HOUR"] = (df["CRS_DEP_TIME"] // 100).astype(int)


# ============================================================
# 6. SELECT FEATURES
# ============================================================

features = [
    "OP_UNIQUE_CARRIER",
    "ORIGIN",
    "DEST",
    "CRS_ARR_TIME",
    "CRS_ELAPSED_TIME",
    "DISTANCE",
    "DAY_OF_WEEK",
    "DEP_HOUR"
]

X = df[features]
y = df["IS_DELAYED"]


# ============================================================
# 7. TRAIN-TEST SPLIT
# ============================================================

X_train, X_test, y_train, y_test = train_test_split(
    X,
    y,
    test_size=0.20,
    random_state=42,
    stratify=y
)

print("Training data:", X_train.shape)
print("Testing data:", X_test.shape)


# ============================================================
# 8. DEFINE FEATURES
# ============================================================

categorical_features = [
    "OP_UNIQUE_CARRIER",
    "ORIGIN",
    "DEST"
]

numerical_features = [
    "CRS_ARR_TIME",
    "CRS_ELAPSED_TIME",
    "DISTANCE",
    "DAY_OF_WEEK",
    "DEP_HOUR"
]


# ============================================================
# 9. PREPROCESSING
# ============================================================

preprocessor = ColumnTransformer(
    transformers=[
        (
            "categorical",
            OneHotEncoder(handle_unknown="ignore"),
            categorical_features
        ),
        (
            "numerical",
            "passthrough",
            numerical_features
        )
    ]
)


# ============================================================
# 10. RANDOM FOREST MODEL
# ============================================================

model = Pipeline(
    steps=[
        ("preprocessor", preprocessor),
        (
            "model",
            RandomForestClassifier(
                n_estimators=100,
                max_depth=15,
                min_samples_split=10,
                class_weight="balanced",
                random_state=42,
                n_jobs=-1
            )
        )
    ]
)


# ============================================================
# 11. TRAIN FINAL MODEL
# ============================================================

print("\nTraining final Random Forest model...")

model.fit(X_train, y_train)

print("Model training completed!")


# ============================================================
# 12. SAVE MODEL
# ============================================================

model_path = "analysis/flight_delay_random_forest.pkl"

joblib.dump(model, model_path)

print("\nModel saved successfully!")
print("Saved model:", model_path)


# ============================================================
# 13. END
# ============================================================

print("\n")
print("=" * 60)
print("FINAL MODEL SAVED SUCCESSFULLY!")
print("=" * 60)