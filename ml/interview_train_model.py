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

from sklearn.metrics import (
    mean_absolute_error,
    r2_score
)


# =====================================================
# PROJECT PATHS
# =====================================================

BASE_DIR = Path(__file__).resolve().parent.parent

DATA_DIR = BASE_DIR / "data"

MODEL_PATH = BASE_DIR / "ml" / "interview_model.pkl"


# =====================================================
# FIND INTERVIEW CSV DATASET
# =====================================================

csv_files = list(DATA_DIR.glob("*.csv"))


if not csv_files:

    print("\n❌ DATASET NOT FOUND")
    print("--------------------------------------")

    print(
        "Data folder:"
    )

    print(
        DATA_DIR
    )

    print("--------------------------------------")

    print(
        "No CSV file found inside data folder."
    )

    raise SystemExit


# =====================================================
# SELECT DATASET
# =====================================================

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
# HEADER
# =====================================================

print("\n======================================")
print("🎤 INTERVIEW ML TRAINING")
print("======================================")


print("\n📂 Dataset found:")

print(
    DATA_PATH
)


# =====================================================
# LOAD DATASET
# =====================================================

try:

    df = pd.read_csv(
        DATA_PATH
    )

except Exception as e:

    print("\n❌ DATASET LOADING ERROR")

    print(e)

    raise SystemExit


print("\n✅ Dataset loaded successfully!")

print(
    "Total rows:",
    len(df)
)

print(
    "Columns:",
    list(df.columns)
)


# =====================================================
# REQUIRED COLUMNS
# =====================================================

required_columns = [

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


missing_columns = [

    column

    for column in required_columns

    if column not in df.columns

]


if missing_columns:

    print("\n❌ REQUIRED COLUMNS MISSING")

    print("--------------------------------------")

    for column in missing_columns:

        print(
            " -",
            column
        )

    print("--------------------------------------")

    raise SystemExit


print(
    "\n✅ All required columns found!"
)


# =====================================================
# COPY DATA
# =====================================================

df = df.copy()


# =====================================================
# TEXT CLEANING
# =====================================================

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


# =====================================================
# NUMERIC CLEANING
# =====================================================

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


# =====================================================
# REMOVE INVALID SCORES
# =====================================================

df = df.dropna(
    subset=["score"]
)


# =====================================================
# LIMIT SCORE BETWEEN 0 AND 10
# =====================================================

df["score"] = df["score"].clip(

    lower=0,

    upper=10

)


# =====================================================
# REMOVE EMPTY STUDENT ANSWERS
# =====================================================

df = df[
    df["student_answer"].str.len() > 0
]


# =====================================================
# CREATE COMBINED TEXT
# =====================================================

df["combined_text"] = (

    df["question"]

    + " "

    + df["expected_answer"]

    + " "

    + df["student_answer"]

)


# =====================================================
# DATASET INFORMATION
# =====================================================

print("\n======================================")
print("📊 DATASET INFORMATION")
print("======================================")


print(
    "Rows after cleaning:",
    len(df)
)


print(
    "Roles:",
    df["role"].nunique()
)


print(
    "Question types:",
    df["question_type"].nunique()
)


print(
    "Average score:",
    round(
        df["score"].mean(),
        2
    )
)


# =====================================================
# FEATURES
# =====================================================

feature_columns = [

    "role",

    "question_type",

    "combined_text",

    "keyword_match",

    "answer_similarity",

    "answer_length",

    "technical_terms"

]


X = df[
    feature_columns
]


y = df[
    "score"
]


# =====================================================
# CHECK DATASET SIZE
# =====================================================

if len(df) < 5:

    print("\n❌ NOT ENOUGH DATA")

    print(
        "At least 5 valid rows are recommended "
        "for model training."
    )

    raise SystemExit


# =====================================================
# TRAIN TEST SPLIT
# =====================================================

X_train, X_test, y_train, y_test = train_test_split(

    X,

    y,

    test_size=0.20,

    random_state=42

)


print("\n======================================")
print("📊 DATA SPLIT")
print("======================================")


print(
    "Training rows:",
    len(X_train)
)


print(
    "Testing rows:",
    len(X_test)
)


# =====================================================
# PREPROCESSOR
# =====================================================

preprocessor = ColumnTransformer(

    transformers=[


        # =============================================
        # ROLE
        # =============================================

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


        # =============================================
        # QUESTION TYPE
        # =============================================

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


        # =============================================
        # TEXT FEATURES
        # =============================================

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


        # =============================================
        # NUMERIC FEATURES
        # =============================================

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


# =====================================================
# RANDOM FOREST REGRESSOR
# =====================================================

model = RandomForestRegressor(

    n_estimators=300,

    max_depth=15,

    min_samples_split=2,

    min_samples_leaf=1,

    random_state=42,

    n_jobs=-1

)


# =====================================================
# COMPLETE PIPELINE
# =====================================================

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


# =====================================================
# TRAIN MODEL
# =====================================================

print("\n======================================")
print("🤖 TRAINING MODEL")
print("======================================")


pipeline.fit(

    X_train,

    y_train

)


print(
    "\n✅ Model training completed!"
)


# =====================================================
# PREDICTION
# =====================================================

predictions = pipeline.predict(

    X_test

)


# =====================================================
# LIMIT PREDICTIONS
# =====================================================

predictions = predictions.clip(

    0,

    10

)


# =====================================================
# MODEL EVALUATION
# =====================================================

mae = mean_absolute_error(

    y_test,

    predictions

)


r2 = r2_score(

    y_test,

    predictions

)


print("\n======================================")
print("📈 MODEL EVALUATION")
print("======================================")


print(
    f"MAE Score : {mae:.4f}"
)


print(
    f"R2 Score  : {r2:.4f}"
)


# =====================================================
# SAVE MODEL
# =====================================================

try:

    joblib.dump(

        pipeline,

        MODEL_PATH

    )

except Exception as e:

    print("\n❌ MODEL SAVE ERROR")

    print(e)

    raise SystemExit


print("\n======================================")
print("💾 MODEL SAVED")
print("======================================")


print(
    "Model:"
)


print(
    MODEL_PATH
)


print(
    "\n🎉 INTERVIEW ML MODEL TRAINING COMPLETED!"
)


print(
    "\nYou can now run Interview.py"
)


print(
    "The application will use:"
)


print(
    "ml/interview_recommend.py"
)
