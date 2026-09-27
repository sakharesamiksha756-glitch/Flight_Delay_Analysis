import pandas as pd

from sklearn.model_selection import train_test_split
from sklearn.compose import ColumnTransformer
from sklearn.preprocessing import OneHotEncoder
from sklearn.ensemble import RandomForestClassifier


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
# 4. DATE FEATURES
# =========================================================

df["FL_DATE"] = pd.to_datetime(df["FL_DATE"])

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
# 5. FEATURES
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
# 6. TRAIN-TEST SPLIT
# =========================================================

X_train, X_test, y_train, y_test = train_test_split(
    X,
    y,
    test_size=0.20,
    random_state=42,
    stratify=y
)


# =========================================================
# 7. CATEGORICAL FEATURES
# =========================================================

categorical_features = [
    "OP_UNIQUE_CARRIER",
    "ORIGIN",
    "DEST"
]


# =========================================================
# 8. ENCODING
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
# 9. ENCODE DATA
# =========================================================

X_train_encoded = preprocessor.fit_transform(X_train)


# =========================================================
# 10. TRAIN RANDOM FOREST
# =========================================================

print("========== FEATURE IMPORTANCE ==========")

print("\nTraining Random Forest...")

model = RandomForestClassifier(
    n_estimators=100,
    max_depth=15,
    min_samples_split=10,
    random_state=42,
    n_jobs=-1,
    class_weight="balanced"
)

model.fit(
    X_train_encoded,
    y_train
)

print("Model training completed!")


# =========================================================
# 11. GET FEATURE NAMES
# =========================================================

feature_names = preprocessor.get_feature_names_out()


# =========================================================
# 12. FEATURE IMPORTANCE
# =========================================================

importance = model.feature_importances_


importance_df = pd.DataFrame({
    "FEATURE": feature_names,
    "IMPORTANCE": importance
})


# Sort from highest to lowest
importance_df = importance_df.sort_values(
    by="IMPORTANCE",
    ascending=False
)


# =========================================================
# 13. DISPLAY TOP 20
# =========================================================

print("\n========== TOP 20 FEATURES ==========")

print(
    importance_df.head(20).to_string(index=False)
)