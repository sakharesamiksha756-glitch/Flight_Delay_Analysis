import pandas as pd

from sklearn.model_selection import train_test_split
from sklearn.compose import ColumnTransformer
from sklearn.preprocessing import OneHotEncoder
from sklearn.pipeline import Pipeline
from sklearn.linear_model import LogisticRegression
from sklearn.ensemble import RandomForestClassifier
from sklearn.metrics import (
    accuracy_score,
    precision_score,
    recall_score,
    f1_score,
    roc_auc_score,
    confusion_matrix
)

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

print("\nTraining data:", X_train.shape)
print("Testing data:", X_test.shape)


# ============================================================
# 8. DEFINE CATEGORICAL AND NUMERICAL FEATURES
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
# 10. LOGISTIC REGRESSION MODEL
# ============================================================

logistic_model = Pipeline(
    steps=[
        ("preprocessor", preprocessor),
        (
            "model",
            LogisticRegression(
                solver="liblinear",
                class_weight="balanced",
                max_iter=1000,
                random_state=42
            )
        )
    ]
)


print("\nTraining Logistic Regression...")

logistic_model.fit(X_train, y_train)

print("Logistic Regression training completed!")


# ============================================================
# 11. LOGISTIC REGRESSION PREDICTIONS
# ============================================================

logistic_predictions = logistic_model.predict(X_test)

logistic_probabilities = logistic_model.predict_proba(X_test)[:, 1]


# ============================================================
# 12. RANDOM FOREST MODEL
# ============================================================

random_forest_model = Pipeline(
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


print("\nTraining Random Forest...")

random_forest_model.fit(X_train, y_train)

print("Random Forest training completed!")


# ============================================================
# 13. RANDOM FOREST PREDICTIONS
# ============================================================

rf_predictions = random_forest_model.predict(X_test)

rf_probabilities = random_forest_model.predict_proba(X_test)[:, 1]


# ============================================================
# 14. CALCULATE LOGISTIC REGRESSION METRICS
# ============================================================

logistic_accuracy = accuracy_score(
    y_test,
    logistic_predictions
)

logistic_precision = precision_score(
    y_test,
    logistic_predictions
)

logistic_recall = recall_score(
    y_test,
    logistic_predictions
)

logistic_f1 = f1_score(
    y_test,
    logistic_predictions
)

logistic_roc_auc = roc_auc_score(
    y_test,
    logistic_probabilities
)


# ============================================================
# 15. CALCULATE RANDOM FOREST METRICS
# ============================================================

rf_accuracy = accuracy_score(
    y_test,
    rf_predictions
)

rf_precision = precision_score(
    y_test,
    rf_predictions
)

rf_recall = recall_score(
    y_test,
    rf_predictions
)

rf_f1 = f1_score(
    y_test,
    rf_predictions
)

rf_roc_auc = roc_auc_score(
    y_test,
    rf_probabilities
)


# ============================================================
# 16. DISPLAY MODEL COMPARISON
# ============================================================

print("\n")
print("=" * 70)
print("              FINAL MODEL COMPARISON")
print("=" * 70)

print(
    f"{'Metric':<15}"
    f"{'Logistic Regression':>25}"
    f"{'Random Forest':>20}"
)

print("-" * 70)

print(
    f"{'Accuracy':<15}"
    f"{logistic_accuracy:>25.4f}"
    f"{rf_accuracy:>20.4f}"
)

print(
    f"{'Precision':<15}"
    f"{logistic_precision:>25.4f}"
    f"{rf_precision:>20.4f}"
)

print(
    f"{'Recall':<15}"
    f"{logistic_recall:>25.4f}"
    f"{rf_recall:>20.4f}"
)

print(
    f"{'F1 Score':<15}"
    f"{logistic_f1:>25.4f}"
    f"{rf_f1:>20.4f}"
)

print(
    f"{'ROC-AUC':<15}"
    f"{logistic_roc_auc:>25.4f}"
    f"{rf_roc_auc:>20.4f}"
)


# ============================================================
# 17. CONFUSION MATRICES
# ============================================================

print("\n")
print("=" * 70)
print("LOGISTIC REGRESSION CONFUSION MATRIX")
print("=" * 70)

print(confusion_matrix(y_test, logistic_predictions))


print("\n")
print("=" * 70)
print("RANDOM FOREST CONFUSION MATRIX")
print("=" * 70)

print(confusion_matrix(y_test, rf_predictions))


# ============================================================
# 18. END
# ============================================================

print("\n")
print("=" * 70)
print("FINAL MODEL EVALUATION COMPLETED!")
print("=" * 70)