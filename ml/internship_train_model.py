import os
from pathlib import Path

import joblib
import pandas as pd

from sklearn.ensemble import RandomForestRegressor


# =========================================================
# PATH
# =========================================================

BASE_DIR = Path(__file__).resolve().parent.parent

MODEL_PATH = (
    BASE_DIR
    / "ml"
    / "internship_model.pkl"
)


# =========================================================
# FEATURES
# =========================================================

FEATURES = [
    "python",
    "java",
    "sql",
    "machine_learning",
    "data_science",
    "javascript",
    "aws",
    "azure",
    "power_bi",
    "excel"
]


# =========================================================
# TRAINING DATA
#
# This is a demo/initial internship dataset.
# Later real internship data can replace it.
# =========================================================

DATA = [

    # Python internships
    [1, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0.90],
    [1, 0, 1, 0, 0, 0, 0, 0, 0, 0, 0.95],
    [1, 0, 0, 0, 0, 1, 0, 0, 0, 0, 0.85],

    # Java internships
    [0, 1, 0, 0, 0, 0, 0, 0, 0, 0, 0.90],
    [0, 1, 1, 0, 0, 0, 0, 0, 0, 0, 0.95],

    # Data Science
    [1, 0, 1, 0, 1, 0, 0, 0, 0, 1, 0.98],
    [1, 0, 1, 1, 1, 0, 0, 0, 0, 0, 1.00],
    [0, 0, 1, 0, 1, 0, 0, 0, 1, 1, 0.92],

    # Machine Learning
    [1, 0, 1, 1, 1, 0, 0, 0, 0, 0, 1.00],
    [1, 0, 0, 1, 1, 0, 0, 0, 0, 0, 0.95],

    # Web Development
    [1, 0, 0, 0, 0, 1, 0, 0, 0, 0, 0.90],
    [1, 0, 0, 0, 0, 1, 1, 0, 0, 0, 0.95],

    # Cloud
    [1, 0, 0, 0, 0, 0, 1, 1, 0, 0, 0.98],
    [0, 0, 1, 0, 0, 0, 1, 1, 0, 0, 0.92],

    # Data Analytics
    [0, 0, 1, 0, 1, 0, 0, 0, 1, 1, 0.98],
    [0, 0, 1, 0, 0, 0, 0, 0, 1, 1, 0.90],

    # General combinations
    [1, 1, 0, 0, 0, 0, 0, 0, 0, 0, 0.75],
    [1, 0, 1, 1, 0, 0, 0, 0, 0, 0, 0.90],
    [0, 1, 1, 0, 0, 0, 0, 0, 0, 0, 0.85],
    [1, 0, 0, 0, 1, 1, 0, 0, 0, 0, 0.88],
    [0, 0, 1, 0, 1, 0, 0, 0, 0, 1, 0.90],
    [1, 0, 0, 1, 0, 0, 1, 0, 0, 0, 0.92],
    [0, 1, 0, 0, 0, 1, 0, 0, 0, 0, 0.82],
    [0, 0, 1, 1, 1, 0, 1, 0, 0, 0, 0.98],

]


# =========================================================
# CREATE DATAFRAME
# =========================================================

columns = FEATURES + ["skill_match"]

df = pd.DataFrame(
    DATA,
    columns=columns
)


# =========================================================
# FEATURES / TARGET
# =========================================================

X = df[FEATURES]

y = df["skill_match"]


# =========================================================
# MODEL
# =========================================================

model = RandomForestRegressor(
    n_estimators=200,
    random_state=42,
    min_samples_leaf=1
)


print()
print("=" * 50)
print("INTERNSHIP ML MODEL TRAINING")
print("=" * 50)

print(
    f"Training records: {len(df)}"
)

print(
    f"Features: {len(FEATURES)}"
)


# =========================================================
# TRAIN
# =========================================================

model.fit(
    X,
    y
)


# =========================================================
# SAVE
# =========================================================

joblib.dump(
    model,
    MODEL_PATH
)


print()
print("✅ Internship model trained successfully!")

print(
    f"✅ Model saved at:"
)

print(
    MODEL_PATH
)

print()
print("🎉 Internship ML training completed!")
