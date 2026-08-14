import os
import joblib


# =====================================================
# MODEL PATH
# =====================================================

MODEL_PATH = "ml/resume_model.pkl"


# =====================================================
# LOAD MODEL
# =====================================================

if not os.path.exists(MODEL_PATH):

    raise FileNotFoundError(
        "❌ resume_model.pkl not found. "
        "First run: python ml/resume_train.py"
    )


model = joblib.load(
    MODEL_PATH
)


# =====================================================
# PREDICT RESUME CONTENT RELEVANCE
# =====================================================

def predict_relevance(
    target_role,
    content
):
    """
    Predict whether resume content is
    relevant to the selected target role.
    """

    target_role = str(
        target_role
    ).lower().strip()


    content = str(
        content
    ).lower().strip()


    # Same format used during training
    input_text = (
        target_role
        + " "
        + content
    )


    # ---------------------------------------------
    # Prediction
    # ---------------------------------------------

    prediction = model.predict(
        [input_text]
    )[0]


    # ---------------------------------------------
    # Probability
    # ---------------------------------------------

    probabilities = model.predict_proba(
        [input_text]
    )[0]


    confidence = max(
        probabilities
    ) * 100


    # ---------------------------------------------
    # Relevant probability
    # ---------------------------------------------

    relevant_score = (
        probabilities[1] * 100
    )


    return {
        "relevant": bool(prediction == 1),
        "score": round(
            relevant_score,
            2
        ),
        "confidence": round(
            confidence,
            2
        )
    }


# =====================================================
# RANK MULTIPLE RESUME ITEMS
# =====================================================

def rank_content(
    target_role,
    items
):
    """
    Rank skills/projects/content according
    to relevance for the selected target role.

    items = [
        "Python SQL Machine Learning",
        "HTML CSS JavaScript",
        ...
    ]
    """

    results = []


    for item in items:

        result = predict_relevance(
            target_role,
            item
        )


        results.append(
            {
                "content": item,
                "score": result["score"],
                "relevant": result["relevant"]
            }
        )


    # Highest relevance first

    results.sort(
        key=lambda x: x["score"],
        reverse=True
    )


    return results


# =====================================================
# GET RELEVANT CONTENT
# =====================================================

def get_relevant_content(
    target_role,
    items,
    threshold=50
):
    """
    Return only content whose relevance
    score is greater than or equal to threshold.
    """

    ranked = rank_content(
        target_role,
        items
    )


    relevant_items = [
        item
        for item in ranked
        if item["score"] >= threshold
    ]


    return relevant_items


# =====================================================
# TEST
# =====================================================

if __name__ == "__main__":

    role = "Data Scientist"


    sample_items = [

        "Python SQL Machine Learning Pandas",

        "HTML CSS JavaScript React",

        "Statistics Data Analysis NumPy",

        "Java Spring Boot Hibernate"

    ]


    print(
        "\n🤖 Resume Recommendation Test"
    )

    print(
        "Target Role:",
        role
    )

    print(
        "\n--------------------------------"
    )


    ranked = rank_content(
        role,
        sample_items
    )


    for item in ranked:

        print(
            f"{item['score']:6.2f}%  "
            f"{item['content']}"
        )


    print(
        "\n--------------------------------"
    )

    print(
        "✅ Recommendation test completed."
    )
