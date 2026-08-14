from pathlib import Path

import joblib
import pandas as pd


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
# ALIASES
# =========================================================

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
        "machinelearning",
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
        "java script",
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


# =========================================================
# LOAD MODEL
# =========================================================

if not MODEL_PATH.exists():

    raise FileNotFoundError(
        "Internship ML model not found. "
        "Run internship_train_model.py first."
    )


model = joblib.load(
    MODEL_PATH
)


# =========================================================
# CREATE FEATURES
# =========================================================

def create_features(text):

    text = str(text).lower()

    values = {}

    for feature in FEATURES:

        values[feature] = 0

        for alias in ALIASES[feature]:

            if alias in text:

                values[feature] = 1

                break

    return pd.DataFrame(
        [values],
        columns=FEATURES
    )


# =========================================================
# PREDICT INTERNSHIP MATCH
# =========================================================

def predict_internship_score(
    student_skills,
    internship_text
):

    student_text = " ".join(
        str(skill).lower()
        for skill in student_skills
    )


    internship_text = str(
        internship_text
    ).lower()


    # -----------------------------------------------------
    # Find skills present in student + internship
    # -----------------------------------------------------

    matching_skills = []


    for feature in FEATURES:

        student_has = False

        internship_has = False


        for alias in ALIASES[feature]:

            if alias in student_text:

                student_has = True


            if alias in internship_text:

                internship_has = True


        if student_has and internship_has:

            matching_skills.append(
                feature.replace(
                    "_",
                    " "
                )
            )


    # -----------------------------------------------------
    # ML prediction
    # -----------------------------------------------------

    features = create_features(
        student_text
    )


    ml_score = model.predict(
        features
    )[0]


    ml_score = max(
        0,
        min(
            float(ml_score),
            1
        )
    )


    # -----------------------------------------------------
    # Internship skill match
    # -----------------------------------------------------

    internship_features = create_features(
        internship_text
    )


    required_skills = []

    for feature in FEATURES:

        if internship_features.iloc[0][feature] == 1:

            required_skills.append(
                feature
            )


    if required_skills:

        company_match = (
            len(matching_skills)
            / len(required_skills)
        )

    else:

        company_match = 0


    company_match = max(
        0,
        min(
            company_match,
            1
        )
    )


    # -----------------------------------------------------
    # FINAL SCORE
    # -----------------------------------------------------

    final_score = (
        (ml_score * 0.5)
        +
        (company_match * 0.5)
    )


    return {

        "ml_score": round(
            ml_score * 100,
            2
        ),

        "skill_match": round(
            company_match * 100,
            2
        ),

        "final_score": round(
            final_score * 100,
            2
        ),

        "matching_skills":
            matching_skills

    }
