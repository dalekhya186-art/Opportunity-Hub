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
# ALIASES
# =========================================================

ALIASES = {

    "engineering": [
        "engineering",
        "btech",
        "b.tech",
        "be",
        "b.e"
    ],

    "computer_science": [
        "computer science",
        "computer science engineering",
        "cse",
        "software"
    ],

    "medical": [
        "medical",
        "medicine",
        "mbbs",
        "health"
    ],

    "mba": [
        "mba",
        "management",
        "business administration"
    ],

    "arts": [
        "arts",
        "humanities"
    ],

    "science": [
        "science",
        "physics",
        "chemistry",
        "biology"
    ],

    "government": [
        "government",
        "govt"
    ],

    "private": [
        "private",
        "foundation",
        "company"
    ],

    "women": [
        "women",
        "woman",
        "female",
        "girl"
    ],

    "merit": [
        "merit",
        "academic excellence",
        "marks",
        "cgpa"
    ],

    "need_based": [
        "need based",
        "financial need",
        "low income",
        "income"
    ],

    "international": [
        "international",
        "abroad",
        "overseas"
    ]
}


# =========================================================
# LOAD MODEL
# =========================================================

if not MODEL_PATH.exists():

    raise FileNotFoundError(
        "Scholarship ML model not found. "
        "Run scholarship_train_model.py first."
    )


model = joblib.load(MODEL_PATH)


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
# PREDICT SCHOLARSHIP SCORE
# =========================================================

def predict_scholarship_score(
    student_text,
    scholarship_text
):

    student_text = str(
        student_text
    ).lower()

    scholarship_text = str(
        scholarship_text
    ).lower()


    # -----------------------------------------------------
    # STUDENT FEATURES
    # -----------------------------------------------------

    student_features = create_features(
        student_text
    )


    # -----------------------------------------------------
    # ML SCORE
    # -----------------------------------------------------

    ml_score = model.predict(
        student_features
    )[0]

    ml_score = max(
        0,
        min(
            float(ml_score),
            1
        )
    )


    # -----------------------------------------------------
    # SCHOLARSHIP MATCH
    # -----------------------------------------------------

    student_data = create_features(
        student_text
    )

    scholarship_data = create_features(
        scholarship_text
    )


    matching = []

    required = []


    for feature in FEATURES:

        student_has = (
            student_data.iloc[0][feature] == 1
        )

        scholarship_has = (
            scholarship_data.iloc[0][feature] == 1
        )


        if scholarship_has:

            required.append(
                feature
            )


        if student_has and scholarship_has:

            matching.append(
                feature.replace(
                    "_",
                    " "
                )
            )


    if required:

        skill_match = (
            len(matching)
            / len(required)
        )

    else:

        skill_match = 0


    skill_match = max(
        0,
        min(
            skill_match,
            1
        )
    )


    # -----------------------------------------------------
    # FINAL SCORE
    # -----------------------------------------------------

    final_score = (
        ml_score * 0.5
        +
        skill_match * 0.5
    )


    return {

        "ml_score": round(
            ml_score * 100,
            2
        ),

        "match_score": round(
            skill_match * 100,
            2
        ),

        "final_score": round(
            final_score * 100,
            2
        ),

        "matching_categories": matching
    }
