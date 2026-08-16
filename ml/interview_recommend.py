from pathlib import Path

import pandas as pd
import joblib

from sklearn.model_selection import train_test_split
from sklearn.compose import ColumnTransformer
from sklearn.pipeline import Pipeline
from sklearn.preprocessing import OneHotEncoder
from sklearn.impute import SimpleImputer
from sklearn.feature_extraction.text import TfidfVectorizer
from sklearn.ensemble import RandomForestRegressor
from sklearn.metrics import mean_absolute_error, r2_score


# =====================================================
# PROJECT PATHS
# =====================================================

BASE_DIR = Path(__file__).resolve().parent.parent

DATA_DIR = BASE_DIR / "data"
MODEL_PATH = BASE_DIR / "ml" / "interview_model.pkl"


# =====================================================
# FIND DATASET
# =====================================================

csv_files = list(DATA_DIR.glob("*.csv"))

if not csv_files:
    raise FileNotFoundError(
        f"No CSV dataset found inside: {DATA_DIR}"
    )


if len(csv_files) == 1:
    DATA_PATH = csv_files[0]
else:

    interview_files = [
        file
        for file in csv_files
        if "interview" in file.name.lower()
    ]

    if interview_files:
        DATA_PATH = interview_files[0]
    else:
        DATA_PATH = csv_files[0]


# =====================================================
# REQUIRED COLUMNS
# =====================================================

REQUIRED_COLUMNS = [
    "role",
    "question_type",
    "question",
    "expected_answer",
    "student_answer",
    "keyword_match",
    "answer_similarity",
    "answer_length",
    "technical_terms",
    "score"
]


# =====================================================
# LOAD AND CLEAN DATA
# =====================================================

def load_dataset():

    df = pd.read_csv(DATA_PATH)

    missing_columns = [
        column
        for column in REQUIRED_COLUMNS
        if column not in df.columns
    ]

    if missing_columns:
        raise ValueError(
            "Dataset is missing required columns: "
            + ", ".join(missing_columns)
        )

    df = df.copy()

    # -------------------------------------------------
    # TEXT COLUMNS
    # -------------------------------------------------

    text_columns = [
        "role",
        "question_type",
        "question",
        "expected_answer",
        "student_answer"
    ]

    for column in text_columns:

        df[column] = (
            df[column]
            .fillna("")
            .astype(str)
            .str.strip()
        )

    # -------------------------------------------------
    # NUMERIC COLUMNS
    # -------------------------------------------------

    numeric_columns = [
        "keyword_match",
        "answer_similarity",
        "answer_length",
        "technical_terms",
        "score"
    ]

    for column in numeric_columns:

        df[column] = pd.to_numeric(
            df[column],
            errors="coerce"
        )

    # -------------------------------------------------
    # REMOVE INVALID SCORES
    # -------------------------------------------------

    df = df.dropna(
        subset=["score"]
    )

    # -------------------------------------------------
    # LIMIT SCORE
    # -------------------------------------------------

    df["score"] = df["score"].clip(
        lower=0,
        upper=10
    )

    # -------------------------------------------------
    # REMOVE EMPTY ANSWERS
    # -------------------------------------------------

    df = df[
        df["student_answer"].str.len() > 0
    ]

    # -------------------------------------------------
    # CREATE COMBINED TEXT
    #
    # IMPORTANT:
    # This column MUST exist before feature_columns.
    # -------------------------------------------------

    df["combined_text"] = (
        df["question"]
        + " "
        + df["expected_answer"]
        + " "
        + df["student_answer"]
    )

    return df


# =====================================================
# TRAIN MODEL
# =====================================================

