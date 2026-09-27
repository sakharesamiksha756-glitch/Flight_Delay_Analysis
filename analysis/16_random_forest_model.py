import pandas as pd

from sklearn.model_selection import train_test_split
from sklearn.compose import ColumnTransformer
from sklearn.preprocessing import OneHotEncoder
from sklearn.ensemble import RandomForestClassifier
from sklearn.metrics import (
    accuracy_score,
    precision_score,
    recall_score,
    f1_score,
    roc_auc_score,
    confusion_matrix
)


# =========================================================
# 1. LOAD DATA
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

df["DAY_OF_WEEK"] = df["FL_DATE"].dt.dayofweek

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
# 8. CATEGORICAL FEATURES
# =========================================================

categorical_features = [
    "OP_UNIQUE_CARRIER",
    "ORIGIN",
    "DEST"
]


# =========================================================
# 9. ENCODING
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
# 10. ENCODE DATA
# =========================================================

X_train_encoded = preprocessor.fit_transform(X_train)

X_test_encoded = preprocessor.transform(X_test)


print("========== RANDOM FOREST MODEL ==========")

print("\nTraining data:")
print(X_train_encoded.shape)

print("\nTesting data:")
print(X_test_encoded.shape)


# =========================================================
# 11. CREATE RANDOM FOREST
# =========================================================

model = RandomForestClassifier(
    n_estimators=100,
    max_depth=15,
    min_samples_split=10,
    random_state=42,
    n_jobs=-1,
    class_weight="balanced"
)


# =========================================================
# 12. TRAIN MODEL
# =========================================================

print("\nTraining Random Forest...")

model.fit(
    X_train_encoded,
    y_train
)

print("Model training completed!")


# =========================================================
# 13. MAKE PREDICTIONS
# =========================================================

y_pred = model.predict(X_test_encoded)

y_probability = model.predict_proba(
    X_test_encoded
)[:, 1]


# =========================================================
# 14. EVALUATE MODEL
# =========================================================

accuracy = accuracy_score(
    y_test,
    y_pred
)

precision = precision_score(
    y_test,
    y_pred
)

recall = recall_score(
    y_test,
    y_pred
)

f1 = f1_score(
    y_test,
    y_pred
)

roc_auc = roc_auc_score(
    y_test,
    y_probability
)

cm = confusion_matrix(
    y_test,
    y_pred
)


# =========================================================
# 15. RESULTS
# =========================================================

print("\n========== RANDOM FOREST RESULTS ==========")

print(f"\nAccuracy : {accuracy:.4f}")
print(f"Precision: {precision:.4f}")
print(f"Recall   : {recall:.4f}")
print(f"F1 Score : {f1:.4f}")
print(f"ROC-AUC  : {roc_auc:.4f}")


print("\n========== CONFUSION MATRIX ==========")

print(cm)

print("\nMatrix format:")
print("[[True Negative, False Positive],")
print(" [False Negative, True Positive]]")