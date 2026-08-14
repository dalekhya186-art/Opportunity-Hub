from pathlib import Path

import pandas as pd
import joblib

from sklearn.ensemble import RandomForestRegressor
from sklearn.model_selection import train_test_split
from sklearn.metrics import mean_absolute_error, r2_score


# =========================================================
# PATHS
# =========================================================

BASE_DIR = Path(__file__).resolve().parent.parent

DATA_DIR = BASE_DIR / "data"

DATA_PATH = DATA_DIR / "scholarships_dataset.csv"

MODEL_PATH = (
    BASE_DIR
    / "ml"
    / "scholarship_model.pkl"
)


# =========================================================
# FEATURES
# =========================================================

FEATURES = [
    "engineering",
    "computer_science",
    "medical",
    "mba",
    "arts",
    "science",
    "government",
    "private",
    "women",
    "merit",
    "need_based",
    "international"
]


# =========================================================
# CREATE DATASET
# =========================================================

def create_dataset():

    DATA_DIR.mkdir(
        exist_ok=True
    )

    data = [

        # Engineering
        [1, 0, 0, 0, 0, 0, 1, 0, 0, 1, 0, 0, 0.90],

        [1, 0, 0, 0, 0, 0, 0, 1, 0, 1, 0, 0, 0.85],

        [1, 1, 0, 0, 0, 0, 1, 0, 0, 1, 0, 0, 0.95],

        # Computer Science
        [0, 1, 0, 0, 0, 0, 1, 0, 0, 1, 0, 0, 0.92],

        [0, 1, 0, 0, 0, 0, 0, 1, 0, 1, 0, 0, 0.86],

        [0, 1, 0, 0, 0, 0, 1, 0, 0, 0, 1, 0, 0.88],

        # Medical
        [0, 0, 1, 0, 0, 0, 1, 0, 0, 1, 0, 0, 0.93],

        [0, 0, 1, 0, 0, 0, 0, 1, 0, 1, 0, 0, 0.84],

        # MBA
        [0, 0, 0, 1, 0, 0, 1, 0, 0, 1, 0, 0, 0.91],

        [0, 0, 0, 1, 0, 0, 0, 1, 0, 1, 0, 0, 0.82],

        # Arts
        [0, 0, 0, 0, 1, 0, 1, 0, 0, 1, 0, 0, 0.89],

        [0, 0, 0, 0, 1, 0, 0, 1, 0, 1, 0, 0, 0.81],

        # Science
        [0, 0, 0, 0, 0, 1, 1, 0, 0, 1, 0, 0, 0.90],

        [0, 0, 0, 0, 0, 1, 0, 1, 0, 1, 0, 0, 0.83],

        # Women
        [1, 0, 0, 0, 0, 0, 1, 0, 1, 1, 0, 0, 0.96],

        [0, 1, 0, 0, 0, 0, 1, 0, 1, 1, 0, 0, 0.95],

        [0, 0, 1, 0, 0, 0, 1, 0, 1, 1, 0, 0, 0.94],

        # Need Based
        [1, 0, 0, 0, 0, 0, 1, 0, 0, 0, 1, 0, 0.87],

        [0, 1, 0, 0, 0, 0, 1, 0, 0, 0, 1, 0, 0.86],

        [0, 0, 1, 0, 0, 0, 1, 0, 0, 0, 1, 0, 0.88],

        # International
        [1, 1, 0, 0, 0, 0, 0, 0, 0, 1, 0, 1, 0.91],

        [0, 1, 0, 0, 0, 1, 0, 0, 0, 1, 0, 1, 0.90],

        [0, 0, 0, 1, 0, 0, 0, 0, 0, 1, 0, 1, 0.89],

        # Mixed
        [1, 1, 0, 0, 0, 0, 1, 0, 1, 1, 0, 0, 0.97],

        [0, 0, 0, 0, 0, 1, 0, 1, 1, 0, 1, 0, 0.80]
    ]


    columns = FEATURES + [
        "match_score"
    ]


    df = pd.DataFrame(
        data,
        columns=columns
    )


    df.to_csv(
        DATA_PATH,
        index=False
    )


    print(
        "✅ Scholarship dataset created:"
    )

    print(
        DATA_PATH
    )

    print(
        f"Training records: {len(df)}"
    )


    return df


# =========================================================
# LOAD / CREATE DATASET
# =========================================================

if DATA_PATH.exists():

    print(
        "✅ Scholarship dataset found."
    )

    df = pd.read_csv(
        DATA_PATH
    )

else:

    print(
        "⚠️ Scholarship dataset not found."
    )

    print(
        "Creating scholarship dataset..."
    )

    df = create_dataset()


# =========================================================
# CHECK DATA
# =========================================================

print(
    f"📊 Dataset rows: {len(df)}"
)

print(
    f"🔢 Features: {len(FEATURES)}"
)


# =========================================================
# FEATURES + TARGET
# =========================================================

X = df[FEATURES]

y = df["match_score"]


# =========================================================
# TRAIN / TEST SPLIT
# =========================================================

X_train, X_test, y_train, y_test = train_test_split(
    X,
    y,
    test_size=0.20,
    random_state=42
)


# =========================================================
# RANDOM FOREST
# =========================================================

print(
    "\n🤖 Training Scholarship Random Forest..."
)


model = RandomForestRegressor(
    n_estimators=200,
    random_state=42
)


model.fit(
    X_train,
    y_train
)


# =========================================================
# EVALUATION
# =========================================================

predictions = model.predict(
    X_test
)


mae = mean_absolute_error(
    y_test,
    predictions
)


r2 = r2_score(
    y_test,
    predictions
)


print(
    "\n=============================="
)

print(
    "SCHOLARSHIP MODEL EVALUATION"
)

print(
    "=============================="
)

print(
    f"MAE Score : {mae:.4f}"
)

print(
    f"R2 Score  : {r2:.4f}"
)


# =========================================================
# SAVE MODEL
# =========================================================

joblib.dump(
    model,
    MODEL_PATH
)


print(
    "\n✅ Scholarship model saved successfully!"
)

print(
    MODEL_PATH
)

print(
    "\n🎓 Scholarship ML training completed!"
)