def train_model():

    print("\n======================================")
    print("🎤 INTERVIEW ML TRAINING")
    print("======================================")

    print("\nDataset:")
    print(DATA_PATH)

    df = load_dataset()

    print("\nRows:", len(df))
    print("Columns:", list(df.columns))

    if len(df) < 2:
        raise ValueError(
            "Dataset must contain at least 2 valid rows."
        )

    # =================================================
    # FEATURES
    # =================================================

    feature_columns = [
        "role",
        "question_type",
        "combined_text",
        "keyword_match",
        "answer_similarity",
        "answer_length",
        "technical_terms"
    ]

    X = df[feature_columns]

    y = df["score"]

    # =================================================
    # TRAIN TEST SPLIT
    # =================================================

    # For very small datasets, use all data for training.
    if len(df) < 5:

        X_train = X
        X_test = X
        y_train = y
        y_test = y

    else:

        X_train, X_test, y_train, y_test = train_test_split(
            X,
            y,
            test_size=0.20,
            random_state=42
        )

    print("\nTraining rows:", len(X_train))
    print("Testing rows:", len(X_test))

    # =================================================
    # PREPROCESSOR
    # =================================================

    preprocessor = ColumnTransformer(
        transformers=[

            # -----------------------------------------
            # ROLE
            # -----------------------------------------

            (
                "role",

                Pipeline(
                    steps=[
                        (
                            "imputer",
                            SimpleImputer(
                                strategy="most_frequent"
                            )
                        ),

                        (
                            "encoder",
                            OneHotEncoder(
                                handle_unknown="ignore"
                            )
                        )
                    ]
                ),

                ["role"]
            ),

            # -----------------------------------------
            # QUESTION TYPE
            # -----------------------------------------

            (
                "question_type",

                Pipeline(
                    steps=[
                        (
                            "imputer",
                            SimpleImputer(
                                strategy="most_frequent"
                            )
                        ),

                        (
                            "encoder",
                            OneHotEncoder(
                                handle_unknown="ignore"
                            )
                        )
                    ]
                ),

                ["question_type"]
            ),

            # -----------------------------------------
            # TEXT
            # -----------------------------------------

            (
                "text",

                TfidfVectorizer(
                    lowercase=True,
                    stop_words="english",
                    ngram_range=(1, 2),
                    max_features=3000
                ),

                "combined_text"
            ),

            # -----------------------------------------
            # NUMERIC FEATURES
            # -----------------------------------------

            (
                "numeric",

                Pipeline(
                    steps=[
                        (
                            "imputer",
                            SimpleImputer(
                                strategy="median"
                            )
                        )
                    ]
                ),

                [
                    "keyword_match",
                    "answer_similarity",
                    "answer_length",
                    "technical_terms"
                ]
            )
        ]
    )

    # =================================================
    # MODEL
    # =================================================

    model = RandomForestRegressor(
        n_estimators=300,
        max_depth=15,
        min_samples_split=2,
        min_samples_leaf=1,
        random_state=42,
        n_jobs=-1
    )

    # =================================================
    # COMPLETE PIPELINE
    # =================================================

    pipeline = Pipeline(
        steps=[
            (
                "preprocessor",
                preprocessor
            ),

            (
                "model",
                model
            )
        ]
    )

    # =================================================
    # TRAIN
    # =================================================

    print("\n🤖 Training model...")

    pipeline.fit(
        X_train,
        y_train
    )

    print("✅ Training completed!")

    # =================================================
    # TEST
    # =================================================

    predictions = pipeline.predict(
        X_test
    )

    predictions = predictions.clip(
        0,
        10
    )

    mae = mean_absolute_error(
        y_test,
        predictions
    )

    # R2 only when enough different target values exist
    try:
        r2 = r2_score(
            y_test,
            predictions
        )
    except Exception:
        r2 = 0.0

    print("\n======================================")
    print("📈 MODEL EVALUATION")
    print("======================================")

    print(
        f"MAE Score : {mae:.4f}"
    )

    print(
        f"R2 Score  : {r2:.4f}"
    )

    # =================================================
    # SAVE MODEL
    # =================================================

    joblib.dump(
        pipeline,
        MODEL_PATH
    )

    print("\n💾 Model saved:")
    print(MODEL_PATH)

    return pipeline


# =====================================================
# LOAD MODEL
# =====================================================

def get_model():

    # If model doesn't exist, train it.
    if not MODEL_PATH.exists():

        return train_model()

    try:

        return joblib.load(
            MODEL_PATH
        )

    except Exception:

        print(
            "Existing model could not be loaded."
        )

        print(
            "Training a new model..."
        )

        return train_model()


# =====================================================
# EVALUATE ANSWER
# =====================================================

def evaluate_answer(
    role,
    question_type,
    question,
    expected_answer,
    student_answer,
    keyword_match,
    answer_similarity,
    answer_length,
    technical_terms
):

    trained_model = get_model()

    # -------------------------------------------------
    # INPUT DATA
    #
    # MUST contain the exact same columns used during
    # training.
    # -------------------------------------------------

    input_data = pd.DataFrame([
        {
            "role": role,

            "question_type": question_type,

            "combined_text": (
                question
                + " "
                + expected_answer
                + " "
                + student_answer
            ),

            "keyword_match": keyword_match,

            "answer_similarity": answer_similarity,

            "answer_length": answer_length,

            "technical_terms": technical_terms
        }
    ])

    # -------------------------------------------------
    # PREDICTION
    # -------------------------------------------------

    try:

        prediction = trained_model.predict(
            input_data
        )[0]

    except Exception as error:

        print(
            "Existing model is incompatible."
        )

        print(
            "Retraining model..."
        )

        trained_model = train_model()

        prediction = trained_model.predict(
            input_data
        )[0]

    # -------------------------------------------------
    # LIMIT SCORE
    # -------------------------------------------------

    prediction = max(
        0,
        min(
            10,
            float(prediction)
        )
    )

    return round(
        prediction,
        2
    )


# =====================================================
# DO NOT TRAIN WHEN IMPORTING
# =====================================================

if __name__ == "__main__":

    train_model()
