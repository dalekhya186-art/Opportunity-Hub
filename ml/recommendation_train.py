from pathlib import Path

import joblib
import pandas as pd


# =====================================================
# PATH
# =====================================================

BASE_DIR = Path(__file__).resolve().parent.parent

MODEL_PATH = BASE_DIR / "ml" / "recommendation_model.pkl"


# =====================================================
# FEATURES
# =====================================================

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


# =====================================================
# LOAD MODEL
# =====================================================

model = joblib.load(
    MODEL_PATH
)


# =====================================================
# FEATURE ALIASES
# =====================================================

ALIASES = {
    "python": [
        "python"
    ],

    "java": [
        "java"
    ],

    "sql": [
        "sql",
        "mysql",
        "postgresql"
    ],

    "machine_learning": [
        "machine learning",
        "ml",
        "scikit-learn",
        "sklearn"
    ],

    "data_science": [
        "data science",
        "data scientist"
    ],

    "javascript": [
        "javascript",
        "js"
    ],

    "aws": [
        "aws",
        "amazon web services"
    ],

    "azure": [
        "azure",
        "microsoft azure"
    ],

    "power_bi": [
        "power bi",
        "powerbi"
    ],

    "excel": [
        "excel",
        "microsoft excel"
    ]
}


# =====================================================
# CREATE FEATURES
# =====================================================

def create_features(
    detected_skills
):

    skills_text = " ".join(
        str(skill).lower()
        for skill in detected_skills
    )


    values = {}


    for feature in FEATURES:

        values[feature] = 0

        for alias in ALIASES[feature]:

            if alias in skills_text:

                values[feature] = 1

                break


    return pd.DataFrame(
        [values],
        columns=FEATURES
    )


# =====================================================
# PREDICT SCORE
# =====================================================

def predict_match_score(
    detected_skills
):

    features = create_features(
        detected_skills
    )


    score = model.predict(
        features
    )[0]


    score = max(
        0,
        min(
            float(score),
            1
        )
    )


    return round(
        score * 100,
        2
    )
