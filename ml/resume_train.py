# resume_train.py

import os
import pandas as pd
import joblib

from sklearn.model_selection import train_test_split
from sklearn.pipeline import Pipeline
from sklearn.feature_extraction.text import TfidfVectorizer
from sklearn.linear_model import LogisticRegression
from sklearn.metrics import accuracy_score, classification_report


# =====================================================
# FILE PATHS
# =====================================================

DATA_PATH = r"C:\Users\ALEKHYA\OneDrive\Desktop\hub\data\resume_dataset.csv"
MODEL_PATH = "ml/resume_model.pkl"


# =====================================================
# CHECK DATASET
# =====================================================

if not os.path.exists(DATA_PATH):

    raise FileNotFoundError(
        f"❌ Dataset not found: {DATA_PATH}"
    )


# =====================================================
# LOAD DATASET
# =====================================================

print("📂 Loading dataset...")

df = pd.read_csv(DATA_PATH)


print(
    f"✅ Dataset loaded: {len(df)} rows"
)


# =====================================================
# CHECK REQUIRED COLUMNS
# =====================================================

required_columns = [
    "target_role",
    "content",
    "label"
]


for column in required_columns:

    if column not in df.columns:

        raise ValueError(
            f"❌ Missing column: {column}"
        )


# =====================================================
# REMOVE EMPTY VALUES
# =====================================================

df = df.dropna(
    subset=required_columns
)


# =====================================================
# CLEAN TEXT
# =====================================================

df["target_role"] = (
    df["target_role"]
    .astype(str)
    .str.lower()
    .str.strip()
)


df["content"] = (
    df["content"]
    .astype(str)
    .str.lower()
    .str.strip()
)


df["label"] = (
    df["label"]
    .astype(int)
)


# =====================================================
# CREATE INPUT TEXT
# =====================================================

df["input_text"] = (
    df["target_role"]
    + " "
    + df["content"]
)


X = df["input_text"]

y = df["label"]


# =====================================================
# TRAIN / TEST SPLIT
# =====================================================

X_train, X_test, y_train, y_test = train_test_split(

    X,
    y,

    test_size=0.20,

    random_state=42,

    stratify=y
)


print(
    f"Training samples: {len(X_train)}"
)

print(
    f"Testing samples: {len(X_test)}"
)


# =====================================================
# ML PIPELINE
# =====================================================

model = Pipeline(

    [

        # ---------------------------------------------
        # TF-IDF
        # ---------------------------------------------

        (
            "tfidf",

            TfidfVectorizer(

                ngram_range=(1, 2),

                max_features=5000,

                stop_words="english"
            )
        ),


        # ---------------------------------------------
        # CLASSIFIER
        # ---------------------------------------------

        (
            "classifier",

            LogisticRegression(

                max_iter=1000
            )
        )

    ]
)


# =====================================================
# TRAIN MODEL
# =====================================================

print(
    "\n🤖 Training Resume ML model..."
)


model.fit(
    X_train,
    y_train
)


print(
    "✅ Training completed!"
)


# =====================================================
# PREDICTION
# =====================================================

predictions = model.predict(
    X_test
)


# =====================================================
# ACCURACY
# =====================================================

accuracy = accuracy_score(
    y_test,
    predictions
)


print(
    "\n================================="
)

print(
    f"🎯 Model Accuracy: {accuracy * 100:.2f}%"
)

print(
    "================================="
)


# =====================================================
# CLASSIFICATION REPORT
# =====================================================

print(
    "\n📊 Classification Report:"
)


print(
    classification_report(

        y_test,

        predictions,

        zero_division=0
    )
)


# =====================================================
# CREATE ML FOLDER
# =====================================================

os.makedirs(
    "ml",
    exist_ok=True
)


# =====================================================
# SAVE MODEL
# =====================================================

joblib.dump(
    model,
    MODEL_PATH
)


print(
    "\n💾 Model saved successfully!"
)

print(
    f"📁 Location: {MODEL_PATH}"
)


# =====================================================
# TEST MODEL
# =====================================================

print(
    "\n🔍 Testing model with sample..."
)


sample_role = "data scientist"

sample_content = (
    "python sql machine learning "
    "pandas numpy statistics"
)


sample_input = (
    sample_role
    + " "
    + sample_content
)


result = model.predict(
    [sample_input]
)[0]


probability = model.predict_proba(
    [sample_input]
)[0]


if result == 1:

    print(
        "✅ Result: Relevant Resume Content"
    )

else:

    print(
        "❌ Result: Not Relevant Resume Content"
    )


print(
    f"📈 Confidence: "
    f"{max(probability) * 100:.2f}%"
)


print(
    "\n🎉 Resume ML training finished!"
)
