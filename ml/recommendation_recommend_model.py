from pathlib import Path
import pandas as pd
import numpy as np
import joblib

from sklearn.ensemble import RandomForestRegressor
from sklearn.model_selection import train_test_split
from sklearn.metrics import mean_absolute_error, r2_score


# =========================================================
# PROJECT PATHS
# =========================================================

BASE_DIR = Path(__file__).resolve().parent.parent

DATA_DIR = BASE_DIR / "data"
MODEL_DIR = BASE_DIR / "ml"

DATA_DIR.mkdir(exist_ok=True)
MODEL_DIR.mkdir(exist_ok=True)

DATA_PATH = DATA_DIR / "jobs_dataset.csv"
MODEL_PATH = MODEL_DIR / "recommendation_model.pkl"


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
# CREATE SAMPLE DATA
# =========================================================

def create_sample_dataset():

    data = []

    jobs = [
        ("Python Developer", "TCS"),
        ("Java Developer", "Infosys"),
        ("Data Analyst", "Deloitte"),
        ("Machine Learning Engineer", "Google"),
        ("Data Scientist", "IBM"),
        ("Web Developer", "Accenture"),
        ("Cloud Engineer", "Microsoft"),
        ("Business Analyst", "Wipro"),
        ("AI Engineer", "Tech Mahindra"),
        ("Backend Developer", "HCL"),
    ]

    for job_title, company in jobs:

        for _ in range(50):

            values = {
                skill: np.random.randint(0, 2)
                for skill in FEATURES
            }

            # Calculate an initial skill match
            match = sum(values.values()) / len(FEATURES)

            # Small random variation
            match += np.random.uniform(-0.08, 0.08)

            match = max(
                0,
                min(match, 1)
            )

            row = {
                "job_title": job_title,
                "company": company,
                **values,
                "skill_match": match
            }

            data.append(row)

    df = pd.DataFrame(data)

    df.to_csv(
        DATA_PATH,
        index=False
    )

    print(
        "✅ Dataset created:"
    )

    print(
        DATA_PATH
    )

    return df


# =========================================================
# LOAD DATASET
# =========================================================

def load_dataset():

    if not DATA_PATH.exists():

        print(
            "⚠️ jobs_dataset.csv not found."
        )

        print(
            "Creating dataset automatically..."
        )

        return create_sample_dataset()

    try:

        df = pd.read_csv(
            DATA_PATH
        )

        print(
            f"✅ Dataset loaded: {len(df)} rows"
        )

        return df

    except Exception as e:

        print(
            "⚠️ Unable to read existing CSV."
        )

        print(
            "Reason:",
            e
        )

        print(
            "Creating a fresh dataset..."
        )

        return create_sample_dataset()


# =========================================================
# PREPARE DATASET
# =========================================================

def prepare_dataset(df):

    # ---------------------------------------------
    # Add missing feature columns
    # ---------------------------------------------

    for feature in FEATURES:

        if feature not in df.columns:

            print(
                f"⚠️ Missing column: {feature}"
            )

            df[feature] = 0


    # ---------------------------------------------
    # Add target column
    # ---------------------------------------------

    if "skill_match" not in df.columns:

        print(
            "⚠️ skill_match column missing."
        )

        # Calculate a basic target
        df["skill_match"] = (
            df[FEATURES]
            .apply(
                pd.to_numeric,
                errors="coerce"
            )
            .fillna(0)
            .mean(axis=1)
        )


    # ---------------------------------------------
    # Convert feature columns to numbers
    # ---------------------------------------------

    for feature in FEATURES:

        df[feature] = pd.to_numeric(
            df[feature],
            errors="coerce"
        ).fillna(0)

        df[feature] = (
            df[feature]
            .clip(0, 1)
        )


    # ---------------------------------------------
    # Convert target
    # ---------------------------------------------

    df["skill_match"] = pd.to_numeric(
        df["skill_match"],
        errors="coerce"
    )


    df["skill_match"] = (
        df["skill_match"]
        .fillna(
            df[FEATURES].mean(axis=1)
        )
        .clip(0, 1)
    )


    # ---------------------------------------------
    # Remove invalid rows
    # ---------------------------------------------

    df = df.dropna(
        subset=FEATURES
    )


    return df


# =========================================================
# TRAIN MODEL
# =========================================================

def train_model(df):

    X = df[FEATURES]

    y = df["skill_match"]


    # ---------------------------------------------
    # Check dataset
    # ---------------------------------------------

    if len(df) < 10:

        print(
            "⚠️ Dataset too small."
        )

        print(
            "Creating additional training records..."
        )

        extra = create_sample_dataset()

        df = pd.concat(
            [df, extra],
            ignore_index=True
        )

        X = df[FEATURES]

        y = df["skill_match"]


    # ---------------------------------------------
    # Train/Test Split
    # ---------------------------------------------

    X_train, X_test, y_train, y_test = train_test_split(
        X,
        y,
        test_size=0.2,
        random_state=42
    )


    # ---------------------------------------------
    # Random Forest
    # ---------------------------------------------

    model = RandomForestRegressor(
        n_estimators=200,
        max_depth=10,
        min_samples_split=4,
        random_state=42,
        n_jobs=-1
    )


    print(
        "🤖 Training Random Forest..."
    )


    model.fit(
        X_train,
        y_train
    )


    # ---------------------------------------------
    # Prediction
    # ---------------------------------------------

    predictions = model.predict(
        X_test
    )


    predictions = np.clip(
        predictions,
        0,
        1
    )


    # ---------------------------------------------
    # Evaluation
    # ---------------------------------------------

    mae = mean_absolute_error(
        y_test,
        predictions
    )


    r2 = r2_score(
        y_test,
        predictions
    )


    print()
    print(
        "=============================="
    )

    print(
        "MODEL EVALUATION"
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


    # ---------------------------------------------
    # Save model
    # ---------------------------------------------

    joblib.dump(
        model,
        MODEL_PATH
    )


    print()
    print(
        "=============================="
    )

    print(
        "✅ MODEL SAVED SUCCESSFULLY"
    )

    print(
        "=============================="
    )

    print(
        MODEL_PATH
    )


    return model


# =========================================================
# MAIN
# =========================================================

if __name__ == "__main__":

    print()
    print(
        "======================================"
    )

    print(
        "🎓 STUDENT OPPORTUNITY HUB"
    )

    print(
        "🤖 ML RECOMMENDATION MODEL TRAINING"
    )

    print(
        "======================================"
    )

    print()


    # Load
    df = load_dataset()


    # Prepare
    df = prepare_dataset(
        df
    )


    print(
        f"Training rows: {len(df)}"
    )


    print(
        f"Features: {len(FEATURES)}"
    )


    # Train
    train_model(
        df
    )


    print()
    print(
        "🎉 Training completed!"
    )
